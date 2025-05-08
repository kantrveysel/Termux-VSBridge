# Contributing to Termux-VSBridge

Thank you for considering contributing to **Termux-VSBridge**! 🎉  
This guide will help you get started quickly and contribute effectively to our lightweight toolchain for running Python, C++, Java, and Rust projects on Termux via VS Code.

---

## 💡 How Can You Help?

We welcome contributions in many forms:
- 🐛 **Bug Reports**: Found a bug? Please [open an issue](https://github.com/kantrveysel/Termux-VSBridge/issues) with details about the problem and steps to reproduce it.
- 🚀 **Feature Suggestions**: Have an idea to improve the tool? Share it in the [issues](https://github.com/kantrveysel/Termux-VSBridge/issues) section.
- 🧪 **Testing**: Help test the toolchain on different Termux setups, Android versions, or host operating systems (Windows, Linux, macOS).
- 📦 **Code Contributions**: Want to fix bugs, add features, or improve documentation? Fork the repository and submit a pull request!

---

## 🧰 Development Setup

To start contributing, follow these steps:

1. **Fork the Repository**:
   - Click the "Fork" button on the [Termux-VSBridge GitHub page](https://github.com/kantrveysel/Termux-VSBridge) to create your own copy.

2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Termux-VSBridge.git
   cd Termux-VSBridge
   ```

3. **Set Up Your Environment**:
   - **Python**: Ensure you have Python 3.6+ installed.
   - **Dependencies**: Install required Python packages:
     ```bash
     pip install paramiko
     ```
   - **Termux**: Install Termux on your Android device and set up the SSH server:
     ```bash
     pkg install openssh python clang make cmake openjdk-17 rust
     sshd
     ```
   - **VS Code**: Install VS Code with task runner support (no additional extensions needed).
   - **Configuration**: Edit `remote_toolchain/config.json` with your Termux SSH credentials:
     ```json
     {
       "host": "localhost",
       "port": 8022,
       "username": "u0_a123",
       "password": "your_password",
       "remote_dir": "/data/data/com.termux/files/home/tmp"
     }
     ```

4. **Test Your Setup**:
   - Run a sample project:
     ```bash
     python remote_toolchain/run.py -python test_project/test_script.py
     ```
   - Run the unit tests to ensure everything works:
     ```bash
     python remote_toolchain/tests/test_runner.py
     ```

---

## 🔀 Submitting a Pull Request

1. **Create a New Branch**:
   - Use a descriptive branch name, e.g., `feature/add-go-runner` or `fix/windows-path-handling`:
     ```bash
     git checkout -b feature/your-feature-name
     ```

2. **Make Your Changes**:
   - Work on your feature, bug fix, or documentation improvement.
   - Add or update tests in the `tests` directory (e.g., `tests/test_cpp`, `tests/test_python`) if your changes affect the runners or core functionality.

3. **Commit Your Changes**:
   - Write clear, concise commit messages:
     ```bash
     git commit -m "Add: Support for Go runner in toolchain"
     ```

4. **Push Your Branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request**:
   - Go to the [Termux-VSBridge repository](https://github.com/kantrveysel/Termux-VSBridge) and create a pull request from your branch.
   - Describe your changes, why they’re needed, and any relevant details (e.g., new dependencies, test results).

---

## 🧹 Code Style

To keep the codebase consistent and maintainable, please follow these guidelines:
- **Python Conventions**: Adhere to [PEP8](https://www.python.org/dev/peps/pep-0008/) for Python code.
  - Use `black` or `flake8` for code formatting and linting.
  - Keep functions modular and avoid overly long functions.
- **Path Handling**: Use `pathlib.Path().as_posix()` for cross-platform path compatibility (especially for Windows).
- **Comments**: Write clear, concise comments to explain complex logic.
- **File Transfers**: Ensure `sftp_client.py` only transfers relevant files (e.g., `.py`, `.cpp`, `.java`, `.rs`, `Makefile`, `CMakeLists.txt`).
- **Testing**: Add unit tests for new features or bug fixes in the `tests` directory. For example:
  - Python tests: `tests/test_python/test_script.py`
  - C++ tests: `tests/test_cpp/test.cpp`

---

## 🧪 Adding Tests

The `tests` directory contains modular test suites for each supported language:
- `test_python`: Tests Python scripts with modular utilities (`core/utils.py`).
- `test_cpp`: Tests C++ projects with `make`, `cmake`, and helper modules (`utils/helper.h`).
- `test_java`: Tests Java classes with package structure (`utils/Helper.java`).
- `test_rust`: Tests Rust projects with `cargo` and modular utilities (`src/utils.rs`).

To add a new test:
1. Create or update a test file in the relevant directory (e.g., `tests/test_python/new_test.py`).
2. Ensure the test is modular (e.g., uses helper modules or classes).
3. Run the test suite to verify:
   ```bash
   python remote_toolchain/tests/test_runner.py
   ```

---

## 📦 Building the Binary

Termux-VSBridge can be compiled into a single executable using PyInstaller, eliminating the need for Python on the user’s machine.

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Compile the project:
   ```bash
   pyinstaller --onefile --name Termux-VSBridge remote_toolchain/run.py
   ```

3. Test the binary:
   ```bash
   ./dist/Termux-VSBridge -python test_project/test_script.py
   ```

If you add new files or dependencies, update the `Termux-VSBridge.spec` file to include them.

---

## 🤝 Code of Conduct

We strive to create a welcoming and inclusive community. Please:
- Be respectful and supportive in all interactions.
- Provide constructive feedback and avoid personal attacks.
- Help others learn and grow through your contributions.

---

## 🙌 Thank You!

Your contributions help make Termux-VSBridge better for everyone. Whether it’s a bug fix, a new feature, or improved documentation, we appreciate your effort! If you have questions, feel free to reach out via [issues](https://github.com/kantrveysel/Termux-VSBridge/issues).

Happy coding! 🚀