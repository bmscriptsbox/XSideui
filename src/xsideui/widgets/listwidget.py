from ..utils.qt_compat import Qt, QListWidget


class XListWidget(QListWidget):
    """列表组件"""

    def __init__(
            self,
            show_border=True,
            parent=None
    ):
        """初始化列表控件基类。

            Args:
                show_border: 是否显示组件外边框。默认 True。
                    若嵌入其他容器（如 XCard 或 XCollapse）时，通常设为 False。
                parent: 父级组件。
            """
        super().__init__(parent)
        self.setObjectName("XListWidget")
        self._show_border = show_border
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._init_properties()
        self.set_show_border(show_border)

    def _init_properties(self):
        """初始化基本属性"""
        self.setFrameShape(QListWidget.NoFrame)
        self.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        self.setHorizontalScrollMode(QListWidget.ScrollPerPixel)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setFocusPolicy(Qt.NoFocus)

    def set_show_border(self, show: bool):
        """
        动态设置是否显示边框
        """
        self._show_border = show
        # 使用 Qt 属性系统，以便 QSS 能够识别
        self.setProperty("hasBorder", str(show).lower())

        # 更新样式
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
