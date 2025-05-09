import sys
import dotenv
import os
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from termux_vsbridge.core.config_manager import ConfigManager
from termux_vsbridge.core.toolchain import Toolchain

dotenv.load_dotenv(".env")

run_mode = os.environ.get("MODE", "PRODUCTION")

print(run_mode)
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Use: python run.py [-python|-cpp] <file>")
        sys.exit(1)

    mode = sys.argv[1]
    local_file = sys.argv[2]
    config_manager = ConfigManager(run_mode=run_mode)
    toolchain = Toolchain(config_manager)
    toolchain.run(mode, local_file)