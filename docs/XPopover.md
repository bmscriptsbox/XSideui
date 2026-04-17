# XPopover

气泡卡片组件，提供轻量级的提示信息展示。

## 示例
![XPopover示例](./images/XPopover.png "XPopover示例")


## 导入

```python
from xsideui import XPopover
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `title` | str | None | 标题文本 |
| `content` | str | None | 内容文本 |
| `placement` | Placement 或 str | Placement.TOP | 显示位置 |
| `trigger` | Trigger 或 str | Trigger.HOVER | 触发方式 |
| `parent` | QWidget | None | 父组件 |

## 显示位置

| 位置 | 枚举值 | 字符串值 | 说明 |
|------|--------|----------|------|
| 上方 | Placement.TOP | "top" | 在目标组件上方显示 |
| 下方 | Placement.BOTTOM | "bottom" | 在目标组件下方显示 |
| 左侧 | Placement.LEFT | "left" | 在目标组件左侧显示 |
| 右侧 | Placement.RIGHT | "right" | 在目标组件右侧显示 |

## 触发方式

| 触发方式 | 枚举值 | 字符串值 | 说明 |
|----------|---------|----------|------|
| 悬浮 | Trigger.HOVER | "hover" | 鼠标悬浮时显示 |
| 点击 | Trigger.CLICK | "click" | 鼠标点击时显示/隐藏 |

## 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `show_at_target()` | 在目标组件位置显示 | None |
| `hide()` | 隐藏气泡 | None |
| `set_target(widget)` | 设置触发组件 | None |
| `cleanup()` | 清理资源 | None |

## 类方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `show_popover(target, content, title, placement, trigger)` | 显示气泡卡片 | XPopover |

## 示例

```python
# 基础用法
XPopover.show_popover(button, "这是一个提示")

# 带标题
XPopover.show_popover(
    button,
    content="这是详细说明",
    title="提示标题"
)

# 自定义位置
XPopover.show_popover(
    button,
    content="底部显示",
    placement="bottom"
)

# 点击触发
XPopover.show_popover(
    button,
    content="点击切换",
    trigger="click"
)

# 使用枚举（推荐，类型安全）
XPopover.show_popover(
    button,
    content="提示内容",
    title="标题",
    placement=XPopover.Placement.BOTTOM,
    trigger=XPopover.Trigger.CLICK
)

# 手动控制
popover = XPopover(
    parent=window,
    title="自定义标题",
    content="自定义内容",
    placement="right",
    trigger="click"
)
popover.set_target(button)
popover.show_at_target()
popover.hide()
popover.cleanup()
```

## 特性

- ✅ 四种显示位置（top/bottom/left/right）
- ✅ 两种触发方式（hover/click）
- ✅ 支持标题和内容
- ✅ 支持枚举和字符串参数
- ✅ 明暗主题自动适配
- ✅ 自动调整位置避免超出屏幕
- ✅ 多个气泡自动互斥显示
- ✅ 点击其他区域自动隐藏
- ✅ 类型安全的枚举支持
- ✅ 自动复用实例
