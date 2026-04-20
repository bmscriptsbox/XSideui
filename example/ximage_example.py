"""
XImage 组件使用示例
展示图片组件如何自动适配明暗主题切换
"""

import sys


try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget, QHBoxLayout
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QHBoxLayout

from src.xsideui import XImage, XWidget, XLabel, XDivider, xicon_engine, XIcon
from example import app_rc

class XImageDemo(XWidget):
    def __init__(self, parent=None):
        super(XImageDemo, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self.set_title("XImage Demo")
        self.resize(800, 600)

        content_widget = QWidget(self)
        self.addWidget(content_widget)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 20, 20, 20)

        content_layout.addWidget(XLabel('基础用法/none/contain/cover/fill'))
        content_layout.addWidget(XDivider())

        fit_layout = QHBoxLayout()
        image1 = XImage(source='./img/wukong.jpeg', lazy=True, fit=XImage.FitMode.NONE, min_size=128)
        fit_layout.addWidget(image1)
        content_layout.addLayout(fit_layout)

        image2 = XImage(source='./img/wukong.jpeg', lazy=True, fit=XImage.FitMode.CONTAIN, min_size=128)
        fit_layout.addWidget(image2)
        content_layout.addLayout(fit_layout)

        image3 = XImage(source=XIcon.get(name='caihong', size=128).pixmap(), lazy=True, min_size=128)
        fit_layout.addWidget(image3)
        content_layout.addLayout(fit_layout)

        image4 = XImage(source='./img/wukong.jpeg', lazy=True, fit=XImage.FitMode.FILL, min_size=128)
        fit_layout.addWidget(image4)
        content_layout.addLayout(fit_layout)

        content_layout.addWidget(XLabel('占位图'))
        content_layout.addWidget(XDivider())
        image5 = XImage(source='', lazy=True, fit=XImage.FitMode.NONE, min_size=120)
        content_layout.addWidget(image5)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    XIcon.add_resource_path(":/app/")
    demo = XImageDemo()
    demo.show()
    sys.exit(app.exec_())
