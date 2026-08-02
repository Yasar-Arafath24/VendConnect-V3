from pathlib import Path
from loguru import logger
import sys

# Create logs directory
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.remove()

# Console logging
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
           "{message}",
)

# File logging
logger.add(
    "logs/vendconnect.log",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    level="INFO",
)

app_logger = logger