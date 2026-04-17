# XNavTree

继承 QTreeWidget 的树形导航菜单，支持多级菜单、图标显示和主题适配。

## 示例

![XNavTree示例](./images/XNavTree.png "XNavTree示例")

## 导入

```python
from xsideui import XNavTree
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `indent` | int | 16 | 子项缩进（像素） |
| `icon_size` | int | 16 | 图标大小（像素） |
| `text_size` | int | 13 | 文本大小（像素） |
| `parent` | QWidget | None | 父组件 |

## 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `add_item_batch(items)` | 批量添加导航项 | XNavTree |
| `set_current_id(item_id)` | 设置当前选中的导航项 | None |

## 信号

| 信号 | 说明 |
|------|------|
| `changed(str)` | 导航项切换时发出，参数为 item_id |

## 示例

```python
# 基础用法
nav_tree = XNavTree()

menu_items = [
    {'icon': 'home', 'text': '首页', 'id': 'home'},
    {'icon': 'dashboard', 'text': '仪表盘', 'id': 'dashboard'},
    {'icon': 'settings', 'text': '设置', 'id': 'settings'}
]

nav_tree.add_item_batch(menu_items)

# 监听切换事件
nav_tree.changed.connect(lambda item_id: print(f"切换到: {item_id}"))

# 设置默认选中
nav_tree.set_current_id('home')
```

```python
# 多级菜单
menu_items = [
    {
        'icon': 'home',
        'text': '首页',
        'id': 'home'
    },
    {
        'icon': 'settings',
        'text': '系统设置',
        'children': [
            {'icon': 'user', 'text': '用户管理', 'id': 'user_management'},
            {'icon': 'lock', 'text': '权限管理', 'id': 'permission_management'}
        ]
    }
]

nav_tree.add_item_batch(menu_items)
```

```python
# 使用 IconName 枚举
from xsideui.icon import IconName

menu_items = [
    {'icon': IconName.HOME_FILLED, 'text': '首页', 'id': 'home'},
    {'icon': IconName.DASHBOARD, 'text': '仪表盘', 'id': 'dashboard'}
]

nav_tree.add_item_batch(menu_items)
```

```python
# 页面切换
from PySide2.QtWidgets import QStackedWidget

nav_tree = XNavTree()
stacked_widget = QStackedWidget()

# 创建页面
home_page = QWidget()
dashboard_page = QWidget()
settings_page = QWidget()

stacked_widget.addWidget(home_page)
stacked_widget.addWidget(dashboard_page)
stacked_widget.addWidget(settings_page)

# 添加菜单项
menu_items = [
    {'icon': 'home', 'text': '首页', 'id': 'home'},
    {'icon': 'dashboard', 'text': '仪表盘', 'id': 'dashboard'},
    {'icon': 'settings', 'text': '设置', 'id': 'settings'}
]

nav_tree.add_item_batch(menu_items)

# 页面映射
page_map = {'home': 0, 'dashboard': 1, 'settings': 2}

# 监听切换事件
def on_nav_changed(item_id):
    if item_id in page_map:
        stacked_widget.setCurrentIndex(page_map[item_id])

nav_tree.changed.connect(on_nav_changed)

# 设置默认选中
nav_tree.set_current_id('home')
```

```python
# 自定义尺寸
nav_tree = XNavTree(
    indent=20,
    icon_size=20,
    text_size=14
)

menu_items = [
    {'icon': 'home', 'text': '首页', 'id': 'home'}
]

nav_tree.add_item_batch(menu_items)
```

## 菜单项格式

```python
{
    'icon': Union[str, IconName],  # 图标名称（支持字符串或枚举）
    'text': str,                   # 显示文本（必填）
    'id': str,                     # 项目 ID（可选）
    'children': list               # 子菜单列表（可选）
}
```

## 特性

- ✅ 多级菜单 - 支持无限层级嵌套
- ✅ 图标显示 - 支持图标和颜色变化
- ✅ 悬停效果 - 鼠标悬停高亮
- ✅ 选中状态 - 左侧指示条展示
- ✅ 主题适配 - 自动适配深色/浅色主题
- ✅ 图标缓存 - 高效缓存，提升性能
- ✅ 自定义绘制 - 使用 Delegate 完全控制渲染
- ✅ 支持链式调用 - add_item_batch 返回 self
