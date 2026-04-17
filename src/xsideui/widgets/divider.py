from typing import Union

from ..utils.qt_compat import QWidget, QHBoxLayout, QFrame, QSizePolicy, Qt
from ..xenum import XColor
from .label import XLabel

class XDivider(QFrame):
    """
    极简分割线：深度适配 XColor 枚举
    """

    def __init__(self, vertical=False, size=1, color: Union[XColor, str] = '', parent=None):
        super().__init__(parent)
        self.setObjectName('XDivider')
        self.setProperty('color', color.value if isinstance(color, XColor) else color)
        self.setAttribute(Qt.WA_MacShowFocusRect, True)
        self._vertical = vertical
        self._size = size
        self._color = color  # 支持 XColor 或 str

        # 1. 基础设置
        self.setFrameShape(QFrame.VLine if vertical else QFrame.HLine)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(size)

        # 2. 尺寸策略
        if vertical:
            self.setFixedWidth(size)
            self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        else:
            self.setFixedHeight(size)
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def set_color_type(self, color: Union[XColor, str]):
        """动态改变颜色类型（如 'primary', 'danger'）"""
        if not color:
            return
        color = color.value if isinstance(color, XColor) else color
        self.setProperty('color', color)
        self.style().unpolish(self)
        self.style().polish(self)






class XTextDivider(QWidget):
    """
    带文字的分割线组件
    """

    def __init__(
            self,
            text: str = "",
            align: Qt.AlignmentFlag = Qt.AlignCenter,
            color: Union[XColor, str] = '',
            thickness: int = 1,
            fix_width: int = 20,
            parent=None
    ):
        super().__init__(parent)
        self.setObjectName("XTextDivider")

        # 主布局：水平排列
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)  # 文字与线的间距

        # 左侧分割线
        self.left_line = XDivider(vertical=False, size=thickness, color=color)

        # 中间文字
        self.label = XLabel(text).set_color(XColor.TERTIARY).set_font_size(12)

        # 右侧分割线
        self.right_line = XDivider(vertical=False, size=thickness, color=color)

        # 根据对齐方式调整布局
        if align == Qt.AlignCenter:
            layout.addWidget(self.left_line, 1)
            layout.addWidget(self.label, 0)
            layout.addWidget(self.right_line, 1)
        elif align == Qt.AlignLeft:
            self.left_line.setFixedWidth(fix_width)
            layout.addWidget(self.left_line, 0)  # Stretch 为 0
            layout.addWidget(self.label, 0)
            layout.addWidget(self.right_line, 1)  # 右线拉伸
        elif align == Qt.AlignRight:
            layout.addWidget(self.left_line, 1)  # 左线拉伸
            layout.addWidget(self.label, 0)
            self.right_line.setFixedWidth(fix_width)
            layout.addWidget(self.right_line, 0)  # Stretch 为 0

    def set_text(self, text: str):
        self.label.setText(text)

    def set_color_type(self, color: Union[XColor, str]):
        """同步修改两端线条颜色"""
        self.left_line.set_color_type(color)
        self.right_line.set_color_type(color)