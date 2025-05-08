from ssh_client import SSHClient
from sftp_client import SFTPClient
import os
from pathlib import Path

class CppRunner:
    """C++ Project Runner"""
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

    def create_temp_cmake(self, remote_dir, main_file, additional_files=None):
        """Creates a temporary CMakeLists.txt for single-file or modular projects."""
        project_name = os.path.splitext(os.path.basename(main_file))[0]
        cmake_content = [
            "cmake_minimum_required(VERSION 3.10)",
            f"project({project_name})",
            "set(CMAKE_CXX_COMPILER \"clang++\")",
            "set(CMAKE_CXX_STANDARD 17)",
            "set(CMAKE_CXX_STANDARD_REQUIRED ON)",
            f"add_executable({project_name} {os.path.basename(main_file)}"
        ]
        if additional_files:
            for file in additional_files:
                cmake_content.append(f" {file}")
        cmake_content.append(")")
        cmake_content = "\n".join(cmake_content)

        # Write temporary CMakeLists.txt to remote_dir
        temp_cmake_path = os.path.join(remote_dir, "CMakeLists.txt").replace('\\', '/')
        with open("temp_CMakeLists.txt", "w") as f:
            f.write(cmake_content)
        self.sftp_client.sftp.put("temp_CMakeLists.txt", temp_cmake_path)
        os.remove("temp_CMakeLists.txt")
        print(f"Temporary CMakeLists.txt created at {temp_cmake_path}")

    def run(self, local_file, remote_path):
        """Compiles & Runs C++ Projects"""
        self.sftp_client.push(local_file, remote_path)
        remote_dir = os.path.dirname(remote_path).replace('\\', '/')
        self.ssh_client.connect()
        self.sftp_client.connect()

        # Makefile Check
        makefile_path = os.path.join(remote_dir, "Makefile").replace('\\', '/')
        try:
            self.sftp_client.sftp.stat(makefile_path)
            print(f"Makefile found, running make in {remote_dir}")
            self.ssh_client.execute(f"cd {remote_dir} && make && ./test")
            self.sftp_client.close()
            return
        except FileNotFoundError:
            print("No Makefile found, checking for CMakeLists.txt")

        # CMakeLists.txt Check
        cmake_path = os.path.join(remote_dir, "CMakeLists.txt").replace('\\', '/')
        try:
            self.sftp_client.sftp.stat(cmake_path)
            print(f"CMakeLists.txt found, running cmake in {remote_dir}")
            self.ssh_client.execute(f"cd {remote_dir} && cmake . && make && ./test")
            self.sftp_client.close()
            return
        except FileNotFoundError:
            print("No CMakeLists.txt found, generating temporary CMakeLists.txt")

        # Generate temporary CMakeLists.txt for single-file or modular project
        additional_files = []
        local_dir = os.path.dirname(local_file)
        for root, _, files in os.walk(local_dir):
            for file in files:
                if file.endswith('.cpp') and file != os.path.basename(local_file):
                    rel_path = os.path.relpath(os.path.join(root, file), local_dir).replace('\\', '/')
                    additional_files.append(rel_path)
                    # Ensure additional files are transferred
                    local_additional = os.path.join(root, file)
                    remote_additional = os.path.join(remote_dir, rel_path).replace('\\', '/')
                    self.sftp_client.sftp.put(local_additional, remote_additional)
                    print(f"Sending additional file {local_additional} -> {remote_additional}")

        self.create_temp_cmake(remote_dir, remote_path, additional_files)
        self.ssh_client.execute(f"cd {remote_dir} && cmake . && make && ./test")
        self.sftp_client.close()