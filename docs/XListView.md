# XListView

基于 Qt Model/View 架构的高性能列表视图组件，继承自 QListView，支持自定义委托和灵活的数据管理。

## 示例

![XListView示例](./images/XListView.png "XListView示例")

## 导入

```python
from xsideui import XListView
from PySide6.QtWidgets import QAbstractItemView  # 用于选择模式
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `show_border` | bool | True | 是否显示边框 |
| `selection_mode` | SelectionMode | SingleSelection | 选择模式 |
| `drag_enabled` | bool | False | 是否启用拖拽 |
| `show_alternating_colors` | bool | False | 是否显示交替行颜色 |
| `parent` | QWidget | None | 父组件 |

## 选择模式

```python
from PySide6.QtWidgets import QAbstractItemView

# 可选值
QAbstractItemView.SingleSelection      # 单选
QAbstractItemView.MultiSelection       # 多选（点击切换）
QAbstractItemView.ExtendedSelection    # 扩展选择（Ctrl/Shift）
QAbstractItemView.ContiguousSelection  # 连续选择
QAbstractItemView.NoSelection          # 禁止选择
```

## 方法

### 样式相关

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `set_show_border(show)` | 设置是否显示边框 | self |
| `show_border()` | 获取边框显示状态 | bool |
| `set_alternating_row_colors(enabled)` | 设置交替行颜色 | self |
| `is_alternating_row_colors()` | 获取交替行颜色状态 | bool |

### 选择相关

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `set_selection_mode(mode)` | 设置选择模式 | self |
| `selection_mode()` | 获取当前选择模式 | SelectionMode |
| `clear_selection()` | 清空所有选择 | self |
| `select_all()` | 选择所有项 | self |

### 拖拽相关

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `set_drag_enabled(enabled)` | 设置是否启用拖拽 | self |
| `is_drag_enabled()` | 获取拖拽启用状态 | bool |

### 布局相关

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `set_grid_size(width, height)` | 设置网格尺寸 | self |
| `set_icon_size(width, height)` | 设置图标大小 | self |
| `set_view_mode(mode)` | 设置视图模式（list/icon） | self |
| `set_resize_mode(mode)` | 设置调整模式（fixed/adjust） | self |
| `set_word_wrap(wrap)` | 设置自动换行 | self |

## 信号

继承自 QListView 的常用信号：

| 信号 | 说明 |
|------|------|
| `clicked(index)` | 项目被点击时发出 |
| `doubleClicked(index)` | 项目被双击时发出 |
| `activated(index)` | 项目被激活时发出 |
| `selectedIndexes()` | 获取所有选中的索引 |

## 示例

### 基础用法

```python
from xsideui import XListView
from PySide6.QtGui import QStandardItemModel, QStandardItem

# 创建视图
list_view = XListView()

# 创建模型
model = QStandardItemModel()
for i, text in enumerate(["项目 1", "项目 2", "项目 3"]):
    item = QStandardItem(text)
    item.setEditable(False)  # 只读
    model.appendRow(item)

# 设置模型
list_view.setModel(model)

# 监听点击
list_view.clicked.connect(lambda index: print(f"点击: {index.data()}"))
```

### 带图标和子标题的列表

```python
from xsideui import XListView, XIcon, IconName
from PySide6.QtGui import QStandardItemModel, QStandardItem

list_view = XListView()
model = QStandardItemModel()

# 添加带图标的项
items_data = [
    {"title": "文档", "subtitle": "10 个文件", "icon": IconName.FILE},
    {"title": "图片", "subtitle": "25 张照片", "icon": IconName.IMAGE},
    {"title": "视频", "subtitle": "5 个视频", "icon": IconName.VIDEO},
]

for data in items_data:
    item = QStandardItem()
    item.setText(data["title"])
    item.setEditable(False)
    # 可通过 setData 存储额外信息
    item.setData(data["subtitle"], Qt.UserRole + 1)
    model.appendRow(item)

list_view.setModel(model)
list_view.set_icon_size(20)
```

### 高级用法 - 扩展选择模式

```python
from xsideui import XListView
from PySide6.QtWidgets import QAbstractItemView

list_view = XListView(
    show_border=True,
    selection_mode=QAbstractItemView.ExtendedSelection,  # 支持 Ctrl/Shift 多选
    show_alternating_colors=True
)

# 获取选中的项
def get_selected_items():
    indexes = list_view.selectedIndexes()
    return [index.data() for index in indexes]

# 监听选择变化
list_view.selectionModel().selectionChanged.connect(
    lambda: print(f"已选择: {get_selected_items()}")
)
```

### 动态添加/删除项

```python
from xsideui import XListView
from PySide6.QtGui import QStandardItemModel, QStandardItem

list_view = XListView()
model = QStandardItemModel()
list_view.setModel(model)

def add_item(text):
    item = QStandardItem(text)
    item.setEditable(False)
    model.appendRow(item)

def remove_selected():
    indexes = list_view.selectedIndexes()
    for index in indexes:
        model.removeRow(index.row())

# 添加
add_item("新项目 1")
add_item("新项目 2")

# 删除选中项
remove_selected()
```

## XListView vs XListWidget

| 特性 | XListWidget | XListView |
|------|-------------|-----------|
| 架构 | 数据+视图耦合 | Model/View 分离 |
| 复杂度 | 简单易用 | 需要更多代码 |
| 性能 | 一般 | 更优（适合大数据） |
| 自定义 | 受限 | 完全自定义 |
| 适用场景 | 简单列表 | 复杂列表、大数据 |

### 选择建议

- **用 XListWidget**：列表项简单（<100条），快速开发
- **用 XListView**：需要高性能、自定义样式、多视图共享数据

## 特性

- ✅ Model/View 架构分离
- ✅ 属性驱动样式（QSS）
- ✅ 自动适配主题切换
- ✅ 支持链式调用 API
- ✅ 多种选择模式
- ✅ 可选交替行颜色
- ✅ 像素级平滑滚动
- ✅ 可选边框显示
- ✅ 拖拽支持
