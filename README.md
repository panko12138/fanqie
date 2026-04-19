# 考研番茄钟

专为考研学子设计的桌面专注力管理工具，基于番茄工作法。

## 功能特性

- 🕒 经典番茄工作法（25分钟专注+5分钟休息）
- 📋 任务管理，支持科目分类
- 📊 数据统计与可视化
- 📅 打卡激励机制与成就系统
- 🎨 浅色/深色主题切换
- 🔔 提示音与系统通知
- 📦 数据备份与恢复
- 🎯 考研倒计时
- 📌 系统托盘支持

## 技术栈

- Python 3.10+
- PyQt5 (GUI)
- MySQL 8.0+ (数据库)
- SQLAlchemy (ORM)

## 安装步骤

### 1. 安装依赖

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 配置数据库

复制 `.env.example` 为 `.env` 并配置数据库连接信息：

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=pomodoro_db
DB_CHARSET=utf8mb4

APP_NAME=考研番茄钟
APP_VERSION=1.0.0
LOG_LEVEL=INFO
```

确保MySQL服务已启动，并且用户有创建数据库的权限。

### 3. 运行应用

```bash
python main.py
```

首次运行时会自动创建数据库表并初始化默认设置。

## 使用说明

1. **专注计时**：在计时器页面点击"开始"按钮开始专注
2. **管理任务**：在任务页面添加、编辑和管理学习任务
3. **查看统计**：在统计页面查看学习数据和成就
4. **设置选项**：点击导航栏底部的设置按钮自定义应用

## 项目结构

```
pomodoro/
├── main.py                 # 程序入口
├── config.py               # 配置管理
├── timer.py                # 计时器核心逻辑
├── task_manager.py         # 任务管理逻辑
├── statistics.py           # 统计分析逻辑
├── backup.py               # 数据备份与恢复
├── notification.py         # 通知系统
├── white_noise.py          # 白噪音播放器
├── themes.py               # 主题管理
├── models/                 # 数据模型
├── database/               # 数据库相关
├── utils/                  # 工具函数
├── ui/                     # 用户界面
├── resources/              # 资源文件
├── tests/                  # 测试代码
├── docs/                   # 文档
└── requirements.txt        # 依赖列表
```

## 开发说明

### 运行测试

```bash
pytest tests/
```

### 代码规范

- 遵循 PEP 8 代码风格
- 使用 type hints
- 编写文档字符串

## 许可证

MIT License
