# 考研番茄钟应用 - Product Requirement Document

## Overview
- **Summary**: 一款专为考研学子设计的桌面专注力管理工具，基于番茄工作法，结合考研复习场景，提供时间管理、任务管理、数据可视化、习惯养成等功能。
- **Purpose**: 解决考研学生学习分心、时间管理困难、进度模糊、缺乏持续动力等问题。
- **Target Users**: 18-30岁备考研究生的学生，在图书馆、自习室、家中使用，无需编程基础。

## Goals
- 实现经典番茄工作法循环机制（专注-短休息-长休息）
- 提供完整的任务管理功能，支持任务关联番茄
- 实现数据统计与可视化展示
- 建立打卡激励机制和成就系统
- 支持考研倒计时、白噪音、系统托盘等辅助功能
- 提供完整的设置功能（外观、通知、数据管理、数据库配置）
- 确保跨平台兼容性（Windows/macOS/Linux）
- 所有数据本地MySQL存储，不上传云端

## Non-Goals (Out of Scope)
- 云端同步功能
- 社交功能（好友、排行榜等）
- 移动端App
- 在线课程集成
- 实时协作功能

## Background & Context
- 技术栈已确定：Python 3.10+ / PyQt5 / MySQL 8.0+
- 用户已有详细的PRD文档作为需求依据
- 当前项目目录几乎为空，需要从零开始
- 用户使用Windows系统，PowerShell终端
- 数据库使用MySQL

## Functional Requirements
- **FR-1**: 核心计时器功能（番茄钟循环、操作控制、自定义时长、专注模式）
- **FR-2**: 任务管理功能（创建、编辑、删除、完成任务，任务关联番茄）
- **FR-3**: 统计分析功能（数据可视化、打卡机制、成就系统）
- **FR-4**: 提醒系统功能（音效、系统通知、弹窗提醒）
- **FR-5**: 考研倒计时功能
- **FR-6**: 系统托盘功能
- **FR-7**: 设置功能（外观、通知、数据管理、数据库配置）
- **FR-8**: 数据备份与恢复功能
- **FR-9**: 白噪音播放功能
- **FR-10**: 主题切换功能（浅色/深色/自动）

## Non-Functional Requirements
- **NFR-1**: 启动时间 ≤ 3 秒
- **NFR-2**: 内存占用 ≤ 80MB
- **NFR-3**: 计时精度误差 ≤ 1 秒/小时
- **NFR-4**: UI 流畅度 ≥ 30 FPS
- **NFR-5**: 支持 Windows 10+、macOS 11+、Linux (Ubuntu 20.04+ / Debian 11+)
- **NFR-6**: 数据库连接稳定，最小连接池5个，最大20个
- **NFR-7**: 符合 WCAG 2.1 可访问性标准

## Constraints
- **Technical**: 必须使用Python 3.10+、PyQt5、MySQL 8.0+
- **Business**: 所有数据本地存储，不上传云端
- **Dependencies**: PyQt5、SQLAlchemy、matplotlib、pygame、mysql-connector-python、python-dotenv、alembic、PyInstaller

## Assumptions
- 用户已安装Python 3.10+
- 用户已安装MySQL 8.0+并有权限创建数据库
- 用户使用Windows/macOS/Linux系统
- 用户有基本的电脑操作能力

## Acceptance Criteria

### AC-1: 番茄钟计时器正常运行
- **Given**: 应用已启动
- **When**: 用户点击开始按钮或按Space键
- **Then**: 计时器开始计时，显示圆形进度条和倒计时数字
- **Verification**: `programmatic`

### AC-2: 番茄钟循环正常切换
- **Given**: 计时器正在运行专注阶段
- **When**: 专注阶段结束
- **Then**: 自动切换到短休息阶段
- **Verification**: `programmatic`

### AC-3: 任务创建成功
- **Given**: 用户在任务管理页面
- **When**: 用户填写任务信息并点击创建
- **Then**: 任务成功保存到数据库并显示在列表中
- **Verification**: `programmatic`

### AC-4: 番茄完成后任务实际番茄数+1
- **Given**: 一个任务被选为当前任务
- **When**: 完成一个专注番茄
- **Then**: 该任务的实际番茄数自动加1
- **Verification**: `programmatic`

### AC-5: 统计数据正确显示
- **Given**: 用户已有学习记录
- **When**: 用户打开统计页面
- **Then**: 显示今日、本周、本月的学习数据和图表
- **Verification**: `programmatic`

### AC-6: 打卡机制正常工作
- **Given**: 用户当天完成至少1个番茄
- **When**: 完成番茄后
- **Then**: 当天标记为打卡成功，连续打卡天数更新
- **Verification**: `programmatic`

### AC-7: 数据库连接正常
- **Given**: 用户已正确配置MySQL连接信息
- **When**: 应用启动
- **Then**: 成功连接数据库并初始化表结构
- **Verification**: `programmatic`

### AC-8: 系统托盘功能正常
- **Given**: 应用正在运行
- **When**: 用户最小化窗口
- **Then**: 应用最小化到系统托盘，右键菜单可用
- **Verification**: `human-judgment`

### AC-9: 主题切换功能正常
- **Given**: 用户在设置页面
- **When**: 用户选择不同主题（浅色/深色/自动）
- **Then**: 界面主题立即切换
- **Verification**: `human-judgment`

### AC-10: 数据备份功能正常
- **Given**: 用户有数据
- **When**: 用户执行备份操作
- **Then**: 成功创建备份文件
- **Verification**: `programmatic`

## Open Questions
- [ ] 白噪音音频文件是否需要提供默认资源？
- [ ] 是否需要实现Alembic数据库迁移？（PRD提到了，但可先简化）
- [ ] 成就系统的解锁条件是否需要全部实现？
