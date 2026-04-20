"""
XSwitch 组件使用示例
展示开关组件如何自动适配明暗主题切换
"""

import sys
try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from src.xsideui import XHeaderCard, XSize, XWidget, XLabel, XSwitch, XColor


class XSwitchDemo(XWidget):
    def __init__(self):
        super(XSwitchDemo, self).__init__()
        self._init_ui()

    def _init_ui(self):
        self.set_title("XSwitch Demo")
        self.resize(800, 600)

        context_widget = QWidget()
        self.addWidget(context_widget)

        layout = QVBoxLayout(context_widget)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(20)

        layout.addWidget(XLabel("XSwitch 组件示例", style=XLabel.Style.H2))
        color_card = XHeaderCard('颜色')
        layout.addWidget(color_card)


        color_card.addWidget(XSwitch(checked=True,color=XColor.PRIMARY, text_position='left'))
        color_card.addWidget(XSwitch(checked=True,color=XColor.SUCCESS, text_position='left'))
        color_card.addWidget(XSwitch( checked=True,color=XColor.WARNING, text_position='left'))
        color_card.addWidget(XSwitch( checked=True,color=XColor.DANGER))
        color_card.addWidget(XSwitch( checked=True,color=XColor.SECONDARY))
        color_card.addWidget(XSwitch( checked=True,color=XColor.TERTIARY))

        click_switch = XSwitch(checked=True,color='#9805ae', size=XSize.DEFAULT, text_on='自定义颜色带信号',text_off='自定义颜色带信号')
        click_switch.clicked.connect(lambda statu:print(f'收到点击信号:{statu}'))
        color_card.addWidget(click_switch,stretch= 1)

        size_card = XHeaderCard('尺寸')
        layout.addWidget(size_card)
        size_card.addWidget(XSwitch( checked=True, size=XSize.LARGE))
        size_card.addWidget(XSwitch( checked=True, size=XSize.DEFAULT))
        size_card.addWidget(XSwitch( checked=True, size=XSize.SMALL))
        size_card.addWidget(XSwitch(checked=True, size=XSize.MINI),stretch= 1)

        status_card = XHeaderCard('状态')
        layout.addWidget(status_card)
        status_card.addWidget(XSwitch(checked=True))
        status_card.addWidget(XSwitch(checked=False))
        switch_1 = XSwitch(checked=False)
        switch_1.setEnabled(False)
        status_card.addWidget(switch_1,stretch= 1)

        text_card = XHeaderCard('文字')
        layout.addWidget(text_card)
        text_card.addWidget(XSwitch("", "",))
        text_card.addWidget(XSwitch("开启", "关闭",))
        text_card.addWidget(XSwitch("on", "off",),stretch= 1)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = XSwitchDemo()
    demo.show()
    sys.exit(app.exec_())
