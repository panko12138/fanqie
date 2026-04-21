import atexit
import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


class DatabaseManager:
    _instance = None
    _engine = None
    _SessionFactory = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self._init_engine()
            self._init_session_factory()
            atexit.register(self.dispose)

    def _init_engine(self):
        config = Config()
        db_url = config.get_database_url()
        host = config.get('DB_HOST', 'localhost')
        logger.info(f"初始化数据库连接: {host}@***")

        self._engine = create_engine(
            db_url,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=15,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False,
        )

    def _init_session_factory(self):
        self._SessionFactory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            )
        )

    @contextmanager
    def session(self):
        session = self._SessionFactory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"数据库操作异常: {e}")
            raise
        finally:
            session.close()

    def get_engine(self):
        return self._engine

    def dispose(self):
        if self._engine:
            self._engine.dispose()
            logger.info("数据库连接已关闭")


def get_db_manager():
    return DatabaseManager()
