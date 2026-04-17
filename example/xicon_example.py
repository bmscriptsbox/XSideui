#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""XIcon 图标组件使用示例

展示在各种 PySide2 组件中使用 XIcon 的方法
"""

import sys
try:
    from PySide2.QtCore import Qt, QSize
    from PySide2.QtWidgets import (QApplication,  QWidget, QVBoxLayout, QHBoxLayout,QLabel)
except ImportError:
    from PySide6.QtCore import Qt, QSize
    from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton)

from src.xsideui import XIcon, IconName, XWidget, XLabel, XDivider, XPushButton, XButtonVariant, xicon_theme_adapter, theme_manager
from src.xsideui import XColor


class IconExampleWindow(XWidget):
    """图标使用示例窗口"""

    def __init__(self):
        super().__init__()
        print(f"DEBUG [窗口连接时]: Manager ID = {id(theme_manager)}")
        self._init_ui()
        theme_manager.theme_changed.connect(self._on_theme_changer)




    def _on_theme_changer(self):
        self.tool_btn.setIcon(XIcon.get(IconName.SETTING, size=48, color=XColor.SECONDARY).icon())

    def _init_ui(self):
        self.set_title("XIcon 图标使用示例")
        self.hide_minimize_button()
        self.hide_maximize_button()
        self.resize(600, 600)

        content_widget = QWidget(self)
        self.addWidget(content_widget)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # QIcon 示例
        content_layout.addWidget(XLabel('QIcon 示例 ', style=XLabel.Style.H4))
        content_layout.addWidget(XDivider())

        qicon_layout = QHBoxLayout()
        self.tool_btn = QPushButton()
        # 获取图标和设置图标用意义的尺寸。这样图标在自适应dpr时能始终保持清晰
        # 原始按键设置图标需要自己写主题变化、通过接受主题变化信号。重新为按钮设置图标。从而实现图标明暗变化
        self.tool_btn.setIcon(XIcon.get(IconName.SETTING, size=48, color=XColor.SECONDARY).icon())
        self.tool_btn.setIconSize(QSize(48, 48))
        qicon_layout.addWidget(self.tool_btn)
        content_layout.addLayout(qicon_layout)
        #
        # QPixmap 示例
        content_layout.addWidget(XLabel('QPixmap 示例 ', style=XLabel.Style.H4))
        content_layout.addWidget(XDivider())
        qpixmap_layout = QHBoxLayout()
        pixmap_label1 = QLabel()
        pixmap1 = XIcon.get(IconName.HOME, size=32, color=XColor.PRIMARY).pixmap()
        pixmap_label1.setPixmap(pixmap1)
        qpixmap_layout.addWidget(pixmap_label1)

        # 使用 QPixmap 在 QLabel 中显示
        pixmap_label2 = QLabel()
        pixmap_label2.setPixmap(XIcon(IconName.USER, size=32, color=XColor.SUCCESS).pixmap())
        qpixmap_layout.addWidget(pixmap_label2)

        # 使用 QPixmap 在 QLabel 中显示
        pixmap_label3 = QLabel()
        pixmap3 = XIcon.get(IconName.UP, size=32, color=XColor.WARNING).pixmap()
        pixmap_label3.setPixmap(pixmap3)
        qpixmap_layout.addWidget(pixmap_label3)

        qpixmap_layout.addStretch()
        content_layout.addLayout(qpixmap_layout)

        content_layout.addStretch()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IconExampleWindow()
    window.show()
    sys.exit(app.exec_())
