import sys

from xsideui import XI18N

try:
    from PySide2.QtCore import QTimer, QPoint
    from PySide2.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPushButton)
except ImportError:
    from PySide6.QtCore import QTimer
    from PySide6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QWidget)

from src.xsideui import XColor, XButtonVariant, XPushButton, XWidget, XTextBadge, XIconBadge, XLabel, \
    IconName


class BadgeExampleWindow(XWidget):
    def __init__(self):
        super().__init__()
        self.set_title("XBadge Demo")
        self.resize(800, 600)
        self._init_ui()

    def _init_ui(self):
        content_widget = QWidget()
        self.addWidget(content_widget)

        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(30)

        title = XLabel("XBadge 徽章组件示例", style=XLabel.Style.H2)
        main_layout.addWidget(title)

        main_layout.addWidget(self._create_color_section())
        main_layout.addWidget(self._create_text_section())
        main_layout.addWidget(self._create_icon_section())

        clear_button = XPushButton("清理徽章")
        clear_button.clicked.connect(self._on_clear_button_clicked)
        main_layout.addWidget(clear_button)
        QTimer.singleShot(0, self._create_badges)

    def _create_color_section(self):
        section = QWidget()
        layout = QVBoxLayout(section)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        layout.addWidget(XLabel("多标签/多锚点", style=XLabel.Style.H4))

        colors = [
            (XColor.PRIMARY, "主要"),
            (XColor.SUCCESS, "成功"),
            (XColor.WARNING, "警告"),
            (XColor.DANGER, "危险"),
            (XColor.SECONDARY, "次要"),
            (XColor.TERTIARY, "浅色"),
        ]

        row = QHBoxLayout()
        row.setSpacing(20)

        self.color_buttons = []
        for color, name in colors:
            btn = XPushButton(name,variant=XButtonVariant.OUTLINED,color=XColor.TERTIARY)
            self.color_buttons.append((btn, color, name))
            row.addWidget(btn)

        layout.addLayout(row)
        return section

    def _create_text_section(self):
        section = QWidget()
        layout = QVBoxLayout(section)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        layout.addWidget(XLabel("文字/数字徽章", style=XLabel.Style.H4))

        row = QHBoxLayout()
        row.setSpacing(20)

        texts = ["1", "99", "999+", "消息", "New", "HOT"]
        self.text_buttons = []
        for text in texts:
            btn = XPushButton(text)
            self.text_buttons.append(btn)
            row.addWidget(btn)

        layout.addLayout(row)
        return section

    def _create_icon_section(self):
        section = QWidget()
        layout = QVBoxLayout(section)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        layout.addWidget(XLabel("图标徽章", style=XLabel.Style.H4))

        colors = [
            (XColor.PRIMARY, "置顶", IconName.PIN_FILL),
            (XColor.SUCCESS, "收藏", IconName.STAR_FILL),
            (XColor.WARNING, "点赞", IconName.LIKE_FILL),
            (XColor.DANGER, "消息", IconName.DOT),
            (XColor.DANGER, "离线", IconName.REMIND_FILL),
        ]

        row = QHBoxLayout()
        row.setSpacing(20)

        self.dot_buttons = []
        for color, name, icon in colors:
            btn = XPushButton(text=name, variant=XButtonVariant.OUTLINED, color=XColor.SECONDARY)
            self.dot_buttons.append((btn, color))
            row.addWidget(btn)
        layout.addLayout(row)
        return section

    def _create_badges(self):
        """创建徽章"""
        for btn, color, name in self.color_buttons:
            # 多徽章，多锚点
            XTextBadge(btn, name, color=color,offset=QPoint(-10, 0),tag="message")
            XIconBadge(btn, IconName.LIKE_FILL, color=XColor.DANGER, tag="icon", anchor=XTextBadge.Anchor.BOTTOM_LEFT, size=14,offset=QPoint(10, -10))

        for btn in self.text_buttons:
            XTextBadge(btn, btn.text(), color=XColor.DANGER, tag="text")

        for  btn, color in self.dot_buttons:
            XIconBadge(btn, IconName.PIN_FILL, color=XColor.TERTIARY, size=14, offset=QPoint(-10, 10))

    def _on_clear_button_clicked(self):
        """清理徽章"""
        for btn, color, name in self.color_buttons:
            # 只清除tag为two的徽章
            XTextBadge.remove_tag_from(btn,'icon')
        for btn in self.text_buttons:
            # 清理所有徽章
            XTextBadge.remove_all_from(btn)
        for btn, color in self.dot_buttons:
            # 清理所有徽章
            XIconBadge.remove_all_from(btn)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    XI18N.set_language("zh_CN")
    window = BadgeExampleWindow()
    window.show()
    sys.exit(app.exec_())
