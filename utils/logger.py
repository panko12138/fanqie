
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

from config import get_config


def get_logger(
    name='pomodoro',
    log_dir=None,
    log_level=None
):
    """
    获取配置好的日志记录器

    Args:
        name: 日志记录器名称
        log_dir: 日志文件目录
        log_level: 日志级别

    Returns:
        配置好的 logger 对象
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    if log_level is None:
        log_level = get_config('LOG_LEVEL', 'INFO')

    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)
    logger.propagate = False

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_dir is None:
        base_dir = get_config('BASE_DIR', Path(__file__).parent.parent)
        log_dir = base_dir / 'logs'

    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / 'pomodoro.log'

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


logger = get_logger()
