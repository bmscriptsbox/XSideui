"""
XTabWidget Example 标签页组件示例
展示标签页组件的使用
"""
import sys



try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget
    from PySide2.QtCore import QSize
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
    from PySide6.QtCore import QSize
from src.xsideui import XLabel, XTabWidget, XWidget, XI18N


class XTabWidgetExample(XWidget):
    """XTabWidget Example Window 标签页组件示例窗口"""

    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        """Setup user interface 设置用户界面"""
        self.set_title("XTabWidget Demo")
        self.resize(QSize(600, 400))

        container_widget  = QWidget()
        self.addWidget(container_widget)

        self.main_layout = QVBoxLayout(container_widget)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        title = XLabel("XTabWidget 标签页组件", style=XLabel.Style.H1)
        self.main_layout.addWidget(title)
        self.setup_tab()




    def setup_tab(self):
        tab_widget_flat = XTabWidget()
        tab_widget_flat.setIconSize(QSize(16,16))

        tab1 = XLabel("这是flat样式Tab第一个标签页的内容")
        tab_widget_flat.addTab(tab1,  "测试五个")


        tab2 = XLabel("这是这是flat样式Tab第二个标签页的内容")
        tab_widget_flat.addTab(tab2, "Open")

        tab3 = XLabel("这是这是flat样式Tab第三个标签页的内容")
        tab_widget_flat.addTab(tab3, "Save")

        tab4 = XLabel("这是这是flat样式Tab第四个标签页的内容")
        tab_widget_flat.addTab(tab4, "tab4")

        self.main_layout.addWidget(tab_widget_flat)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    XI18N.set_language("zh_CN")
    window = XTabWidgetExample()
    window.show()
    sys.exit(app.exec_())
