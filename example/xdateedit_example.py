"""
Test for XDateEdit component
"""
import sys
try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget
    from PySide2.QtCore import QDate
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
    from PySide6.QtCore import QDate

from src.xsideui import XDateEdit, XWidget, XLabel, theme_manager, XSize


class XDateEditDemo(XWidget):
    def __init__(self):
        super().__init__()
        self.set_title("XDateEdit Demo")
        self.resize(500, 600)

        content_widget = QWidget()
        self.addWidget(content_widget)
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        layout.addWidget(XLabel("Large Date Edit:"))
        date_edit_large = XDateEdit(size=XSize.LARGE)
        layout.addWidget(date_edit_large)

        layout.addWidget(XLabel("Default Date Edit:"))
        date_edit_default = XDateEdit(size=XSize.DEFAULT)
        layout.addWidget(date_edit_default)

        layout.addWidget(XLabel("Small Date Edit:"))
        date_edit_small = XDateEdit(size=XSize.SMALL)
        layout.addWidget(date_edit_small)

        layout.addWidget(XLabel("Mini Date Edit:"))
        date_edit_mini = XDateEdit(size=XSize.MINI)
        layout.addWidget(date_edit_mini)

        layout.addWidget(XLabel("Date with specific value:"))
        date_with_value = XDateEdit()
        date_with_value.setMinimumHeight(80)
        date_with_value.setDate(QDate.currentDate())
        layout.addWidget(date_with_value)



def main():
    app = QApplication(sys.argv)
    theme_manager.set_theme("light")

    window = XDateEditDemo()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
