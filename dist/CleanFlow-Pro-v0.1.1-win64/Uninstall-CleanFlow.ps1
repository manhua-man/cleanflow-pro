# Windows Native PowerShell Uninstaller for CleanFlow Pro
# Zero Emoji Rule strictly enforced

$ErrorActionPreference = "SilentlyContinue"

$AppName = "CleanFlow Pro"
$AppId = "CleanFlowPro"
$InstallDir = Join-Path $env:LOCALAPPDATA "Programs\CleanFlow-Pro"

Write-Host "========================================"
Write-Host " CleanFlow Pro - Windows 卸载向导"
Write-Host "========================================"

# Terminate running process
Get-Process cleanflow -ErrorAction SilentlyContinue | Stop-Process -Force

# Remove Desktop Shortcut
$DesktopDir = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopDir "$AppName.lnk"
if (Test-Path $ShortcutPath) {
    Remove-Item $ShortcutPath -Force
    Write-Host "已清理桌面快捷方式"
}

# Remove Start Menu Shortcut
$StartMenuDir = [Environment]::GetFolderPath("Programs")
$StartShortcutPath = Join-Path $StartMenuDir "$AppName.lnk"
if (Test-Path $StartShortcutPath) {
    Remove-Item $StartShortcutPath -Force
    Write-Host "已清理开始菜单快捷方式"
}

# Remove Uninstall Registry Key
$UninstallRegKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\$AppId"
if (Test-Path $UninstallRegKey) {
    Remove-Item -Path $UninstallRegKey -Recurse -Force
    Write-Host "已清理系统注册表信息"
}

# Remove Install Directory
if (Test-Path $InstallDir) {
    # Remove files except this uninstaller script if it is executing, then self-delete
    Get-ChildItem -Path $InstallDir -Exclude "Uninstall-CleanFlow.ps1" | Remove-Item -Recurse -Force
    Write-Host "已清理主程序文件"
}

Write-Host "----------------------------------------"
Write-Host "CleanFlow Pro 已从系统中完全卸载。"
