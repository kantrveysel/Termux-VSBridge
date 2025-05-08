# Termux-VSBridge

**Termux-VSBridge** is a lightweight toolchain that lets you run **Python**, **C++**, **Java**, and **Rust** projects directly on your Android device via **Termux**, using **Visual Studio Code** as your primary IDE. It leverages **SSH**, **Paramiko**, and VS Code's **Tasks API** to provide a seamless remote development experience with minimal setup.

[![Image](https://i.hizliresim.com/oar7wpr.gif)](https://hizliresim.com/oar7wpr)


---

## ✨ Features

- **Multi-Language Support**: Run Python, C++ (with `clang++`, `make`, `cmake`), Java, and Rust (with `cargo` or `rustc`) projects.
- **Real-Time Output**: Stream output from Termux to VS Code with `python -u` and optimized SSH handling.
- **Modular Test Suite**: Comprehensive unit tests for validating project functionality across languages.
- **VS Code Integration**: Seamless tasks for running and debugging projects.
- **Efficient File Transfer**: Transfers only relevant files (`.py`, `.cpp`, `.java`, `.rs`, `Makefile`, `CMakeLists.txt`, etc.).
- **Cross-Platform**: Works on Windows, Linux, and macOS, with Termux as the runtime environment.
- **Compiled Binary**: Optional single-file executable with PyInstaller, eliminating Python dependency.

---

## 🚀 Getting Started

### Prerequisites
- **Termux**: Installed on your Android device.
- **VS Code**: Installed on your computer.
- **SSH Access**: Termux SSH server running.
- **Compilers**: Required compilers installed in Termux (see Installation).

### Installation
1. **Set up Termux**:
   - Install Termux from [F-Droid](https://f-droid.org/packages/com.termux/) or the Play Store.
   - Install necessary packages:
     ```bash
     pkg install openssh
     ```
   - Start the SSH server and note your username and port (default: 8022):
     ```bash
     sshd
     whoami
     ss -tuln | grep 8022
     ```

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/kantrveysel/Termux-VSBridge.git
   cd Termux-VSBridge
   ```

3. **Install Python Dependencies** (if not using compiled binary):
   ```bash
   pip install paramiko
   ```

4. **Configure SSH**:
   - Edit `remote_toolchain/config.json` with your Termux SSH details:
     ```json
     {
       "host": "localhost",
       "port": 8022,
       "username": "u0_a123",
       "password": "your_password",
       "remote_dir": "/data/data/com.termux/files/home/tmp"
     }
     ```

### Using the Compiled Binary
To avoid installing Python and dependencies, download the precompiled `Termux-VSBridge` binary from the [Releases](https://github.com/kantrveysel/Termux-VSBridge/releases) page and run it directly:
```bash
./Termux-VSBridge -python test_project/test_script.py
```

---

## 🛠 Usage

1. Open the project in **VS Code**.
2. Open a source file (`.py`, `.cpp`, `.java`, `.rs`) in the `test_project` or `tests` directory.
3. Press `Ctrl + Shift + B` to open the task menu.
4. Select a runner:
   - `Run Python on Termux`
   - `Run C++ on Termux`
   - `Run Java on Termux`
   - `Run Rust on Termux`

Alternatively, use the command line:
- **Python**:
  ```bash
  python remote_toolchain/run.py -python test_project/test_script.py
  ```
- **C++**:
  ```bash
  python remote_toolchain/run.py -cpp test_project/test.cpp
  ```
- **Java**:
  ```bash
  python remote_toolchain/run.py -java test_project/test.java
  ```
- **Rust**:
  ```bash
  python remote_toolchain/run.py -rust test_project/test.rs
  ```

---


## 📁 Project Structure

```
Termux-VSBridge/
├── remote_toolchain/
│   ├── runners/
│   ├── tests/
├── test_project/
│   ├── core/
├── tests/
│   ├── test_cpp/
│   ├── test_python/
│   ├── test_java/
│   ├── test_rust/
├── .vscode/
│   ├── tasks.json
├── README.md
├── LICENSE
```

---

## 🛠 To Do

- **Windows Automation**: Improve path handling for Windows environments.
- **VS Code Extension**: Develop a dedicated extension for seamless integration.
- **Auto-Install Dependencies**: Script to install Termux dependencies automatically.
- **Interactive Terminal**: Support for interactive SSH sessions.
- **Incremental Builds**: Optimize file transfers by syncing only changed files.

---

## 🤝 Contributing

Contributions are welcome! Please check [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

Happy coding from your pocket! 🚀
