# XProgressBar & XCircleProgress

进度条组件，支持不同颜色、尺寸、文本位置和动画，自动适配主题切换。

## 示例

![XProgressBar示例](./images/XProgressBar.png "XProgressBar示例")

## 导入

```python
from xsideui import XProgressBar, XCircleProgress
```

## XProgressBar 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `value` | int | 0 | 初始值 |
| `minimum` | int | 0 | 最小值 |
| `maximum` | int | 100 | 最大值 |
| `height` | int | 6 | 进度条高度（像素，最小 4px） |
| `color` | XColor 或 str | XColor.PRIMARY | 进度条颜色 |
| `text_visible` | bool | True | 是否显示百分比文本 |
| `text_position` | str | "center" | 文本位置（center/right） |
| `animation_enabled` | bool | True | 是否启用动画 |
| `parent` | QWidget | None | 父组件 |

## XCircleProgress 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `value` | int | 0 | 初始值 |
| `minimum` | int | 0 | 最小值 |
| `maximum` | int | 100 | 最大值 |
| `size` | int | 100 | 进度条直径（像素，最小 40px） |
| `color` | XColor 或 str | XColor.PRIMARY | 进度颜色 |
| `text_visible` | bool | True | 是否显示百分比文本 |
| `animation_enabled` | bool | True | 是否启用动画 |
| `parent` | QWidget | None | 父组件 |

## 文本位置

| 位置 | 说明 |
|------|------|
| center | 居中显示（默认） |
| right | 右侧显示 |

## XProgressBar 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `set_height(height)` | 设置进度条高度 | XProgressBar |
| `set_color(color)` | 设置进度条颜色 | XProgressBar |
| `set_text_position(position)` | 设置文本位置 | XProgressBar |
| `set_animation_enabled(enabled)` | 设置是否启用动画 | XProgressBar |
| `setValue(value)` | 设置进度值（支持动画） | XProgressBar |
| `setMinimum(minimum)` | 设置最小值 | None |
| `setMaximum(maximum)` | 设置最大值 | None |
| `setTextVisible(visible)` | 设置是否显示文本 | None |
| `setEnabled(enabled)` | 设置启用/禁用状态 | None |

## XCircleProgress 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `set_size(size)` | 设置进度条尺寸 | XCircleProgress |
| `set_color(color)` | 设置进度颜色 | XCircleProgress |
| `set_animation_enabled(enabled)` | 设置是否启用动画 | XCircleProgress |
| `setValue(value)` | 设置进度值（支持动画） | XCircleProgress |
| `setMinimum(minimum)` | 设置最小值 | None |
| `setMaximum(maximum)` | 设置最大值 | None |
| `setTextVisible(visible)` | 设置是否显示文本 | None |
| `setEnabled(enabled)` | 设置启用/禁用状态 | None |

## 示例

```python
# 线性进度条 - 基础用法
progress = XProgressBar(value=50, height=16, color=XColor.PRIMARY)

# 圆形进度条 - 基础用法
circle = XCircleProgress(value=50, size=100, color=XColor.PRIMARY)

# 自定义文本位置
progress = XProgressBar(value=5, text_position='right')

# 禁用动画
progress = XProgressBar(value=50, animation_enabled=False)

# 链式调用
progress = XProgressBar() \
    .set_height(16) \
    .set_color(XColor.SUCCESS) \
    .set_text_position('right') \
    .setValue(75)

circle = XCircleProgress() \
    .set_size(80) \
    .set_color(XColor.SUCCESS) \
    .setValue(75)

# 自定义颜色
progress = XProgressBar(color='#FF0000')
circle = XCircleProgress(color='rgb(255, 0, 0)')

# 禁用状态
progress.setEnabled(False)
circle.setEnabled(False)

# 隐藏文本
progress.setTextVisible(False)
circle.setTextVisible(False)

# 获取当前值
current_value = progress.value()
```

## 特性

- ✅ 支持主题预设颜色（primary/success/warning/danger 等）
- ✅ 支持自定义颜色值（如 #FF0000）
- ✅ 自动适配主题切换
- ✅ 文本显示/隐藏控制
- ✅ 文本位置灵活（居中/右侧/上方）
- ✅ 平滑动画（进度过渡动画）
- ✅ 禁用状态样式
- ✅ 支持链式调用
- ✅ LRU 缓存优化（最多 50 个）
- ✅ 高分屏支持
- ✅ 节流机制（16ms）
