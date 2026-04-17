# XCheckBox

复选框组件，支持多种尺寸和颜色，自动适配主题切换。

## 示例

![XCheckBox示例](./images/XCheckBox.png "XCheckBox示例")

## 导入

```python
from xsideui import XCheckBox
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `text` | str | "" | 复选框文本内容 |
| `checked` | bool | False | 是否选中 |
| `size` | XSize | XSize.DEFAULT | 复选框尺寸 |
| `color` | XColor 或 str | None | 复选框颜色 |
| `parent` | QWidget | None | 父组件 |

## 尺寸

| 尺寸 | 枚举值 | 字符串值 | 高度 | 方框大小 | 字号 |
|------|--------|----------|------|-----------|------|
| 大尺寸 | XSize.LARGE | "large" | 40px | 24px | 15px |
| 默认尺寸 | XSize.DEFAULT | "default" | 32px | 20px | 14px |
| 小尺寸 | XSize.SMALL | "small" | 24px | 16px | 12px |
| 迷你尺寸 | XSize.MINI | "mini" | 22px | 14px | 11px |

## 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `setChecked(checked)` | 设置选中状态 | None |
| `isChecked()` | 获取选中状态 | bool |
| `setEnabled(enabled)` | 设置启用/禁用状态 | None |
| `set_size(size)` | 设置尺寸 | XCheckBox |
| `set_color(color)` | 设置颜色 | XCheckBox |

## 信号

| 信号 | 说明 |
|------|------|
| `clicked(bool)` | 复选框被点击时发出 |
| `stateChanged(int)` | 状态变化时发出 |
| `toggled(bool)` | 选中状态改变时发出 |

## 示例

```python
# 基础用法
checkbox = XCheckBox("选项")

# 指定初始状态
checkbox = XCheckBox("选项", checked=True)

# 自定义尺寸
checkbox = XCheckBox("选项", size=XSize.LARGE)

# 自定义颜色
checkbox = XCheckBox("选项", color=XColor.SUCCESS)

# 链式调用
checkbox = XCheckBox("选项") \
    .set_size(XSize.SMALL) \
    .set_color(XColor.WARNING)

# 监听状态变化
checkbox.clicked.connect(lambda checked: print(f"选中状态: {checked}"))

# 禁用复选框
checkbox.setEnabled(False)

# 获取当前状态
is_checked = checkbox.isChecked()

# 多选
checkbox1 = XCheckBox("选项 A", checked=True)
checkbox2 = XCheckBox("选项 B", checked=True)
checkbox3 = XCheckBox("选项 C")
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
- ✅ 独立选择（可多选）
