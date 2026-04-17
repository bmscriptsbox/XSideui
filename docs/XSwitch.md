# XSwitch

开关组件，支持多种尺寸和颜色，自动适配主题切换。

## 示例
![XSwitch示例](./images/XSwitch.png "XSwitch示例")


## 导入

```python
from xsideui import XSwitch
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `text_on` | str | "On" | 开关开启时显示的文本 |
| `text_off` | str | "Off" | 开关关闭时显示的文本 |
| `checked` | bool | False | 是否开启 |
| `color` | XColor 或 str | XColor.PRIMARY | 开关颜色 |
| `size` | XSize  | XSize.DEFAULT | 开关尺寸 |
| `parent` | QWidget | None | 父组件 |

## 尺寸

| 尺寸 | 枚举值 | 字符串值 | 宽度 | 高度 |
|------|--------|----------|------|------|
| 大尺寸 | XSize.LARGE | "large" | 48px | 26px |
| 默认尺寸 | XSize.DEFAULT | "default" | 40px | 22px |
| 小尺寸 | XSize.SMALL | "small" | 32px | 18px |
| 迷你尺寸 | XSize.MINI | "mini" | 24px | 14px |

## 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `setChecked(checked)` | 设置开关状态 | None |
| `set_checked(checked)` | 设置开关状态（链式调用） | XSwitch |
| `isChecked()` | 获取开关状态 | bool |
| `setEnabled(enabled)` | 设置开关启用/禁用状态 | None |
| `set_size(size)` | 设置尺寸 | XSwitch |
| `set_color(color)` | 设置开关颜色 | XSwitch |

## 信号

| 信号 | 说明 |
|------|------|
| `clicked(bool)` | 开关被点击时发出 |

## 示例

```python
# 基础用法
switch = XSwitch("开启", "关闭")

# 指定初始状态
switch = XSwitch("开启", "关闭", checked=True)

# 自定义尺寸
switch = XSwitch("开启", "关闭", size=XSize.LARGE)

# 自定义颜色
switch = XSwitch("开启", "关闭", color=XColor.SUCCESS)

# 链式调用
switch = XSwitch("开启", "关闭") \
    .set_size(XSize.SMALL) \
    .set_color(XColor.WARNING)

# 监听状态变化
switch.clicked.connect(lambda checked: print(f"开关状态: {checked}"))

# 禁用开关
switch.setEnabled(False)

# 获取当前状态
is_on = switch.isChecked()
```

## 特性

- ✅ 4 种预设尺寸（large/default/small/mini）
- ✅ 支持主题预设颜色（primary/success/warning/danger 等）
- ✅ 支持自定义颜色值（如 #FF0000）
- ✅ 自动适配主题切换
- ✅ 悬浮效果（鼠标悬浮时滑块放大）
- ✅ 禁用状态样式
- ✅ 平滑动画（开关切换时的平滑过渡）
- ✅ 带标签（支持开启/关闭文本标签）
- ✅ 支持链式调用
- ✅ 使用 QPixmap 缓存提升性能
