import json
import subprocess
from pathlib import Path
import os
import sys


DUMMY_CONFIG = {
    "host": "localhost",
    "port": 8022,
    "username": "u0_a123",
    "password": "password",
    "remote_dir": "/data/data/com.termux/files/home/tmp/"
  }

class ConfigManager:
    CONFIG_PATH = Path("./.vscode/config.json")
    """Configuration Manager"""
    def __init__(self, run_mode, config_path = CONFIG_PATH):
        if run_mode == "TEST":
            print(f" Running on {run_mode} Mode")
            self.get_config_env()
            return
        self.config_path = config_path
        config_path.parent.mkdir(parents=True, exist_ok=True)
        if self.config_path.exists():
            self.config = self._load_config()
        else:
            self._check_config_file()

    def get_config_env(self):
        self.config ={
                    "host": os.environ.get("HOST"),
                    "port": int(os.environ.get("PORT")),
                    "username": os.environ.get("USERNAME"),
                    "password": os.environ.get("PASSWORD"),
                    "remote_dir": os.environ.get("REMOTE_DIR")
        }
    def _check_config_file(self):
        with open(self.config_path, "w") as f:
            json.dump(DUMMY_CONFIG, f, indent=4)
            f.flush()
            os.fsync(f.fileno())
            
        try:
            subprocess.run(['start', 'code', str(self.config_path)], shell=True)
        except:
            print("VSCode not installed or not in the path -> You need to edit config.json")
        sys.exit(1)

    def _load_config(self):
        """Loads Configuration from config.json"""
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def get(self, key):
        """Assigns config keys"""
        return self.config.get(key)