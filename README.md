# DLLMaster: Advanced DLL Analysis & Proxying Toolkit

![Platform](https://img.shields.io/badge/Platform-Windows-blue)
![Python](https://img.shields.io/badge/Python-3.x-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

**DLLMaster** is a modular, CLI-based tool designed for security researchers and reverse engineers. It automates the process of analyzing DLL exports, executing functions dynamically, and generating **DLL Proxies** for Red Teaming (DLL Sideloading/Hijacking) scenarios.

## 🚀 Features

*   **🔍 Deep Analysis:** Scans DLLs for exported functions and attempts to **demangle C++ function signatures** (using `dbghelp.dll`).
*   **⚡ Dynamic Execution:** Load and execute specific exported functions directly from the terminal with argument support.
*   **🛡️ Automated Proxy Generation:**
    *   Generates complete C++ source code for DLL Proxying.
    *   Implements **function forwarding** to the original DLL.
    *   Injects a custom payload (e.g., `calc.exe` or shellcode runners).
*   **⚙️ Auto-Compilation & Deployment:**
    *   Compiles the generated C++ code using MSVC (`cl.exe`) automatically.
    *   **Auto-Swapping Logic:** Handles the file renaming dance (`Original` -> `Original_real` & `Proxy` -> `Original`) to make the proxy ready for deployment instantly.

---

## 📖 Command Line Reference

Below is the full documentation of the tool's help menu, allowing you to learn the syntax without running the tool.

### 1. Main Menu
The entry point for the toolkit.

```text
usage: python -m dllmaster <command> [options]

DLLMaster: The Ultimate DLL Hacking Tool

positional arguments:
  {analyze,run,proxy}   Available Commands
    analyze             Scan DLL for exports & signatures
    run                 Execute a specific DLL function
    proxy               Generate Proxy DLL C++ code

options:
  -h, --help            show this help message and exit
```

### 2. Analyze Mode (`analyze`)
Used to inspect the target DLL and list all exported functions.

```text
usage: python -m dllmaster analyze <dll_path>

positional arguments:
  dll_path    Target .dll file to analyze

options:
  -h, --help  show this help message and exit
```

### 3. Run Mode (`run`)
Used to test specific functions inside a DLL dynamically.

```text
usage: python -m dllmaster run <dll_path> <function> [args...]

positional arguments:
  dll_path    Target .dll file
  function    Function name to call
  args        Function arguments (int or string)

options:
  -h, --help  show this help message and exit
```

### 4. Proxy Mode (`proxy`)
The core feature for generating the hijacking DLL.

```text
usage: python -m dllmaster proxy <dll_path> --hook <func> [options]

positional arguments:
  dll_path              Original Target DLL

options:
  -h, --help            show this help message and exit
  --hook HOOK, -f HOOK  Function to intercept (The Hook) [Required]
  --template TEMPLATE, -t TEMPLATE
                        Path to template.cpp (default: template.cpp)
  --output OUTPUT, -o OUTPUT
                        Output filename base (default: proxy_result)
  --payload PAYLOAD, -p PAYLOAD
                        Payload executable to run (default: calc.exe)
  --compile, -c         Compile immediately using MSVC (cl.exe)
```

---

## 📋 Prerequisites

Before using DLLMaster, ensure you have the following:

### 1. System Requirements
*   **Operating System:** Windows 10/11 (Required for ctypes and PE headers).
*   **Python:** Version 3.8 or higher.

### 2. Python Libraries
Install the required dependency for parsing PE headers:

```bash
pip install pefile
```

### 3. Compiler (For Proxy Mode)
To use the `--compile` feature, you must have Microsoft Visual C++ Compiler (`cl.exe`).

*   Install Visual Studio Build Tools (C++ Desktop Development workload).
*   **IMPORTANT:** You must run this tool inside the "x64 Native Tools Command Prompt for VS 20xx" to access `cl.exe`.

---

## 📂 Project Structure

Ensure your directory is organized as follows:

```text
ProjectRoot/
│
├── README.md              <-- This file
└── dllmaster/             <-- Main Package
    ├── __init__.py
    ├── __main__.py        <-- Entry point
    ├── cli.py             <-- CLI Argument Parser
    ├── template.cpp       <-- C++ Proxy Template
    ├── core/
    │   ├── analyzer.py    <-- Export scanning logic
    │   ├── executor.py    <-- Function running logic
    │   └── generator.py   <-- C++ generation & compilation
    └── utils/
        └── ui.py          <-- Colors & Banner
```

---

## 🛠️ Usage Guide

Run the tool as a Python module from the root directory:

```bash
python -m dllmaster <command> [arguments]
```

**Example Workflow: Sideloading `calc.exe`**

This command creates a malicious DLL proxy that forwards calls to the original DLL but executes a payload first.

**Command:**

```bash
python -m dllmaster proxy MyDll.dll --hook SayHelloFromDll --payload calc.exe --compile
```

**What happens automatically?**

1.  Analyzes `MyDll.dll` to find exports.
2.  Generates C++ code hooking `SayHelloFromDll`.
3.  Compiles the code into a DLL using `cl.exe`.
4.  Renames `MyDll.dll` -> `MyDll_real.dll`.
5.  Renames the new Proxy -> `MyDll.dll`.

The folder is now ready for the target application!

---

## 🧠 How Proxying Works (Under the Hood)

When you run the Proxy command with `--compile`, DLLMaster performs a Man-in-the-Middle attack setup on the file system:

1.  **The Hook:** The tool identifies the target function you want to intercept.
2.  **The Forwarding:** It creates linker comments (`#pragma`) to forward all other functions to a file named `OriginalName_real.dll`.
3.  **The Swap:** Since Windows cannot have two files with the same name, the tool renames the legitimate DLL to `_real.dll` and places the malicious Proxy DLL in its place using the original name.

When the target application starts: `App.exe` -> loads `MyDll.dll` (The Proxy) -> Executes Payload -> Forwards calls to `MyDll_real.dll`.

---

## ⚠️ Disclaimer

DLLMaster is developed for educational and security research purposes only. Usage of this tool for attacking targets without prior mutual consent is illegal. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.

---

## 🤝 Contributing

Feel free to fork the repository and submit Pull Requests for:

*   More advanced payload templates (Shellcode, Reflective Loading).
*   Support for x86 (32-bit) compilation flags.
*   Linux/Wine support.