import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from termux_vsbridge.core.ssh_client import SSHClient
from termux_vsbridge.core.sftp_client import SFTPClient
import os