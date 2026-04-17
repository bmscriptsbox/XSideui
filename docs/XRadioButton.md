# XRadioButton

单选按钮组件，支持多种尺寸和颜色，自动适配主题切换。

## 示例

![XRadioButton示例](./images/XRadioButton.png "XRadioButton示例")

## 导入

```python
from xsideui import XRadioButton
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `text` | str | "" | 按钮文本内容 |
| `checked` | bool | False | 是否选中 |
| `size` | XSize | XSize.DEFAULT | 按钮尺寸 |
| `color` | XColor 或 str | None | 按钮颜色 |
| `parent` | QWidget | None | 父组件 |

## 尺寸

| 尺寸 | 枚举值 | 字符串值 | 高度 | 圆圈半径 | 字号 |
|------|--------|----------|------|-----------|------|
| 大尺寸 | XSize.LARGE | "large" | 36px | 9px | 14px |
| 默认尺寸 | XSize.DEFAULT | "default" | 32px | 8px | 13px |
| 小尺寸 | XSize.SMALL | "small" | 24px | 7px | 12px |
| 迷你尺寸 | XSize.MINI | "mini" | 20px | 6px | 11px |

## 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `setChecked(checked)` | 设置选中状态 | None |
| `isChecked()` | 获取选中状态 | bool |
| `setEnabled(enabled)` | 设置启用/禁用状态 | None |
| `set_size(size)` | 设置尺寸 | XRadioButton |
| `set_color(color)` | 设置颜色 | XRadioButton |

## 信号

| 信号 | 说明 |
|------|------|
| `clicked(bool)` | 单选按钮被点击时发出 |
| `stateChanged(int)` | 状态变化时发出 |
| `toggled(bool)` | 选中状态改变时发出 |

## 示例

```python
# 基础用法
radio = XRadioButton("选项")

# 指定初始状态
radio = XRadioButton("选项", checked=True)

# 自定义尺寸
radio = XRadioButton("选项", size=XSize.LARGE)

# 自定义颜色
radio = XRadioButton("选项", color=XColor.SUCCESS)

# 链式调用
radio = XRadioButton("选项") \
    .set_size(XSize.SMALL) \
    .set_color(XColor.WARNING)

# 监听状态变化
radio.clicked.connect(lambda checked: print(f"选中状态: {checked}"))

# 禁用单选按钮
radio.setEnabled(False)

# 获取当前状态
is_checked = radio.isChecked()

# 单选组
from PySide2.QtWidgets import QButtonGroup

button_group = QButtonGroup()
radio1 = XRadioButton("选项 A", checked=True)
radio2 = XRadioButton("选项 B")
radio3 = XRadioButton("选项 C")

button_group.addButton(radio1)
button_group.addButton(radio2)
button_group.addButton(radio3)
```

## 特性

- ✅ 4 种预设尺寸（large/default/small/mini）
- ✅ 支持主题预设颜色（primary/success/warning/danger 等）
- ✅ 支持自定义颜色值（如 #FF0000）
- ✅ 自动适配主题切换
- ✅ 交互反馈（按下、悬停时颜色变化）
- ✅ 禁用状态样式
- ✅ 支持链式调用
- ✅ 高分屏支持（Retina/4K）
- ✅ 性能优化（缓存和节流机制）
- ✅ 单选互斥（同一父组件下自动互斥）
