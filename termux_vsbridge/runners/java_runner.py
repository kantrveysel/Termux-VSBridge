from . import SSHClient, SFTPClient, os


class JavaRunner:
    """Java Project Runner"""

    def __init__(self, config_manager):
        self.config_manager = config_manager
        self._setup_clients()

    def _setup_clients(self):
        """Initialize SSH and SFTP clients"""
        credentials = (
            self.config_manager.get("host"),
            self.config_manager.get("port"),
            self.config_manager.get("username"),
            self.config_manager.get("password")
        )
        self.ssh_client = SSHClient(*credentials)
        self.sftp_client = SFTPClient(*credentials)

    def _extract_paths(self, remote_path):
        """Extract remote directory and class name"""
        remote_dir = os.path.dirname(remote_path).replace('\\', '/')
        class_name = os.path.splitext(os.path.basename(remote_path))[0]
        return remote_dir, class_name

    def _compile_java(self, remote_dir, filename):
        """Compile Java file on remote"""
        self.ssh_client.execute(f"cd {remote_dir} && javac {filename}")

    def _run_java(self, remote_dir, class_name):
        """Run Java class on remote"""
        self.ssh_client.execute(f"cd {remote_dir} && java {class_name}")

    def run(self, local_file, remote_path):
        """Main entry: Compile & Run Java source"""
        self.sftp_client.push(local_file, remote_path)
        remote_dir, class_name = self._extract_paths(remote_path)

        self.ssh_client.connect()
        self._compile_java(remote_dir, os.path.basename(remote_path))
        self._run_java(remote_dir, class_name)