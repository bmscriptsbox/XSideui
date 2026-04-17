"""
XFlowLayout 组件使用示例
展示流式布局组件如何自动排列子组件
"""

import sys
try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from src.xsideui import XWidget, XLabel, XDivider, XFlowLayout


# class XFlowLayoutDemo(XWidget):
#     def __init__(self, parent=None):
#         super(XFlowLayoutDemo, self).__init__(parent)
#         self._init_ui()
#
#     def _init_ui(self):
#         self.set_title('XFlowLayout Demo')
#         self.resize(600, 800)
#         content_widget = QWidget()
#         self.addWidget(content_widget)
#         flow_layout1 = XFlowLayout(content_widget,spacing=20)
#         flow_layout1.setContentsMargins(20,20,20,20)
#         for i in range(99):
#             label = XLabel(f"标签 {i + 1}", style=XLabel.Style.BODY)
#             flow_layout1.addWidget(label)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     demo = XFlowLayoutDemo()
#     demo.show()
#     sys.exit(app.exec_())


import sys
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout
from xsideui import XWidget, XLabel, XScrollArea, XFlowLayout


class XFlowLayoutDemo(XWidget):
    def __init__(self, parent=None):
        super(XFlowLayoutDemo, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self.set_title('XFlowLayout 自动换行演示')
        self.resize(600, 500)

        # 1. 创建滚动区域（这是流式布局的标配）
        self.scroll_area = XScrollArea()
        # 关键！必须设置为 True，否则内部容器不会随宽度拉伸，导致流式布局无法换行
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.set_scrollbar_visible(False, True)  # 隐藏横向，显示纵向

        # 2. 创建内部承载容器
        self.content_widget = QWidget()
        # 3. 将 XFlowLayout 直接安装在容器上
        self.flow_layout = XFlowLayout(self.content_widget)
        self.flow_layout.setContentsMargins(20, 20, 20, 20)
        self.flow_layout.setSpacing(15)

        # 4. 填充大量标签
        for i in range(99):
            # 给标签加个背景或边框，视觉上更容易观察“流”的效果
            label = XLabel(f"标签 {i + 1}", style=XLabel.Style.BODY)
            label.setStyleSheet("""
                XLabel { 
                    background-color: #333; 
                    border-radius: 4px; 
                    padding: 8px 15px; 
                }
            """)
            self.flow_layout.addWidget(label)

        # 5. 装载路径：FlowLayout -> ContentWidget -> ScrollArea -> XWidget(Main)
        self.scroll_area.setWidget(self.content_widget)
        self.addWidget(self.scroll_area)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 假设你的环境里已经能识别 XFlowLayout 和 XLabel
    demo = XFlowLayoutDemo()
    demo.show()
    sys.exit(app.exec_())
