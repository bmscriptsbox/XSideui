"""
XCheckBox 组件使用示例
展示复选框组件如何自动适配明暗主题切换
"""

import sys

from xsideui import XPushButton

try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from src.xsideui import XWidget, XCheckBox, XColor, XSize, XHeaderCard, XI18N


class XCheckBoxDemo(XWidget):
    def __init__(self):
        super(XCheckBoxDemo, self).__init__()
        self._init_ui()

    def _init_ui(self):
        self.set_title('XCheckBox Demo')
        self.resize(600, 500)

        context_widget = QWidget()
        self.addWidget(context_widget)
        context_layout = QVBoxLayout(context_widget)
        context_layout.setContentsMargins(20,20,20,20)
        context_layout.setSpacing(20)

        color_card = XHeaderCard('颜色')
        context_layout.addWidget(color_card)
        color_card.addWidget(XCheckBox(color=XColor.PRIMARY,text='Primary', checked=True))
        color_card.addWidget(XCheckBox(color=XColor.SUCCESS, text='Success', checked=True))
        color_card.addWidget(XCheckBox(color=XColor.WARNING, text='Warning', checked=True))
        color_card.addWidget(XCheckBox(color=XColor.DANGER, text='Danger', checked=True))
        color_card.addWidget(XCheckBox(color=XColor.SECONDARY, text='Secondary', checked=True))
        color_card.addWidget(XCheckBox(color=XColor.TERTIARY, text='Tertiary'), stretch=1)

        size_card = XHeaderCard('尺寸')
        context_layout.addWidget(size_card)
        size_card.addWidget(XCheckBox(size=XSize.LARGE, checked=True, text='Large'))
        size_card.addWidget(XCheckBox(size=XSize.DEFAULT, checked=True, text='Default'))
        size_card.addWidget(XCheckBox(size=XSize.SMALL, checked=True, text='Small'))
        size_card.addWidget(XCheckBox(size=XSize.MINI, checked=True,text='Mini'), stretch=1)

        status_card = XHeaderCard('状态')
        context_layout.addWidget(status_card)
        status_card.addWidget(XCheckBox(checked=True, text='Checked'))
        status_card.addWidget(XCheckBox(checked=False, text='Unchecked'))
        checkbox_1 = XCheckBox('禁用')
        checkbox_1.setEnabled(False)
        status_card.addWidget(checkbox_1,stretch=1)


        btn = XPushButton('语言切换')
        btn.clicked.connect(self.chang_langs)
        context_layout.addWidget(btn)

    def chang_langs(self):
        langs = XI18N.current_lang
        if langs == "zh_CN":
            XI18N.set_language("en_US")
        else:
            XI18N.set_language("zh_CN")
        print(langs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    XI18N.set_language("zh_CN")
    demo = XCheckBoxDemo()
    demo.show()
    sys.exit(app.exec_())
