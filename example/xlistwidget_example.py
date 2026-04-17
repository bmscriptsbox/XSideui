"""
XListWidget 组件使用示例
展示列表控件如何自动适配明暗主题切换
"""

import sys
try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget, QListWidgetItem
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QListWidgetItem

from src.xsideui import XLabel, XListWidget, XWidget, XIcon, IconName


class XListWidgetDemo(XWidget):
    def __init__(self):
        super(XListWidgetDemo, self).__init__()
        self._init_ui()

    def _init_ui(self):
        self.set_title('XListWidget Demo')
        self.resize(400, 500)

        content_widget = QWidget()
        self.addWidget(content_widget)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20,20,20,20)
        content_layout.setSpacing(20)
        content_layout.addWidget(XLabel("默认列表示例", style=XLabel.Style.H3))
        default_list = XListWidget(show_border=False)
        default_list.addItems([
            "选项 1：默认列表项",
            "选项 2：带边框和圆角",
            "选项 3：支持悬停效果",
            "选项 4：支持选中效果",
            "选项 5：自定义滚动条样式",
            "选项 7：支持明暗切换",
            "选项 8：继承QListWidget",
            "选项 9：QSS样式控制",
        ])
        item = QListWidgetItem('带图标的Item')
        item.setIcon(XIcon(IconName.SHARE).icon())
        default_list.addItem(item)
        content_layout.addWidget(default_list)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = XListWidgetDemo()
    demo.show()
    sys.exit(app.exec_())
