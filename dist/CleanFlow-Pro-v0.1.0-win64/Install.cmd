@echo off
chcp 65001 >nul
echo 正在启动 CleanFlow Pro 安装向导...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-CleanFlow.ps1"
echo.
pause
