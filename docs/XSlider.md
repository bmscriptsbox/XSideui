# XSlider

滑块组件，支持不同颜色、尺寸、方向和提示框，自动适配主题切换。

## 示例

![XSlider示例](./images/XSlider.png "XSlider示例")

## 导入

```python
from xsideui import XSlider
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `orientation` | Qt.Orientation | `Qt.Horizontal` | 滑块方向（水平/垂直） |
| `value` | int | `0` | 初始值 |
| `minimum` | int | `0` | 最小值 |
| `maximum` | int | `100` | 最大值 |
| `step` | int | `1` | 步长 |
| `color` | XColor 或 str | `None` | 滑块颜色（XColor 枚举或字符串） |
| `groove_height` | int | `6` | 轨道高度（像素） |
| `show_tooltip` | bool | `True` | 是否显示值提示 |
| `parent` | QWidget | `None` | 父组件 |

## 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `set_color(color)` | 设置滑块颜色 | XSlider |
| `set_show_tooltip(show)` | 设置是否显示提示框 | XSlider |
| `setValue(value)` | 设置滑块值 | None |
| `value()` | 获取滑块值 | int |

## 信号

| 信号 | 说明 |
|------|------|
| `valueChanged(int)` | 值变化时发出 |

## 示例

```python
from xsideui import XSlider, XColor
from PySide2.QtCore import Qt

# 基础用法
slider = XSlider()

# 指定初始值
slider = XSlider(value=50)

# 自定义范围和步长
slider = XSlider(value=50, minimum=0, maximum=100, step=1)

# 自定义轨道高度
slider = XSlider(value=50, groove_height=8)

# 自定义颜色（枚举）
slider = XSlider(value=50, color=XColor.PRIMARY)

# 自定义颜色（字符串）
slider = XSlider(value=50, color="primary")

# 自定义颜色（十六进制）
slider = XSlider(value=50, color="#FF0000")

# 垂直滑块
slider = XSlider(orientation=Qt.Vertical, value=50)
slider.setMinimumHeight(200)

# 隐藏提示框
slider = XSlider(value=50, show_tooltip=False)

# 链式调用
slider = XSlider(value=50) \
    .set_color(XColor.SUCCESS) \
    .set_show_tooltip(True)

# 监听值变化
slider.valueChanged.connect(lambda value: print(f"当前值: {value}"))

# 禁用滑块
slider.setEnabled(False)

# 获取当前值
current_value = slider.value()
```

## 特性

- ✅ 支持水平和垂直方向
- ✅ 支持主题预设颜色（primary/secondary/success/warning/danger 等）
- ✅ 支持自定义颜色值（如 #FF0000）
- ✅ 自动适配主题切换
- ✅ 悬浮效果（鼠标悬浮时手柄放大）
- ✅ 禁用状态样式
- ✅ 平滑动画（手柄悬浮时的平滑缩放）
- ✅ 可选的值提示框
- ✅ 可自定义轨道高度
- ✅ 支持链式调用
- ✅ 使用 QPixmap 缓存提升性能
- ✅ 竖向滑块从下往上滑（最小值在底部，最大值在顶部）
