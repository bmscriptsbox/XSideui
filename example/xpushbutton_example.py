"""
XPushButton Example 按钮组件示例
展示不同变体、颜色和尺寸的按钮
"""
import sys

from xsideui import XI18N

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea

from src.xsideui import (
    XLabel, XPushButton, XGroupBox, IconName, XPushButtonGroup, XPushButtonDropdown, XButtonVariant,
    XColor, XSize, XWidget
)


class XPushButtonExample(XWidget):
    """XPushButton Example Window 按钮组件示例窗口"""

    def __init__(self):
        super().__init__()
        self.set_title("XPushButton Demo")
        self.resize(800, 800)
        self.setup_ui()

    def setup_ui(self):
        """Setup user interface 设置用户界面"""

        central_widget = QWidget()
        self.addWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(11)
        main_layout.setContentsMargins(11, 11, 11, 11)
        main_layout.addWidget(XLabel(" 按钮组件", style=XLabel.Style.H1))

        main_layout.addWidget(self.create_variants_section())
        main_layout.addWidget(self.create_icon_section())
        main_layout.addWidget(self.create_size_section())
        main_layout.addWidget(self.create_loading_section())
        main_layout.addWidget(self.create_group_section())
        main_layout.addWidget(self.create_dropdown_section())

        main_layout.addStretch()

    def create_variants_section(self) -> XGroupBox:
        """基础按钮"""
        group = XGroupBox("基础用法")

        layout = QVBoxLayout()
        layout.setSpacing(11)

        variants = [
            (XButtonVariant.SOLID, "Solid"),
            (XButtonVariant.OUTLINED, "Outlined"),
            (XButtonVariant.FILLED, "Filled"),
            (XButtonVariant.TEXT, "Text"),
            (XButtonVariant.LINK, "Link"),
        ]

        primary_layout = QHBoxLayout()
        primary_layout.setSpacing(11)
        for variant, text in variants:
            btn = XPushButton(text, variant=variant, color=XColor.PRIMARY, size=XSize.DEFAULT, icon='sync')
            primary_layout.addWidget(btn)

        success_layout = QHBoxLayout()
        success_layout.setSpacing(11)
        for variant, text in variants:
            btn = XPushButton(text, variant=variant, color=XColor.SUCCESS, size=XSize.DEFAULT, icon=IconName.CHECK)
            success_layout.addWidget(btn)

        warning_layout = QHBoxLayout()
        warning_layout.setSpacing(11)
        for variant, text in variants:
            btn = XPushButton(text, variant=variant, color=XColor.WARNING, size=XSize.DEFAULT, icon=IconName.WARNING)
            warning_layout.addWidget(btn)

        danger_layout = QHBoxLayout()
        danger_layout.setSpacing(11)
        for variant, text in variants:
            btn = XPushButton(text, variant=variant, color=XColor.DANGER, size=XSize.DEFAULT, icon=IconName.DELETE)
            danger_layout.addWidget(btn)

        secondary_layout = QHBoxLayout()
        secondary_layout.setSpacing(11)
        for variant, text in variants:
            btn = XPushButton(text, variant=variant, color=XColor.SECONDARY, size=XSize.DEFAULT, icon=IconName.LINK)
            secondary_layout.addWidget(btn)

        tertiary_layout = QHBoxLayout()
        tertiary_layout.setSpacing(11)
        for variant, text in variants:
            btn = XPushButton(text, variant=variant, color=XColor.TERTIARY, size=XSize.DEFAULT, icon=IconName.PAUSE)
            tertiary_layout.addWidget(btn)

        layout.addLayout(primary_layout)
        layout.addLayout(success_layout)
        layout.addLayout(warning_layout)
        layout.addLayout(danger_layout)
        layout.addLayout(secondary_layout)
        layout.addLayout(tertiary_layout)
        group.setLayout(layout)

        return group

    def create_size_section(self):
        """各尺寸"""
        group = XGroupBox("各尺寸")
        layout = QHBoxLayout()
        layout.setSpacing(11)
        layout.setContentsMargins(11, 11, 11, 11)

        layout.addWidget(XPushButton("Large", size=XSize.LARGE, icon=IconName.SEARCH))
        layout.addWidget(XPushButton("Default", size=XSize.DEFAULT, icon=IconName.SEARCH))
        layout.addWidget(XPushButton("Small", size=XSize.SMALL, icon=IconName.SEARCH))
        layout.addWidget(XPushButton("Mini", size=XSize.MINI, icon=IconName.SEARCH))
        layout.addStretch()
        group.setLayout(layout)
        return group

    def create_icon_section(self):
        """图标按钮"""
        group = XGroupBox("图标按钮")
        layout = QVBoxLayout()
        content_layout = QHBoxLayout()
        content_layout.setSpacing(11)

        content_layout.addWidget(XPushButton(icon=IconName.EDIT))
        content_layout.addWidget(XPushButton(icon=IconName.SHARE))
        content_layout.addWidget(XPushButton(icon=IconName.DELETE))
        content_layout.addWidget(XPushButton(icon=IconName.SEARCH, text="搜索"))
        content_layout.addWidget(XPushButton(icon=IconName.UPLOAD, text="上传").set_icon_position('right'))
        content_layout.addStretch()

        layout.addLayout(content_layout)
        group.setLayout(layout)
        return group

    def create_loading_section(self) -> XGroupBox:
        """加载状态"""
        group = XGroupBox("加载状态 / 会阻止鼠标点击")
        layout = QVBoxLayout()
        content_layout = QHBoxLayout()
        content_layout.setSpacing(11)

        btn = XPushButton('处理中..', variant=XButtonVariant.SOLID, color=XColor.PRIMARY)
        btn.set_loading(True)

        btn1 = XPushButton('处理中..', variant=XButtonVariant.FILLED, color=XColor.SUCCESS)
        btn1.set_loading(True)

        btn3 = XPushButton('处理中..', variant=XButtonVariant.OUTLINED, color=XColor.WARNING)
        btn3.set_loading(True)

        btn4 = XPushButton('处理中..', variant=XButtonVariant.TEXT, color=XColor.DANGER)
        btn4.set_loading(True)

        content_layout.addWidget(btn)
        content_layout.addWidget(btn1)
        content_layout.addWidget(btn3)
        content_layout.addWidget(btn4)
        content_layout.addStretch()

        layout.addLayout(content_layout)
        group.setLayout(layout)

        return group

    def create_group_section(self) -> XGroupBox:
        """按钮组"""
        group = XGroupBox("按钮组")

        layout = QVBoxLayout()
        content_layout = QHBoxLayout()

        group_btn1 = XPushButtonGroup(spacing=1, vertical=False)
        fist_btn = XPushButton('上一页', icon=IconName.LEFT_ARROW)
        right_btn = XPushButton('下一页', icon=IconName.RIGHT_ARROW).set_icon_position('right')
        group_btn1.add_button(fist_btn)
        group_btn1.add_button(right_btn)

        group_btn2 = XPushButtonGroup(spacing=1, vertical=False)
        group_btn2.add_button(XPushButton(icon=IconName.EDIT))
        group_btn2.add_button(XPushButton(icon=IconName.CHECK))
        group_btn2.add_button(XPushButton(icon=IconName.DELETE))
        content_layout.addWidget(group_btn1)
        content_layout.addWidget(group_btn2)
        content_layout.addStretch()

        layout.addLayout(content_layout)
        group.setLayout(layout)

        return group

    def create_dropdown_section(self) -> XGroupBox:
        """下拉按钮"""
        group = XGroupBox("下拉按钮")

        layout = QVBoxLayout()
        content_layout = QHBoxLayout()

        # 1. 定义菜单数据
        items = [
            {"text": "居中显示", "value": "center"},
            {"text": "右上显示", "value": "top_right"},
            {"text": "左上显示", "value": "top_left"},
            {"text": "右下显示", "value": "bottom_right"},
            {"text": "左下显示", "value": "bottom_left"},
        ]

        # 2. 实例化按钮
        dropdown = XPushButtonDropdown(
            text="操作",
            menu_items=items,  # 传入数据
            variant=XButtonVariant.SOLID,
            color=XColor.PRIMARY,
            icon=IconName.TOOL
        )

        # 3. 监听点击
        dropdown.menuTriggered.connect(lambda data: print(f"触发了下拉项目: {data}"))
        dropdown.clicked.connect(lambda: print(f"点击了主按钮"))

        content_layout.addWidget(dropdown)
        content_layout.addStretch()

        layout.addLayout(content_layout)
        group.setLayout(layout)

        return group


if __name__ == "__main__":
    app = QApplication(sys.argv)
    XI18N.set_language("zh_CN")
    # theme_manager.set_primary_colors({
    #     "light": "#ab7ae0",
    #     "dark": "#51258f"
    # })

    window = XPushButtonExample()
    window.show()

    sys.exit(app.exec_())
