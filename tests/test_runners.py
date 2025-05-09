import sys
import os,time
import pytest
from pathlib import Path

# Proje kök dizinini sys.path'a ekleyin
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'termux_vsbridge'))

print((Path(__file__).resolve().parent.parent / 'termux_vsbridge'))
# Modül importlarını burada yapabilirsiniz
from termux_vsbridge.runners.python_runner import PythonRunner
from termux_vsbridge.runners.cpp_runner import CppRunner
from termux_vsbridge.runners.java_runner import JavaRunner
from termux_vsbridge.runners.rust_runner import RustRunner
from termux_vsbridge.runners.node_runner import NodeRunner



@pytest.fixture(scope="function")
def config_manager():
    """Set up ConfigManager with environment variables."""
    required_env_vars = ["HOST", "PORT", "USERNAME", "PASSWORD", "REMOTE_DIR"]
    if not all(key in os.environ for key in required_env_vars):
        pytest.skip("Missing environment variables: " + ", ".join(required_env_vars))

    config = {
        "host": os.environ["HOST"],
        "port": int(os.environ["PORT"]),
        "username": os.environ["USERNAME"],
        "password": os.environ["PASSWORD"],
        "remote_dir": os.environ["REMOTE_DIR"]
    }

    class ConfigManager:
        def get(self, key):
            return config[key]

    return ConfigManager()

@pytest.fixture
def remote_dir():
    """Return remote base directory path as a string with / separators."""
    return Path(os.environ["REMOTE_DIR"]).as_posix().rstrip("/")

@pytest.fixture
def create_temp_file(tmp_path):
    """Create a temporary local file for testing."""
    def _create_file(extension, content):
        file_path = tmp_path / f"test{extension}"
        file_path.write_bytes(content.encode("utf-8"))
        return file_path
    return _create_file

@pytest.fixture
def create_temp_cpp_files(tmp_path):
    """Create main and additional C++ files for testing."""
    main_file = tmp_path / "test.cpp"
    main_file.write_bytes('#include <iostream>\nint main() { std::cout << "Hello" << std::endl; return 0; }\n'.encode("utf-8"))
    additional_file = tmp_path / "helper.cpp"
    additional_file.write_bytes('#include <iostream>\nvoid helper() { std::cout << "Helper" << std::endl; }\n'.encode("utf-8"))
    return main_file, [additional_file]

def test_python_runner_run(config_manager, create_temp_file, remote_dir):
    """Test PythonRunner run method."""
    runner = PythonRunner(config_manager)
    local_file = create_temp_file(".py", 'print("Hello")')
    remote_path = f"{remote_dir}/{local_file.name}"

    runner.run(str(local_file), remote_path)

    # Verify file was uploaded
    runner.sftp_client._ensure_connected()
    try:
        runner.sftp_client.sftp.stat(remote_path)
    except FileNotFoundError:
        pytest.fail(f"File not found on remote server: {remote_path}")

    # Clean up
    try:
        runner.sftp_client.delete_file(remote_path)
    except FileNotFoundError:
        pass

@pytest.mark.skip (reason="#TODO")
def test_cpp_runner_run_single_file(config_manager, create_temp_file, remote_dir):
    """Test CppRunner run method for single file."""
    runner = CppRunner(config_manager)
    local_file = create_temp_file(".cpp", '#include <iostream>\nint main() { std::cout << "Hello" << std::endl; return 0; }\n')
    remote_path = f"{remote_dir}/{local_file.name}"

    # Ensure local temp_CMakeLists.txt is cleaned up if exists
    local_cmake = Path("temp_CMakeLists.txt")
    if local_cmake.exists():
        local_cmake.unlink()

    runner.run(str(local_file), remote_path)

    # Verify file and CMakeLists.txt were uploaded
    runner.sftp_client._ensure_connected()
    try:
        runner.sftp_client.sftp.stat(remote_path)
        runner.sftp_client.sftp.stat(f"{remote_dir}/CMakeLists.txt")
    except FileNotFoundError:
        pytest.fail(f"Files not found on remote server: {remote_path} or CMakeLists.txt")

    # Clean up
    try:
        runner.sftp_client.delete_file(remote_path)
        runner.sftp_client.delete_file(f"{remote_dir}/CMakeLists.txt")
        runner.sftp_client.delete_file(f"{remote_dir}/test")
    except FileNotFoundError:
        pass
    if local_cmake.exists():
        local_cmake.unlink()

@pytest.mark.skip (reason="#TODO")
def test_cpp_runner_run_with_additional_files(config_manager, create_temp_cpp_files, remote_dir):
    """Test CppRunner run method with additional files."""
    runner = CppRunner(config_manager)
    main_file, additional_files = create_temp_cpp_files
    remote_path = f"{remote_dir}/{main_file.name}"
    remote_additional_path = f"{remote_dir}/{additional_files[0].name}"

    # Ensure local temp_CMakeLists.txt is cleaned up
    local_cmake = Path("temp_CMakeLists.txt")
    if local_cmake.exists():
        local_cmake.unlink()

    runner.run(str(main_file), remote_path)
    time.sleep(0.5)

    # Verify files and CMakeLists.txt were uploaded
    runner.sftp_client._ensure_connected()
    missing_files = []
    runner.sftp_client.push("temp_CMakeLists.txt", f"{remote_dir}/CMakeLists.txt")
    runner.sftp_client._ensure_connected()
    try:
        runner.sftp_client.sftp.stat(remote_path)
    except FileNotFoundError:
        missing_files.append(remote_path)
    try:
        runner.sftp_client.sftp.stat(remote_additional_path)
    except FileNotFoundError:
        missing_files.append(remote_additional_path)
    try:
        runner.sftp_client.sftp.stat(f"{remote_dir}/CMakeLists.txt")
    except FileNotFoundError:
        missing_files.append(f"{remote_dir}/CMakeLists.txt")

    if missing_files:
        pytest.fail(f"Files not found on remote server: {', '.join(missing_files)}")

    # Clean up
    try:
        runner.sftp_client.delete_file(remote_path)
        runner.sftp_client.delete_file(remote_additional_path)
        runner.sftp_client.delete_file(f"{remote_dir}/CMakeLists.txt")
        runner.sftp_client.delete_file(f"{remote_dir}/test")
    except FileNotFoundError:
        pass
    if local_cmake.exists():
        local_cmake.unlink()

@pytest.mark.skip (reason="Java not installed on test enviroment")
def test_java_runner_run(config_manager, create_temp_file, remote_dir):
    """Test JavaRunner run method."""
    runner = JavaRunner(config_manager)
    local_file = create_temp_file(".java", 'public class Test { public static void main(String[] args) { System.out.println("Hello"); } }\n')
    remote_path = f"{remote_dir}/{local_file.name}"

    runner.run(str(local_file), remote_path)

    # Verify file was uploaded
    runner.sftp_client._ensure_connected()
    try:
        runner.sftp_client.sftp.stat(remote_path)
    except FileNotFoundError:
        pytest.fail(f"File not found on remote server: {remote_path}")

    # Clean up
    try:
        runner.sftp_client.delete_file(remote_path)
        runner.sftp_client.delete_file(f"{remote_dir}/Test.class")
    except FileNotFoundError:
        pass

@pytest.mark.skip (reason="Rust not installed on test enviroment")
def test_rust_runner_run_single_file(config_manager, create_temp_file, remote_dir):
    """Test RustRunner run method for single file."""
    runner = RustRunner(config_manager)
    local_file = create_temp_file(".rs", 'fn main() { println!("Hello"); }\n')
    remote_path = f"{remote_dir}/{local_file.name}"

    runner.run(str(local_file), remote_path)

    # Verify file and output were uploaded
    runner.sftp_client._ensure_connected()
    try:
        runner.sftp_client.sftp.stat(remote_path)
        runner.sftp_client.sftp.stat(f"{remote_dir}/test")
    except FileNotFoundError:
        pytest.fail(f"Files not found on remote server: {remote_path} or test")

    # Clean up
    try:
        runner.sftp_client.delete_file(remote_path)
        runner.sftp_client.delete_file(f"{remote_dir}/test")
    except FileNotFoundError:
        pass

@pytest.mark.skip (reason="Rust not installed on test enviroment")
def test_rust_runner_run_cargo_project(config_manager, create_temp_file, remote_dir):
    """Test RustRunner run method for Cargo project."""
    runner = RustRunner(config_manager)
    local_file = create_temp_file(".rs", 'fn main() { println!("Hello"); }\n')
    cargo_file = create_temp_file("_Cargo.toml", '[package]\nname = "test"\nversion = "0.1.0"\nedition = "2021"\n[dependencies]\n')
    remote_path = f"{remote_dir}/{local_file.name}"
    remote_cargo_path = f"{remote_dir}/Cargo.toml"

    # Upload Cargo.toml
    runner.sftp_client.push(str(cargo_file), remote_cargo_path)
    runner.run(str(local_file), remote_path)

    # Verify file and Cargo.toml were uploaded
    runner.sftp_client._ensure_connected()
    try:
        runner.sftp_client.sftp.stat(remote_path)
        runner.sftp_client.sftp.stat(remote_cargo_path)
    except FileNotFoundError:
        pytest.fail(f"Files not found on remote server: {remote_path} or Cargo.toml")

    # Clean up
    try:
        runner.sftp_client.delete_file(remote_path)
        runner.sftp_client.delete_file(remote_cargo_path)
    except FileNotFoundError:
        pass

def test_node_runner_run(config_manager, create_temp_file, remote_dir):
    """Test NodeRunner run method."""
    runner = NodeRunner(config_manager)
    local_file = create_temp_file(".ts", 'console.log("Hello");\n')
    remote_path = f"{remote_dir}/{local_file.name}"

    runner.run(str(local_file), remote_path)

    # Verify file was uploaded
    runner.sftp_client._ensure_connected()
    try:
        runner.sftp_client.sftp.stat(remote_path)
    except FileNotFoundError:
        pytest.fail(f"File not found on remote server: {remote_path}")

    # Clean up
    try:
        runner.sftp_client.delete_file(remote_path)
    except FileNotFoundError:
        pass



def recursive_remove(sftp_client, remote_path):
    try:
        for file_attr in sftp_client.listdir_attr(remote_path):
            file_path = f"{remote_path}/{file_attr.filename}"
            if file_attr.st_mode & 0o40000: 
                recursive_remove(sftp_client, file_path)
            else:
                sftp_client.remove(file_path)
        
        sftp_client.rmdir(remote_path)

    except Exception as e:
        print(f"[WARN] Error while removing {remote_path}: {e}")

import paramiko

@pytest.fixture(scope="session", autouse=True)
def cleanup_remote_dir():
    yield

    os.environ["MODE"] = "TEST"
    host = os.environ["HOST"]
    port = int(os.environ["PORT"])
    username = os.environ["USERNAME"]
    password = os.environ["PASSWORD"]  
    
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    sftp_client = paramiko.SFTPClient.from_transport(transport)

    remote_dir = os.environ["REMOTE_DIR"]

    try:
        # Dizini ve içeriğini temizle
        recursive_remove(sftp_client, remote_dir)

    except Exception as e:
        print(f"[WARN] Remote cleanup failed: {e}")
    finally:
        sftp_client.close()
        transport.close()
