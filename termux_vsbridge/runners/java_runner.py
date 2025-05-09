from . import SSHClient, SFTPClient, os

class JavaRunner:
    """Java Runner"""
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
        """Java Compiler &  Runner"""
        self.sftp_client.push(local_file, remote_path)
        remote_dir = os.path.dirname(remote_path).replace('\\', '/')
        class_name = os.path.splitext(os.path.basename(remote_path))[0]
        self.ssh_client.connect()
        self.ssh_client.execute(f"cd {remote_dir} && javac {os.path.basename(remote_path)}")
        self.ssh_client.execute(f"cd {remote_dir} && java {class_name}")