"""
Test for XTimeEdit component
"""
import sys
try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from src.xsideui import XTimeEdit, XSize, XWidget, XLabel



class XTimeEditDemo(XWidget):
    def __init__(self):
        super().__init__()
        self.set_title("XTimeEdit Demo")
        self.resize(500, 600)

        content_widget = QWidget()
        self.addWidget(content_widget)

        layout = QVBoxLayout(content_widget)
        layout.setSpacing(20)

        layout.addWidget(XLabel("Large Time Edit:"))
        time_edit_large = XTimeEdit(size=XSize.LARGE)
        layout.addWidget(time_edit_large)

        layout.addWidget(XLabel("Default Time Edit:"))
        time_edit_default = XTimeEdit(size=XSize.DEFAULT)
        layout.addWidget(time_edit_default)

        layout.addWidget(XLabel("Small Time Edit:"))
        time_edit_small = XTimeEdit(size=XSize.SMALL)
        layout.addWidget(time_edit_small)

        layout.addWidget(XLabel("Mini Time Edit:"))
        time_edit_mini = XTimeEdit(size=XSize.MINI)
        layout.addWidget(time_edit_mini)


        layout.addStretch()

def main():
    app = QApplication(sys.argv)
    window = XTimeEditDemo()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
