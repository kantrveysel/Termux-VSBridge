from . import SSHClient, SFTPClient

class PythonRunner:
    """Python dosyalarını uzak sunucuda çalıştırır."""
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
        """Python dosyasını çalıştırır."""
        self.sftp_client.push(local_file, remote_path)
        self.ssh_client.connect()
        self.ssh_client.execute(f"python -u {remote_path}")