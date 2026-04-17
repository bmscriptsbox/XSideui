"""
XSpinBox 和 XDoubleSpinBox 组件使用示例
展示数字输入框组件如何自动适配明暗主题切换
"""

import sys
try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout,  QWidget
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from src.xsideui import XWidget, XLabel, XDivider, XSpinBox, XDoubleSpinBox,XSize



class XPinBoxDemo(XWidget):
    def __init__(self, parent=None):
        super(XPinBoxDemo, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self.set_title("XPinBox Demo")
        self.resize(600,500)
        content_widget = QWidget()
        self.addWidget(content_widget)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20,20,20,20)
        content_layout.setSpacing(20)

        content_layout.addWidget(XLabel("XSpinBox 和 XDoubleSpinBox 组件示例", style=XLabel.Style.H1))
        content_layout.addWidget(XDivider())
        content_layout.addWidget(XLabel("整数/小数输入框", style=XLabel.Style.H3))
        int_layout = QVBoxLayout()
        int_layout.addWidget(XSpinBox(value=50, prefix="$", suffix="刀"))
        int_layout.addWidget(XDoubleSpinBox(value=50.99, prefix="￥", suffix="元"))
        content_layout.addLayout(int_layout)

        content_layout.addWidget(XLabel("尺寸", style=XLabel.Style.H3))
        size_layout = QVBoxLayout()
        size_layout.addWidget(XSpinBox(size=XSize.LARGE))
        size_layout.addWidget(XSpinBox(size=XSize.DEFAULT))
        size_layout.addWidget(XSpinBox(size=XSize.SMALL))
        size_layout.addWidget(XSpinBox(size=XSize.MINI))
        content_layout.addLayout(size_layout)


        content_layout.addWidget(XLabel("禁用", style=XLabel.Style.H3))
        disabled_layout = QVBoxLayout()
        spin_disabled1 = XSpinBox(value=50)
        spin_disabled1.setEnabled(False)
        disabled_layout.addWidget(spin_disabled1)
        spin_disabled2 = XSpinBox(value=50, prefix="$", suffix="个")
        spin_disabled2.setEnabled(False)
        disabled_layout.addWidget(spin_disabled2)
        content_layout.addLayout(disabled_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = XPinBoxDemo()
    demo.show()
    sys.exit(app.exec_())
