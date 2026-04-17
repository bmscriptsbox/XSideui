# XNotif

通知提示组件，支持多种类型、位置和自动消失控制，具备淡入淡出和平滑移动动画。

## 示例

![XNotif示例](./images/XNotif.png "XNotif示例")

## 导入

```python
from xsideui import XNotif
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `text` | str | "" | 通知文本内容（最多 500 字符） |
| `parent` | QWidget | None | 父组件 |
| `position` | XNotif.Pos 或 str | "center" | 显示位置 |
| `duration` | int | 2000 | 自动消失时间（毫秒），0 表示不自动消失 |
| `show_close` | bool | True | 是否显示关闭按钮 |
| `in_window` | bool | True | 是否在窗口内显示 |
| `animated` | bool | None | 是否启用动画，None 表示使用全局配置 |

## 位置

| 位置 | 枚举值 | 字符串值 | 说明 |
|------|--------|----------|------|
| 居中 | XNotif.Pos.CENTER | "center" | 窗口/屏幕中心 |
| 左上角 | XNotif.Pos.TOP_LEFT | "top_left" | 左上角 |
| 右上角 | XNotif.Pos.TOP_RIGHT | "top_right" | 右上角 |
| 左下角 | XNotif.Pos.BOTTOM_LEFT | "bottom_left" | 左下角 |
| 右下角 | XNotif.Pos.BOTTOM_RIGHT | "bottom_right" | 右下角 |

## 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `info(text, parent, position, duration, show_close, in_window, animated)` | 显示信息通知 | XNotif |
| `success(text, parent, position, duration, show_close, in_window, animated)` | 显示成功通知 | XNotif |
| `warning(text, parent, position, duration, show_close, in_window, animated)` | 显示警告通知 | XNotif |
| `error(text, parent, position, duration, show_close, in_window, animated)` | 显示错误通知 | XNotif |
| `close_notification()` | 关闭通知 | None |

## 示例

```python
# 基础用法
XNotif.info("操作成功完成")
XNotif.success("文件保存成功")
XNotif.warning("请注意检查输入内容")
XNotif.error("操作失败，请重试")

# 自定义位置
XNotif.info("右上角显示", position="top_right")
XNotif.success("居中显示", position=XNotif.Pos.CENTER)

# 自定义显示时长
XNotif.info("5秒后消失", duration=5000)
XNotif.success("不自动消失", duration=0)

# 窗口内通知
XNotif.info("窗口内通知", parent=window)

# 屏幕通知
XNotif.info("屏幕通知", in_window=False)

# 禁用动画
XNotif.info("无动画通知", animated=False)

# 不显示关闭按钮
XNotif.info("无法关闭的通知", show_close=False)

# 组合参数
XNotif.success(
    text="完整通知",
    parent=window,
    position="top_right",
    duration=3000,
    show_close=True,
    in_window=True,
    animated=True
)

# 多通知堆叠
XNotif.info("第一条通知", position="top_right")
XNotif.success("第二条通知", position="top_right")
XNotif.warning("第三条通知", position="top_right")
```

## 特性

- ✅ 4 种通知类型（信息、成功、警告、错误）
- ✅ 5 种显示位置（居中、四角）
- ✅ 自动消失控制（可配置时长）
- ✅ 淡入淡出动画（300ms）
- ✅ 平滑移动动画（堆叠时）
- ✅ 自动适配主题切换
- ✅ 支持窗口内/屏幕显示
- ✅ 文本长度限制（500 字符）
- ✅ 多通知自动堆叠
- ✅ 可配置动画开关
