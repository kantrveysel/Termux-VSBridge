from . import SSHClient, SFTPClient, os


class RustRunner:
    """Rust Project Runner"""

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

    def _extract_dir(self, remote_path):
        return os.path.dirname(remote_path).replace('\\', '/')

    def _is_cargo_project(self, remote_dir):
        """Check if Cargo.toml exists"""
        cargo_path = os.path.join(remote_dir, "Cargo.toml").replace('\\', '/')
        try:
            self.sftp_client.sftp.stat(cargo_path)
            return True
        except FileNotFoundError:
            return False

    def _run_cargo(self, remote_dir):
        """Run cargo project"""
        print(f"Cargo.toml found, running cargo in {remote_dir}")
        self.ssh_client.execute(f"cd {remote_dir} && cargo run")

    def _compile_and_run_single(self, remote_path):
        """Compile and run single Rust file"""
        output_path = os.path.splitext(remote_path)[0].replace('\\', '/')
        print("No Cargo.toml found, compiling single file")
        self.ssh_client.execute(f"rustc {remote_path} -o {output_path}")
        self.ssh_client.execute(output_path)

    def run(self, local_file, remote_path):
        """Main entry: Compile & Run Rust code"""
        self.sftp_client.push(local_file, remote_path)
        remote_dir = self._extract_dir(remote_path)

        self.ssh_client.connect()
        self.sftp_client.connect()

        try:
            if self._is_cargo_project(remote_dir):
                self._run_cargo(remote_dir)
            else:
                self._compile_and_run_single(remote_path)
        finally:
            self.sftp_client.close()