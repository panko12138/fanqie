# 考研番茄钟 - 设计系统规范文档

## 目录

1. [设计原则](#设计原则)
2. [色彩系统](#色彩系统)
3. [字体排版](#字体排版)
4. [间距系统](#间距系统)
5. [圆角与阴影](#圆角与阴影)
6. [组件规范](#组件规范)
7. [布局规范](#布局规范)
8. [动画规范](#动画规范)
9. [响应式断点](#响应式断点)

---

## 设计原则

### 温暖专注
以暖色调传递陪伴感，帮助用户进入专注状态。主色采用温暖的琥珀色，营造积极向上的学习氛围。

### 简洁克制
减少不必要的装饰，让每个元素都有存在的意义。遵循"少即是多"的设计哲学。

### 清晰层级
通过字号、字重、色彩建立明确的信息层级，让用户一眼就能获取关键信息。

### 细腻反馈
微妙的动画和状态变化，让交互更有质感，提升用户体验的愉悦度。

---

## 色彩系统

### 主色

| Token | 色值 | 用途 |
|-------|------|------|
| primary | `#E85D04` | 主按钮、选中态、强调 |
| primary-hover | `#D14903` | 主按钮悬停 |
| primary-pressed | `#B83D02` | 主按钮按下 |

### 状态色

| Token | 色值 | 用途 |
|-------|------|------|
| focus | `#E85D04` | 专注状态 |
| short-break | `#2D6A4F` | 短休息状态 |
| long-break | `#4361EE` | 长休息状态 |
| danger | `#DC2626` | 删除、危险操作 |
| success | `#059669` | 成功、完成 |
| info | `#0891B2` | 信息提示 |

### 浅色主题中性色

| Token | 色值 | 用途 |
|-------|------|------|
| background | `#FAFAF8` | 页面背景（暖白） |
| surface | `#FFFFFF` | 卡片背景 |
| surface-elevated | `#FFFBF7` | 悬浮卡片 |
| border | `#E8E5E0` | 边框、分割线 |
| text-primary | `#1A1A1A` | 主文字 |
| text-secondary | `#6B7280` | 次要文字 |
| text-tertiary | `#9CA3AF` | 辅助文字、占位符 |
| text-inverse | `#FFFFFF` | 深色背景上的文字 |

### 深色主题中性色

| Token | 色值 | 用途 |
|-------|------|------|
| background | `#121212` | 页面背景 |
| surface | `#1E1E1E` | 卡片背景 |
| surface-elevated | `#252525` | 悬浮卡片 |
| border | `#2D2D2D` | 边框、分割线 |
| text-primary | `#E8E8E8` | 主文字 |
| text-secondary | `#A1A1AA` | 次要文字 |
| text-tertiary | `#71717A` | 辅助文字 |
| text-inverse | `#1A1A1A` | 浅色背景上的文字 |

---

## 字体排版

### 字体栈

```
"SF Pro Display", "Segoe UI", "Microsoft YaHei", "PingFang SC", "Hiragino Sans GB", sans-serif
```

等宽字体（用于计时器）：
```
"SF Mono", "Consolas", "Microsoft YaHei", monospace
```

### 字号层级

| 层级 | 字号 | 字重 | 行高 | 用途 |
|------|------|------|------|------|
| Display | 48px | Bold | 1.1 | 计时器时间显示 |
| H1 | 28px | Bold | 1.2 | 页面标题 |
| H2 | 20px | SemiBold | 1.3 | 卡片标题、区域标题 |
| H3 | 16px | SemiBold | 1.4 | 小标题、标签 |
| Body | 14px | Regular | 1.5 | 正文内容 |
| Caption | 12px | Regular | 1.4 | 辅助说明、时间戳 |
| Overline | 11px | Medium | 1.2 | 标签、徽章文字 |

---

## 间距系统

基础单位 4px。

| Token | 值 | 用途 |
|-------|-----|------|
| space-1 | 4px | 极小间距 |
| space-2 | 8px | 紧凑间距 |
| space-3 | 12px | 小组件内间距 |
| space-4 | 16px | 标准组件间距 |
| space-5 | 20px | 中等间距 |
| space-6 | 24px | 卡片内边距 |
| space-8 | 32px | 页面边距 |
| space-10 | 40px | 大间距 |
| space-12 | 48px | 区域间距 |

---

## 圆角与阴影

### 圆角系统

| Token | 值 | 用途 |
|-------|-----|------|
| radius-sm | 8px | 小按钮、输入框、标签 |
| radius-md | 12px | 标准按钮、下拉框 |
| radius-lg | 16px | 卡片、对话框 |
| radius-xl | 20px | 大容器、模态框 |
| radius-full | 9999px | 胶囊按钮、徽章 |

### 阴影系统

#### 浅色主题

| Token | 值 | 用途 |
|-------|-----|------|
| shadow-sm | `0 1px 3px rgba(0,0,0,0.06)` | 卡片默认 |
| shadow-md | `0 4px 12px rgba(0,0,0,0.08)` | 卡片悬停、下拉菜单 |
| shadow-lg | `0 8px 24px rgba(0,0,0,0.10)` | 对话框、浮层 |

#### 深色主题

深色主题使用浅色投影效果增强层次感：

| Token | 值 | 用途 |
|-------|-----|------|
| shadow-light | `0 1px 3px rgba(255,255,255,0.06)` | 卡片默认 |
| shadow-medium | `0 4px 12px rgba(255,255,255,0.08)` | 卡片悬停、下拉菜单 |
| shadow-heavy | `0 8px 24px rgba(255,255,255,0.10)` | 对话框、浮层 |

---

## 组件规范

### 按钮

#### 基础按钮 (StyledButton)
- 最小高度：40px
- 圆角：12px (radius-md)
- 内边距：10px 20px
- 字号：14px，字重：600

#### 变体

| 变体 | 背景 | 文字 | 边框 |
|------|------|------|------|
| Default | surface | text-primary | 1px border |
| Primary | primary | white | none |
| Danger | danger | white | none |
| Success | success | white | none |
| Outline | transparent | text-primary | 2px border |
| Ghost | transparent | text-secondary | none |

#### 图标按钮 (IconButton)
- 尺寸：88x72px（带文字）/ 50x50px（纯图标）
- 圆角：12px
- 选中态：背景 surface，文字 primary 色

#### 纯图标按钮 (IconOnlyButton)
- 尺寸：32x32px（默认）
- 圆角：8px
- 悬停：背景 surface，文字 text-primary

### 卡片

#### 基础卡片 (StyledCard)
- 背景：surface
- 圆角：16px (radius-lg)
- 浅色模式：无边框，使用阴影
- 深色模式：1px border 色边框
- 内边距：24px

#### 统计卡片 (StatCard)
- 最小高度：140px
- 标题：Overline 样式，text-secondary，全大写，字间距 1px
- 数值：H1 样式（28px），text-primary
- 副标题：Caption 样式，text-tertiary

### 输入框

#### 文本输入 (StyledLineEdit / StyledTextEdit)
- 背景：surface
- 边框：2px border 色
- 圆角：12px
- 内边距：10px 14px
- 最小高度：44px
- Focus：2px primary 色边框
- 占位符：text-tertiary

#### 下拉选择 (StyledComboBox)
- 同输入框样式
- 下拉箭头：6px 三角形
- 下拉面板：同卡片样式

#### 数字选择 (StyledSpinBox)
- 同输入框样式
- 箭头：6px 三角形

### 进度条

#### 圆形进度条 (CircularProgressBar)
- 最小尺寸：260x260px
- 轨道线宽：14px
- 进度线宽：14px，圆角端点
- 发光效果：QGraphicsDropShadowEffect

#### 番茄指示器 (PomodoroIndicator)
- 圆点尺寸：14x14px
- 已完成：实心 primary 色
- 未完成：透明背景，2px border 色边框
- 间距：10px

### 徽章 (Badge)
- 圆角：9999px（胶囊形）
- 内边距：4px 10px
- 字号：11px，字重：500
- 变体：primary / success / danger / outline / default

### 分隔线 (Divider)
- 颜色：border
- 方向：水平或垂直

### 空状态 (EmptyState)
- 图标：48px，text-tertiary
- 标题：H3 样式，text-primary
- 副标题：Body 样式，text-secondary
- 可选操作按钮

---

## 布局规范

### 导航栏
- 宽度：88px
- 背景：surface
- 图标按钮：88x72px，带文字标签
- 选中指示器：左侧 3px 竖线，primary 色，圆角

### 顶部栏
- 高度：64px
- 背景：background
- 底部边框：1px border 色
- 左右边距：32px

### 内容区域
- 边距：32px
- 间距：24px

### 页面切换
- 动画：淡入淡出
- 时长：250ms

---

## 动画规范

| 场景 | 时长 | 缓动函数 | 说明 |
|------|------|----------|------|
| 按钮悬停 | 150ms | ease-out | 背景色、边框色过渡 |
| 卡片悬停 | 200ms | ease-out | 阴影加深、微上移 |
| 页面切换 | 250ms | ease-in-out | 淡入淡出 |
| 导航指示器 | 200ms | ease-out | 滑动过渡 |
| 进度条更新 | 300ms | ease-out | 平滑过渡 |
| 数字变化 | 150ms | ease-out | 缩放脉冲 |
| Focus Ring | 100ms | ease | 边框色过渡 |

---

## 响应式断点

| 断点 | 宽度 | 布局调整 |
|------|------|----------|
| sm | < 800px | 统计卡片 2 列，任务卡片全宽 |
| md | 800px - 1100px | 统计卡片 4 列，正常布局 |
| lg | > 1100px | 统计卡片 4 列，更大留白 |

### 实现方式

PyQt5 非 Web 框架，响应式通过以下机制实现：

1. **弹性布局**：使用 QSizePolicy.Expanding / Preferred
2. **Stretch 因子**：QHBoxLayout/QVBoxLayout 设置合理的 stretch
3. **尺寸约束**：setMinimumSize / setMaximumSize
4. **滚动区域**：QScrollArea 处理溢出内容
5. **动态重排**：重写 resizeEvent，根据窗口宽度调整网格列数

---

## 文件结构

```
ui/
├── components/
│   ├── __init__.py
│   ├── animations.py      # 动画工具类
│   ├── badges.py          # 徽章组件
│   ├── buttons.py         # 按钮组件
│   ├── cards.py           # 卡片组件
│   ├── dividers.py        # 分隔线组件
│   ├── emptystate.py      # 空状态组件
│   ├── inputs.py          # 输入组件
│   └── progress.py        # 进度组件
├── main_window.py         # 主窗口
├── timer_widget.py        # 计时器页面
├── task_panel.py          # 任务面板
├── stats_panel.py         # 统计面板
└── settings_dialog.py     # 设置对话框

themes.py                  # 主题系统
docs/
└── design_system.md       # 设计规范文档
```

---

## 使用示例

### 创建主题感知按钮

```python
from ui.components import PrimaryButton

btn = PrimaryButton("开始")
btn.setMinimumWidth(120)
```

### 创建卡片

```python
from ui.components import StyledCard

card = StyledCard()
card.layout.addWidget(QLabel("卡片内容"))
```

### 使用动画

```python
from ui.components import FadeAnimation

FadeAnimation.fade_in(widget, 250)
FadeAnimation.fade_out(widget, 150, callback)
```

### 获取设计 Token

```python
from themes import ThemeManager, Typography, Shadows, Radius, Spacing

theme = ThemeManager()
colors = theme.get_colors()

# 使用颜色
bg = colors["background"]
primary = colors["primary"]

# 使用字体样式
style = Typography.get_style("H2", colors["text_primary"])

# 使用阴影
shadow = Shadows.get_shadow("medium", theme.is_dark_theme())

# 使用圆角
radius = Radius.LG  # 16

# 使用间距
spacing = Spacing.SPACE_6  # 24
```

---

*文档版本：1.0*
*更新日期：2026-04-21*
