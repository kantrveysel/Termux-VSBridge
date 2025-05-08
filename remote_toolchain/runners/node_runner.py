from ssh_client import SSHClient
from sftp_client import SFTPClient

class NodeRunner:
    """Node.js dosyalarını uzak sunucuda çalıştırır, nyaaa~"""
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.ssh_client = SSHClient(
            config_manager.get("host"),
            config_manager.get("port"),
            config_manager.get("username"),
            config_manager.get("password")
        )
        self.sftp_client = SFTPClient(
            config_manager.get("host"),
            config_manager.get("port"),
            config_manager.get("username"),
            config_manager.get("password")
        )

    def run(self, local_file, remote_path):
        """Node.js dosyasını çalıştırır uwu~"""
        self.sftp_client.push(local_file, remote_path)
        self.ssh_client.connect()
        self.ssh_client.execute(f"npx -y tsx {remote_path}")
