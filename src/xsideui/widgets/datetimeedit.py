"""
DateTime Edit Component 日期时间编辑框组件
"""

from typing import Union
from ..utils.qt_compat import  QDateTimeEdit, QDateTime, QDate, QTime
from ..icon import IconName
from ..theme import theme_manager
from ..xenum import XSize
from .xarrowbutton import XArrowButton

class XDateTimeEdit(QDateTimeEdit):
    """DateTime Edit Component 日期时间编辑框组件"""

    def __init__(self, size: Union[XSize, str] = XSize.DEFAULT, parent=None):
        """
        Initialize. 初始化。

        Args:
            size: 组件尺寸 (Component size)
            parent: 父组件 (Parent widget)
        """
        super().__init__(parent)
        self.setObjectName("xqdatetimeedit")
        self._size_value = self._parse_size(size)

        self.setDateTimeRange(
            QDateTime(QDate(1000, 1, 1), QTime(0, 0, 0)),
            QDateTime(QDate(9999, 12, 31), QTime(23, 59, 59))
        )
        self.setWrapping(True)
        self.setButtonSymbols(QDateTimeEdit.NoButtons)
        self.setCalendarPopup(False)
        self.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.setDateTime(QDateTime.currentDateTime())

        self._init_arrow_buttons()
        self._update_style()

        theme_manager.theme_changed.connect(self._on_theme_changed)

    def _parse_size(self, size: Union[XSize, str]) -> str:
        if isinstance(size, XSize):
            return size.value
        return size

    def _init_arrow_buttons(self):
        self._up_btn = XArrowButton(icon_name=IconName.UP_CARET, parent=self)
        self._down_btn = XArrowButton(icon_name=IconName.DOWN_CARET, parent=self)
        self._up_btn.show()
        self._down_btn.show()
        self._up_btn.clicked.connect(self._step_up)
        self._down_btn.clicked.connect(self._step_down)

    def _step_up(self):
        current_section = self.currentSection()
        self.stepUp()
        self.setCurrentSection(current_section)

    def _step_down(self):
        current_section = self.currentSection()
        self.stepDown()
        self.setCurrentSection(current_section)

    def _get_size_config(self) -> dict:
        size_map = {
            'large': 28,
            'default': 24,
            'small': 22,
            'mini': 20
        }
        return {'btn_width': size_map.get(self._size_value, size_map['default'])}

    def _update_style(self):
        self.setProperty("componentSize", self._size_value)
        self._update_button_positions()

    def _update_button_positions(self):
        config = self._get_size_config()
        btn_width = config['btn_width']
        height = self.height()
        btn_height = height // 2

        self._up_btn.setFixedSize(btn_width, btn_height)
        self._down_btn.setFixedSize(btn_width, btn_height)
        self._up_btn.move(self.width() - btn_width, 0)
        self._down_btn.move(self.width() - btn_width, btn_height)
        self._up_btn.raise_()
        self._down_btn.raise_()
        self.setContentsMargins(0, 0, btn_width, 0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_button_positions()

    def showEvent(self, event):
        super().showEvent(event)
        self._update_button_positions()

    def set_size(self, size: Union[XSize, str]):
        """Set component size. 设置组件尺寸"""
        self._size_value = self._parse_size(size)
        self._update_style()
        return self

    def size(self) -> str:
        return self._size_value

    def _on_theme_changed(self, theme_name):
        self._up_btn.update()
        self._down_btn.update()
