# XDialog

无边框 Dialog 窗口容器组件，支持拖拽移动、调整大小和阴影效果。
该组件不建议作为主窗口使用，建议作为模态窗口使用。

## 示例

![XDialog示例](./images/XDialog.png "XDialog示例")

## 导入

```python
from xsideui import XDialog
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `title` | str | "XDialog" | 窗口标题 |
| `logo` | str / QIcon | None | 窗口图标（路径或 QIcon 对象） |
| `show_close` | bool | True | 是否显示关闭按钮 |
| `parent` | QWidget | None | 父组件 |

## 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `addWidget(widget)` | 添加组件到内容区域 | self |
| `addLayout(layout)` | 添加布局到内容区域 | self |
| `set_title(title)` | 设置窗口标题 | self |
| `set_logo(icon)` | 设置窗口图标 | self |
| `hide_title_bar()` | 隐藏标题栏 | self |
| `hide_minimize_button()` | 隐藏最小化按钮 | self |
| `hide_maximize_button()` | 隐藏最大化按钮 | self |
| `hide_theme_button()` | 隐藏主题切换按钮 | self |

## 示例

```python
# 基础使用
dialog = XDialog(title="设置", parent=parent)
dialog.addWidget(XLabel("这是对话框内容"))
dialog.exec_()

# 带图标的对话框
from xsideui import XIcon, IconName
dialog = XDialog(
    title="系统设置",
    logo=XIcon.get(IconName.SETTING, size=20, color="primary").icon(),
    parent=parent
)
dialog.addWidget(XLabel("设置内容"))
dialog.exec_()

# 链式调用
dialog = (XDialog(title="用户信息", parent=parent)
    .addWidget(XLabel("姓名：张三"))
    .addWidget(XLabel("年龄：25"))
    .addWidget(XPushButton("确定")))

# 添加自定义布局
from PySide2.QtWidgets import QFormLayout

form_layout = QFormLayout()
form_layout.addRow("姓名：", XLineEdit(placeholder="请输入姓名"))
form_layout.addRow("邮箱：", XLineEdit(placeholder="请输入邮箱"))
form_layout.addRow("电话：", XLineEdit(placeholder="请输入电话"))

dialog = XDialog(title="填写信息", parent=parent)
dialog.addLayout(form_layout)
dialog.exec_()

# 隐藏标题栏按钮
dialog = XDialog(title="提示", show_close=False, parent=parent)
dialog.addWidget(XLabel("这是一个没有关闭按钮的对话框"))
dialog.hide_title_bar()
dialog.exec_()

# 组合使用多个组件
dialog = XDialog(title="登录", parent=parent)

content_widget = QWidget()
content_layout = QVBoxLayout(content_widget)

username_input = XLineEdit(placeholder="请输入用户名")
password_input = XLineEdit(placeholder="请输入密码", echo_mode=2)
login_button = XPushButton("登录")

content_layout.addWidget(username_input)
content_layout.addWidget(password_input)
content_layout.addWidget(login_button)

dialog.addWidget(content_widget)
dialog.exec_()

# 获取用户输入
dialog = XDialog(title="登录", parent=parent)

username_input = XLineEdit(placeholder="请输入用户名")
password_input = XLineEdit(placeholder="请输入密码", echo_mode=2)
login_button = XPushButton("登录")

dialog.addWidget(username_input)
dialog.addWidget(password_input)
dialog.addWidget(login_button)

if dialog.exec_() == QDialog.Accepted:
    print(f"用户名: {username_input.text()}")
    print(f"密码: {password_input.text()}")
```

## 特性

- ✅ 无边框设计，现代化外观
- ✅ 支持拖拽移动窗口
- ✅ 支持调整窗口大小
- ✅ 优雅的阴影效果
- ✅ 标题栏支持图标和标题
- ✅ 自动居中显示
- ✅ 支持链式调用
- ✅ 灵活的内容区域
- ✅ 可隐藏标题栏按钮
- ✅ 兼容 PySide2 和 PySide6

## 注意事项

1. **窗口拖拽**：按住标题栏可以拖拽移动窗口
2. **调整大小**：窗口四角可以调整窗口大小
3. **居中显示**：窗口会自动在父组件中居中显示
4. **阴影优化**：调整窗口大小时会暂时移除阴影效果以提高性能
5. **关闭按钮**：默认显示关闭按钮，可通过 `show_close=False` 隐藏
