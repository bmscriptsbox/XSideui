# XListWidget

列表组件，继承自 QListWidget，支持明暗主题切换。

## 示例

![XListWidget示例](./images/XListWidget.png "XListWidget示例")

## 导入

```python
from xsideui import XListWidget
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `parent` | QWidget | None | 父组件 |

## 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `addItems(items)` | 添加多个项目 | None |
| `addItem(item)` | 添加单个项目 | None |
| `currentItem()` | 获取当前选中的项目 | QListWidgetItem |
| `currentRow()` | 获取当前选中项目的行号 | int |

## 信号

| 信号 | 说明 |
|------|------|
| `itemClicked(item)` | 项目被点击时发出 |
| `itemSelectionChanged()` | 项目选择改变时发出 |

## 示例

```python
# 基础用法
list_widget = XListWidget()
list_widget.addItems(["项目 1", "项目 2", "项目 3"])

# 添加单个项目
list_widget.addItem("新项目")

# 监听项目点击
list_widget.itemClicked.connect(lambda item: print(f"点击: {item.text()}"))

# 监听选择变化
list_widget.itemSelectionChanged.connect(lambda: print(f"选择改变"))

# 获取当前选中项目
current_item = list_widget.currentItem()
if current_item:
    print(f"当前选中: {current_item.text()}")

# 获取当前选中行号
current_row = list_widget.currentRow()
print(f"当前行号: {current_row}")
```

## 特性

- ✅ 自动适配主题切换
- ✅ 悬浮效果（鼠标悬浮时项目背景变化）
- ✅ 选中效果（项目选中时背景高亮）
- ✅ 自定义滚动条样式（极细风格）
- ✅ 默认单选模式
- ✅ 支持像素级滚动
- ✅ 无边框设计
