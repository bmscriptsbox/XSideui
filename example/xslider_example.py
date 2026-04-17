"""
XSlider 组件使用示例
展示滑块组件如何自动适配明暗主题切换
"""

import sys
try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel


from src.xsideui import XWidget, XLabel, XDivider, XSlider, XColor



class XSliderDemo(XWidget):
    def __init__(self):
        super(XSliderDemo, self).__init__()
        self._init_ui()


    def _init_ui(self):
        self.set_title("XSlider Demo")
        self.resize(600, 500)

        content_widget = QWidget()
        self.addWidget(content_widget)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 20, 20, 20)

        content_layout.addWidget(XLabel("XSlider 组件示例", style=XLabel.Style.H1))
        content_layout.addWidget(XLabel("点击下方按钮切换明暗主题，观察滑块样式变化", style=XLabel.Style.CAPTION))
        content_layout.addWidget(XDivider())

        content_layout.addWidget(XLabel("颜色/高度", style=XLabel.Style.H4))
        color_layout = QVBoxLayout()
        color_layout.addWidget(XSlider(value=20, color=XColor.PRIMARY, groove_height=4))
        color_layout.addWidget(XSlider(value=40, color=XColor.SUCCESS, groove_height=6))
        color_layout.addWidget(XSlider(value=60, color=XColor.WARNING, groove_height=7))
        color_layout.addWidget(XSlider(value=80, color=XColor.DANGER, groove_height=8))
        content_layout.addLayout(color_layout)


        content_layout.addWidget(XLabel("垂直滑块", style=XLabel.Style.H4))
        vertical_layout = QHBoxLayout()
        vertical_layout.addWidget(XSlider(orientation=Qt.Vertical, value=20, color=XColor.PRIMARY, groove_height=4))
        slider_vertical2 = XSlider(orientation=Qt.Vertical, value=40, color=XColor.SUCCESS, groove_height=6)
        slider_vertical2.setMinimumHeight(200)
        vertical_layout.addWidget(slider_vertical2)
        vertical_layout.addWidget(XSlider(orientation=Qt.Vertical, value=60, color=XColor.WARNING, groove_height=7))
        vertical_layout.addWidget(XSlider(orientation=Qt.Vertical, value=80, color=XColor.DANGER, groove_height=8))
        content_layout.addLayout(vertical_layout)

        content_layout.addWidget(XLabel("禁用状态", style=XLabel.Style.H4))
        disabled_layout = QVBoxLayout()
        slider_disabled1 = XSlider(value=50)
        slider_disabled1.setEnabled(False)
        disabled_layout.addWidget(slider_disabled1)
        content_layout.addLayout(disabled_layout)


        content_layout.addWidget(XLabel("监听值变化", style=XLabel.Style.H4))
        value_label = XLabel("当前值: 50")
        slider_value = XSlider(value=50)
        slider_value.valueChanged.connect(lambda v: value_label.setText(f"当前值: {v}"))
        value_layout = QVBoxLayout()
        value_layout.addWidget(slider_value)
        value_layout.addWidget(value_label)
        content_layout.addLayout(value_layout)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = XSliderDemo()
    demo.show()
    sys.exit(app.exec_())
