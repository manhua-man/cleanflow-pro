import os
import shutil
import zipfile

def package_v020():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    release_exe = os.path.join(base_dir, 'target', 'release', 'cleanflow.exe')
    root_exe = os.path.join(base_dir, 'cleanflow.exe')
    shutil.copy2(release_exe, root_exe)
    print(f"Copied {release_exe} -> {root_exe}")

    dist_dir = os.path.join(base_dir, 'dist', 'CleanFlow-Pro-v0.2.0-win64')
    os.makedirs(dist_dir, exist_ok=True)

    files_to_copy = [
        (release_exe, 'cleanflow.exe'),
        (os.path.join(base_dir, 'rules.json'), 'rules.json'),
        (os.path.join(base_dir, 'README.md'), 'README.md'),
    ]

    prev_dist = os.path.join(base_dir, 'dist', 'CleanFlow-Pro-v0.1.1-win64')
    for script_name in ['Install-CleanFlow.ps1', 'Install.cmd', 'Uninstall-CleanFlow.ps1', 'Uninstall.cmd', 'start-cleanflow.cmd']:
        src = os.path.join(prev_dist, script_name)
        if os.path.exists(src):
            files_to_copy.append((src, script_name))

    for src_path, target_name in files_to_copy:
        dest_path = os.path.join(dist_dir, target_name)
        shutil.copy2(src_path, dest_path)
        print(f"Added {target_name} ({os.path.getsize(dest_path)} bytes)")

    zip_path = os.path.join(base_dir, 'dist', 'CleanFlow-Pro-v0.2.0-win64.zip')
    if os.path.exists(zip_path):
        os.remove(zip_path)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(dist_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, dist_dir)
                zf.write(full_path, arcname=os.path.join('CleanFlow-Pro-v0.2.0-win64', rel_path))

    print(f"Release ZIP packaged: {zip_path} ({os.path.getsize(zip_path)} bytes)")

if __name__ == '__main__':
    package_v020()
