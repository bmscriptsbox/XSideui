"""
XWidget 组件使用示例
展示基础容器组件如何自动适配明暗主题切换
"""
import ctypes
import sys
try:
    from PySide2.QtWidgets import QApplication, QFrame, QVBoxLayout
    from PySide2.QtGui import Qt
except ImportError:
    from PySide6.QtWidgets import QApplication, QFrame, QVBoxLayout
    from PySide6.QtGui import Qt

from xsideui import XImage, XIcon, IconName, XColor, XWidget, XLabel

class ExampleWidget(XWidget):
    """示例容器组件"""
    def __init__(self):
        super().__init__()
        self._init_ui()
        
    def _init_ui(self):
        """初始化 UI"""
        self.set_title('XWidget Demo')
        self.resize(600, 400)
        self.set_logo(r'..\resources\logo.png')

        context_widget = QFrame()
        layout = QVBoxLayout(context_widget)
        layout.setContentsMargins(20,100,20,20)
        self.addWidget(context_widget)
        layout.addWidget(XImage(source=XIcon.get(name=IconName.XSIDEUI,color=XColor.PRIMARY, size=128).pixmap(), min_height=128))
        layout.addStretch()
        layout.addWidget(XLabel('xsideui 原生无边框阴影窗口演示').set_font_size(16), alignment=Qt.AlignCenter)
        layout.addWidget(XLabel('带windows动画，支持pyside2/pyside6').set_font_size(16), alignment=Qt.AlignCenter)

if __name__ == "__main__":
    if sys.platform == 'win32':
        # 确保windows任务栏能正确显示图标，字符串标识符（格式：公司名.产品名.子模块.版本号）
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('mycompany.myproduct.subelement.version')
    app = QApplication(sys.argv)
    window = ExampleWidget()
    window.show()
    sys.exit(app.exec_())


