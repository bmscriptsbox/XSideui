"""XDialog Example 对话框组件示例"""
import ctypes
import sys

try:
    from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout
except ImportError:
    from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

from src.xsideui import XTableWidget, XDialog


class DemoDialog(XDialog):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.set_title("XDialog示例")
        self.set_logo(r'..\resources\logo.png')
        self.resize(800, 600)

        content_widget = QWidget()
        self.addWidget(content_widget)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        self.tab = XTableWidget()
        content_layout.addWidget(self.tab)




if __name__ == "__main__":
    if sys.platform == 'win32':
        # 确保windows任务栏能正确显示图标，字符串标识符（格式：公司名.产品名.子模块.版本号）
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('mycompany.myproduct.subelement.version')
    app = QApplication(sys.argv)
    window = DemoDialog()
    window.show()
    sys.exit(app.exec_())
