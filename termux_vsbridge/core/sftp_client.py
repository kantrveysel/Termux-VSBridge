import paramiko
import os
from pathlib import Path

class SFTPClient:
    """Manages File & Folders"""
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.transport = None
        self.sftp = None

    def _ensure_connected(self):
        """Ensure the SFTP connection is active, reconnect if necessary."""
        if not self.transport or not self.sftp:
            self.connect()
        try:
            self.sftp.listdir(".")  # Test connection
        except (paramiko.SSHException, OSError):
            self.connect()

    def connect(self):
        """Starts SFTP"""
        self.transport = paramiko.Transport((self.host, self.port))
        self.transport.connect(username=self.username, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def mkdir(self, dir_path):
        """Creates folders and subfolders recursively"""
        parts = Path(dir_path).parts
        current_path = ""
        for part in parts:
            current_path = os.path.join(current_path, part) if current_path else part
            current_path_posix = Path(current_path).as_posix()
            try:
                self.sftp.stat(current_path_posix)
            except FileNotFoundError:
                print(f"Creating directory: {current_path_posix}")
                self.sftp.mkdir(current_path_posix)

    def create_file_structure(self, project_dir, remote_dir):
        """Uploads project to the remote connection"""
        for root, dirs, files in os.walk(project_dir):
            # Uzak yol, remote_dir altında relatif yol ile oluşturulur
            r_path = os.path.join(remote_dir, os.path.relpath(root, project_dir))
            r_path_posix = Path(r_path).as_posix()
            self.mkdir(r_path_posix)

            for file in files:
                local_path = os.path.join(root, file)
                remote_path = os.path.join(r_path, file)
                remote_path_posix = Path(remote_path).as_posix()
                self.sftp.put(local_path, remote_path_posix)
                print(f"Sending {local_path} -> {remote_path_posix}")
            print(f"Processed folder: {r_path_posix}")

    def push(self, local_path, remote_path):
        """Pushs local files to remote folder"""
        self.connect()
        local_dir = os.path.dirname(local_path)
        remote_dir = os.path.dirname(remote_path)
        self.mkdir(remote_dir)
        self.create_file_structure(local_dir, remote_dir)
        self.close()

    def delete_file(self, remote_path):
        """Deletes a file on the remote server"""
        try:
            self.sftp.remove(remote_path)
            print(f"Deleted file: {remote_path}")
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {remote_path}")
        except Exception as e:
            raise Exception(f"Error deleting file {remote_path}: {str(e)}")

    def delete_directory(self, remote_path):
        """Deletes an empty directory on the remote server"""
        try:
            self.sftp.rmdir(remote_path)
            print(f"Deleted directory: {remote_path}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Directory not found: {remote_path}")
        except OSError:
            raise OSError(f"Directory is not empty: {remote_path}")
        except Exception as e:
            raise Exception(f"Error deleting directory {remote_path}: {str(e)}")

    def close(self):
        """Cloeses SFTP Connection"""
        if self.sftp:
            self.sftp.close()
        if self.transport:
            self.transport.close()