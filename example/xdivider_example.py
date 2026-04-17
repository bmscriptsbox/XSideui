"""
XDivider 完整使用示例
"""

import sys



try:
    from PySide2.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QWidget)
    from PySide2.QtCore import Qt
except ImportError:
    from PySide6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout,QWidget)
    from PySide6.QtCore import Qt
from src.xsideui.widgets import XLabel, XDivider, XWidget
from src.xsideui.widgets.divider import XTextDivider


class XDividerExampleWindow(XWidget):
    """XDivider 完整示例窗口"""
    
    def __init__(self):
        super().__init__()
        self.set_title("XDivider Demo")
        self.resize(300, 200)

        
        # 主容器
        container = QWidget()
        self.addWidget(container)
        layout = QVBoxLayout(container)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        layout.addWidget(XLabel("落霞与孤鹜齐飞，天水共长天一色"))
        layout.addWidget(XTextDivider(text='文字分割线', align=Qt.AlignRight))
        layout.addWidget(XLabel("无边落木萧萧下，不尽长江滚滚来"))
        layout.addWidget(XDivider())


        row = QHBoxLayout()
        row.addWidget(XLabel("三湘四水"))
        row.addWidget(XDivider(vertical=True))
        row.addWidget(XLabel("相约湖南"))
        row.addWidget(XDivider(vertical=True))
        row.addWidget(XLabel("周末不忙"))
        row.addWidget(XDivider(vertical=True))
        row.addWidget(XLabel("来趟衡阳"))
        row.addStretch()
        layout.addLayout(row)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = XDividerExampleWindow()
    window.show()
    sys.exit(app.exec_())