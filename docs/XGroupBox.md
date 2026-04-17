# XGroupBox

分组框组件，支持自定义标题，自动适配主题切换。

## 示例

![XGroupBox示例](./images/XGroupBox.png "XGroupBox示例")

## 导入

```python
from xsideui import XGroupBox
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `title` | str | "" | 分组标题 |
| `parent` | QWidget | None | 父组件 |

## 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `setTitle(title)` | 设置分组标题 | None |
| `setEnabled(enabled)` | 设置启用/禁用状态 | None |

## 示例

```python
# 基础用法
group = XGroupBox(title="用户设置")

# 添加内容
from PySide2.QtWidgets import QVBoxLayout, QLabel
layout = QVBoxLayout(group)
layout.addWidget(QLabel("用户名：张三"))
layout.addWidget(QLabel("邮箱：zhangsan@example.com"))

# 动态修改标题
group.setTitle("新标题")

# 禁用分组框
group.setEnabled(False)

# 启用分组框
group.setEnabled(True)
```

## 特性

- ✅ 自动适配主题切换
- ✅ 圆角边框
- ✅ 自定义标题
- ✅ 禁用状态样式
- ✅ 透明背景
