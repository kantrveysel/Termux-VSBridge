import json
import os

class ConfigManager:
    """Configuration Manager"""
    def __init__(self, config_path="remote_toolchain/config.json"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        """Loads Configuration from config.json"""
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def get(self, key):
        """Assigns config keys"""
        return self.config.get(key)