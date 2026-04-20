from ..utils.qt_compat import Qt, QTextEdit


class XTextEdit(QTextEdit):
    """
    文本编辑器组件
    """

    def __init__(
        self,
        text: str = "",
        placeholder: str = "",
        max_length: int = 0,
        read_only: bool = False,
        parent=None
    ):
        """
        Args:
            text: 初始文本
            placeholder: 占位文本
            max_length: 最大长度，0 表示不限制
            read_only: 是否只读
            parent: 父组件
        """
        super().__init__(parent)

        self.setObjectName("xtextedit")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFrameShape(self.Shape.NoFrame)

        self._max_length = max_length

        if text:
            self.setText(text)
        if placeholder:
            self.setPlaceholderText(placeholder)
        if read_only:
            self.setReadOnly(True)

        self.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self):
        """文本变化时限制长度"""
        if self._max_length > 0:
            text = self.toPlainText()
            if len(text) > self._max_length:
                self.setText(text[:self._max_length])
                cursor = self.textCursor()
                cursor.movePosition(cursor.End)
                self.setTextCursor(cursor)
