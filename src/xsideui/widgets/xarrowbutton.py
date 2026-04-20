
from ..utils.qt_compat import QPushButton, QPainter, Qt
from ..icon import XIcon
from ..theme import theme_manager


class XArrowButton(QPushButton):
    """自定义箭头按钮"""

    def __init__(self, icon_name, parent=None):
        super().__init__(parent)
        self.icon_name = icon_name
        self._hovered = False
        self.setCursor(Qt.PointingHandCursor)
        self.setAutoRepeat(True)
        self.setAutoRepeatDelay(300)
        self.setAutoRepeatInterval(50)

    def enterEvent(self, event):
        self._hovered = True
        self.update()

    def leaveEvent(self, event):
        self._hovered = False
        self.update()

    def _get_color(self) -> str:
        if not self.isEnabled():
            return theme_manager.colors.text_disabled
        elif self._hovered:
            return theme_manager.colors.primary
        return theme_manager.colors.text_1

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = self._get_color()
        icon_size = max(8, self.height() - 6)
        qicon = XIcon.get(name=self.icon_name, color=color, size=icon_size).icon()
        if qicon:
            # 如果按钮按下去(isDown)，增加 1px 偏移增加交互感
            offset = 1 if self.isDown() else 0
            rect = self.rect().adjusted(2, 2 + offset, -2, -2 + offset)
            qicon.paint(painter, rect, Qt.AlignCenter)