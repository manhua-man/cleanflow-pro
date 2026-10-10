use std::collections::HashMap;
use std::sync::{OnceLock, RwLock};

#[cfg(windows)]
mod ffi {
    #[repr(C)]
    pub struct ShFileInfoW {
        pub h_icon: isize,
        pub i_icon: i32,
        pub dw_attributes: u32,
        pub sz_display_name: [u16; 260],
        pub sz_type_name: [u16; 80],
    }

    #[repr(C)]
    pub struct IconInfo {
        pub f_icon: i32,
        pub x_hotspot: u32,
        pub y_hotspot: u32,
        pub hbm_mask: isize,
        pub hbm_color: isize,
    }

    #[repr(C)]
    pub struct BitmapInfoHeader {
        pub bi_size: u32,
        pub bi_width: i32,
        pub bi_height: i32,
        pub bi_planes: u16,
        pub bi_bit_count: u16,
        pub bi_compression: u32,
        pub bi_size_image: u32,
        pub bi_x_pels_per_meter: i32,
        pub bi_y_pels_per_meter: i32,
        pub bi_clr_used: u32,
        pub bi_clr_important: u32,
    }

    #[repr(C)]
    pub struct BitmapInfo {
        pub bmi_header: BitmapInfoHeader,
        pub bmi_colors: [u32; 1],
    }

    pub const SHGFI_ICON: u32 = 0x000000100;
    pub const SHGFI_SMALLICON: u32 = 0x000000001;
    pub const SHGFI_USEFILEATTRIBUTES: u32 = 0x000000010;
    pub const FILE_ATTRIBUTE_NORMAL: u32 = 0x00000080;
    pub const DIB_RGB_COLORS: u32 = 0;
    pub const BI_RGB: u32 = 0;

    #[link(name = "shell32")]
    extern "system" {
        pub fn SHGetFileInfoW(
            psz_path: *const u16,
            dw_file_attributes: u32,
            psfi: *mut ShFileInfoW,
            cb_file_info: u32,
            u_flags: u32,
        ) -> usize;
    }

    #[link(name = "user32")]
    extern "system" {
        pub fn DestroyIcon(h_icon: isize) -> i32;
        pub fn GetIconInfo(h_icon: isize, piconinfo: *mut IconInfo) -> i32;
        pub fn GetDC(h_wnd: isize) -> isize;
        pub fn ReleaseDC(h_wnd: isize, h_dc: isize) -> i32;
    }

    #[link(name = "gdi32")]
    extern "system" {
        pub fn DeleteObject(ho: isize) -> i32;
        pub fn GetDIBits(
            hdc: isize,
            hbm: isize,
            start: u32,
            c_lines: u32,
            lpv_bits: *mut u8,
            lpbmi: *mut BitmapInfo,
            usage: u32,
        ) -> i32;
    }
}

pub struct IconCacheManager {
    cache: RwLock<HashMap<String, Vec<u8>>>,
}

impl IconCacheManager {
    pub fn new() -> Self {
        Self {
            cache: RwLock::new(HashMap::new()),
        }
    }

    pub fn get_icon_png(&self, path_or_ext: &str) -> Option<Vec<u8>> {
        let key = normalize_cache_key(path_or_ext);
        if let Ok(guard) = self.cache.read() {
            if let Some(bytes) = guard.get(&key) {
                return Some(bytes.clone());
            }
        }

        #[cfg(windows)]
        {
            if let Some(png_bytes) = extract_native_icon_png(path_or_ext) {
                if let Ok(mut guard) = self.cache.write() {
                    guard.insert(key, png_bytes.clone());
                }
                return Some(png_bytes);
            }
        }

        #[cfg(not(windows))]
        {
            let _ = path_or_ext;
        }

        None
    }
}

static GLOBAL_ICON_CACHE: OnceLock<IconCacheManager> = OnceLock::new();

pub fn get_global_icon_cache() -> &'static IconCacheManager {
    GLOBAL_ICON_CACHE.get_or_init(IconCacheManager::new)
}

fn normalize_cache_key(path_or_ext: &str) -> String {
    let lower = path_or_ext.trim().to_lowercase();
    if lower.ends_with(".exe") || lower.ends_with(".lnk") || lower.ends_with(".ico") {
        lower
    } else if let Some(pos) = lower.rfind('.') {
        lower[pos..].to_string()
    } else {
        lower
    }
}

#[cfg(windows)]
fn extract_native_icon_png(path_or_ext: &str) -> Option<Vec<u8>> {
    use std::os::windows::ffi::OsStrExt;
    use std::path::Path;

    let path_obj = Path::new(path_or_ext);
    let ext_opt = path_obj.extension().and_then(|e| e.to_str()).map(|e| e.to_lowercase());
    let is_standalone_file = ext_opt.as_deref() == Some("exe")
        || ext_opt.as_deref() == Some("lnk")
        || ext_opt.as_deref() == Some("ico");

    let (query_str, flags) = if is_standalone_file && path_obj.exists() {
        (path_or_ext.to_string(), ffi::SHGFI_ICON | ffi::SHGFI_SMALLICON)
    } else {
        let ext = if let Some(ref e) = ext_opt {
            format!(".{}", e)
        } else if path_or_ext.starts_with('.') {
            path_or_ext.to_string()
        } else {
            ".file".to_string()
        };
        (
            format!("cleanflow_dummy{}", ext),
            ffi::SHGFI_ICON | ffi::SHGFI_SMALLICON | ffi::SHGFI_USEFILEATTRIBUTES,
        )
    };

    let wide_str: Vec<u16> = std::ffi::OsStr::new(&query_str)
        .encode_wide()
        .chain(Some(0))
        .collect();

    unsafe {
        let mut sfi: ffi::ShFileInfoW = std::mem::zeroed();
        let res = ffi::SHGetFileInfoW(
            wide_str.as_ptr(),
            ffi::FILE_ATTRIBUTE_NORMAL,
            &mut sfi,
            std::mem::size_of::<ffi::ShFileInfoW>() as u32,
            flags,
        );

        if res == 0 || sfi.h_icon == 0 {
            return None;
        }

        let h_icon = sfi.h_icon;
        let mut icon_info: ffi::IconInfo = std::mem::zeroed();
        if ffi::GetIconInfo(h_icon, &mut icon_info) == 0 {
            ffi::DestroyIcon(h_icon);
            return None;
        }

        let hbm = if icon_info.hbm_color != 0 {
            icon_info.hbm_color
        } else {
            icon_info.hbm_mask
        };

        if hbm == 0 {
            if icon_info.hbm_color != 0 { ffi::DeleteObject(icon_info.hbm_color); }
            if icon_info.hbm_mask != 0 { ffi::DeleteObject(icon_info.hbm_mask); }
            ffi::DestroyIcon(h_icon);
            return None;
        }

        let hdc = ffi::GetDC(0);
        let width = 16;
        let height = 16;
        let mut bmi: ffi::BitmapInfo = std::mem::zeroed();
        bmi.bmi_header.bi_size = std::mem::size_of::<ffi::BitmapInfoHeader>() as u32;
        bmi.bmi_header.bi_width = width;
        bmi.bmi_header.bi_height = -height; // top-down bitmap
        bmi.bmi_header.bi_planes = 1;
        bmi.bmi_header.bi_bit_count = 32;
        bmi.bmi_header.bi_compression = ffi::BI_RGB;

        let mut bgra_pixels = vec![0u8; (width * height * 4) as usize];
        let lines = ffi::GetDIBits(
            hdc,
            hbm,
            0,
            height as u32,
            bgra_pixels.as_mut_ptr(),
            &mut bmi,
            ffi::DIB_RGB_COLORS,
        );

        ffi::ReleaseDC(0, hdc);

        if icon_info.hbm_color != 0 { ffi::DeleteObject(icon_info.hbm_color); }
        if icon_info.hbm_mask != 0 { ffi::DeleteObject(icon_info.hbm_mask); }
        ffi::DestroyIcon(h_icon);

        if lines == 0 {
            return None;
        }

        let mut rgba = vec![0u8; bgra_pixels.len()];
        let mut has_non_zero_alpha = false;
        for i in 0..(width * height) as usize {
            let b = bgra_pixels[i * 4];
            let g = bgra_pixels[i * 4 + 1];
            let r = bgra_pixels[i * 4 + 2];
            let a = bgra_pixels[i * 4 + 3];

            if a > 0 {
                has_non_zero_alpha = true;
            }
            rgba[i * 4] = r;
            rgba[i * 4 + 1] = g;
            rgba[i * 4 + 2] = b;
            rgba[i * 4 + 3] = a;
        }

        if !has_non_zero_alpha {
            for i in 0..(width * height) as usize {
                if rgba[i * 4] > 0 || rgba[i * 4 + 1] > 0 || rgba[i * 4 + 2] > 0 {
                    rgba[i * 4 + 3] = 255;
                }
            }
        }

        Some(encode_png_uncompressed(width as u32, height as u32, &rgba))
    }
}

pub fn encode_png_uncompressed(width: u32, height: u32, rgba: &[u8]) -> Vec<u8> {
    let mut out = Vec::new();
    out.extend_from_slice(b"\x89PNG\r\n\x1a\n");

    // IHDR
    let mut ihdr_data = Vec::with_capacity(13);
    ihdr_data.extend_from_slice(&width.to_be_bytes());
    ihdr_data.extend_from_slice(&height.to_be_bytes());
    ihdr_data.push(8); // bit depth
    ihdr_data.push(6); // RGBA
    ihdr_data.push(0); // compression
    ihdr_data.push(0); // filter
    ihdr_data.push(0); // interlace
    write_chunk(&mut out, b"IHDR", &ihdr_data);

    // IDAT with uncompressed deflate
    let row_len = (width * 4) as usize;
    let mut raw_data = Vec::with_capacity((height * (width * 4 + 1)) as usize);
    for y in 0..height {
        raw_data.push(0); // filter None
        let start = (y as usize) * row_len;
        let end = start + row_len;
        if end <= rgba.len() {
            raw_data.extend_from_slice(&rgba[start..end]);
        }
    }

    let adler = adler32(&raw_data);
    let mut idat_data = Vec::with_capacity(raw_data.len() + 11);
    idat_data.push(0x78); // zlib CMF
    idat_data.push(0x01); // zlib FLG (no compression)

    // uncompressed deflate block (BFINAL=1, BTYPE=00)
    idat_data.push(0x01);
    let len = raw_data.len() as u16;
    let nlen = !len;
    idat_data.extend_from_slice(&len.to_le_bytes());
    idat_data.extend_from_slice(&nlen.to_le_bytes());
    idat_data.extend_from_slice(&raw_data);
    idat_data.extend_from_slice(&adler.to_be_bytes());

    write_chunk(&mut out, b"IDAT", &idat_data);
    write_chunk(&mut out, b"IEND", &[]);

    out
}

fn adler32(data: &[u8]) -> u32 {
    let mut s1 = 1u32;
    let mut s2 = 0u32;
    for &b in data {
        s1 = (s1 + b as u32) % 65521;
        s2 = (s2 + s1) % 65521;
    }
    (s2 << 16) | s1
}

fn crc32(data: &[u8]) -> u32 {
    let mut crc = 0xFFFF_FFFFu32;
    for &byte in data {
        crc ^= byte as u32;
        for _ in 0..8 {
            if (crc & 1) != 0 {
                crc = (crc >> 1) ^ 0xEDB8_8320;
            } else {
                crc >>= 1;
            }
        }
    }
    !crc
}

fn write_chunk(out: &mut Vec<u8>, chunk_type: &[u8; 4], data: &[u8]) {
    out.extend_from_slice(&(data.len() as u32).to_be_bytes());
    let mut to_crc = Vec::with_capacity(4 + data.len());
    to_crc.extend_from_slice(chunk_type);
    to_crc.extend_from_slice(data);
    let crc = crc32(&to_crc);
    out.extend_from_slice(&to_crc);
    out.extend_from_slice(&crc.to_be_bytes());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_encode_png_uncompressed() {
        let mut pixels = vec![0u8; 16 * 16 * 4];
        for i in 0..16 * 16 {
            pixels[i * 4] = 0;
            pixels[i * 4 + 1] = 120;
            pixels[i * 4 + 2] = 215;
            pixels[i * 4 + 3] = 255;
        }

        let png = encode_png_uncompressed(16, 16, &pixels);
        assert_eq!(&png[0..8], b"\x89PNG\r\n\x1a\n");
        assert!(png.windows(4).any(|w| w == b"IHDR"));
        assert!(png.windows(4).any(|w| w == b"IDAT"));
        assert!(png.windows(4).any(|w| w == b"IEND"));
    }

    #[test]
    fn test_icon_cache_lifecycle() {
        let mgr = IconCacheManager::new();
        // Ext .exe or .pdf
        let icon_png = mgr.get_icon_png(".txt");
        #[cfg(windows)]
        {
            assert!(icon_png.is_some());
            let bytes = icon_png.unwrap();
            assert_eq!(&bytes[0..8], b"\x89PNG\r\n\x1a\n");
        }
        #[cfg(not(windows))]
        {
            let _ = icon_png;
        }
    }
}
