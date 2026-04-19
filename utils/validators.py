
import re


class ValidationError(Exception):
    pass


def validate_task_name(name):
    if not name or not name.strip():
        return False, "任务名称不能为空"
    if len(name) > 255:
        return False, "任务名称不能超过255个字符"
    return True, None


def validate_subject(subject):
    valid_subjects = ['政治', '英语', '数学', '专业课', '其他']
    if subject not in valid_subjects:
        return False, f"科目必须是以下之一：{', '.join(valid_subjects)}"
    return True, None


def validate_pomodoro_count(count):
    if not isinstance(count, int):
        return False, "番茄数量必须是整数"
    if count < 1:
        return False, "番茄数量至少为1"
    if count > 100:
        return False, "番茄数量不能超过100"
    return True, None


def validate_priority(priority):
    valid_priorities = ['高', '中', '低']
    if priority not in valid_priorities:
        return False, f"优先级必须是以下之一：{', '.join(valid_priorities)}"
    return True, None


def validate_duration(duration, min_val=1, max_val=3600):
    if not isinstance(duration, int):
        return False, "时长必须是整数"
    if duration < min_val:
        return False, f"时长不能小于{min_val}秒"
    if duration > max_val:
        return False, f"时长不能超过{max_val}秒"
    return True, None


def validate_db_config(host, port, user, password, db_name):
    errors = []
    if not host or not host.strip():
        errors.append("主机地址不能为空")
    if not isinstance(port, int) or port < 1 or port > 65535:
        errors.append("端口号必须在1-65535之间")
    if not user or not user.strip():
        errors.append("用户名不能为空")
    if not db_name or not db_name.strip():
        errors.append("数据库名不能为空")
    if not re.match(r'^[a-zA-Z0-9_\-]+$', db_name):
        errors.append("数据库名只能包含字母、数字、下划线和连字符")
    return len(errors) == 0, errors


def validate_date(date_str):
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return False, "日期格式必须为 YYYY-MM-DD"
    return True, None
