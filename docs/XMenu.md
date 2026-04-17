# XMenu

圆角菜单组件，支持主题适配和图标集成。

## 示例

![XMenu示例](./images/XMenu.png "XMenu示例")

## 导入

```python
from xsideui import XMenu
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `title` | str | "" | 菜单标题 |
| `parent` | QWidget | None | 父组件 |

## 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `add_action(text, icon, triggered, shortcut)` | 便捷添加菜单项 | QAction |
| `add_submenu(title, icon)` | 便捷添加子菜单 | XMenu |
| `exec_at_widget(widget, offset)` | 在指定控件下方显示菜单 | QAction |
| `addSeparator()` | 添加分隔符 | QAction |
| `addMenu(menu)` | 添加子菜单 | QAction |

## 示例

```python
# 基础用法
menu = XMenu("菜单", parent)
action1 = menu.add_action("新建")
action1.triggered.connect(lambda: print("新建"))

menu.addSeparator()

action2 = menu.add_action("保存")
action2.triggered.connect(lambda: print("保存"))

# 在按钮下方显示
menu.exec_at_widget(button)

# 带图标的菜单项
from xsideui.icon import get_icon, IconName
from xsideui.widgets import XSize, XColor

action = menu.add_action("保存")
action.setIcon(get_icon(IconName.CIRCLE_CHECK, size=XSize.SMALL, color=XColor.SUCCESS))

# 添加子菜单
submenu = menu.add_submenu("打开最近")
submenu.add_action("文件1.txt")
submenu.add_action("文件2.txt")

# 禁用菜单项
action = menu.add_action("删除")
action.setEnabled(False)

# 设置快捷键
action = menu.add_action("保存", shortcut="Ctrl+S")
```

## 特性

- ✅ 圆角设计
- ✅ 主题适配（自动适配深色/浅色主题）
- ✅ 图标支持（通过 get_icon() 添加图标）
- ✅ 分隔符（支持菜单项分组）
- ✅ 禁用状态（支持禁用菜单项）
- ✅ 悬停效果（菜单项悬停高亮）
- ✅ 子菜单（支持多级菜单）
- ✅ 快捷键（支持设置菜单项快捷键）
- ✅ 屏幕边界检查（自动调整位置避免超出屏幕）
- ✅ 便捷方法（add_action、add_submenu、exec_at_widget）
