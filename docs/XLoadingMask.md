# XLoadingMask

加载遮罩组件，提供带旋转动画的半透明加载遮罩。

## 示例

![XLoadingMask示例](./images/XLoadingMask.png "XLoadingMask示例")

## 导入

```python
from xsideui import XLoadingMask
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `text` | str | "加载中..." | 加载提示文字 |
| `icon_size` | int | 42 | 图标大小（像素） |
| `spacing` | int | 16 | 图标和文字间距（像素） |
| `speed` | str | "fast" | 动画速度（slow/medium/fast） |
| `parent` | QWidget | None | 父组件 |

## 速度

| 速度 | 步进 | 说明 |
|------|------|------|
| slow | 3° | 慢速旋转 |
| medium | 5° | 中速旋转 |
| fast | 8° | 快速旋转 |

## 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `show_loading(parent, text, icon_size, spacing, speed)` | 显示加载遮罩（类方法） | XLoadingMask |
| `hide()` | 隐藏加载遮罩 | None |
| `set_text(text)` | 设置加载文字 | None |
| `text()` | 获取当前文字 | str |
| `set_speed(speed)` | 设置动画速度 | None |

## 示例

```python
# 基础用法
loading = XLoadingMask.show_loading(my_widget, text="正在处理...")
loading.hide()

# 自定义参数
loading = XLoadingMask.show_loading(
    parent=my_widget,
    text="加载中...",
    icon_size=48,
    spacing=20,
    speed="medium"
)

# 手动创建
loading = XLoadingMask(
    text="加载中...",
    icon_size=42,
    spacing=16,
    speed="fast",
    parent=my_widget
)
loading.show()
loading.raise_()

# 动态修改文字
loading.setText("步骤1/3")
loading.setText("步骤2/3")
loading.setText("步骤3/3")

# 切换动画速度
loading.set_speed("slow")
loading.set_speed("medium")
loading.set_speed("fast")

# 定时隐藏
from PySide2.QtCore import QTimer
loading = XLoadingMask.show_loading(my_widget, text="处理中...")
QTimer.singleShot(2000, loading.hide)

# 异步任务
from PySide2.QtCore import QThread

class Worker(QThread):
    finished = Signal()
    def run(self):
        import time
        time.sleep(3)
        self.finished.emit()

loading = XLoadingMask.show_loading(my_widget, text="处理中...")
worker = Worker()
worker.finished.connect(loading.hide)
worker.start()
```

## 特性

- ✅ 流畅的圆弧旋转动画（60fps）
- ✅ 主题色自动适配
- ✅ 可调节动画速度
- ✅ 自定义文字和图标大小
- ✅ 自动适配父组件大小
- ✅ 便捷的 API 设计
