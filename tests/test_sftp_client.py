import os
import pytest
from pathlib import Path
from termux_vsbridge.core.sftp_client import SFTPClient

@pytest.fixture(scope="function")
def set_environment():
    """Set up SFTP client with environment variables and ensure cleanup."""
    required_env_vars = ["HOST", "PORT", "USERNAME", "PASSWORD", "REMOTE_DIR"]
    if not all(key in os.environ for key in required_env_vars):
        pytest.skip("Missing environment variables: " + ", ".join(required_env_vars))

    host = os.environ["HOST"]
    port = int(os.environ["PORT"])
    username = os.environ["USERNAME"]
    password = os.environ["PASSWORD"]

    sftp_client = SFTPClient(host, port, username, password)
    sftp_client._ensure_connected()

    yield sftp_client

    sftp_client.close()

@pytest.fixture
def remote_dir():
    """Return remote base directory path as a string with / separators."""
    return Path(os.environ["REMOTE_DIR"]).as_posix().rstrip("/")

@pytest.fixture
def create_temp_file(tmp_path):
    """Create a temporary local file for testing."""
    file_path = tmp_path / "test_file.txt"
    file_path.write_bytes(b"Test content")
    return file_path

def test_connect(set_environment):
    """Test connection to the SFTP server."""
    sftp_client = set_environment
    sftp_client._ensure_connected()
    assert sftp_client.sftp is not None, "SFTP connection failed"

def test_create_file(set_environment, create_temp_file, remote_dir):
    """Test uploading a file to the remote server."""
    sftp_client = set_environment
    remote_path = f"{remote_dir}/{create_temp_file.name}"

    sftp_client.push(str(create_temp_file), remote_path)

    sftp_client._ensure_connected()
    try:
        sftp_client.sftp.stat(remote_path)
    except FileNotFoundError:
        pytest.fail(f"File not found on remote server: {remote_path}")

def test_delete_file(set_environment, create_temp_file, remote_dir):
    """Test deleting a file from the remote server."""
    sftp_client = set_environment
    remote_path = f"{remote_dir}/{create_temp_file.name}"

    sftp_client.push(str(create_temp_file), remote_path)
    sftp_client._ensure_connected()
    sftp_client.delete_file(remote_path)

    sftp_client._ensure_connected()
    with pytest.raises(FileNotFoundError):
        sftp_client.sftp.stat(remote_path)

def test_create_directory(set_environment, remote_dir):
    """Test creating a directory on the remote server."""
    sftp_client = set_environment
    remote_path = f"{remote_dir}/new_directory"

    sftp_client._ensure_connected()
    sftp_client.mkdir(remote_path)

    sftp_client._ensure_connected()
    try:
        sftp_client.sftp.stat(remote_path)
    except FileNotFoundError:
        pytest.fail(f"Directory not found on remote server: {remote_path}")

def test_delete_directory(set_environment, remote_dir):
    """Test deleting an empty directory from the remote server."""
    sftp_client = set_environment
    remote_path = f"{remote_dir}/empty_directory"

    sftp_client._ensure_connected()
    sftp_client.mkdir(remote_path)
    sftp_client._ensure_connected()
    sftp_client.delete_directory(remote_path)

    sftp_client._ensure_connected()
    with pytest.raises(FileNotFoundError):
        sftp_client.sftp.stat(remote_path)

def test_delete_non_empty_directory(set_environment, remote_dir, create_temp_file):
    """Test attempting to delete a non-empty directory (should fail)."""
    sftp_client = set_environment
    remote_path = f"{remote_dir}/non_empty_dir"
    file_path = f"{remote_path}/{create_temp_file.name}"

    sftp_client._ensure_connected()
    sftp_client.mkdir(remote_path)
    sftp_client.push(str(create_temp_file), file_path)

    sftp_client._ensure_connected()
    with pytest.raises(OSError):
        sftp_client.delete_directory(remote_path)

def test_file_not_found_error(set_environment, remote_dir):
    """Test attempting to delete a non-existent file."""
    sftp_client = set_environment
    remote_path = f"{remote_dir}/non_existent_file.txt"

    sftp_client._ensure_connected()
    with pytest.raises(FileNotFoundError):
        sftp_client.delete_file(remote_path)