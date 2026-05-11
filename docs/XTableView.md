# XTableView

基于 Qt Model/View 架构的高性能表格视图组件，继承自 QTableView，支持自定义委托和灵活的数据管理。

## 示例

![XTableView示例](./images/XTableView.png "XTableView示例")

## 导入

```python
from xsideui import XTableView
from PySide6.QtWidgets import QAbstractItemView  # 用于选择模式
from PySide6.QtGui import QStandardItemModel, QStandardItem  # 用于数据模型
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `show_border` | bool | True | 是否显示边框 |
| `selection_mode` | SelectionMode | SelectRows | 选择模式 |
| `selection_behavior` | SelectionBehavior | SelectRows | 选择行为 |
| `show_alternating_colors` | bool | False | 是否显示交替行颜色 |
| `row_height` | int | 40 | 行高（像素） |
| `parent` | QWidget | None | 父组件 |

## 样式类型

```python
from xsideui import XTableView

# 可选样式
XTableView.Style.DEFAULT   # 默认样式
XTableView.Style.STRIPED   # 斑马纹样式
```

## 选择模式

```python
from PySide6.QtWidgets import QAbstractItemView

# 选择模式
QAbstractItemView.SingleSelection      # 单选
QAbstractItemView.MultiSelection       # 多选
QAbstractItemView.ExtendedSelection    # 扩展选择（默认）
QAbstractItemView.ContiguousSelection  # 连续选择
QAbstractItemView.NoSelection          # 禁止选择

# 选择行为
QAbstractItemView.SelectItems          # 按单元格选择
QAbstractItemView.SelectRows           # 按行选择（默认）
QAbstractItemView.SelectColumns        # 按列选择
```

## 方法

### 样式相关

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `set_show_border(show)` | 设置是否显示边框 | self |
| `show_border()` | 获取边框显示状态 | bool |
| `set_style_type(style)` | 设置样式类型（default/striped） | self |
| `style_type()` | 获取当前样式类型 | Style |
| `set_alternating_row_colors(enabled)` | 设置交替行颜色 | self |
| `is_alternating_row_colors()` | 获取交替行颜色状态 | bool |

### 选择相关

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `set_selection_mode(mode)` | 设置选择模式 | self |
| `selection_mode()` | 获取当前选择模式 | SelectionMode |
| `set_selection_behavior(behavior)` | 设置选择行为 | self |
| `selection_behavior()` | 获取当前选择行为 | SelectionBehavior |
| `clear_selection()` | 清空所有选择 | self |
| `select_all()` | 选择所有项 | self |
| `get_selected_rows()` | 获取选中行索引列表 | list |
| `get_selected_indexes()` | 获取所有选中索引 | list |

### 布局相关

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `set_row_height(height)` | 设置行高 | self |
| `row_height()` | 获取当前行高 | int |
| `set_column_width(column, width)` | 设置指定列宽 | self |
| `set_column_widths(widths)` | 批量设置列宽 | self |
| `auto_resize_columns(mode)` | 自动调整列宽 | self |
| `hide_row(row)` | 隐藏指定行 | self |
| `show_row(row)` | 显示指定行 | self |
| `hide_column(column)` | 隐藏指定列 | self |
| `show_column(column)` | 显示指定列 | self |

### 功能相关

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `set_sorting_enabled(enabled)` | 设置是否启用排序 | self |
| `is_sorting_enabled()` | 获取排序启用状态 | bool |
| `set_edit_triggers(triggers)` | 设置编辑触发方式 | self |
| `set_grid_visible(visible)` | 设置网格线可见性 | self |
| `get_current_index()` | 获取当前焦点索引 | QModelIndex |

## 信号

继承自 QTableView 的常用信号：

| 信号 | 说明 |
|------|------|
| `clicked(index)` | 单元格被点击时发出 |
| `doubleClicked(index)` | 单元格被双击时发出 |
| `activated(index)` | 单元格被激活时发出 |
| `entered(index)` | 鼠标进入单元格时发出 |
| `pressed(index)` | 单元格被按下时发出 |

## 示例

### 基础用法

```python
from xsideui import XTableView
from PySide6.QtGui import QStandardItemModel, QStandardItem

# 创建表格视图
table = XTableView()

# 创建模型
model = QStandardItemModel()
model.setHorizontalHeaderLabels(["ID", "姓名", "部门"])

# 添加数据
data = [
    ["001", "张三", "技术部"],
    ["002", "李四", "产品部"],
    ["003", "王五", "设计部"],
]

for row_data in data:
    items = [QStandardItem(text) for text in row_data]
    model.appendRow(items)

# 设置模型
table.setModel(model)

# 设置列宽
table.set_column_widths([60, 100, 120])

# 监听点击
table.clicked.connect(lambda index: print(f"点击: {index.data()}"))
```

### 斑马纹样式

```python
from xsideui import XTableView, XTableView

table = XTableView(show_border=True)

# 设置为斑马纹样式
table.set_style_type(XTableView.Style.STRIPED)

# 或者使用字符串
table.set_style_type("striped")
```

### 按列排序

```python
from xsideui import XTableView

table = XTableView()

# 启用排序（默认启用）
table.set_sorting_enabled(True)

# 禁用排序
table.set_sorting_enabled(False)
```

### 动态操作

```python
from xsideui import XTableView
from PySide6.QtGui import QStandardItemModel, QStandardItem

table = XTableView()
model = QStandardItemModel()
table.setModel(model)

# 添加行
def add_row(data):
    items = [QStandardItem(str(text)) for text in data]
    model.appendRow(items)

# 删除选中行
def delete_selected_rows():
    indexes = table.get_selected_rows()
    for index in sorted(indexes, reverse=True):
        model.removeRow(index.row())

# 隐藏/显示列
table.hide_column(0)   # 隐藏第一列
table.show_column(0)   # 显示第一列
```

### 选择监听

```python
from xsideui import XTableView
from PySide6.QtWidgets import QAbstractItemView

table = XTableView(
    selection_mode=QAbstractItemView.ExtendedSelection,
    selection_behavior=QAbstractItemView.SelectRows
)

# 监听选择变化
table.selectionModel().selectionChanged.connect(
    lambda selected, deselected: print("选择变化")
)

# 获取所有选中的行数据
def get_selected_data():
    rows = table.get_selected_rows()
    result = []
    for idx in rows:
        row_data = []
        for col in range(table.model().columnCount()):
            row_data.append(idx.sibling(idx.row(), col).data())
        result.append(row_data)
    return result
```

## XTableView vs XTableWidget

| 特性 | XTableWidget | XTableView |
|------|-------------|-----------|
| 架构 | 数据+视图耦合 | Model/View 分离 |
| 复杂度 | 简单易用 | 需要更多代码 |
| 性能 | 一般 | 更优（适合大数据） |
| 自定义 | 受限 | 完全自定义 |
| 共享数据 | 不支持 | 支持（多个视图共享同一模型） |
| 适用场景 | 简单表格 | 复杂表格、大数据 |

### 选择建议

- **用 XTableWidget**：表格简单（<100行），快速开发
- **用 XTableView**：需要高性能、自定义样式、大数据量、多视图联动

## 特性

- ✅ Model/View 架构分离
- ✅ 属性驱动样式（QSS）
- ✅ 自动适配主题切换
- ✅ 支持链式调用 API
- ✅ 多种选择模式和行為
- ✅ 内置排序功能
- ✅ 可选交替行颜色
- ✅ 两种样式（默认/斑马纹）
- ✅ 行列显示/隐藏
- ✅ 列宽自动调整
- ✅ 网格线控制
- ✅ 单元格编辑控制
