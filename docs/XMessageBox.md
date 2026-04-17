# XMessageBox

消息框组件，支持明暗切换，自定义组件和回调函数。

## 示例

![XMessageBox示例](./images/XMessageBox.png "XMessageBox示例")

## 导入

```python
from xsideui import XMessageBox
```

## 静态方法

### `information(parent, title, text, widget=None, layout=None, on_confirm=None)`

显示信息提示框。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `parent` | QWidget | None | 父组件 |
| `title` | str | - | 消息框标题 |
| `text` | str | - | 消息文本内容 |
| `widget` | QWidget | None | 自定义组件 |
| `layout` | QLayout | None | 自定义布局 |
| `on_confirm` | callable | None | 确定按钮回调函数 |

### `ask(parent, title, text, widget=None, layout=None, on_confirm=None) -> bool`

显示询问对话框。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `parent` | QWidget | None | 父组件 |
| `title` | str | - | 消息框标题 |
| `text` | str | - | 消息文本内容 |
| `widget` | QWidget | None | 自定义组件 |
| `layout` | QLayout | None | 自定义布局 |
| `on_confirm` | callable | None | 确定按钮回调函数 |

**返回值：** `True` 表示确定，`False` 表示取消

## 实例方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `add_custom_widget(widget)` | 添加自定义组件 | self |
| `add_custom_layout(layout)` | 添加自定义布局 | self |
| `set_on_confirm(callback)` | 设置确定按钮的回调函数 | self |

## 示例

```python
# 信息提示框
XMessageBox.information(parent, "操作成功", "您的操作已成功完成！")

# 询问对话框
result = XMessageBox.ask(parent, "删除确认", "确定要删除此项目吗？")
if result:
    print("用户确认删除")

# 带输入框的消息框
input_field = XLineEdit(placeholder="请输入内容...")

def on_confirm(msg_box):
    print(f"用户输入: {input_field.text()}")

XMessageBox.information(
    parent,
    "输入信息",
    "请输入信息：",
    widget=input_field,
    on_confirm=on_confirm
)

# 带开关组件的消息框
switch = XSwitch()
switch.setChecked(True)

def on_confirm(msg_box):
    print(f"开关状态: {switch.isChecked()}")

XMessageBox.information(
    parent,
    "开关设置",
    "请设置开关状态：",
    widget=switch,
    on_confirm=on_confirm
)

# 带表单布局的消息框
from PySide2.QtWidgets import QFormLayout

form_layout = QFormLayout()
name_input = XLineEdit(placeholder="请输入姓名...")
email_input = XLineEdit(placeholder="请输入邮箱...")

form_layout.addRow("姓名：", name_input)
form_layout.addRow("邮箱：", email_input)

def on_confirm(msg_box):
    print(f"姓名: {name_input.text()}, 邮箱: {email_input.text()}")

XMessageBox.information(
    parent,
    "填写信息",
    "请填写以下信息：",
    layout=form_layout,
    on_confirm=on_confirm
)

# 使用实例方法
msg_box = XMessageBox("标题", "内容", parent)
msg_box.add_custom_widget(XLineEdit()).add_custom_widget(XSwitch())
msg_box.exec_()
```

## 特性

- ✅ 信息提示框和询问对话框
- ✅ 支持自定义组件和布局
- ✅ 支持回调函数获取表单数据
- ✅ 文本可选择，方便复制
- ✅ 自动换行显示长文本
- ✅ 自动适配主题
