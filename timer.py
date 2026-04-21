from enum import Enum
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, List, Dict
from database import get_db_manager
from models import PomodoroSession, Setting, DailyStat
from utils.logger import get_logger

if TYPE_CHECKING:
    from statistics import StatisticsManager

logger = get_logger(__name__)


class TimerState(Enum):
    IDLE = "idle"
    FOCUS = "focus"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"


class PomodoroTimer(QObject):
    timer_updated = pyqtSignal(int, int)
    state_changed = pyqtSignal(TimerState)
    pomodoro_completed = pyqtSignal(int)
    break_started = pyqtSignal(TimerState)
    session_saved = pyqtSignal(int)
    progress_updated = pyqtSignal(float)
    is_running_changed = pyqtSignal(bool)
    achievement_unlocked = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.state = TimerState.IDLE
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.focus_duration = 1500
        self.short_break_duration = 300
        self.long_break_duration = 900
        self.long_break_interval = 4
        self.completed_pomodoros = 0
        self.current_task_id = None
        self.start_time = None
        self.session_start_time = None

        self.timer = QTimer()
        self.timer.timeout.connect(self._on_tick)
        self._load_settings()

    def _load_settings(self):
        try:
            db_manager = get_db_manager()
            with db_manager.session() as session:
                settings = session.query(Setting).all()
                settings_dict = {s.key: s.value for s in settings}
                self.focus_duration = int(settings_dict.get("focus_duration", 1500))
                self.short_break_duration = int(settings_dict.get("short_break_duration", 300))
                self.long_break_duration = int(settings_dict.get("long_break_duration", 900))
                self.long_break_interval = int(settings_dict.get("long_break_interval", 4))
        except (ValueError, TypeError, KeyError) as e:
            logger.warning(f"加载设置失败，使用默认值: {e}")

    def start(self):
        if self.state == TimerState.IDLE:
            self.state = TimerState.FOCUS
            self.remaining_seconds = self.focus_duration
            self.total_seconds = self.focus_duration
            self.session_start_time = datetime.now()
            self.start_time = datetime.now()

        self.timer.start(1000)
        self.state_changed.emit(self.state)
        self.is_running_changed.emit(True)
        self._emit_timer_update()
        logger.info(f"计时器开始: {self.state.value}")

    def pause(self):
        if self.timer.isActive():
            self.timer.stop()
            self.is_running_changed.emit(False)
            logger.info(f"计时器暂停: {self.state.value}, 剩余 {self.remaining_seconds}秒")

    def reset(self):
        self.timer.stop()
        self.state = TimerState.IDLE
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.start_time = None
        self.session_start_time = None
        self.is_running_changed.emit(False)
        self.state_changed.emit(self.state)
        self._emit_timer_update()
        logger.info("计时器重置")

    def skip(self):
        if self.state in [TimerState.FOCUS, TimerState.SHORT_BREAK, TimerState.LONG_BREAK]:
            self._transition_to_next_state()

    def stop(self):
        if self.state == TimerState.FOCUS and self.start_time:
            self._save_session(completed=False)

        self.timer.stop()
        self.state = TimerState.IDLE
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.start_time = None
        self.session_start_time = None
        self.is_running_changed.emit(False)
        self.state_changed.emit(self.state)
        self._emit_timer_update()
        logger.info("计时器停止")

    def _on_tick(self):
        self.remaining_seconds -= 1
        self._emit_timer_update()

        if self.remaining_seconds <= 0:
            self._on_state_completed()

    def _on_state_completed(self):
        self.timer.stop()
        self.is_running_changed.emit(False)

        if self.state == TimerState.FOCUS:
            self.completed_pomodoros += 1
            self._save_session(completed=True)
            self.pomodoro_completed.emit(self.completed_pomodoros)
            # 检查成就解锁
            try:
                from statistics import StatisticsManager
                stats_manager = StatisticsManager()
                unlocked = stats_manager.check_and_unlock_achievements()
                if unlocked:
                    self.achievement_unlocked.emit(unlocked)
            except (ImportError, ValueError, TypeError) as e:
                logger.error(f"检查成就解锁失败: {e}")
            self._transition_to_next_state()
        else:
            self._transition_to_next_state()

    def _transition_to_next_state(self):
        if self.state == TimerState.FOCUS:
            if self.completed_pomodoros > 0 and (self.completed_pomodoros % self.long_break_interval) == 0:
                self._start_break(TimerState.LONG_BREAK)
            else:
                self._start_break(TimerState.SHORT_BREAK)
        else:
            self._start_focus()

    def _start_focus(self):
        self.state = TimerState.FOCUS
        self.remaining_seconds = self.focus_duration
        self.total_seconds = self.focus_duration
        self.session_start_time = datetime.now()
        self.start_time = datetime.now()
        self.timer.start(1000)
        self.state_changed.emit(self.state)
        self._emit_timer_update()
        logger.info(f"开始专注")

    def _start_break(self, break_type: TimerState):
        if break_type == TimerState.LONG_BREAK:
            self.remaining_seconds = self.long_break_duration
            self.total_seconds = self.long_break_duration
        else:
            self.remaining_seconds = self.short_break_duration
            self.total_seconds = self.short_break_duration

        self.state = break_type
        self.start_time = None
        self.timer.start(1000)
        self.state_changed.emit(self.state)
        self.break_started.emit(break_type)
        self._emit_timer_update()
        logger.info(f"开始休息: {break_type.value}")

    def _save_session(self, completed: bool):
        if not self.session_start_time:
            return

        try:
            end_time = datetime.now()
            duration = int((end_time - self.session_start_time).total_seconds())

            db_manager = get_db_manager()
            with db_manager.session() as session:
                # 检查task_id是否存在
                valid_task_id = self.current_task_id
                if valid_task_id:
                    from models import Task
                    task_exists = session.query(Task).filter_by(id=valid_task_id).first()
                    if not task_exists:
                        valid_task_id = None
                        logger.warning(f"任务ID {self.current_task_id} 不存在，将task_id设置为None")

                session_record = PomodoroSession(
                    task_id=valid_task_id,
                    start_time=self.session_start_time,
                    end_time=end_time,
                    duration=duration,
                    completed=completed,
                )
                session.add(session_record)
                session.flush()

                if completed and valid_task_id:
                    from models import Task
                    task = session.query(Task).filter_by(id=valid_task_id).first()
                    if task:
                        task.actual_pomodoros += 1

                self._update_daily_stat(session, completed)

                # 获取会话ID并在会话关闭前使用
                session_id = session_record.id
                # 发出信号，只传递会话ID
                self.session_saved.emit(session_id)
                logger.info(f"番茄会话已保存: {session_id}")
                # session.commit() 由上下文管理器自动处理
        except (ValueError, TypeError) as e:
            logger.error(f"保存番茄会话失败: {e}")

    def _update_daily_stat(self, session, completed: bool):
        today = datetime.now().date()
        stat = session.query(DailyStat).filter_by(date=today).first()
        if not stat:
            stat = DailyStat(date=today)
            session.add(stat)

        if completed:
            stat.total_pomodoros += 1
            if self.start_time and self.session_start_time:
                duration = int((datetime.now() - self.session_start_time).total_seconds())
                stat.total_focus_time += duration

            goal_setting = session.query(Setting).filter_by(key="daily_goal").first()
            daily_goal = int(goal_setting.value) if goal_setting else 8
            if stat.total_pomodoros >= daily_goal and not stat.goal_achieved:
                stat.goal_achieved = True

    def set_current_task(self, task_id: int):
        self.current_task_id = task_id
        logger.info(f"设置当前任务: {task_id}")

    def get_state(self) -> TimerState:
        return self.state

    def is_running(self) -> bool:
        return self.timer.isActive()

    def get_remaining_time(self) -> tuple:
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        return minutes, seconds

    def get_progress(self) -> float:
        if self.total_seconds <= 0:
            return 0.0
        return (self.total_seconds - self.remaining_seconds) / self.total_seconds

    def _emit_timer_update(self):
        minutes, seconds = self.get_remaining_time()
        self.timer_updated.emit(minutes, seconds)
        self.progress_updated.emit(self.get_progress())

    def update_settings(self):
        self._load_settings()
