# XPagination

分页器组件，提供完整的分页导航功能。

## 示例

![XPagination示例](./images/XPagination.png "XPagination示例")

## 导入

```python
from xsideui import XPagination
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `total` | int | 0 | 总条目数 |
| `page_size` | int | 10 | 每页显示数量 |
| `current_page` | int | 1 | 初始页码 |
| `parent` | QWidget | None | 父组件 |

## 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `page_size` | int | 每页显示数量 |
| `current_page` | int | 当前页码 |
| `total` | int | 总条目数 |
| `can_go_prev` | bool | 是否可以上一页 |
| `can_go_next` | bool | 是否可以下一页 |

## 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `get_total_pages()` | 获取总页数 | int |
| `get_page_range()` | 获取当前页数据范围 | Tuple[int, int] |
| `set_current_page(page)` | 设置当前页码 | None |
| `set_page_size(page_size)` | 设置每页数量 | None |
| `set_total(total)` | 设置总条目数 | None |
| `go_to_page(page)` | 跳转到指定页码 | None |
| `go_to_first_page()` | 跳转到第一页 | None |
| `go_to_last_page()` | 跳转到最后一页 | None |

## 信号

| 信号 | 说明 |
|------|------|
| `pageChanged(int)` | 当前页改变时发出 |
| `pageSizeChanged(int)` | 每页数量改变时发出 |
| `prevClicked(int)` | 点击上一页按钮时发出 |
| `nextClicked(int)` | 点击下一页按钮时发出 |
| `pageClicked(int)` | 点击页码按钮时发出 |
| `jumped(int)` | 输入框跳转时发出 |

## 示例

```python
# 基础用法
pagination = XPagination(total=100, page_size=10, current_page=1)

# 获取数据范围
start, end = pagination.get_page_range()
data = all_data[start:end]

# 监听页码变化
pagination.pageChanged.connect(lambda page: print(f"页码变化到：{page}"))

# 跳转到指定页
pagination.go_to_page(5)
pagination.go_to_first_page()
pagination.go_to_last_page()

# 修改每页数量
pagination.set_page_size(20)

# 更新总数
pagination.set_total(200)

# 判断是否可以翻页
if pagination.can_go_prev:
    print("可以上一页")
if pagination.can_go_next:
    print("可以下一页")

# 监听各种事件
pagination.pageChanged.connect(load_data)
pagination.prevClicked.connect(lambda page: print("上一页"))
pagination.nextClicked.connect(lambda page: print("下一页"))
pagination.pageClicked.connect(lambda page: print("点击页码"))
pagination.jumped.connect(lambda page: print("跳转页码"))
```

## 特性

- ✅ 页码导航（点击页码直接跳转）
- ✅ 导航按钮（上一页/下一页）
- ✅ 页码跳转（输入框直接输入）
- ✅ 智能省略号（页数较多时自动显示）
- ✅ 数据统计（显示总条目数）
- ✅ 主题适配（自动适配深色/浅色主题）
- ✅ 边界检查（自动限制页码范围）
- ✅ 便捷属性（can_go_prev、can_go_next）
- ✅ 便捷方法（go_to_page、go_to_first_page、go_to_last_page）
- ✅ 丰富信号（支持多种事件监听）
