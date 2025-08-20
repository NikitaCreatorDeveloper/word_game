import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging():
    log_dir = Path.home() / ".word_game_kivy"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "app.log"

    fmt = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=fmt,
        handlers=[
            logging.StreamHandler(),
            RotatingFileHandler(
                log_file, maxBytes=512_000, backupCount=3, encoding="utf-8"
            ),
        ],
    )
    logging.getLogger("kivy").setLevel(logging.WARNING)
