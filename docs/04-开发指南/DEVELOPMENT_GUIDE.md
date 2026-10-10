# CleanFlow Pro 工程开发与调试指南 (Development Guide)

本文档面向 CleanFlow Pro 的工程维护人员与 AI 开发者，提供编译、构建、测试与 Win32 底层调试的完整指南。

---

## 1. 开发环境要求

- **操作系统**：Windows 10 / Windows 11 (x64)
- **Rust 工具链**：Rust 1.75+ (Stable), Cargo
- **Shell**：PowerShell 5.1+ 或 pwsh 7+
- **C/C++ 工具链（可选）**：MSVC (Visual Studio 2022 C++ Build Tools)，用于特定 Win32 符号链接

---

## 2. 常用构建与测试指令

### 2.1 自动化测试
```powershell
# 运行全量 90 项单元测试
cargo test

# 运行特定模块测试 (例如智能护航)
cargo test intelligent_guard

# 运行测试并查看详细 stdout 输出
cargo test -- --nocapture
```

### 2.2 生产级单文件构建
```powershell
# 编译高度优化的生产二进制
cargo build --release

# 验证产物生成
Get-Item target\release\cleanflow.exe
```

### 2.3 启动与运行调试
```powershell
# 正常模式运行 (自动在系统默认浏览器打开控制台)
.\target\release\cleanflow.exe

# 静默托盘模式 (后台驻留右下角托盘，双击 Ctrl / Alt+Space 呼出 Spotlight)
.\target\release\cleanflow.exe --silent

# 指定端口启动
.\target\release\cleanflow.exe --port 9090
```

---

## 3. Win32 底层开发与避坑指南

### 3.1 绝对零 Emoji 规范
- 任何控制台打印、日志、错误信息严禁输出任何 Emoji 字符；
- 前端界面与 SVG 渲染严禁引入包含 Emoji 的第三方字体或模板。

### 3.2 句柄生命周期与 FFI 签名统一
- 在调用 Win32 原生 API（如 `CreateFileW`、`CloseHandle`、`DeviceIoControl`）时，统一句柄类型定义为 `isize`，避免多模块 extern 声明不一致引发链接冲突；
- 必须在所有的 FFI 句柄使用后显式调用 `CloseHandle`，避免句柄泄漏导致文件被系统锁定。

### 3.3 云端文件脱水安全
- 对接 `cldapi.dll` 时，若系统动态加载失败，必须平滑回退至 `attrib.exe +U -P`，绝不允许物理调用 `remove_file`。

### 3.4 互斥进程预检
- 任何涉及移动或清理的敏感操作，必须先通过 `process_lock.rs` 探测持有句柄的进程并友好提示用户，杜绝强杀导致数据损坏。
