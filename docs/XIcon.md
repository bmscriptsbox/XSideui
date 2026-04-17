# XIcon

高性能 SVG 图标组件，支持主题感知和链式调用。
包含约450个图标，图标来自 [Ant Design Icons 查询图标名请访问](https://ant.design/components/icon-cn/)，图标名称枚举类为 `IconName`

## 示例

![XIcon示例](./images/XIcon.png "XIcon示例")

## 导入

```python
from xsideui import XIcon, IconName, get_icon, get_pixmap, XColor, XSize
```

## XIcon 组件

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `name` | str / IconName | None | 图标名称 |
| `parent` | QWidget | None | 父组件 |
| `size` | int / XSize | None | 图标尺寸 |
| `color` | str / XColor | XColor.SECONDARY | 图标颜色 |
| `theme_aware` | bool | True | 是否启用主题感知 |
| `rotation` | float | 0 | 旋转角度（0-360） |
| `flip_h` | bool | False | 是否水平翻转 |
| `flip_v` | bool | False | 是否垂直翻转 |

### 类方法

| 方法 | 说明                   | 返回值   |
|------|----------------------|-------|
| `get(name, size, color)` | 获取图标实例（带内部缓存）        | XIcon |
| `add_resource_path(prefix)` | 添加自定义图标资源前缀(用于自定义图标) | None  |

### 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `set_name(name)` | 设置图标名称 | self |
| `set_size(size)` | 设置图标尺寸 | self |
| `set_color(color)` | 设置图标颜色 | self |
| `set_theme_aware(enabled)` | 设置主题感知 | self |
| `set_rotation(rotation)` | 设置旋转角度 | self |
| `set_flip_h(flip)` | 设置水平翻转 | self |
| `set_flip_v(flip)` | 设置垂直翻转 | self |
| `with_name(name)` | 链式设置图标名称 | self |
| `with_size(size)` | 链式设置图标尺寸 | self |
| `with_color(color)` | 链式设置图标颜色 | self |
| `with_theme_aware(enabled)` | 链式设置主题感知 | self |
| `with_rotate(degrees)` | 链式设置旋转角度 | self |
| `with_flip_h(flip)` | 链式设置水平翻转 | self |
| `with_flip_v(flip)` | 链式设置垂直翻转 | self |
| `with_primary()` | 链式设置主题色 | self |
| `with_success()` | 链式设置成功色 | self |
| `with_warning()` | 链式设置警告色 | self |
| `with_danger()` | 链式设置危险色 | self |
| `with_secondary()` | 链式设置次要色 | self |
| `with_mini()` | 链式设置最小尺寸 | self |
| `with_small()` | 链式设置小尺寸 | self |
| `with_large()` | 链式设置大尺寸 | self |
| `with_default()` | 链式设置默认尺寸 | self |
| `pixmap()` | 获取 QPixmap | QPixmap |
| `icon()` | 获取 QIcon | QIcon |

预加载图标到缓存。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `names` | list | - | 图标名称列表 |
| `sizes` | list | [16, 24, 32, 48] | 尺寸列表 |
| `colors` | list | None | 颜色列表 |
| `theme_aware` | bool | True | 是否启用主题感知 |

### `clear_icon_cache()`

清理图标缓存。

### `get_icon_names() -> list`

获取所有已加载的图标名称。

### `search_icons(keyword) -> list`

搜索图标。

### `has_icon(name) -> bool`

检查图标是否存在。

## 示例

```python
"""获取图标QIcon/pixmap的推荐方式  XIcon.get()"""
icon = XIcon.get(IconName.SETTING, size=24, color=XColor.PRIMARY).icon()
pixmap = XIcon.get(IconName.SETTING, size=24, color=XColor.PRIMARY).pixmap()
btn.setIcon(icon)
label.setIcon(pixmap)
# 链式调用
icon = XIcon.get(IconName.CHECK).with_size(32).with_color(XColor.SUCCESS).icon()


"""
自定义图标的使用方法

# 先导入自定义的图标资源（*_rc.py）
# 再添加自定义资源文件中的前缀
# 自定义图标名无法从IconName枚举中获取、直接使用原图标名从XIcon中统一获取即可
# 自定义的优先级大于组件库自带的图标,如存在同名图标会优先使用自定义的图标
"""
from example import custom_rc  # 导入自定义资源
from xsideui import XIcon

XIcon.add_resource_path(':/custom/')  # 添加资源前缀
icon = XIcon.get('custom_icon_name', size=24, color=XColor.PRIMARY).icon()  # 使用自定义图标



# 预加载图标
preload_icons(["add", "edit", "delete", "search"])

# 搜索图标
results = search_icons("add")

# 检查图标是否存在
if has_icon("settings"):
    print("图标存在")

# 清理缓存
clear_icon_cache()

# 获取所有图标名称
all_names = get_icon_names()
print(f"共有 {len(all_names)} 个图标")
```

## 特性

- ✅ 高效渲染（基于缓存）
- ✅ 主题感知
- ✅ 链式调用
- ✅ 自定义颜色
- ✅ 尺寸变换
- ✅ 旋转和翻转
- ✅ 图标名称枚举
- ✅ 快捷函数
- ✅ 内部缓存（XIcon.get()）
- ✅ QIcon 对象DPI 适配

## 鸣谢

组件的 SVG 图标文件来自 [IconPark](https://github.com/bytedance/iconpark) 开源图标库，感谢 IconPark 团队的优秀贡献！
