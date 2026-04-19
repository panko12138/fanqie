
import datetime
from pathlib import Path

from config import get_config


def format_time(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes:02d}:{remaining_seconds:02d}"


def format_duration(seconds, show_hours=False):
    if seconds < 60:
        return f"{seconds}秒"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    
    if show_hours or hours > 0:
        if minutes > 0:
            return f"{hours}小时{minutes}分钟"
        return f"{hours}小时"
    return f"{minutes}分钟"


def format_date(date):
    if isinstance(date, str):
        try:
            date = datetime.datetime.fromisoformat(date).date()
        except ValueError:
            return date
    return date.strftime('%Y-%m-%d')


def format_datetime(dt=None):
    if dt is None:
        dt = datetime.datetime.now()
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def get_today_date():
    return datetime.date.today()


def get_week_range(date=None):
    if date is None:
        date = get_today_date()
    monday = date - datetime.timedelta(days=date.weekday())
    sunday = monday + datetime.timedelta(days=6)
    return monday, sunday


def get_month_range(date=None):
    if date is None:
        date = get_today_date()
    first_day = datetime.date(date.year, date.month, 1)
    if date.month == 12:
        next_month_first = datetime.date(date.year + 1, 1, 1)
    else:
        next_month_first = datetime.date(date.year, date.month + 1, 1)
    last_day = next_month_first - datetime.timedelta(days=1)
    return first_day, last_day


def ensure_dir(path):
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def get_resources_path():
    base_dir = get_config('BASE_DIR', Path(__file__).parent.parent)
    return base_dir / 'resources'


def get_data_path():
    base_dir = get_config('BASE_DIR', Path(__file__).parent.parent)
    return ensure_dir(base_dir / 'data')


def truncate_string(text, max_length=50, suffix='...'):
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
