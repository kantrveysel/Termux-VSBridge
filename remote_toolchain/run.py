import sys
from config_manager import ConfigManager
from toolchain import Toolchain

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Use: python run.py [-python|-cpp] <file>")
        sys.exit(1)

    mode = sys.argv[1]
    local_file = sys.argv[2]
    config_manager = ConfigManager()
    toolchain = Toolchain(config_manager)
    toolchain.run(mode, local_file)