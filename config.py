from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent

# Application directories
IMAGE_DIR = BASE_DIR / "imgattendance"
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
IMAGE_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
