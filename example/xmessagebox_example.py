"""
XMessageBox Example 消息框组件示例
"""
import sys
try:
    from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout
except ImportError:
    from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QMessageBox, QDialog

from src.xsideui import XLabel, XPushButton, XMessageBox, XLineEdit, XWidget, XDivider, XSize


class XMessageBoxDemo(XWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self.set_title("XMessageBox Demo")
        self.resize(600,600)

        content_widget = QWidget()
        self.addWidget(content_widget)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        content_layout.addWidget(XLabel('对话框'))
        content_layout.addWidget(XDivider())

        btn_info = XPushButton('常规对话框')
        btn_info.clicked.connect(lambda: XMessageBox.information(self, "信息提示", "这是一个信息提示框。"))
        content_layout.addWidget(btn_info)

        btn_ask = XPushButton('询问对话框')
        btn_ask.clicked.connect(self._ask)
        content_layout.addWidget(btn_ask)

        btn_form = XPushButton('自定义表单对话框')
        btn_form.clicked.connect(self._form)
        content_layout.addWidget(btn_form)



    def _ask(self):
        result = XMessageBox.ask(self, "确认操作", "您确定要执行此操作吗？")
        print(f"用户选择: {'确定' if result else '取消'}")

    def _form(self):
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        name_input = XLineEdit(size=XSize.SMALL, placeholder="请输入姓名...")
        email_input = XLineEdit(size=XSize.SMALL, placeholder="请输入邮箱...")

        form_layout.addRow(XLabel('姓名:'), name_input)
        form_layout.addRow(XLabel('邮箱:'), email_input)

        def on_confirm(msg_box):
            print(f"姓名: {name_input.text()}, 邮箱: {email_input.text()}")

        XMessageBox.information(self, "填写信息", "请填写以下信息：", layout=form_layout, on_confirm=on_confirm)









if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = XMessageBoxDemo()
    demo.show()
    sys.exit(app.exec_())
