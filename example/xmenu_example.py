"""
XMenu Example 菜单组件示例
展示菜单组件的使用
"""
import sys

from xsideui import XIcon, XI18N

try:
    from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout
except ImportError:
    from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from src.xsideui import XLabel, XPushButton, XButtonVariant, XSize, XColor, XWidget, IconName, XMenu



class XMenuExample(XWidget):
    """XMenu Example Window 菜单组件示例窗口"""

    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.set_title("XMenu Demo")
        self.resize(300, 400)
        main_widget = QWidget()
        self.addWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addWidget(XLabel("菜单组件", style=XLabel.Style.H1))

        self._menu_button1 = XPushButton("点击显示菜单", variant=XButtonVariant.SOLID, color=XColor.PRIMARY, size=XSize.DEFAULT)
        self._menu_button1.clicked.connect(self.show_menu)
        main_layout.addWidget(self._menu_button1)

        btn = XPushButton('语言切换')
        btn.clicked.connect(self.chang_langs)
        main_layout.addWidget(btn)

    def chang_langs(self):
        langs = XI18N.current_lang
        if langs == "zh_CN":
            XI18N.set_language("en_US")
        else:
            XI18N.set_language("zh_CN")
        print(langs)




    def show_menu(self):
        """Show basic menu 显示基本菜单"""
        menu = XMenu("菜单", self)

        menu.add_action('New',icon=XIcon.get(name=IconName.FOLDER, color=XColor.PRIMARY, size=16).icon(), triggered=lambda: print('点击了新建'))
        menu.add_action('Open',icon=XIcon.get(IconName.FILE_ADD, size=16).icon(), triggered=lambda: print('点击了打开'))
        menu.add_action('Save',icon=XIcon.get(IconName.SAVE, size=16, color=XColor.PRIMARY).icon(),shortcut='ctrl+s', triggered=lambda: print('点击了保存'))
        menu.addSeparator()
        menu.add_action('Export',icon=XIcon.get(IconName.EXPORT, size=16).icon(), triggered=lambda: print('点击了导出'))
        menu.add_action('Download',icon=XIcon.get(IconName.DOWNLOAD, size=16).icon(), triggered=lambda: print('点击了下载'))
        menu.add_action('Delete',icon=XIcon.get(IconName.DELETE,color=XColor.DANGER, size=16).icon(), triggered=lambda: print('点击了删除'))
        more_menu = menu.add_submenu("More", icon=XIcon.get(IconName.MORE).icon())
        more_menu.add_action("Share", icon=XIcon.get(IconName.SHARE, size=16).icon())
        more_menu.add_action("重命名", icon=XIcon.get(IconName.EDIT, size=16).icon())

        menu.exec_at_widget(self._menu_button1)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    XI18N.set_language("zh_CN")
    window = XMenuExample()
    window.show()
    sys.exit(app.exec_())
