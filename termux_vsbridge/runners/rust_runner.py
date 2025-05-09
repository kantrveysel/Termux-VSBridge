from . import SSHClient, SFTPClient,os

class RustRunner:
    """Rust dosyalarını uzak sunucuda derler ve çalıştırır."""
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
        """Rust dosyasını derler ve çalıştırır."""
        self.sftp_client.push(local_file, remote_path)
        remote_dir = os.path.dirname(remote_path).replace('\\', '/')
        self.ssh_client.connect()
        # Cargo projesi kontrolü
        cargo_path = os.path.join(remote_dir, "Cargo.toml").replace('\\', '/')
        self.sftp_client.connect()
        try:
            self.sftp_client.sftp.stat(cargo_path)
            print(f"Cargo.toml found, running cargo in {remote_dir}")
            self.ssh_client.execute(f"cd {remote_dir} && cargo run")
        except FileNotFoundError:
            print("No Cargo.toml found, compiling single file")
            output_file = os.path.splitext(remote_path)[0].replace('\\', '/')
            self.ssh_client.execute(f"rustc {remote_path} -o {output_file}")
            self.ssh_client.execute(f"{output_file}")
        finally:
            self.sftp_client.close()