# XCollapse

折叠面板组件，支持展开/收起动画和手风琴模式。

## 示例

![XCollapse示例](./images/XCollapse.png "XCollapse示例")

## 导入

```python
from xsideui import XCollapse, XCollapseGroup
```

## XCollapse

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `title` | str | "" | 标题文本 |
| `expanded` | bool | False | 初始是否展开 |
| `parent` | QWidget | None | 父组件 |

### 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `add_content_widget(widget)` | 添加内容组件 | None |
| `add_content_layout(layout)` | 添加内容布局 | None |
| `expand()` | 展开面板 | None |
| `collapse()` | 收起面板 | None |

### 信号

| 信号 | 说明 |
|------|------|
| `state_changed(bool)` | 展开/收起时触发，参数为展开状态 |

## XCollapseGroup

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `accordion` | bool | False | 手风琴模式（同时只能展开一个） |
| `parent` | QWidget | None | 父组件 |

### 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `add_panel(title)` | 添加新面板 | XCollapse |

## 示例

```python
# 单个面板
panel = XCollapse(title="面板标题", expanded=True)
panel.add_content_widget(XLabel("面板内容"))

# 面板组
group = XCollapseGroup()
panel1 = group.add_panel("面板 1")
panel1.add_content_widget(XLabel("内容 1"))

panel2 = group.add_panel("面板 2")
panel2.add_content_widget(XLabel("内容 2"))

# 手风琴模式
group = XCollapseGroup(accordion=True)
panel1 = group.add_panel("选项 A")
panel1.add_content_widget(XLabel("选项 A 的内容"))

panel2 = group.add_panel("选项 B")
panel2.add_content_widget(XLabel("选项 B 的内容"))

# 状态监听
panel = XCollapse(title="状态监听")
panel.state_changed.connect(lambda expanded: print(f"状态: {'展开' if expanded else '收起'}"))

# 展开和收起
panel.expand()
panel.collapse()
```

## 特性

- ✅ 平滑动画（250ms 展开/收起）
- ✅ 手风琴模式（同时只能展开一个）
- ✅ 灵活布局（支持添加任意组件和布局）
- ✅ 状态监听
