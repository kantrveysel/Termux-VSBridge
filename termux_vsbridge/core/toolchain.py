import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from termux_vsbridge.runners.python_runner import PythonRunner
from termux_vsbridge.runners.cpp_runner import CppRunner
from termux_vsbridge.runners.java_runner import JavaRunner
from termux_vsbridge.runners.rust_runner import RustRunner
from termux_vsbridge.runners.node_runner import NodeRunner
from termux_vsbridge.runners.shell_runner import ShellRunner

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
            "-node": NodeRunner,
            "-python": PythonRunner,
            "-cpp": CppRunner,
            "-java": JavaRunner,
            "-rust": RustRunner,
            "-shell": ShellRunner
        }
        runner_class = runners.get(mode)
        if not runner_class:
            raise ValueError(f"Unsupported mode: {mode}")
        runner = runner_class(self.config_manager)
        runner.run(local_file, self.get_remote_path(local_file))