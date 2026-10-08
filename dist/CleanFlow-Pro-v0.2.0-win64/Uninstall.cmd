@echo off
chcp 65001 >nul
echo 正在执行 CleanFlow Pro 卸载向导...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Uninstall-CleanFlow.ps1"
echo.
pause
