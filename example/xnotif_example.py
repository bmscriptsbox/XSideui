"""
XNotif Example 通知提示组件示例
展示通知提示组件的使用
"""
try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget

from src.xsideui import (XNotif, XLabel, XButtonVariant, XWidget, XPushButtonDropdown, XColor, IconName)


class XNotifExample(XWidget):
    """XNotif Example Window 通知提示示例窗口"""

    def __init__(self):
        super().__init__()
        self.set_title("XNotif Demo - 通知提示组件示例")
        self.resize(800, 600)

        self._setup_ui()

    def _setup_ui(self):
        """Setup user interface.
        设置用户界面。"""

        container = QWidget()
        self.addWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(20,20,20,20)
        main_layout.setSpacing(20)
        main_layout.addWidget(XLabel("XNotif 通知提示组件示例", style=XLabel.Style.H2))
        row = QHBoxLayout()
        main_layout.addLayout(row)

        # 定义菜单数据
        items = [
            {"text": "居中显示", "value": "center"},
            {"text": "右上显示", "value": "top_right"},
            {"text": "左上显示", "value": "top_left"},
            {"text": "右下显示", "value": "bottom_right"},
            {"text": "左下显示", "value": "bottom_left"},
        ]


        btn_info = XPushButtonDropdown(
            text="信息通知",
            menu_items=items,  # 传入数据
            variant=XButtonVariant.OUTLINED,
            color=XColor.PRIMARY,
            icon=IconName.COMMENT
        )
        row.addWidget(btn_info)
        btn_info.clicked.connect(self._show_info)
        btn_info.menuTriggered.connect(lambda position:self._show_info(position))

        btn_success = XPushButtonDropdown(
            text="成功通知",
            menu_items=items,  # 传入数据
            variant=XButtonVariant.OUTLINED,
            color=XColor.SUCCESS,
            icon=IconName.COMMENT
        )
        row.addWidget(btn_success)
        btn_success.clicked.connect(self._show_success)
        btn_success.menuTriggered.connect(lambda position:self._show_success(position))

        btn_warning = XPushButtonDropdown(
            text="警告通知",
            menu_items=items,  # 传入数据
            variant=XButtonVariant.SOLID,
            color=XColor.WARNING,
            icon=IconName.COMMENT
        )
        row.addWidget(btn_warning)
        btn_warning.clicked.connect(self._show_warning)
        btn_warning.menuTriggered.connect(lambda position:self._show_warning(position))

        btn_error = XPushButtonDropdown(
            text="错误通知",
            menu_items=items,  # 传入数据
            variant=XButtonVariant.OUTLINED,
            color=XColor.DANGER,
            icon=IconName.COMMENT
        )
        row.addWidget(btn_error)
        btn_error.clicked.connect(self._show_error)
        btn_error.menuTriggered.connect(lambda position:self._show_error(position))



    def _show_info(self,position='center'):
        """显示信息通知"""
        XNotif.info("信息通知", animated=True,position=position,parent=self)

    def _show_success(self,position=XNotif.Pos.TOP_LEFT):
        """显示成功通知"""
        XNotif.success("成功通知！",animated=True,position=position, parent=self)

    def _show_warning(self,position=XNotif.Pos.TOP_RIGHT):
        """显示警告通知"""
        XNotif.warning("警告信息",animated=True,position=position, parent=self)

    def _show_error(self,position=XNotif.Pos.BOTTOM_RIGHT):
        """显示错误通知"""
        XNotif.error("错误通知",animated=True,position=position, parent=self)



if __name__ == "__main__":
    app = QApplication([])
    window = XNotifExample()
    window.show()
    app.exec_()