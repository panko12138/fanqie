# 考研番茄钟 UI 全面重构计划

## 项目概述

对现有 PyQt5 考研番茄钟桌面应用进行全面 UI 重构，以实现简洁大方、现代专业的视觉设计风格。重构遵循"少即是多"的设计哲学，在保持功能完整性的前提下，显著提升视觉品质与用户体验。

---

## 一、当前问题诊断

### 1.1 视觉层面
- 色彩方案偏冷硬，缺乏温度感，与"考研陪伴"的产品调性不符
- 卡片边框过于明显，视觉噪音较多
- 阴影效果生硬，缺乏层次感
- 按钮样式单一，缺少层次区分
- 字体层级不清晰，信息密度不均

### 1.2 交互层面
- 页面切换生硬，无过渡动画
- 按钮悬停反馈微弱
- 导航栏选中状态不够突出
- 表单控件 focus 状态不够明显
- 缺少空状态、加载状态等边界场景处理

### 1.3 架构层面
- 样式代码分散，硬编码值过多
- 组件复用度低，同类元素样式不统一
- 缺少集中式的设计 token 管理
- 间距、圆角、阴影缺乏系统化定义

---

## 二、设计方向与原则

### 2.1 设计理念
- **温暖专注**：以暖色调传递陪伴感，帮助用户进入专注状态
- **简洁克制**：减少不必要的装饰，让每个元素都有存在的意义
- **清晰层级**：通过字号、字重、色彩建立明确的信息层级
- **细腻反馈**：微妙的动画和状态变化，让交互更有质感

### 2.2 设计原则
1. **减少视觉噪音**：弱化边框，用留白和阴影区分层级
2. **优化信息层级**：标题-正文-辅助文字三级清晰区分
3. **简约色彩方案**：主色+2个辅助色+中性色，避免色彩泛滥
4. **足够留白空间**：内容区域边距 32px，卡片内边距 24px
5. **提升一致性**：所有组件遵循统一的设计 token

---

## 三、设计系统规范

### 3.1 色彩系统

#### 主色
| Token | 色值 | 用途 |
|-------|------|------|
| primary | `#E85D04` | 主按钮、选中态、强调 |
| primary-hover | `#D14903` | 主按钮悬停 |
| primary-pressed | `#B83D02` | 主按钮按下 |

#### 状态色
| Token | 色值 | 用途 |
|-------|------|------|
| focus | `#E85D04` | 专注状态 |
| short-break | `#2D6A4F` | 短休息状态 |
| long-break | `#4361EE` | 长休息状态 |
| danger | `#DC2626` | 删除、危险操作 |
| success | `#059669` | 成功、完成 |
| info | `#0891B2` | 信息提示 |

#### 浅色主题中性色
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

#### 深色主题中性色
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

### 3.2 字体排版

#### 字体栈
```
"SF Pro Display", "Segoe UI", "Microsoft YaHei", "PingFang SC", "Hiragino Sans GB", sans-serif
```

#### 字号层级
| 层级 | 字号 | 字重 | 行高 | 用途 |
|------|------|------|------|------|
| Display | 48px | Bold | 1.1 | 计时器时间显示 |
| H1 | 28px | Bold | 1.2 | 页面标题 |
| H2 | 20px | SemiBold | 1.3 | 卡片标题、区域标题 |
| H3 | 16px | SemiBold | 1.4 | 小标题、标签 |
| Body | 14px | Regular | 1.5 | 正文内容 |
| Caption | 12px | Regular | 1.4 | 辅助说明、时间戳 |
| Overline | 11px | Medium | 1.2 | 标签、徽章文字 |

### 3.3 间距系统

基础单位 4px，token 如下：

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

### 3.4 圆角系统

| Token | 值 | 用途 |
|-------|-----|------|
| radius-sm | 8px | 小按钮、输入框、标签 |
| radius-md | 12px | 标准按钮、下拉框 |
| radius-lg | 16px | 卡片、对话框 |
| radius-xl | 20px | 大容器、模态框 |
| radius-full | 9999px | 胶囊按钮、徽章 |

### 3.5 阴影系统

#### 浅色主题
| Token | 值 | 用途 |
|-------|-----|------|
| shadow-sm | `0 1px 3px rgba(0,0,0,0.06)` | 卡片默认 |
| shadow-md | `0 4px 12px rgba(0,0,0,0.08)` | 卡片悬停、下拉菜单 |
| shadow-lg | `0 8px 24px rgba(0,0,0,0.10)` | 对话框、浮层 |

#### 深色主题
深色主题以边框区分层级，阴影使用极少：
| Token | 值 | 用途 |
|-------|-----|------|
| shadow-sm | `0 0 0 1px rgba(255,255,255,0.05)` | 卡片边框替代 |

### 3.6 动画规范

| 场景 | 时长 | 缓动函数 | 说明 |
|------|------|----------|------|
| 按钮悬停 | 150ms | ease-out | 背景色、边框色过渡 |
| 卡片悬停 | 200ms | ease-out | 阴影加深、微上移(translateY -2px) |
| 页面切换 | 250ms | ease-in-out | 淡入淡出 |
| 导航指示器 | 200ms | ease-out | 滑动过渡 |
| 进度条更新 | 300ms | ease-out | 平滑过渡 |
| 数字变化 | 150ms | ease-out | 缩放 1.0 -> 1.05 -> 1.0 |
| Focus Ring | 100ms | ease | 边框色过渡 |

---

## 四、组件库规划

### 4.1 按钮组件 (buttons.py)

| 组件 | 说明 | 变体 |
|------|------|------|
| StyledButton | 基础按钮 | default, outline |
| PrimaryButton | 主按钮 | 继承 StyledButton，primary 变体 |
| DangerButton | 危险按钮 | 继承 StyledButton，danger 变体 |
| SuccessButton | 成功按钮 | 继承 StyledButton，success 变体 |
| GhostButton | 幽灵按钮 | 透明背景，悬停时显示背景 |
| IconButton | 图标按钮 | 方形，用于导航栏 |
| IconOnlyButton | 纯图标按钮 | 无文字，用于工具栏操作 |

**改进点**：
- 增加 focus-ring（2px 外边框，主色 30% 透明度）
- 增加 disabled 状态样式
- 统一最小高度 40px（标准）/ 36px（紧凑）
- 增加图标+文字组合支持

### 4.2 卡片组件 (cards.py)

| 组件 | 说明 |
|------|------|
| StyledCard | 基础卡片 |
| HoverCard | 带悬停动效的卡片 |
| StatCard | 统计卡片（专用于 stats_panel） |

**改进点**：
- 圆角统一为 16px
- 浅色模式使用弥散阴影替代边框
- 深色模式使用极细边框（1px）+ 无阴影
- 悬停时阴影加深 + 微上移 2px
- 可选的头部/底部区域

### 4.3 输入组件 (inputs.py)

| 组件 | 说明 |
|------|------|
| StyledLineEdit | 单行输入框 |
| StyledTextEdit | 多行文本框 |
| StyledComboBox | 下拉选择框 |
| StyledSpinBox | 数字选择框 |

**改进点**：
- 统一高度 44px
- Focus 状态：2px 主色边框 + 外发光（box-shadow: 0 0 0 3px primary-20%）
- 圆角 12px
- 占位符颜色使用 text-tertiary
- 增加错误状态样式（红色边框）

### 4.4 进度组件 (progress.py)

| 组件 | 说明 |
|------|------|
| CircularProgressBar | 圆形进度条 |
| PomodoroIndicator | 番茄完成指示器 |
| LinearProgressBar | 线性进度条（新增） |

**改进点**：
- 圆形进度条：线宽 14px，圆角端点，增加轨道发光效果
- 番茄指示器：已完成用实心圆点，未完成用空心圆点（边框 2px）
- 增加进度更新动画

### 4.5 新增组件

| 组件 | 文件 | 说明 |
|------|------|------|
| FadeAnimation | animations.py | 淡入淡出动画工具 |
| SlideAnimation | animations.py | 滑动动画工具 |
| ScaleAnimation | animations.py | 缩放动画工具 |
| Badge | badges.py | 徽章标签（数字/文字） |
| Divider | dividers.py | 水平/垂直分隔线 |
| EmptyState | emptystate.py | 空状态占位（图标+文字+可选操作） |
| FocusRingMixin | mixins.py | Focus 环效果混入类 |

---

## 五、页面重构方案

### 5.1 主窗口 (main_window.py)

**导航栏改进**：
- 宽度从 80px 增加到 88px
- 增加左侧 3px 选中指示器（主色，圆角）
- 图标下方增加文字标签（Timer / Tasks / Stats）
- 未选中状态：text-secondary 颜色
- 选中状态：text-primary 颜色 + 指示器
- 设置按钮移至底部，与其他导航项区分
- 导航栏背景：surface 色，与内容区 background 区分

**顶部栏改进**：
- 高度保持 64px
- 考研倒计时：使用 H2 字号，增加火焰/日历 emoji，更突出
- 今日统计：改为图标 + 数字形式，更紧凑
- 增加底部 1px 边框（border 色）

**内容区域改进**：
- 边距从 20px 增加到 32px
- 添加页面切换淡入淡出动画（QPropertyAnimation + QGraphicsOpacityEffect）

### 5.2 计时器页面 (timer_widget.py)

**布局重构**：
- 整体垂直居中，增加上下留白
- 状态标签：H2 字号，增加字间距（letter-spacing: 2px），使用状态对应颜色
- 圆形进度条：增大到 260px，线宽 14px，增加微妙的发光效果（glow）
- 时间显示：Display 字号（48px），等宽字体，字间距 2px
- 当前任务：增加任务图标，使用 text-secondary 颜色
- 番茄指示器：4 个圆点，已完成实心（主色），未完成空心（border 色）
- 按钮组：
  - 开始/暂停：PrimaryButton，大尺寸（宽 120px）
  - 重置、跳过：GhostButton
  - 停止：DangerButton，outline 变体

**动画**：
- 状态切换时，进度条颜色平滑过渡
- 时间数字变化时，轻微缩放脉冲
- 开始/暂停按钮文字切换时淡入淡出

### 5.3 任务面板 (task_panel.py)

**工具栏改进**：
- 使用更紧凑的布局
- "+ 新建任务"按钮：PrimaryButton，增加加号图标
- 筛选器：StyledComboBox，宽度自适应
- 增加搜索框（StyledLineEdit，带搜索图标）

**任务卡片改进**：
- 减少边框使用（浅色模式用阴影，深色模式用细边框）
- 信息层级：任务名（H3）> 科目/预估（Caption）> 备注（Caption，text-tertiary）
- 操作按钮改为图标按钮组（选择、编辑、完成、删除）
- 增加悬停效果（阴影加深 + 微上移）
- 已完成任务：降低透明度或增加删除线

**任务编辑对话框改进**：
- 增大圆角到 20px
- 表单标签使用 Caption 样式，右对齐
- 输入框统一高度 44px
- 底部按钮组：取消（GhostButton）+ 确定（PrimaryButton）

**空状态**：
- 当没有任务时显示 EmptyState 组件
- 图标：📋 或自定义图标
- 文字："还没有任务，创建一个开始专注吧"
- 操作："创建任务"按钮

### 5.4 统计面板 (stats_panel.py)

**统计卡片改进**：
- 统一高度 140px
- 标题：Overline 样式，text-secondary，全大写
- 数值：H1 样式（28px），text-primary
- 副标题：Caption 样式，text-tertiary
- 卡片布局：标题在上，数值居中，副标题在下

**响应式网格**：
- 窗口宽度 < 800px：2 列
- 窗口宽度 >= 800px：4 列
- 通过 resizeEvent 动态调整 QGridLayout

**成就区域改进**：
- 改为徽章式展示（Badge 组件）
- 已解锁：主色背景 + 白色文字
- 未解锁：border 色背景 + text-tertiary 文字
- 横向滚动或换行排列

### 5.5 设置对话框 (settings_dialog.py)

**标签页改进**：
- 标签文字：Body 字号，Medium 字重
- 选中态：底部 2px 主色边框 + text-primary
- 未选中：text-secondary，无边框
- 悬停：text-primary，背景微变

**表单改进**：
- 标签右对齐，宽度统一
- 输入框左对齐，宽度一致
- 增加表单组间距（每组之间 24px）
- 复选框：增大到 20x20，圆角 6px

**底部按钮栏**：
- 增加顶部 1px 分隔线
- 取消（GhostButton）+ 确定（PrimaryButton）
- 按钮最小宽度 80px

---

## 六、响应式布局策略

由于 PyQt5 非 Web 框架，响应式通过以下机制实现：

1. **弹性布局**：大量使用 QSizePolicy.Expanding / Preferred
2. **Stretch 因子**：QHBoxLayout/QVBoxLayout 设置合理的 stretch
3. **尺寸约束**：setMinimumSize / setMaximumSize 防止过度压缩
4. **滚动区域**：QScrollArea 处理溢出内容
5. **动态重排**：重写 resizeEvent，根据窗口宽度调整网格列数

**断点定义**：
| 断点 | 宽度 | 布局调整 |
|------|------|----------|
| sm | < 800px | 统计卡片 2 列，任务卡片全宽 |
| md | 800px - 1100px | 统计卡片 4 列，正常布局 |
| lg | > 1100px | 统计卡片 4 列，更大留白 |

---

## 七、实施步骤（按优先级排序）

### 阶段一：基础设计系统（步骤 1-2）

**步骤 1：重构主题系统 (themes.py)**
- 更新 Colors 类：新的色彩 token（primary、surface、text-primary 等）
- 新增 Typography 类：字号、字重、行高定义
- 新增 Shadows 类：阴影层级定义
- 新增 Spacing 类：间距 token
- 重写 get_stylesheet()：生成完整的全局 QSS 样式
- 保持 ThemeType 枚举和 ThemeManager 单例模式不变
- 确保主题切换信号正常工作

**步骤 2：重构基础组件库 (ui/components/)**
- 重构 buttons.py：改进现有按钮，新增 GhostButton、IconOnlyButton，增加 focus-ring 和 disabled 状态
- 重构 cards.py：改进 StyledCard，增加 HoverCard，统一圆角和阴影
- 重构 inputs.py：改进 StyledLineEdit、StyledComboBox，新增 StyledTextEdit、StyledSpinBox，增加 focus 发光效果
- 重构 progress.py：改进 CircularProgressBar（发光效果、圆角端点），改进 PomodoroIndicator（空心/实心样式）
- 新增 animations.py：FadeAnimation、SlideAnimation、ScaleAnimation 工具类
- 新增 badges.py：Badge 组件
- 新增 dividers.py：Divider 组件
- 新增 emptystate.py：EmptyState 组件
- 更新 __init__.py 导出列表

### 阶段二：核心页面重构（步骤 3-5）

**步骤 3：重构主窗口 (ui/main_window.py)**
- 导航栏：加宽到 88px，增加文字标签，增加左侧选中指示器
- 顶部栏：改进考研倒计时和今日统计展示
- 内容区域：边距增加到 32px
- 添加页面切换淡入淡出动画

**步骤 4：重构计时器页面 (ui/timer_widget.py)**
- 重新设计布局，增加留白
- 改进圆形进度条样式和大小
- 时间显示使用 Display 字号
- 重新排列按钮组
- 添加状态切换动画

**步骤 5：重构任务面板 (ui/task_panel.py)**
- 改进工具栏布局
- 重新设计任务卡片（减少边框、图标按钮组、悬停效果）
- 改进任务编辑对话框
- 添加空状态组件

### 阶段三：辅助页面重构（步骤 6-7）

**步骤 6：重构统计面板 (ui/stats_panel.py)**
- 重新设计统计卡片（统一高度、改进数值展示）
- 实现响应式网格（resizeEvent 动态调整列数）
- 改进成就展示为徽章式

**步骤 7：重构设置对话框 (ui/settings_dialog.py)**
- 改进标签页样式
- 优化表单布局
- 统一输入框和按钮样式
- 改进备份列表样式

### 阶段四：完善与文档（步骤 8-9）

**步骤 8：全局测试与调优**
- 测试明暗主题切换
- 测试窗口大小调整（响应式布局）
- 测试所有交互状态（hover、focus、disabled）
- 测试动画性能
- 确保现有功能不受影响

**步骤 9：编写设计规范文档**
- 创建 docs/design_system.md
- 包含：设计原则、色彩系统、字体排版、间距系统、圆角与阴影、组件规范、布局规范、动画规范

---

## 八、文件变更清单

### 修改文件（8 个）
| 文件 | 变更类型 | 说明 |
|------|----------|------|
| themes.py | 大幅修改 | 更新色彩系统，新增设计 token |
| ui/main_window.py | 大幅修改 | 重构导航栏、顶部栏、页面切换动画 |
| ui/timer_widget.py | 大幅修改 | 重新设计计时器页面布局与样式 |
| ui/task_panel.py | 大幅修改 | 重构任务卡片、工具栏、对话框 |
| ui/stats_panel.py | 大幅修改 | 重构统计卡片、响应式网格、成就展示 |
| ui/settings_dialog.py | 中等修改 | 改进标签页、表单、按钮样式 |
| ui/components/buttons.py | 中等修改 | 新增组件，改进现有按钮 |
| ui/components/cards.py | 中等修改 | 改进卡片样式，新增 HoverCard |
| ui/components/inputs.py | 中等修改 | 改进输入框，新增组件 |
| ui/components/progress.py | 中等修改 | 改进进度条视觉效果 |
| ui/components/__init__.py | 小幅修改 | 更新导出列表 |

### 新增文件（5 个）
| 文件 | 说明 |
|------|------|
| ui/components/animations.py | 动画工具类 |
| ui/components/badges.py | 徽章组件 |
| ui/components/dividers.py | 分隔线组件 |
| ui/components/emptystate.py | 空状态组件 |
| docs/design_system.md | 设计规范文档 |

---

## 九、验收标准

1. **视觉一致性**：所有界面元素遵循统一的设计系统，无明暗主题下的样式错乱
2. **主题切换**：明暗主题切换流畅，所有组件正确响应主题变化
3. **交互反馈**：所有可交互元素（按钮、输入框、卡片）有适当的 hover/focus/active 状态
4. **动画效果**：页面切换、状态变化、数字更新均有平滑动画，不卡顿
5. **响应式布局**：窗口大小调整时，统计卡片网格自动调整列数，布局不崩坏
6. **功能完整**：所有现有功能（计时、任务管理、统计、设置、备份）保持正常工作
7. **代码质量**：组件复用度高，样式硬编码减少 80% 以上，设计 token 集中管理
8. **设计文档**：design_system.md 文档完整，可作为后续开发的参考标准

---

## 十、风险与应对

| 风险 | 影响 | 应对措施 |
|------|------|----------|
| PyQt5 QSS 限制较多 | 部分设计效果无法实现 | 使用自定义 PaintEvent 绘制复杂效果，或适当简化设计 |
| 动画影响计时器精度 | 计时功能异常 | 动画使用独立 QPropertyAnimation，不影响 QTimer 计时逻辑 |
| 主题切换时界面闪烁 | 用户体验差 | 批量更新样式，减少重绘次数 |
| 窗口大小频繁调整导致性能问题 | 界面卡顿 | 使用 QTimer 防抖处理 resizeEvent |
| 重构范围大引入 bug | 功能异常 | 分阶段实施，每阶段完成后测试，保持版本控制 |

---

## 十一、后续优化建议

1. **自定义窗口边框**：移除系统默认标题栏，实现完全自定义的窗口外观（圆角、阴影）
2. **更多动画**：计时器完成时的庆祝动画、成就解锁动画
3. **声音主题**：不同状态下播放不同的白噪音/提示音
4. **数据可视化**：统计页面增加折线图、柱状图展示学习趋势
5. **快捷键系统**：全局快捷键（开始/暂停、跳过）
6. **插件系统**：允许用户自定义主题色
