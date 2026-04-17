"""
XWidget 组件使用示例
展示基础容器组件如何自动适配明暗主题切换
"""
import ctypes
import sys
try:
    from PySide2.QtWidgets import QApplication
except ImportError:
    from PySide6.QtWidgets import QApplication

from src.xsideui import XWidget


class ExampleWidget(XWidget):
    """示例容器组件"""
    def __init__(self, parent=None):
        super().__init__()
        self._init_ui()
        
    def _init_ui(self):
        """初始化 UI"""
        self.set_title('XWidget Demo')
        self.resize(600, 400)
        self.set_logo(r'..\resources\logo.png')

        
if __name__ == "__main__":
    if sys.platform == 'win32':
        # 确保windows任务栏能正确显示图标，字符串标识符（格式：公司名.产品名.子模块.版本号）
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('mycompany.myproduct.subelement.version')
    app = QApplication(sys.argv)
    window = ExampleWidget()
    window.show()
    sys.exit(app.exec_())


