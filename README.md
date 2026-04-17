# XSideUI

<div align="center">

![XSideUI Logo](https://img.shields.io/badge/XSideUI-Qt%20UI%20Library-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge)
![PySide2](https://img.shields.io/badge/PySide2-5.15+-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**一款现代化的 Python Qt UI 组件库(PySide2 / PySide6)**

[快速开始](#快速开始) • [组件文档](#组件列表) • [主题系统](#主题系统) • [示例代码](#使用示例)

</div>

---

## ✨ 特性

### 🎯 框架兼容

- **零成本接入 PySide2/PySide6** – 深度适配 Qt 生态，一套代码无缝切换双版本，告别兼容性困扰
- **跨平台通用** – Windows、Linux、macOS 全平台支持，构建一致体验

### ⚡️ 性能体验

- **极致轻量** – 核心库零外部依赖，体积小巧，秒级加载不拖沓
- **智能渲染引擎** – 内置缓存优化机制，界面流畅丝滑，告别卡顿

### 🎨 视觉设计

- **现代美学体系** – 精雕细琢的视觉语言，从色彩到动效，尽显专业质感
- **全局视觉统一** – 颜色、字体、间距、圆角遵循 Qt 设计规范，界面浑然一体
- **智能主题引擎** – 明暗主题一键切换，支持动态配色，适配不同场景需求

### 🧩 组件生态

- **30+ 开箱组件** – 按钮、卡片、对话框、菜单等高频组件全覆盖
- **命名零门槛** – XPushButton、XComboBox 与 Qt 原生命名保持一致，零学习成本上手
- **图标引擎内置** – SVG 图标动态着色，明暗主题自适应，图标管理从未如此简单

### 🔧 定制能力

- **链式调用 API** – 灵活优雅的定制方式，一行代码完成样式配置
- **深度定制支持** – 从基础属性到复杂交互，满足各类定制需求

### 📖 开发者友好

- **中文优先** – 完整的中文文档 + 代码注释，扫清语言障碍
- **示例即用** – 配套丰富的示例工程，复制粘贴即可运行，快速验证效果

## ✨ 样式展示

![xsideui示例](./docs/images/xsideui.gif "xsideui示例")

## 📦 安装

```python
pip install xsideui
```

---

## 🚀 快速开始

### 基础示例

```python
from PySide2.QtWidgets import QApplication
from xsideui import XPushButton, XColor, XButtonVariant

app = QApplication([])

# 创建按钮
button = XPushButton("点击我", color=XColor.PRIMARY, variant=XButtonVariant.SOLID)
button.show()

app.exec_()
```

### 主题切换

```python
from xsideui import theme_manager

# 切换到暗色主题
theme_manager.set_theme("dark")

# 明暗切换
theme_manager.toggle_theme()

# 自定义主题色
theme_manager.set_primary_colors({
    "light": "#ab7ae0",
    "dark": "#51258f"
})
```

---

## 🎨 主题系统

XSideUI 提供强大的主题管理系统，支持：

- ✅ **明暗主题切换** - 一键切换亮色/暗色模式
- ✅ **自定义主题色** - 灵活配置主题颜色
- ✅ **主题预加载** - 快速切换，无延迟
- ✅ **智能缓存** - 优化性能，减少重复计算

### 主题颜色

| 颜色 | 说明 |
|------|------|
| `primary` | 主题色 |
| `secondary` | 次要色 |
| `success` | 成功色 |
| `warning` | 警告色 |
| `danger` | 危险色 |
| `tertiary` | 浅色 |

详细主题文档：[Theme.md](docs/Theme.md)

---

## 📚 组件列表

### 基础组件

| 组件 | 说明 | 文档 |
|------|------|------|
| [XPushButton](docs/XPushButton.md) | 按钮组件 | 📖 |
| [XLabel](docs/XLabel.md) | 标签组件 | 📖 |
| [XIcon](docs/XIcon.md) | 图标组件 | 📖 |
| [XBadge](docs/XBadge.md) | 徽章组件 | 📖 |
| [XDivider](docs/XDivider.md) | 分隔线组件 | 📖 |

### 表单组件

| 组件 | 说明 | 文档 |
|------|------|------|
| [XLineEdit](docs/XLineEdit.md) | 单行输入框 | 📖 |
| [XTextEdit](docs/XTextEdit.md) | 多行文本框 | 📖 |
| [XSpinBox](docs/XSpinBox.md) | 数字输入框 | 📖 |
| [XComboBox](docs/XComboBox.md) | 下拉选择框 | 📖 |
| [XCheckBox](docs/XCheckBox.md) | 复选框 | 📖 |
| [XRadioButton](docs/XRadioButton.md) | 单选按钮 | 📖 |
| [XSwitch](docs/XSwitch.md) | 开关组件 | 📖 |
| [XSlider](docs/XSlider.md) | 滑块组件 | 📖 |
| [XQDateEdit](docs/XQDateEdit.md) | 日期选择器 | 📖 |
| [XQTimeEdit](docs/XQTimeEdit.md) | 时间选择器 | 📖 |
| [XQDateTimeEdit](docs/XQDateTimeEdit.md) | 日期时间选择器 | 📖 |

### 数据展示

| 组件 | 说明 | 文档 |
|------|------|------|
| [XTableWidget](docs/XTableWidget.md) | 表格组件 | 📖 |
| [XListWidget](docs/XListWidget.md) | 列表组件 | 📖 |
| [XTreeWidget](docs/XTreeWidget.md) | 树形组件 | 📖 |
| [XCard](docs/XCard.md) | 卡片组件 | 📖 |
| [XGroupBox](docs/XGroupBox.md) | 分组框组件 | 📖 |
| [XImage](docs/XImage.md) | 图片组件 | 📖 |
| [XCodeBlock](docs/XCodeBlock.md) | 代码块组件 | 📖 |

### 导航组件

| 组件 | 说明 | 文档 |
|------|------|------|
| [XTabWidget](docs/XTabWidget.md) | 标签页组件 | 📖 |
| [XNavSimple](docs/XNavSimple.md) | 简单导航 | 📖 |
| [XNavTree](docs/XNavTree.md) | 树形导航 | 📖 |
| [XPagination](docs/XPagination.md) | 分页组件 | 📖 |
| [XMenu](docs/XMenu.md) | 菜单组件 | 📖 |
| [XPopover](docs/XPopover.md) | 气泡组件 | 📖 |

### 反馈组件

| 组件 | 说明 | 文档 |
|------|------|------|
| [XMessageBox](docs/XMessageBox.md) | 消息对话框 | 📖 |
| [XNotif](docs/XNotif.md) | 通知组件 | 📖 |
| [XProgressBar](docs/XProgressBar.md) | 进度条组件 | 📖 |
| [XLoadingMask](docs/XLoadingMask.md) | 加载遮罩 | 📖 |

### 布局组件

| 组件 | 说明 | 文档 |
|------|------|------|
| [XWidget](docs/XWidget.md) | 容器组件 | 📖 |
| [XScrollArea](docs/XScrollArea.md) | 滚动区域 | 📖 |
| [XCollapse](docs/XCollapse.md) | 折叠面板 | 📖 |
| [XCarousel](docs/XCarousel.md) | 轮播组件 | 📖 |

### 其他组件

| 组件 | 说明 | 文档 |
|------|------|------|
| [XTitleBar](docs/XTitleBar.md) | 标题栏组件 | 📖 |
| [XUpload](docs/XUpload.md) | 上传组件 | 📖 |

---

## 💡 使用示例

### 按钮组件

```python
from xsideui import XPushButton, XColor, XButtonVariant, XSize

# 不同变体
button1 = XPushButton("实心按钮", variant=XButtonVariant.SOLID, color=XColor.PRIMARY)
button2 = XPushButton("描边按钮", variant=XButtonVariant.OUTLINED, color=XColor.PRIMARY)
button3 = XPushButton("文本按钮", variant=XButtonVariant.TEXT, color=XColor.PRIMARY)

# 带图标
button4 = XPushButton("提交", icon="check", color=XColor.SUCCESS)

# Loading 状态
button5 = XPushButton("保存")
button5.set_loading(True)

# 链式调用
button6 = XPushButton("按钮") \
    .set_variant(XButtonVariant.FILLED) \
    .set_color(XColor.WARNING) \
    .set_size(XSize.LARGE)
```

### 卡片组件

```python
from xsideui import XCard, XHeaderCard, XGroupCard, XLabel

# 基础卡片
card1 = XCard()
card1.addWidget(XLabel("卡片内容"))

# 标题卡片
card2 = XHeaderCard(title="设置")
card2.addWidget(XLabel("内容"))

# 分组卡片
card3 = XGroupCard(title="配置")
card3.add_group().add(XLabel("分组1"))
card3.add_group().add(XLabel("分组2"))
```

### 表格组件

```python
from xsideui import XTableWidget

table = XTableWidget()
table.set_headers(["姓名", "年龄", "城市"])
table.add_row(["张三", 25, "北京"])
table.add_row(["李四", 30, "上海"])
```

### 导航组件

```python
from xsideui import XTabWidget

tabs = XTabWidget()
tabs.add_tab("标签1", XLabel("内容1"))
tabs.add_tab("标签2", XLabel("内容2"))
tabs.add_tab("标签3", XLabel("内容3"))
```

---

## 🏗️ 项目结构

```
xsideui/
├── docs/              # 组件文档
├── src/
│   └── xsideui/
│       ├── widgets/   # UI 组件
│       ├── theme/     # 主题系统
│       ├── icon/      # 图标引擎
│       ├── xenum/     # 枚举定义
│       └── utils/     # 工具函数
└── examples/          # 示例代码
```

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证，代码完全开放，您可以在商业项目中自由使用、修改和分发，只需保留原始版权声明。

---

## 🙏 致谢

- [PySide2](https://wiki.qt.io/Qt_for_Python) - Qt for Python
- [Arco Design](https://arco.design/) - 设计灵感来源

---

## 📮 联系方式

- 项目主页：[https://github.com/bmscriptsbox/xsideui](https://github.com/bmscriptsbox/xsideui)
- 问题反馈：[Issues](https://github.com/bmscriptsbox/xsideui/issues)
- 邮箱：<bmscriptsbox@163.com>

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐️ Star 支持一下！**

Made with ❤️ by XSideUI Team

</div>
