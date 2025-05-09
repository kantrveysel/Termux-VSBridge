import os
import pytest
import dotenv

from termux_vsbridge.core.ssh_client import SSHClient

dotenv.load_dotenv()

@pytest.fixture(scope="session")
def set_environment():
    # Environment variable setup
    os.environ["MODE"] = "TEST"
    host = os.environ["HOST"]
    port = os.environ["PORT"]  # Corrected: previously using "HOST" for port as well
    username = os.environ["USERNAME"]  # Corrected: previously using "HOST" for username as well
    password = os.environ["PASSWORD"]  # Corrected: previously using "HOST" for password as well
    
    # Initialize SSH client
    ssh_client = SSHClient(host, port, username, password)
    
    # Return the initialized client for use in tests
    return ssh_client

def test_connect(set_environment):
    ssh_client = set_environment  # Access the fixture
    assert ssh_client.connect()  # Ensure no error is raised

def test_execute(set_environment):
    ssh_client = set_environment  # Access the fixture
    ssh_client.execute("echo testing")  # No error expected here
    assert ssh_client._line == "testing\n"  # Ensure the output is as expected

def test_close(set_environment):
    ssh_client = set_environment  # Access the fixture
    assert ssh_client.close()  # No error expected here