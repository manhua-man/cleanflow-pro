# Windows Native PowerShell Installer for CleanFlow Pro
# Zero Emoji Rule strictly enforced

$ErrorActionPreference = "Stop"

$AppName = "CleanFlow Pro"
$AppId = "CleanFlowPro"
$Version = "0.1.0"
$SourceDir = $PSScriptRoot

$InstallDir = Join-Path $env:LOCALAPPDATA "Programs\CleanFlow-Pro"
if (-not (Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
}

Write-Host "========================================"
Write-Host " CleanFlow Pro - Windows 安装向导"
Write-Host "========================================"
Write-Host "目标安装路径: $InstallDir"

# Copy program files
Copy-Item (Join-Path $SourceDir "cleanflow.exe") -Destination $InstallDir -Force
if (Test-Path (Join-Path $SourceDir "rules.json")) {
    Copy-Item (Join-Path $SourceDir "rules.json") -Destination $InstallDir -Force
}
if (Test-Path (Join-Path $SourceDir "start-cleanflow.cmd")) {
    Copy-Item (Join-Path $SourceDir "start-cleanflow.cmd") -Destination $InstallDir -Force
}
if (Test-Path (Join-Path $SourceDir "Uninstall-CleanFlow.ps1")) {
    Copy-Item (Join-Path $SourceDir "Uninstall-CleanFlow.ps1") -Destination $InstallDir -Force
}

$TargetExe = Join-Path $InstallDir "cleanflow.exe"

# Create Desktop Shortcut
$WshShell = New-Object -ComObject WScript.Shell
$DesktopDir = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopDir "$AppName.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetExe
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.Description = "CleanFlow Pro - 高性能 Windows 空间与系统管家"
$Shortcut.Save()
Write-Host "已创建桌面快捷方式: $ShortcutPath"

# Create Start Menu Shortcut
$StartMenuDir = [Environment]::GetFolderPath("Programs")
$StartShortcutPath = Join-Path $StartMenuDir "$AppName.lnk"
$StartShortcut = $WshShell.CreateShortcut($StartShortcutPath)
$StartShortcut.TargetPath = $TargetExe
$StartShortcut.WorkingDirectory = $InstallDir
$StartShortcut.Description = "CleanFlow Pro - 高性能 Windows 空间与系统管家"
$StartShortcut.Save()
Write-Host "已创建开始菜单快捷方式: $StartShortcutPath"

# Register in Windows Add/Remove Programs (Registry)
$UninstallRegKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\$AppId"
if (-not (Test-Path $UninstallRegKey)) {
    New-Item -Path $UninstallRegKey -Force | Out-Null
}

$ExeSizeKB = [int]((Get-Item $TargetExe).Length / 1024)

Set-ItemProperty -Path $UninstallRegKey -Name "DisplayName" -Value "CleanFlow Pro (净流)"
Set-ItemProperty -Path $UninstallRegKey -Name "DisplayVersion" -Value $Version
Set-ItemProperty -Path $UninstallRegKey -Name "Publisher" -Value "CleanFlow Team"
Set-ItemProperty -Path $UninstallRegKey -Name "InstallLocation" -Value $InstallDir
Set-ItemProperty -Path $UninstallRegKey -Name "DisplayIcon" -Value "$TargetExe,0"
Set-ItemProperty -Path $UninstallRegKey -Name "UninstallString" -Value "powershell.exe -ExecutionPolicy Bypass -File `"$InstallDir\Uninstall-CleanFlow.ps1`""
Set-ItemProperty -Path $UninstallRegKey -Name "EstimatedSize" -Value $ExeSizeKB
Set-ItemProperty -Path $UninstallRegKey -Name "NoModify" -Value 1
Set-ItemProperty -Path $UninstallRegKey -Name "NoRepair" -Value 1

Write-Host "已注册系统应用卸载信息: $UninstallRegKey"
Write-Host "----------------------------------------"
Write-Host "CleanFlow Pro 安装完成！"
Write-Host "您可以通过桌面快捷方式或开始菜单直接启动。"
