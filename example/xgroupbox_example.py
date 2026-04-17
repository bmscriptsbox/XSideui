"""
XGroupBox 组件使用示例
展示分组框组件如何自动适配明暗主题切换
"""

import sys

from xsideui import XI18N

try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QPushButton, QCheckBox, QWidget
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QCheckBox, QWidget

from src.xsideui import XCheckBox, XLabel, XGroupBox, XWidget



class XGroupBoxDemo(XWidget):
    def __init__(self):
        super(XGroupBoxDemo, self).__init__()
        self._init_ui()

    def _init_ui(self):
        self.set_title("XGroupBox Demo")
        self.resize(600, 500)

        # 创建主窗口
        content_widget = QWidget()
        self.addWidget(content_widget)
        # 主布局
        main_layout = QVBoxLayout(content_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20,20,20,20)

        # 基础分组框
        group1 = XGroupBox(title="Primary")
        group1_layout = QVBoxLayout()
        group1_layout.addWidget(XLabel("用户名：张三"))
        group1_layout.addWidget(XLabel("邮箱：zhangsan@example.com"))
        group1.setLayout(group1_layout)
        main_layout.addWidget(group1)


        # 禁用状态的分组框
        group4 = XGroupBox(title="禁用分组框")
        group4_layout = QVBoxLayout()
        group4_layout.addWidget(XCheckBox("禁用的选项 1"))
        group4_layout.addWidget(XCheckBox("禁用的选项 2"))
        group4.setEnabled(False)
        group4.setLayout(group4_layout)
        main_layout.addWidget(group4)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    XI18N.set_language("zh_CN")
    demo = XGroupBoxDemo()
    demo.show()
    sys.exit(app.exec_())
