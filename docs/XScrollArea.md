# XScrollArea 组件文档

## 📋 目录

- [概述](#概述)
- [快速开始](#快速开始)
- [构造函数](#构造函数)
- [方法列表](#方法列表)
- [使用示例](#使用示例)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)

---

## 概述

XScrollArea 是一个滚动区域组件，继承自 `QScrollArea`，提供了支持明暗主题切换的滚动容器功能。

### 主要特性

- ✅ **主题适配** - 滚动条样式自动适配明暗主题切换
- ✅ **自定义滚动条** - 细致的滚动条样式，支持悬停效果
- ✅ **灵活配置** - 可单独控制垂直/水平滚动条的显隐
- ✅ **性能优异** - 使用全局样式表，性能极佳
- ✅ **易于使用** - 继承自 QScrollArea，使用方式与普通 QScrollArea 完全一致

### 基本使用

```python
from PySide2.QtWidgets import QApplication
from src.xsideui.widgets import XScrollArea, XWidget

app = QApplication(sys.argv)

# 创建滚动区域
scroll_area = XScrollArea()

# 设置内容组件
content_widget = XWidget()
scroll_area.setWidget(content_widget)
```

---

## 快速开始

### 1. 导入组件

```python
from src.xsideui.widgets import XScrollArea
```

### 2. 创建滚动区域

```python
# 创建滚动区域
scroll_area = XScrollArea()
```

### 3. 设置内容组件

```python
from src.xsideui.widgets import XWidget

# 创建内容组件
content_widget = XWidget()
scroll_area.setWidget(content_widget)
```

### 4. 添加到布局

```python
from PySide2.QtWidgets import QWidget, QVBoxLayout

parent_widget = QWidget()
parent_layout = QVBoxLayout()
parent_layout.addWidget(scroll_area)
parent_widget.setLayout(parent_layout)
```

---

## 构造函数

### 完整参数

```python
XScrollArea(parent: QWidget = None)
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|---------|------|
| `parent` | `QWidget` | `None` | 父组件 |

### 使用示例

```python
# 使用默认参数
scroll_area = XScrollArea()

# 指定父组件
parent = QWidget()
scroll_area = XScrollArea(parent=parent)
```

---

## 方法列表

### 设置滚动条显隐

#### `set_scrollbar_visible(vertical: bool, horizontal: bool)`

设置垂直和水平滚动条的显隐。

```python
scroll_area.set_scrollbar_visible(vertical=True, horizontal=False)
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `vertical` | `bool` | 垂直滚动条是否可见 |
| `horizontal` | `bool` | 水平滚动条是否可见 |

**说明：**
- 默认情况下，两个滚动条都可见（`AsNeeded` 模式）
- 设置为 `False` 时，对应的滚动条将被隐藏（`AlwaysOff` 模式）

**示例：**
```python
# 只显示垂直滚动条
scroll_area.set_scrollbar_visible(vertical=True, horizontal=False)

# 只显示水平滚动条
scroll_area.set_scrollbar_visible(vertical=False, horizontal=True)

# 隐藏所有滚动条
scroll_area.set_scrollbar_visible(vertical=False, horizontal=False)

# 显示所有滚动条（默认）
scroll_area.set_scrollbar_visible(vertical=True, horizontal=True)
```

---

## 使用示例

### 示例 1：创建简单滚动区域

```python
from src.xsideui.widgets import XScrollArea, XWidget, XLabel

# 创建滚动区域
scroll_area = XScrollArea()

# 创建内容组件
content_widget = XWidget()
content_layout = content_widget.layout()

# 添加多个标签
for i in range(20):
    content_layout.addWidget(XLabel(f"内容项 {i + 1}"))

# 设置内容组件
scroll_area.setWidget(content_widget)
```

### 示例 2：只显示垂直滚动条

```python
from src.xsideui.widgets import XScrollArea, XWidget, XLabel

# 创建滚动区域
scroll_area = XScrollArea()
scroll_area.set_scrollbar_visible(vertical=True, horizontal=False)

# 创建内容组件
content_widget = XWidget()
content_layout = content_widget.layout()

# 添加内容
for i in range(10):
    content_layout.addWidget(XLabel(f"垂直滚动示例 {i + 1}"))

scroll_area.setWidget(content_widget)
```

### 示例 3：只显示水平滚动条

```python
from src.xsideui.widgets import XScrollArea, XWidget, XLabel
from PySide2.QtWidgets import QHBoxLayout

# 创建滚动区域
scroll_area = XScrollArea()
scroll_area.set_scrollbar_visible(vertical=False, horizontal=True)

# 创建内容组件
content_widget = XWidget()
content_layout = QHBoxLayout()

# 添加多个水平排列的标签
for i in range(10):
    content_layout.addWidget(XLabel(f"水平滚动 {i + 1}"))

scroll_area.setWidget(content_widget)
```

### 示例 4：完整示例

```python
import sys
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout
from src.xsideui.widgets import XScrollArea, XWidget, XLabel, XDivider
from src.xsideui.theme import theme_manager

app = QApplication(sys.argv)

# 创建主窗口
window = QWidget()
window.setWindowTitle("XScrollArea 示例")
window.resize(800, 600)

# 主布局
main_layout = QVBoxLayout()
main_layout.setSpacing(20)
main_layout.setContentsMargins(40, 40, 40, 40)

# 添加标题
main_layout.addWidget(XLabel("滚动区域示例", style=XLabel.Style.H3))
main_layout.addWidget(XDivider())

# 创建滚动区域
scroll_area = XScrollArea()
scroll_area.set_scrollbar_visible(vertical=True, horizontal=True)

# 创建内容组件
content_widget = XWidget()
content_layout = content_widget.layout()

# 添加多个内容项
for i in range(30):
    content_layout.addWidget(XLabel(f"这是一个很长的内容项 {i + 1}，用于演示滚动功能"))

scroll_area.setWidget(content_widget)
main_layout.addWidget(scroll_area)

window.setLayout(main_layout)
window.show()

sys.exit(app.exec_())
```

### 示例 5：主题切换

```python
from src.xsideui.widgets import XScrollArea, XWidget, XLabel
from src.xsideui.theme import theme_manager

# 创建滚动区域
scroll_area = XScrollArea()
content_widget = XWidget()
content_layout = content_widget.layout()

for i in range(20):
    content_layout.addWidget(XLabel(f"内容项 {i + 1}"))

scroll_area.setWidget(content_widget)

# 切换主题
theme_manager.toggle_theme()  # 滚动条样式自动更新
```

---

## 最佳实践

### 1. 合理使用滚动条显隐

**推荐：** 根据内容特点选择合适的滚动条配置。

```python
# ✅ 推荐 - 只显示垂直滚动条（常见场景）
scroll_area = XScrollArea()
scroll_area.set_scrollbar_visible(vertical=True, horizontal=False)

# ✅ 推荐 - 显示所有滚动条（需要双向滚动时）
scroll_area = XScrollArea()
scroll_area.set_scrollbar_visible(vertical=True, horizontal=True)

# ❌ 不推荐 - 隐藏所有滚动条（用户无法滚动）
scroll_area = XScrollArea()
scroll_area.set_scrollbar_visible(vertical=False, horizontal=False)
```

### 2. 使用 setWidgetResizable

**推荐：** 让内容组件自适应滚动区域大小。

```python
# ✅ 推荐 - 启用自适应
scroll_area = XScrollArea()
scroll_area.setWidgetResizable(True)  # 默认已启用

# ❌ 不推荐 - 禁用自适应
scroll_area = XScrollArea()
scroll_area.setWidgetResizable(False)  # 内容大小固定
```

### 3. 合理设置内容组件大小

**推荐：** 内容组件应该有合适的最小尺寸。

```python
# ✅ 推荐 - 设置最小尺寸
content_widget = XWidget()
content_widget.setMinimumSize(200, 200)
scroll_area.setWidget(content_widget)

# ✅ 推荐 - 使用布局自动计算尺寸
content_widget = XWidget()
content_layout = content_widget.layout()
# 添加内容后，布局会自动计算尺寸
```

### 4. 避免过度嵌套

**推荐：** 避免在滚动区域内嵌套过多层级。

```python
# ✅ 推荐 - 简单结构
scroll_area = XScrollArea()
content_widget = XWidget()
scroll_area.setWidget(content_widget)

# ❌ 不推荐 - 过度嵌套
scroll_area = XScrollArea()
wrapper1 = XWidget()
wrapper2 = XWidget()
content_widget = XWidget()
wrapper1.layout().addWidget(wrapper2)
wrapper2.layout().addWidget(content_widget)
scroll_area.setWidget(wrapper1)
```

### 5. 主题适配

**推荐：** 让滚动条样式自动适配主题切换。

```python
# ✅ 推荐 - 使用 XScrollArea
scroll_area = XScrollArea()
# 滚动条样式自动适配主题切换

# ❌ 不推荐 - 使用普通 QScrollArea
scroll_area = QScrollArea()
# 滚动条样式不会自动适配主题切换
```

---

## 常见问题

### Q1: 如何修改滚动条的宽度？

**A:** 修改 QSS 文件中的样式。

```css
/* 在 scrollarea.qss 中修改 */
QScrollArea#xscrollarea QScrollBar:vertical {
    width: 8px;  /* 修改垂直滚动条宽度 */
}

QScrollArea#xscrollarea QScrollBar:horizontal {
    height: 8px;  /* 修改水平滚动条高度 */
}
```

### Q2: 如何修改滚动条的颜色？

**A:** 修改 QSS 文件中的颜色变量。

```css
/* 在 scrollarea.qss 中修改 */
QScrollArea#xscrollarea QScrollBar::handle:vertical {
    background-color: {fill_alpha_4};  /* 使用主题变量 */
}

/* 或使用自定义颜色 */
QScrollArea#xscrollarea QScrollBar::handle:vertical {
    background-color: #FF0000;  /* 自定义颜色 */
}
```

### Q3: 滚动条样式如何随主题变化？

**A:** 自动适配，无需额外代码。

```python
scroll_area = XScrollArea()
# 滚动条样式会自动适配主题切换
# Light 主题：浅色滚动条
# Dark 主题：深色滚动条
```

### Q4: 如何设置滚动区域的背景色？

**A:** 修改 QSS 文件。

```css
/* 在 scrollarea.qss 中修改 */
QScrollArea#xscrollarea > QWidget > QWidget {
    background-color: {bg_1};  /* 使用主题变量 */
}
```

### Q5: 如何禁用滚动区域？

**A:** 使用 `setEnabled()` 方法。

```python
scroll_area = XScrollArea()
scroll_area.setEnabled(False)  # 禁用
scroll_area.setEnabled(True)   # 启用
```

### Q6: 如何获取当前滚动位置？

**A:** 使用滚动条的 `value()` 方法。

```python
# 获取垂直滚动位置
vertical_pos = scroll_area.verticalScrollBar().value()

# 获取水平滚动位置
horizontal_pos = scroll_area.horizontalScrollBar().value()
```

### Q7: 如何设置滚动位置？

**A:** 使用滚动条的 `setValue()` 方法。

```python
# 设置垂直滚动位置
scroll_area.verticalScrollBar().setValue(100)

# 设置水平滚动位置
scroll_area.horizontalScrollBar().setValue(50)
```

### Q8: 如何滚动到顶部？

**A:** 将垂直滚动条值设置为 0。

```python
scroll_area.verticalScrollBar().setValue(0)
```

### Q9: 如何滚动到底部？

**A:** 将垂直滚动条值设置为最大值。

```python
scroll_area.verticalScrollBar().setValue(
    scroll_area.verticalScrollBar().maximum()
)
```

### Q10: 可以继承 XScrollArea 吗？

**A:** 可以，继承后可以扩展功能。

```python
class MyScrollArea(XScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 添加自定义功能
```

### Q11: 如何监听滚动事件？

**A:** 连接滚动条的信号。

```python
# 监听垂直滚动
scroll_area.verticalScrollBar().valueChanged.connect(
    lambda value: print(f"垂直滚动位置: {value}")
)

# 监听水平滚动
scroll_area.horizontalScrollBar().valueChanged.connect(
    lambda value: print(f"水平滚动位置: {value}")
)
```

### Q12: 滚动区域支持哪些主题？

**A:** 支持所有已注册的主题。

```python
from src.xsideui.theme import theme_manager

# 切换到 light 主题
theme_manager.set_theme("light")

# 切换到 dark 主题
theme_manager.set_theme("dark")

# 滚动条样式会自动更新
```

---

## 完整示例代码

查看完整示例代码，请运行：

```bash
python example/example_scrollarea.py
```

该示例展示了 XScrollArea 的功能，包括：

- 创建滚动区域
- 设置内容组件
- 控制滚动条显隐
- 主题切换
- 滚动条样式自动适配

---

## 更新日志

### v1.0.0 (2026-02-10)

- ✨ 初始版本发布
- ✅ 支持明暗主题切换
- ✅ 滚动条样式自动适配
- ✅ 灵活的滚动条显隐控制
- ✅ 细致的滚动条样式设计

---

## 许可证

MIT License

---

## 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。
