"""
XTextEdit 组件使用示例
展示文本编辑器组件如何自动适配明暗主题切换
"""

import sys
try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QPushButton, QScrollArea, QWidget
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QScrollArea

from src.xsideui import XWidget, XLabel, XDivider, XTextEdit, theme_manager, XPushButton


class XTextEditDemo(XWidget):
    def __init__(self):
        super(XTextEditDemo, self).__init__()
        self._init_ui()

    def _init_ui(self):
        self.set_title("XTextEdit 主题适配示例")
        self.resize(600, 400)

        content_widget = QWidget()
        self.addWidget(content_widget)

        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(20,20,20,20)
        main_layout.setSpacing(20)

        main_layout.addWidget(XLabel("XTextEdit 组件示例", style=XLabel.Style.H1))
        main_layout.addWidget(XDivider())

        text_edit1 = XTextEdit(
            placeholder="请输入文本...",
            max_length=200
        )
        main_layout.addWidget(text_edit1)
        text_edit1.append("""独立寒秋，湘江北去，橘子洲头。
看万山红遍，层林尽染；漫江碧透，百舸争流。
鹰击长空，鱼翔浅底，万类霜天竞自由。
怅寥廓，问苍茫大地，谁主沉浮？
携来百侣曾游，忆往昔峥嵘岁月稠。
恰同学少年，风华正茂；书生意气，挥斥方遒。
指点江山，激扬文字，粪土当年万户侯。
曾记否，到中流击水，浪遏飞舟？""")








if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = XTextEditDemo()
    demo.show()
    sys.exit(app.exec_())