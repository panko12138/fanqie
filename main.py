#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

from PyQt5.QtWidgets import QApplication, QMessageBox

from database import init_database, test_connection
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("考研番茄钟")
    app.setOrganizationName("PomodoroApp")

    logger.info("=" * 50)
    logger.info("考研番茄钟启动中...")
    logger.info("=" * 50)

    try:
        logger.info("正在初始化数据库...")
        init_database()
        logger.info("数据库初始化成功")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        QMessageBox.critical(
            None,
            "数据库错误",
            f"数据库初始化失败: {e}\n\n请检查：\n1. MySQL服务是否启动\n2. .env文件中的数据库配置是否正确\n3. MySQL用户是否有创建数据库的权限"
        )
        return 1

    try:
        from ui.main_window import MainWindow
        window = MainWindow()
        window.show()
        logger.info("应用启动成功")
        return app.exec_()
    except Exception as e:
        logger.error(f"应用启动失败: {e}", exc_info=True)
        QMessageBox.critical(
            None,
            "启动错误",
            f"应用启动失败: {e}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
