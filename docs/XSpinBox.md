# XSpinBox 和 XDoubleSpinBox

数字输入框组件，提供整数和小数输入框，支持步进按钮。

## 示例

![XSpinBox示例](./images/XSpinBox.png "XSpinBox示例")

## 导入

```python
from xsideui import XSpinBox, XDoubleSpinBox
```

## 参数

### XSpinBox

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `value` | int | 0 | 初始值 |
| `minimum` | int | 0 | 最小值 |
| `maximum` | int | 999999999 | 最大值 |
| `step` | int | 1 | 步长 |
| `prefix` | str | "" | 前缀文本 |
| `suffix` | str | "" | 后缀文本 |
| `size` | XSize | XSize.DEFAULT | 组件尺寸 |
| `parent` | QWidget | None | 父组件 |

### XDoubleSpinBox

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `value` | float | 0.0 | 初始值 |
| `minimum` | float | 0.0 | 最小值 |
| `maximum` | float | 99.99 | 最大值 |
| `step` | float | 0.1 | 步长 |
| `decimals` | int | 2 | 小数位数 |
| `prefix` | str | "" | 前缀文本 |
| `suffix` | str | "" | 后缀文本 |
| `size` | XSize | XSize.DEFAULT | 组件尺寸 |
| `parent` | QWidget | None | 父组件 |

## 尺寸

| 尺寸 | 枚举值 | 字符串值 | 字体大小 |
|------|--------|----------|----------|
| 大尺寸 | XSize.LARGE | "large" | 16px |
| 默认尺寸 | XSize.DEFAULT | "default" | 14px |
| 小尺寸 | XSize.SMALL | "small" | 13px |
| 迷你尺寸 | XSize.MINI | "mini" | 12px |

## 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `setValue(value)` | 设置当前值 | None |
| `setRange(min, max)` | 设置范围 | None |
| `setSingleStep(step)` | 设置步长 | None |
| `setPrefix(prefix)` | 设置前缀 | None |
| `setSuffix(suffix)` | 设置后缀 | None |
| `set_size(size)` | 设置尺寸 | XSpinBox / XDoubleSpinBox |
| `set_decimals(decimals)` | 设置小数位数（仅 XDoubleSpinBox） | XDoubleSpinBox |

## 信号

| 信号 | 说明 |
|------|------|
| `valueChanged` | 值变化时发出 |

## 示例

### XSpinBox - 整数输入框

```python
# 基础用法
spin = XSpinBox(value=50)

# 设置范围和步长
spin = XSpinBox(value=50, minimum=0, maximum=100, step=5)

# 添加前缀和后缀
spin = XSpinBox(value=50, prefix="$", suffix="个")

# 自定义尺寸
spin = XSpinBox(value=50, size=XSize.LARGE)

# 链式调用
spin = XSpinBox(value=50) \
    .set_size(XSize.LARGE) \
    .setRange(0, 200) \
    .setSingleStep(10)

# 监听值变化
spin.valueChanged.connect(lambda value: print(f"值变为: {value}"))

# 禁用组件
spin.setEnabled(False)

# 获取当前值
current_value = spin.value()
```

### XDoubleSpinBox - 小数输入框

```python
# 基础用法
spin = XDoubleSpinBox(value=0.5)

# 设置小数位数
spin = XDoubleSpinBox(value=0.5, decimals=2)

# 设置范围和步长
spin = XDoubleSpinBox(value=0.5, minimum=0.0, maximum=1.0, step=0.1)

# 添加前缀和后缀
spin = XDoubleSpinBox(value=0.5, prefix="￥", suffix="%")

# 自定义尺寸
spin = XDoubleSpinBox(value=0.5, size=XSize.LARGE)

# 链式调用
spin = XDoubleSpinBox(value=0.5) \
    .set_size(XSize.LARGE) \
    .set_decimals(3) \
    .setRange(0.0, 100.0)

# 监听值变化
spin.valueChanged.connect(lambda value: print(f"值变为: {value}"))

# 动态修改小数位数
spin.set_decimals(4)
```

### 不同尺寸

```python
from xsideui import XSpinBox, XSize

# 使用枚举
spin_large = XSpinBox(value=50, size=XSize.LARGE)
spin_default = XSpinBox(value=50, size=XSize.DEFAULT)
spin_small = XSpinBox(value=50, size=XSize.SMALL)
spin_mini = XSpinBox(value=50, size=XSize.MINI)

# 使用字符串
spin_large = XSpinBox(value=50, size="large")
spin_default = XSpinBox(value=50, size="default")
spin_small = XSpinBox(value=50, size="small")
spin_mini = XSpinBox(value=50, size="mini")

# 动态修改尺寸
spin.set_size(XSize.LARGE)
spin.set_size("large")
```

### 完整示例

```python
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout
from xsideui import XWidget, XSpinBox, XDoubleSpinBox, XSize

app = QApplication([])

window = XWidget()
layout = QVBoxLayout()

# 整数输入框
spin1 = XSpinBox(value=50, size=XSize.LARGE)
spin2 = XSpinBox(value=50, minimum=0, maximum=100, step=5)
spin3 = XSpinBox(value=50, prefix="$", suffix="个")

# 小数输入框
double1 = XDoubleSpinBox(value=50.5, decimals=2)
double2 = XDoubleSpinBox(value=0.5, step=0.1, decimals=1)

# 监听值变化
def on_value_changed(value):
    print(f"值变为: {value}")

spin1.valueChanged.connect(on_value_changed)

layout.addWidget(spin1)
layout.addWidget(spin2)
layout.addWidget(spin3)
layout.addWidget(double1)
layout.addWidget(double2)

window.setLayout(layout)
window.show()

app.exec_()
```

## 特性

- ✅ 4 种预设尺寸（large/default/small/mini）
- ✅ 整数和小数输入
- ✅ 自定义范围和步长
- ✅ 支持前缀和后缀
- ✅ 自动适配主题切换
- ✅ 步进按钮（+/-）
- ✅ 长按连续增减
- ✅ 高分屏支持
- ✅ LRU 缓存机制
- ✅ 节流优化（~60fps）
- ✅ 禁用状态样式
- ✅ 支持链式调用
