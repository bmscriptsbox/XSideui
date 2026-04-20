
from ..utils.qt_compat import QScrollArea, Qt, QSizePolicy, QSize


class XScrollArea(QScrollArea):
    def __init__(self, parent=None):
        """初始化滚动区域。

            Args:
                parent: 父级组件。
            """
        super().__init__(parent)
        self.setWidgetResizable(True)  # 允许内容区域大小随内容变化而变化
        self.setObjectName('xscrollarea')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 设置大小策略
        self.setMinimumSize(QSize(0, 0))


    def set_scrollbar_visible(self, vertical: bool, horizontal: bool):
        """设置滚动条的显隐"""
        vertical_policy = Qt.ScrollBarAsNeeded if vertical else Qt.ScrollBarAlwaysOff
        horizontal_policy = Qt.ScrollBarAsNeeded if horizontal else Qt.ScrollBarAlwaysOff
        self.setVerticalScrollBarPolicy(vertical_policy)
        self.setHorizontalScrollBarPolicy(horizontal_policy)


