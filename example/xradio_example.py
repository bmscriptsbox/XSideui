"""
XRadioButton 组件使用示例
展示单选按钮组件如何自动适配明暗主题切换
"""

import sys

from xsideui import XI18N

try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from src.xsideui import XWidget, XLabel, XRadioButton, XColor, XSize, XHeaderCard


class XRadioButtonDemo(XWidget):
    def __init__(self, parent=None):
        super(XRadioButtonDemo, self).__init__()
        self._init_ui()

    def _init_ui(self):
        self.set_title("XRadioButton Demo")
        self.resize(800, 600)

        context_widget = QWidget()
        self.addWidget(context_widget)
        content_layout = QVBoxLayout(context_widget)
        content_layout.setContentsMargins(20,20,20,20)
        content_layout.setSpacing(20)

        content_layout.addWidget(XLabel("XRadioButton 组件示例", style=XLabel.Style.H2))

        color_card = XHeaderCard('颜色')
        content_layout.addWidget(color_card)
        color_card.addWidget(XRadioButton("Primary", color=XColor.PRIMARY,checked=True))
        color_card.addWidget(XRadioButton("Success", color=XColor.SUCCESS,checked=True))
        color_card.addWidget(XRadioButton("Warning", color=XColor.WARNING,checked=True))
        color_card.addWidget(XRadioButton("Danger", color=XColor.DANGER,checked=True))
        color_card.addWidget(XRadioButton("Secondary", color=XColor.SECONDARY,checked=True))
        color_card.addWidget(XRadioButton("Tertiary", color=XColor.TERTIARY,checked=True))
        color_card.addWidget(XRadioButton("自定义", color='#720840',checked=True),stretch=1)

        size_card = XHeaderCard('尺寸')
        content_layout.addWidget(size_card)
        size_card.addWidget(XRadioButton("Lagre", size=XSize.LARGE, checked=True))
        size_card.addWidget(XRadioButton("Default", size=XSize.DEFAULT))
        size_card.addWidget(XRadioButton("Small", size=XSize.SMALL))
        size_card.addWidget(XRadioButton("Mini", size=XSize.MINI),stretch=1)

        state_card = XHeaderCard('状态')
        content_layout.addWidget(state_card)
        state_card.addWidget(XRadioButton("选中", checked=True))
        state_card.addWidget(XRadioButton("未选中"))
        radio_1 = XRadioButton('禁用')
        radio_1.setEnabled(False)
        state_card.addWidget(radio_1,stretch=1)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    XI18N.set_language("zh_CN")
    demo = XRadioButtonDemo()
    demo.show()
    sys.exit(app.exec_())
