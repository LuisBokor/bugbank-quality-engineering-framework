import logging
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
    root = Path(__file__).resolve().parents[1]
    log_dir = root / "reports" / "logs"
    technical_dir = root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    technical_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.FileHandler(technical_dir / "framework.log", encoding="utf-8")
        report_handler = logging.FileHandler(log_dir / "automation.log", encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
        report_handler.setFormatter(handler.formatter)
        logger.addHandler(handler)
        logger.addHandler(report_handler)
        logger.setLevel(logging.INFO)
    return logger
