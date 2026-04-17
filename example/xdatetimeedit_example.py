"""
Test for XDateTimeEdit component
"""
import sys
try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget
    from PySide2.QtCore import QDateTime
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
    from PySide6.QtCore import QDateTime

from src.xsideui.theme import theme_manager
from src.xsideui import XDateTimeEdit, XSize, XWidget, XLabel


class XDateTimeEditDemo(XWidget):
    def __init__(self):
        super().__init__()
        self.set_title("XDateTimeEdit Demo")
        self.resize(500, 600)

        content_widget = QWidget()
        self.addWidget(content_widget)
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        layout.addWidget(XLabel("Large DateTime Edit:"))
        datetime_edit_large = XDateTimeEdit(size=XSize.LARGE)
        layout.addWidget(datetime_edit_large)

        layout.addWidget(XLabel("Default DateTime Edit:"))
        datetime_edit_default = XDateTimeEdit(size=XSize.DEFAULT)
        layout.addWidget(datetime_edit_default)

        layout.addWidget(XLabel("Small DateTime Edit:"))
        datetime_edit_small = XDateTimeEdit(size=XSize.SMALL)
        layout.addWidget(datetime_edit_small)

        layout.addWidget(XLabel("Mini DateTime Edit:"))
        datetime_edit_mini = XDateTimeEdit(size=XSize.MINI)
        layout.addWidget(datetime_edit_mini)

        layout.addWidget(XLabel("DateTime with specific value:"))
        datetime_with_value = XDateTimeEdit()
        datetime_with_value.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(datetime_with_value)

        # btn_theme = XPushButton('切换主题')
        # btn_theme.clicked.connect(theme_manager.toggle_theme)
        # layout.addWidget(btn_theme)
        # layout.addStretch()

def main():
    app = QApplication(sys.argv)
    theme_manager.set_theme("light")

    window = XDateTimeEditDemo()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
