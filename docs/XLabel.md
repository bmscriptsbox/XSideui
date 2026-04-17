# XLabel 组件

高级标签组件，支持预设样式、自定义颜色、字号、字重、文字装饰等功能。

## 示例

![XLabel示例](./images/XLabel.png "XLabel示例")

## 快速开始

```python
from src.xsideui.widgets import XLabel

# 使用预设样式
label = XLabel("标题", style=XLabel.Style.H1)

# 使用自定义样式
label = XLabel("文本", color="#FF0000", size=20)

# 链式调用
label = XLabel("Text").set_color("#FF0000").set_font_size(18).set_underline(True)
```

## 预设样式

| 样式 | 字号 | 字重 | 适用场景 |
|------|------|------|---------|
| H1 | 20px | 700 | 页面主标题 |
| H2 | 18px | 600 | 区块标题 |
| H3 | 16px | 550 | 子标题 |
| H4 | 14px | 500 | 强调正文 |
| BODY | 14px | 400 | 常规正文（默认） |
| CAPTION | 13px | 400 | 说明文字 |
| SECONDARY | 12px | 300 | 次要文字 |
| DISABLED | 12px | 300 | 禁用状态 |

## 构造函数

```python
XLabel(
    text: str = "",
    style: XLabel.Style = None,
    color: Union[XColor, str] = None,
    size: int = None,
    weight: int = None,
    letter_spacing: float = 0.3,
    underline: bool = False,
    strike_out: bool = False,
    elide_mode: bool = False,
    alignment: Qt.Alignment = Qt.AlignLeft | Qt.AlignVCenter,
    selectable: bool = True,
    word_wrap: bool = False,
    theme: Theme = None,
    parent: QWidget = None
)
```

### 参数说明

- `text`: 标签文本内容
- `style`: 预设样式（默认 BODY）
- `color`: 自定义颜色，支持 XColor 枚举或十六进制字符串（如 "#FF0000"）
- `size`: 自定义字号（像素）
- `weight`: 自定义字重（100-900）
- `letter_spacing`: 字间距（像素，默认 0.3）
- `underline`: 是否添加下划线
- `strike_out`: 是否添加删除线
- `elide_mode`: 是否启用文本省略模式
- `alignment`: 文本对齐方式
- `selectable`: 是否支持文本选择（默认 True）
- `word_wrap`: 是否自动换行
- `theme`: 主题实例（默认使用全局主题）
- `parent`: 父组件

## 方法列表

### 样式设置

#### `set_style(style)`

设置预设样式。

```python
label.set_style(XLabel.Style.H1)
```

#### `set_color(color)`

设置自定义颜色，支持 XColor 枚举或字符串。

```python
# 使用 XColor 枚举
label.set_color(XColor.PRIMARY)
label.set_color(XColor.SUCCESS)

# 使用十六进制颜色
label.set_color("#FF0000")
```

#### `set_font_size(size)`

设置字号。

```python
label.set_font_size(20)
```

#### `set_weight(weight)`

设置字重（100-900）。

```python
label.set_weight(700)
```

#### `set_letter_spacing(spacing)`

设置字间距。

```python
label.set_letter_spacing(0.5)
```

#### `set_underline(enable)`

启用/禁用下划线。

```python
label.set_underline(True)
```

#### `set_strike_out(enable)`

启用/禁用删除线。

```python
label.set_strike_out(True)
```

### 交互设置

#### `set_alignment(alignment)`

设置文本对齐方式。

```python
# 左对齐 + 垂直居中
label.set_alignment(Qt.AlignLeft | Qt.AlignVCenter)

# 居中对齐
label.set_alignment(Qt.AlignCenter)
```

#### `set_selectable(enable)`

启用/禁用文本选择。

```python
label.set_selectable(True)
```

#### `set_word_wrap(enable)`

设置是否自动换行。

```python
label.set_word_wrap(True)
```

#### `set_elide_mode(enable)`

启用/禁用文本省略模式。启用后，超长文本会用省略号截断，鼠标悬停显示完整文本。

```python
label.set_elide_mode(True)
```

### 高级功能

#### `set_rich_text(html)`

设置富文本内容（HTML 格式）。

```python
label.set_rich_text("这是<b>粗体</b>和<i>斜体</i>文字")
label.set_rich_text('这是<span style="color: #FF0000">红色</span>文字')
```

#### `set_link(url)`

设置为可点击链接。

```python
label = XLabel("点击访问 GitHub")
label.set_link("https://github.com")
```

#### `set_theme(theme)`

设置主题（支持依赖注入）。

```python
from src.xsideui.theme import Theme

custom_theme = Theme()
label.set_theme(custom_theme)
```

## 使用示例

### 基本使用

```python
# 预设样式
label1 = XLabel("页面主标题", style=XLabel.Style.H1)
label2 = XLabel("正文内容", style=XLabel.Style.BODY)

# 自定义颜色
label3 = XLabel("重要提示", style=XLabel.Style.H4)
label3.set_color("#FF0000")

# 链式调用
label4 = XLabel("自定义样式")
label4.set_color("#165DFF").set_font_size(18).set_weight(600).set_underline(True)
```

### 文本省略

```python
# 启用省略模式
label = XLabel("这是一段很长的文字，会被省略号截断")
label.set_elide_mode(True)
```

### 富文本

```python
label = XLabel("")
label.set_rich_text("这是<b>粗体</b>、<i>斜体</i>和<span style='color: #FF0000'>红色</span>文字")
```

### 链接

```python
link_label = XLabel("点击访问官网")
link_label.set_link("https://example.com")
```

### 完整示例

```python
import sys
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout
from src.xsideui.widgets import XLabel

app = QApplication(sys.argv)

widget = QWidget()
layout = QVBoxLayout()

layout.addWidget(XLabel("标题", style=XLabel.Style.H1))
layout.addWidget(XLabel("正文内容", style=XLabel.Style.BODY))

custom_label = XLabel("自定义样式", style=XLabel.Style.H4)
custom_label.set_color("#FF0000").set_font_size(20).set_underline(True)
layout.addWidget(custom_label)

widget.setLayout(layout)
widget.show()
sys.exit(app.exec_())
```

## 高分辨率屏幕支持

组件自动适配高分辨率屏幕，字体大小会根据 DPI 自动缩放。

### 启用高 DPI 支持

在创建 `QApplication` 之前启用高 DPI 支持：

```python
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

app = QApplication(sys.argv)
```

## 最佳实践

1. **优先使用预设样式**，保持界面一致性
2. **使用链式调用**，代码更简洁
3. **对于可能很长的文本，启用省略模式**
4. **对于需要完整显示的长文本，启用自动换行**
5. **使用全局主题**，自动适配主题切换

## 常见问题

### Q: 如何动态修改文本？

A: 使用 `setText()` 方法。

```python
label = XLabel("初始文本")
label.setText("更新后的文本")
```

### Q: 如何获取当前使用的主题？

A: 使用 `theme` 属性。

```python
current_theme = label.theme
```

### Q: 如何禁用文本选择？

A: 使用 `set_selectable(False)`。

```python
label.set_selectable(False)
```

### Q: 如何设置文本居中？

A: 使用 `set_alignment(Qt.AlignCenter)`。

```python
label.set_alignment(Qt.AlignCenter)
```

### Q: 如何重置为预设样式？

A: 使用 `set_style()` 方法。

```python
label.set_style(XLabel.Style.H1)
```

## 示例代码

运行示例查看完整功能：

```bash
python example/xlabel_example.py
```

高分辨率屏幕支持示例：

```bash
python example/example_xlabel_highdpi.py
```
