from datetime import datetime
from .connection import get_db_manager
from models import (
    Base,
    Setting,
    Achievement,
    TaskTemplate,
    DailyStat,
)
from utils.logger import get_logger

logger = get_logger(__name__)


def init_database():
    from config import Config
    import re
    config = Config()
    
    # 先连接到MySQL服务器创建数据库
    import mysql.connector
    try:
        conn = mysql.connector.connect(
            host=config.get('DB_HOST'),
            port=config.get('DB_PORT'),
            user=config.get('DB_USER'),
            password=config.get('DB_PASSWORD')
        )
        cursor = conn.cursor()
        db_name = config.get('DB_NAME')
        
        # 验证数据库名，防止SQL注入
        if not re.match(r'^[a-zA-Z0-9_\-]+$', db_name):
            raise ValueError(f"无效的数据库名: {db_name}")
        
        # 直接使用反引号包裹数据库名，因为已经通过正则验证
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.close()
        conn.close()
        logger.info(f"数据库 {db_name} 创建成功")
    except Exception as e:
        logger.warning(f"创建数据库失败: {e}")
    
    # 现在连接到具体数据库
    db_manager = get_db_manager()
    engine = db_manager.get_engine()

    logger.info("创建数据库表结构...")
    Base.metadata.create_all(bind=engine)
    logger.info("数据库表结构创建完成")

    with db_manager.session() as session:
        init_settings(session)
        init_achievements(session)
        init_task_templates(session)
        init_today_stat(session)

    logger.info("数据库初始化完成！")


def init_settings(session):
    default_settings = [
        ("focus_duration", "1500"),
        ("short_break_duration", "300"),
        ("long_break_duration", "900"),
        ("long_break_interval", "4"),
        ("daily_goal", "8"),
        ("theme", "light"),
        ("sound_enabled", "true"),
        ("notification_enabled", "true"),
        ("exam_date", ""),
    ]

    for key, value in default_settings:
        existing = session.query(Setting).filter_by(key=key).first()
        if not existing:
            setting = Setting(key=key, value=value)
            session.add(setting)
            logger.info(f"初始化设置: {key} = {value}")


def init_achievements(session):
    default_achievements = [
        {
            "name": "初学者",
            "description": "完成第一个番茄",
            "icon": "🎯",
            "condition": "total_pomodoros >= 1",
        },
        {
            "name": "坚持不懈",
            "description": "连续打卡 7 天",
            "icon": "🔥",
            "condition": "consecutive_days >= 7",
        },
        {
            "name": "学习达人",
            "description": "累计完成 100 个番茄",
            "icon": "⭐",
            "condition": "total_pomodoros >= 100",
        },
        {
            "name": "科目精通",
            "description": "单个科目完成 50 个番茄",
            "icon": "📚",
            "condition": "single_subject_pomodoros >= 50",
        },
        {
            "name": "月度之星",
            "description": "单月完成 200 个番茄",
            "icon": "🌟",
            "condition": "monthly_pomodoros >= 200",
        },
        {
            "name": "百日征程",
            "description": "连续打卡 100 天",
            "icon": "🏆",
            "condition": "consecutive_days >= 100",
        },
        {
            "name": "考研勇士",
            "description": "距离考研 30 天内仍坚持学习",
            "icon": "💪",
            "condition": "exam_days_left <= 30 AND total_pomodoros >= 1",
        },
        {
            "name": "全能学霸",
            "description": "所有科目均完成至少 10 个番茄",
            "icon": "🎓",
            "condition": "all_subjects_pomodoros >= 10",
        },
    ]

    for data in default_achievements:
        existing = session.query(Achievement).filter_by(name=data["name"]).first()
        if not existing:
            achievement = Achievement(**data)
            session.add(achievement)
            logger.info(f"初始化成就: {data['name']}")


def init_task_templates(session):
    default_templates = [
        {
            "name": "数学一章复习",
            "subject": "数学",
            "estimated_pomodoros": 4,
            "description": "复习一章数学教材，完成课后习题",
            "is_default": True,
        },
        {
            "name": "英语阅读一篇",
            "subject": "英语",
            "estimated_pomodoros": 2,
            "description": "完成一篇英语阅读理解并分析错题",
            "is_default": True,
        },
        {
            "name": "政治一章背诵",
            "subject": "政治",
            "estimated_pomodoros": 3,
            "description": "背诵一章政治知识点",
            "is_default": True,
        },
        {
            "name": "专业课笔记整理",
            "subject": "专业课",
            "estimated_pomodoros": 3,
            "description": "整理专业课笔记，梳理知识框架",
            "is_default": True,
        },
        {
            "name": "错题回顾",
            "subject": "其他",
            "estimated_pomodoros": 2,
            "description": "回顾近期错题，总结解题方法",
            "is_default": True,
        },
    ]

    for data in default_templates:
        existing = session.query(TaskTemplate).filter_by(name=data["name"]).first()
        if not existing:
            template = TaskTemplate(**data)
            session.add(template)
            logger.info(f"初始化任务模板: {data['name']}")


def init_today_stat(session):
    today = datetime.now().date()
    existing = session.query(DailyStat).filter_by(date=today).first()
    if not existing:
        stat = DailyStat(date=today)
        session.add(stat)
        logger.info(f"初始化今日统计: {today}")


def test_connection():
    try:
        db_manager = get_db_manager()
        with db_manager.session() as session:
            session.execute("SELECT 1")
        logger.info("数据库连接测试成功！")
        return True
    except Exception as e:
        logger.error(f"数据库连接测试失败: {e}")
        return False
