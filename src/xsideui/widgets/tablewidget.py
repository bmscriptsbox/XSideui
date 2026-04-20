from enum import Enum
from typing import Union

from ..utils.qt_compat import (Qt, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
                               QWidget, QVBoxLayout, QEvent)
from .label import XLabel
from ..i18n import XI18N, tr
from .image import XImage
from ..icon import XIcon, IconName
from ..xenum import XColor


class XTableWidget(QTableWidget):
    """格组件"""

    class Style(Enum):
        """表格样式枚举"""
        DEFAULT = "default"
        STRIPED = "striped"

    def __init__(
            self,
            headers: list = None,
            column_widths: list = None,
            alignment: Qt.Alignment = Qt.AlignLeft | Qt.AlignVCenter,
            style: Union[Style, str] = Style.DEFAULT,
            row_height: int = 40,
            parent=None

    ):
        """初始化表格组件。

            Args:
                headers: 表头标题列表。
                column_widths: 各列的宽度。使用像素值，若设为 -1 则该列开启自动拉伸。
                alignment: 单元格内容的对齐方式。
                style: 表格风格。'default' 为纯色背景，'striped' 为交替行颜色。
                row_height: 统一的行高设置。
                parent: 父级组件。
            """
        super().__init__(parent)
        self._i18n_header_keys = headers
        self.default_alignment = alignment
        self._init_ui(style, row_height)
        self._init_empty_state()
        self.retranslateUi()
        if column_widths:
            self._init_column_widths(column_widths)
        self.set_alignment(alignment)
        self._update_empty_state()

    def _get_style_value(self, style: Union[Style, str]) -> str:
        """获取样式值，支持枚举和字符串

        Args:
            style: 样式，可以是 Style 枚举或字符串

        Returns:
            str: 样式字符串值
        """
        if isinstance(style, self.Style):
            return style.value
        return style

    def _init_ui(self, style: Union[Style, str], row_height: int = 32):
        """初始化表格基本属性"""
        self.setMouseTracking(True)
        self.setShowGrid(False)
        self.setFocusPolicy(Qt.NoFocus)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        header = self.horizontalHeader()
        header.setHighlightSections(False)
        header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header.setSectionResizeMode(QHeaderView.Interactive)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(row_height)
        self.set_style_type(style)

    def _init_empty_state(self):
        """初始化空状态"""
        self._empty_widget = QWidget(self)
        self._empty_widget.setVisible(False)
        self._empty_widget.setObjectName("table-empty-widget")

        layout = QVBoxLayout(self._empty_widget)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        self._empty_label = XLabel(tr("Empty Data"))
        layout.addWidget(
            XImage(source=XIcon.get(name=IconName.EMOTION_HAPPY, color=XColor.TERTIARY, size=32).pixmap(),
                   min_size=32))
        layout.addWidget(self._empty_label, 0, Qt.AlignCenter)

    def _update_empty_state(self):
        """更新空状态显示"""
        is_empty = self.rowCount() == 0
        self._empty_widget.setVisible(is_empty)

    def resizeEvent(self, event):
        """重写 resizeEvent，调整空状态器位置"""
        super().resizeEvent(event)
        self._empty_widget.setGeometry(self.viewport().rect())

    def setRowCount(self, rows: int):
        """重写 setRowCount，更新空状态"""
        super().setRowCount(rows)
        self._update_empty_state()

    def setItem(self, row: int, column: int, item: QTableWidgetItem):
        """重写 setItem 方法，应用默认对齐方式"""
        try:
            if item.textAlignment() == 0:
                item.setTextAlignment(self.default_alignment)
            super().setItem(row, column, item)
        except Exception as e:
            print(f"设置单元格数据错误: {e}")

    def set_alignment(self, alignment: Qt.Alignment) -> 'XTableWidget':
        """设置表格内容对齐方式

        Args:
            alignment: 对齐方式，如 Qt.AlignCenter

        Returns:
            XTableWidget: 返回自身以支持链式调用
        """
        self.default_alignment = alignment
        self.horizontalHeader().setDefaultAlignment(alignment)

        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                item = self.item(row, col)
                if item:
                    item.setTextAlignment(alignment)
        return self

    def set_column_widths(self, widths: list) -> 'XTableWidget':
        """设置列宽度

        Args:
            widths: 列宽列表，-1 表示自动拉伸

        Returns:
            XTableWidget: 返回自身以支持链式调用

        Example:
            >>> table.set_column_widths([100, -1, 80, 120])
        """
        self.horizontalHeader().setStretchLastSection(False)

        for col, width in enumerate(widths):
            if width == -1:
                self.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)
            else:
                self.horizontalHeader().setSectionResizeMode(col, QHeaderView.Fixed)
                self.setColumnWidth(col, width)
        return self

    def set_headers(self, headers: list) -> 'XTableWidget':
        """设置表头

        Args:
            headers: 表头文本列表

        Returns:
            XTableWidget: 返回自身以支持链式调用
        """
        self._i18n_header_keys = headers
        self.setColumnCount(len(headers))
        self.retranslateUi()
        return self

    def set_style_type(self, style: Union[Style, str]) -> 'XTableWidget':
        """设置表格样式类型

        Args:
            style: 样式类型，可以是 Style 枚举或字符串
                - Style.DEFAULT 或 "default": 默认样式
                - Style.STRIPED 或 "striped": 斑马纹样式

        Returns:
            XTableWidget: 返回自身以支持链式调用

        Example:
            >>> table.set_style_type(XTableWidget.Style.STRIPED)  # 使用枚举
            >>> table.set_style_type("striped")  # 使用字符串
        """
        style_value = self._get_style_value(style)

        if style_value == "striped":
            self.setObjectName("xtablewidget-striped")
            self.setAlternatingRowColors(True)
        else:
            self.setObjectName("xtablewidget-default")
            self.setAlternatingRowColors(False)

        return self

    def set_row_height(self, height: int) -> 'XTableWidget':
        """设置行高

        Args:
            height: 行高，单位为像素

        Returns:
            XTableWidget: 返回自身以支持链式调用

        Example:
            >>> table.set_row_height(40)
        """
        self.verticalHeader().setDefaultSectionSize(height)
        return self

    def changeEvent(self, event):
        """监听 I18nManager 发出的 LanguageChange 事件"""
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi()
        super().changeEvent(event)

    def retranslateUi(self):
        """当语言切换或文本更新时调用 / 翻译表头"""
        if not self._i18n_header_keys:
            super().setHorizontalHeaderLabels([])
            return
        translated_labels = [XI18N.x_tr(key) for key in self._i18n_header_keys]
        super().setHorizontalHeaderLabels(translated_labels)
