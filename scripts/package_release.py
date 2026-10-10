import os
import shutil
import zipfile
import re

def get_package_version(base_dir):
    cargo_toml = os.path.join(base_dir, 'Cargo.toml')
    if os.path.exists(cargo_toml):
        with open(cargo_toml, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'version\s*=\s*"([^"]+)"', content)
            if match:
                return match.group(1)
    return "0.4.5"

def package_release():
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(scripts_dir)
    version = get_package_version(base_dir)
    print(f"Packaging CleanFlow Pro v{version}...")

    release_exe = os.path.join(base_dir, 'target', 'release', 'cleanflow.exe')
    if not os.path.exists(release_exe):
        raise FileNotFoundError(f"Release binary not found at: {release_exe}. Please run 'cargo build --release' first.")

    root_exe = os.path.join(base_dir, 'cleanflow.exe')
    shutil.copy2(release_exe, root_exe)
    print(f"Updated root binary: {root_exe}")

    folder_name = f"CleanFlow-Pro-v{version}-win64"
    dist_dir = os.path.join(base_dir, 'dist', folder_name)
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir, exist_ok=True)

    # 1. Core binaries and config
    files_to_copy = [
        (release_exe, 'cleanflow.exe'),
        (os.path.join(base_dir, 'rules.json'), 'rules.json'),
        (os.path.join(base_dir, 'README.md'), 'README.md'),
    ]

    # 2. Helpful batch / shell scripts
    prev_dist = os.path.join(base_dir, 'dist', 'CleanFlow-Pro-v0.1.1-win64')
    for script_name in ['Install-CleanFlow.ps1', 'Install.cmd', 'Uninstall-CleanFlow.ps1', 'Uninstall.cmd', 'start-cleanflow.cmd']:
        src = os.path.join(prev_dist, script_name)
        if os.path.exists(src):
            files_to_copy.append((src, script_name))

    for src_path, target_name in files_to_copy:
        if os.path.exists(src_path):
            dest_path = os.path.join(dist_dir, target_name)
            shutil.copy2(src_path, dest_path)
            print(f"Added: {target_name} ({os.path.getsize(dest_path)} bytes)")

    # 3. Create QUICK_START.txt for testers
    quick_start_content = f"""================================================================================
          CleanFlow Pro (净流) v{version} - 体验与快速上手指南
================================================================================

感谢您参与 CleanFlow Pro 的抢先体验！
CleanFlow Pro 是一款专为 Windows 10/11 打造的高性能磁盘空间资产治理与全盘极速检索中枢。

【快速启动】
1. 绿色便携免安装：解压本压缩包至任意目录（如 D:\\Tools\\CleanFlow）。
2. 双击运行 cleanflow.exe 或 start-cleanflow.cmd 即可启动。
3. 推荐使用方式：建议右键选择【以管理员身份运行】，以便完整体验：
   - NTFS MFT 裸盘流式秒搜（需特权绕过 Win32 API 限制）
   - DriverStore 驱动冗余清理与系统保留空间治理
   - ReFS 零拷贝块克隆去重

【三大业务支柱核心体验建议】
1. 支柱一：空间资产治理 (Storage Governance)
   - [空间全景看板]：直观查看 C 盘光谱分布条与 Top 单体超大文件透视。
   - [开发构建与缓存清理]：一键治理 Docker、Gradle、npm、Rust target 等冗余。
   - [目录透明软搬迁]：测试将微信聊天数据或 Ollama 模型目录无损迁移至 D 盘。
   - [系统原生无损挤水分]：一键收缩 VSCode / Cursor / 微信 SQLite 数据库。

2. 支柱二：全盘极速检索与全局启动器 (Search & Launcher)
   - [快捷键呼出]：随时按下 Alt + Space 或快速双击两次 Ctrl 呼出 Spotlight 悬浮窗。
   - [拼音与容错]：支持汉字全拼、声母缩写（如输入 "jsq" 搜计算器、"wx" 搜微信）。
   - [1-Edit 容错]：误输入 "cagro" 亦可精准纠偏命中 "cargo"。
   - [对话框穿透 Quick Switch]：在任何软件的另存为/打开文件对话框中，按 Ctrl + G 秒级直达。

3. 支柱三：原生数据救援 (Rescue Hub - 技术预览)
   - 工作区 6 提供免慢速扫描的 MFT 软删除秒级抢救与 VSS 快照回溯原型交互体验。

【安全防护说明】
- 资产绝对安全：云盘文件仅做 cldapi.dll 脱水占位，云端完好；
- 原生安全屏障：系统关键目录绝对白名单保护，拒绝破坏性误删；
- 退出方式：在系统右下角托盘图标右键选择【退出】，将彻底释放系统资源。

反馈与建议请直接联系开发者。祝使用愉快！
================================================================================
"""
    quick_start_path = os.path.join(dist_dir, 'QUICK_START.txt')
    with open(quick_start_path, 'w', encoding='utf-8') as f:
        f.write(quick_start_content)
    print(f"Created tester guide: QUICK_START.txt")

    # 4. Create ZIP
    zip_path = os.path.join(base_dir, 'dist', f"{folder_name}.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(dist_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, dist_dir)
                zf.write(full_path, arcname=os.path.join(folder_name, rel_path))

    zip_size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"\nSuccessfully created release package:")
    print(f"Directory: {dist_dir}")
    print(f"ZIP:       {zip_path} ({zip_size_mb:.2f} MB)")

if __name__ == '__main__':
    package_release()
