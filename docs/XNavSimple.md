# XNavSimple

简单高效的导航栏组件，支持主题切换、图标缓存、悬停提示等功能。

## 示例
![XNavSimple示例](./images/XNavSimple.png "XNavSimple示例")


## 导入

```python
from xsideui import XNavSimple
from xsideui.icon import IconName
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `icon_size` | int | 22 | 导航项图标尺寸（像素） |
| `parent` | QWidget | None | 父组件 |

## 位置

| 位置 | 字符串值 | 说明 |
|------|----------|------|
| 顶部 | "top" | 主要导航区域 |
| 底部 | "bottom" | 辅助功能区域 |

## 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `add_item(item_id, icon_name, text, position)` | 添加导航项 | self（支持链式调用） |
| `set_current_item(item_id)` | 设置当前选中项 | None |
| `current_item()` | 获取当前选中项 ID | str 或 None |

## 信号

| 信号 | 参数 | 说明 |
|------|------|------|
| `changed` | item_id (str) | 导航项切换时发送 |

## 示例

```python
# 基础用法
navbar = XNavSimple()
navbar.add_item("home", icon_name=IconName.HOME_FILLED, text="首页")
navbar.add_item("settings", icon_name="settings", text="设置", position="bottom")

# 监听切换事件
navbar.changed.connect(lambda item_id: print(f"切换到: {item_id}"))

# 链式调用
navbar = XNavSimple()
navbar.add_item("home", icon_name=IconName.HOME_FILLED, text="首页") \
       .add_item("dashboard", icon_name="dashboard", text="仪表盘") \
       .add_item("settings", icon_name="settings", text="设置", position="bottom")

# 页面切换
from PySide2.QtWidgets import QStackedWidget

navbar = XNavSimple()
stacked_widget = QStackedWidget()

# 创建页面
home_page = QWidget()
dashboard_page = QWidget()
settings_page = QWidget()

stacked_widget.addWidget(home_page)
stacked_widget.addWidget(dashboard_page)
stacked_widget.addWidget(settings_page)

# 添加导航项
navbar.add_item("home", icon_name=IconName.HOME_FILLED, text="首页")
navbar.add_item("dashboard", icon_name="dashboard", text="仪表盘")
navbar.add_item("settings", icon_name="settings", text="设置", position="bottom")

# 页面映射
page_map = {"home": 0, "dashboard": 1, "settings": 2}

# 监听切换事件
def on_nav_changed(item_id):
    if item_id in page_map:
        stacked_widget.setCurrentIndex(page_map[item_id])

navbar.changed.connect(on_nav_changed)

# 设置默认选中
navbar.set_current_item("home")

# 自定义图标尺寸
navbar = XNavSimple(icon_size=28)
navbar.add_item("home", icon_name="home", text="首页")
navbar.add_item("dashboard", icon_name="dashboard", text="仪表盘")

# 修改导航栏宽度
navbar.setFixedWidth(60)

# 禁用某个导航项
item = navbar._items["settings"]
item.setEnabled(False)

# 隐藏某个导航项
item = navbar._items["settings"]
item.setVisible(False)
```

## 特性

- ✅ 主题适配（自动适配深色/浅色主题）
- ✅ 图标缓存（高效缓存，提升性能）
- ✅ 悬停提示（鼠标悬停显示文本）
- ✅ 选中指示（左侧指示条展示选中状态）
- ✅ 上下布局（支持顶部和底部两个区域）
- ✅ 链式调用（支持流畅的 API 调用）
