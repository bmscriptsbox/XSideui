"""
XPopover Example 气泡卡片组件示例
展示气泡卡片组件的使用
"""
try:
    from PySide2.QtWidgets import (QApplication, QVBoxLayout,
                                   QHBoxLayout, QWidget)
except ImportError:
    from PySide6.QtWidgets import (QApplication, QVBoxLayout,
                                   QHBoxLayout, QWidget)


from src.xsideui import (XLabel, XPushButton, XPopover,
                                 XButtonVariant, XWidget, XColor)


class XPopoverExample(XWidget):
    """XPopover Example Window 气泡卡片示例窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("XPopover Example - 气泡卡片组件示例")
        self.resize(600, 400)
        self._setup_ui()

    def _setup_ui(self):
        """Setup user interface.
        设置用户界面。"""

        content_widget = QWidget()
        self.addWidget(content_widget)
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(20,20,20,20)
        main_layout.setSpacing(20)

        main_layout.addWidget(XLabel("XPopover 气泡卡片组件示例", style=XLabel.Style.H2))

        description = XLabel("悬浮触发", style=XLabel.Style.H4)
        main_layout.addWidget(description)
        btn1 = XPushButton("底部显示", variant=XButtonVariant.OUTLINED)
        XPopover.show_popover(btn1,'XPopover气泡悬浮触发，父组件底部展示。',placement = XPopover.Placement.BOTTOM)

        btn_layout = QHBoxLayout()
        btn2 = XPushButton("顶部提示", variant=XButtonVariant.OUTLINED)
        XPopover.show_popover(btn2,'XPopover气泡悬浮触发，父组件顶部展示。',placement = XPopover.Placement.TOP)

        btn3 = XPushButton("左侧显示", variant=XButtonVariant.OUTLINED)
        XPopover.show_popover(btn3,'XPopover气泡悬浮触发，父组件左侧展示。',placement = 'left')

        btn4 = XPushButton("右侧显示", variant=XButtonVariant.OUTLINED)
        XPopover.show_popover(btn4,'XPopover气泡悬浮触发，父组件右侧展示。',placement = 'right')
        btn_layout.addWidget(btn1)
        btn_layout.addWidget(btn2)
        btn_layout.addWidget(btn3)
        btn_layout.addWidget(btn4)




        click_btn_layout = QHBoxLayout()
        btn5 = XPushButton("底部显示", variant=XButtonVariant.OUTLINED, color=XColor.TERTIARY)
        XPopover.show_popover(btn5, 'XPopover气泡点击触发', placement='bottom', trigger=XPopover.Trigger.CLICK)
        click_btn_layout.addWidget(btn5)

        btn6 = XPushButton("顶部显示", variant=XButtonVariant.OUTLINED, color=XColor.TERTIARY)
        XPopover.show_popover(btn6,'XPopover气泡点击触发',placement = 'top',trigger=XPopover.Trigger.CLICK)
        click_btn_layout.addWidget(btn6)


        btn7 = XPushButton("左侧显示", variant=XButtonVariant.OUTLINED, color=XColor.TERTIARY)
        XPopover.show_popover(btn7, 'XPopover气泡点击触发', placement='left', trigger=XPopover.Trigger.CLICK)
        click_btn_layout.addWidget(btn7)

        btn8 = XPushButton("右侧显示", variant=XButtonVariant.OUTLINED, color=XColor.TERTIARY)
        XPopover.show_popover(btn8, 'XPopover气泡点击触发', placement='right', trigger=XPopover.Trigger.CLICK)
        click_btn_layout.addWidget(btn8)

        main_layout.addLayout(btn_layout)
        main_layout.addWidget(XLabel("点击触发", style=XLabel.Style.H4))
        main_layout.addLayout(click_btn_layout)



if __name__ == "__main__":
    app = QApplication([])
    window = XPopoverExample()
    window.show()
    app.exec_()
