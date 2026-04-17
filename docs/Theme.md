# 主题系统

高性能主题管理系统，支持明暗切换、自定义主题色和异步预加载。

## 导入

```python
from xsideui.theme import theme_manager, ThemeType, ThemeColors, ThemeConfig
```

## 主题管理器

### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `colors` | ThemeColors | 当前主题颜色 |
| `is_dark` | bool | 是否为暗色主题 |
| `theme_name` | str | 当前主题名称 |
| `theme_type` | ThemeType | 当前主题类型 |
| `fonts` | Dict | 当前主题字体配置 |
| `spacing` | Dict | 当前主题间距配置 |
| `height` | Dict | 当前主题高度配置 |
| `border_radius` | Dict | 当前主题圆角配置 |
| `radio` | Dict | 当前主题单选按钮配置 |
| `checkbox` | Dict | 当前主题复选框配置 |
| `switch` | Dict | 当前主题开关配置 |

### 方法

| 方法 | 说明 |
|------|------|
| `set_theme(theme_name)` | 设置明暗主题 |
| `toggle_theme()` | 明暗切换主题 |
| `set_primary_color(color, theme_name)` | 设置主题色 |
| `color_with_alpha(color, alpha)` | 获取带透明度的颜色 |

### 信号

| 信号 | 说明 |
|------|------|
| `theme_changed` | 主题已更改 |
| `theme_changing` | 主题正在更改 |
| `theme_preloaded` | 主题已预加载 |

## 主题类型

| 类型 | 说明 |
|------|------|
| `ThemeType.LIGHT` | 亮色主题 |
| `ThemeType.DARK` | 暗色主题 |

## 主题颜色

| 颜色 | 说明 |
|------|------|
| `primary` | 主题色 |
| `secondary` | 次要色 |
| `tertiary` | 第三色 |
| `success` | 成功色 |
| `warning` | 警告色 |
| `danger` | 危险色 |
| `link` | 链接色 |
| `text_0` | 文本色 0 |
| `text_1` | 文本色 1 |
| `text_2` | 文本色 2 |
| `text_3` | 文本色 3 |
| `text_disabled` | 禁用文本色 |
| `bg_0` | 背景色 0 |
| `bg_1` | 背景色 1 |
| `bg_2` | 背景色 2 |
| `fill` | 填充色 |
| `border` | 边框色 |
| `shadow` | 阴影色 |
| `code_keyword` | 代码关键字色 |
| `code_string` | 代码字符串色 |
| `code_comment` | 代码注释色 |
| `code_function` | 代码函数色 |
| `code_number` | 代码数字色 |
| `code_operator` | 代码操作符色 |

## 示例

```python
# 设置主题
theme_manager.set_theme("dark")

# 明暗切换
theme_manager.toggle_theme()

# 设置主题色
# 需在实例化QApplication后调用
theme_manager.set_primary_colors({
    "light": "#ab7ae0",
    "dark": "#51258f"
})

# 获取当前主题颜色
color = theme_manager.colors.primary

# 检查是否为暗色主题
if theme_manager.is_dark:
    print("当前是暗色主题")

# 获取带透明度的颜色
color_with_alpha = theme_manager.color_with_alpha("#165dff", 0.5)

# 监听主题变化
theme_manager.theme_changed.connect(lambda: print("主题已更改"))
```

## 特性

- ✅ 快速启动（只加载当前主题）
- ✅ 快速切换（全局样式表 + 异步预加载）
- ✅ 智能缓存
- ✅ 自定义主题色
- ✅ 明暗切换
- ✅ 自定义主题注册
- ✅ 主题预加载
- ✅ 透明度支持
