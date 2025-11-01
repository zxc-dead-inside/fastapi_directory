import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from colorama import Fore, Style, init as colorama_init

from app.core.config import settings

colorama_init(autoreset=True)


COLORS = {
    "DEBUG": Fore.CYAN,
    "INFO": Fore.GREEN,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "CRITICAL": Fore.MAGENTA,
}


class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        formatter = logging.Formatter(settings.log_format)
        color = COLORS.get(record.levelname, "")
        return f"{color}{formatter.format(record)}{Style.RESET_ALL}"


def init_logger(name: str) -> logging.Logger:
    log_dir = Path(settings.log_dir)
    log_dir.mkdir(exist_ok=True)

    log_path = log_dir / settings.log_file

    logger = logging.getLogger(name)
    logger.setLevel(settings.log_level.upper())

    # console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.log_level.upper())
    console_handler.setFormatter(ColorFormatter())

    # file handler
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=settings.log_max_bytes,
        backupCount=settings.log_backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(settings.log_level.upper())
    file_handler.setFormatter(logging.Formatter(settings.log_format))

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    logger.propagate = False
    return logger


logger = init_logger("app")
