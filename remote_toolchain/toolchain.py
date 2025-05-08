from pathlib import Path
from runners.python_runner import PythonRunner
from runners.cpp_runner import CppRunner
from runners.java_runner import JavaRunner
from runners.rust_runner import RustRunner

class Toolchain:
    """Toolchain Manager"""
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.remote_dir = self.config_manager.get("remote_dir")

    def get_remote_path(self, local_file):
        """Copy Local Files to Remote Files"""
        project_name = Path(local_file).parent.name
        remote_file = Path(self.remote_dir, project_name, Path(local_file).name).as_posix()
        print(f"Remote file path: {remote_file}")
        return remote_file

    def run(self, mode, local_file):
        """Choses Runner And Activates"""
        runners = {
            "-python": PythonRunner,
            "-cpp": CppRunner,
            "-java": JavaRunner,
            "-rust": RustRunner
        }
        runner_class = runners.get(mode)
        if not runner_class:
            raise ValueError(f"Unsupported mode: {mode}")
        runner = runner_class(self.config_manager)
        runner.run(local_file, self.get_remote_path(local_file))