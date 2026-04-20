from typing import Callable, Optional, Union
from ..utils.qt_compat import (QMenu, QAction, QWidget, QApplication, QIcon, QCursor, Qt, QPoint, QEvent)
from ..i18n import XI18N


class XMenu(QMenu):
    """菜单组件"""

    def __init__(self, title: str = "", parent=None):
        """初始化菜单组件。

            Args:
                title: 菜单标题文本。
                parent: 父级组件。
            """
        super().__init__(title, parent)
        self.setWindowFlags(
            Qt.Popup |
            Qt.FramelessWindowHint |
            Qt.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setObjectName("xmenu")

        self.setMouseTracking(True)
        self.setContentsMargins(0, 0, 0, 0)

        self._action_keys = []  # 存储菜单项的翻译键


    def add_action(
            self,
            text: str,
            icon: Optional[Union[QIcon, str]] = None,
            triggered: Optional[Callable] = None,
            shortcut: Optional[str] = None,
    ) -> QAction:
        """
        便捷添加菜单项

        Args:
            text: 菜单项文本或翻译键
            icon: 菜单项图标，支持 QIcon 或图标路径字符串
            triggered: 菜单项点击回调函数
            shortcut: 快捷键字符串，如 "Ctrl+S"

        Returns:
            QAction: 创建的菜单项对象
        """
        self._action_keys.append(text)
        translated = XI18N.x_tr(text)

        if icon:
            action_icon = QIcon(icon) if isinstance(icon, str) else icon
            action = QAction(action_icon, translated, self)
        else:
            action = QAction(translated, self)

        if shortcut:
            action.setShortcut(shortcut)
        if triggered:
            action.triggered.connect(triggered)

        self.addAction(action)
        return action

    def add_submenu(self, title: str, icon: Optional[Union[QIcon, str]] = None) -> 'XMenu':
        """
        便捷添加子菜单

        确保子菜单也继承 XMenu 的圆角和无边框特性

        Args:
            title: 子菜单标题
            icon: 子菜单图标，支持 QIcon 或图标路径字符串

        Returns:
            XMenu: 创建的子菜单对象
        """
        self._action_keys.append(title)
        translated = XI18N.x_tr(title)

        submenu = XMenu(translated, self)
        if icon:
            submenu.setIcon(QIcon(icon) if isinstance(icon, str) else icon)
        self.addMenu(submenu)

        return submenu

    def exec_at_widget(self, widget: QWidget, offset=QPoint(0, 4)):
        """
        在指定控件的下方对齐弹出菜单，并进行屏幕边界检查
        
        Args:
            widget: 目标控件，菜单将显示在该控件下方
            offset: 偏移量，默认向下偏移 4 像素
            
        Returns:
            QAction: 被触发的菜单项，如果没有则返回 None
        """
        if not widget:
            return self.exec_(QCursor.pos())

        gp = widget.mapToGlobal(QPoint(0, widget.height()))
        target_pos = gp + offset

        screen = QApplication.screenAt(QCursor.pos()) or QApplication.primaryScreen()
        if screen:
            available_geo = screen.availableGeometry()
            if target_pos.y() + self.sizeHint().height() > available_geo.bottom():
                target_pos.setY(gp.y() - widget.height() - self.sizeHint().height() - offset.y())

        return self.exec_(target_pos)

    def showEvent(self, event):
        """
        显示事件处理

        显示时确保菜单有最小宽度，避免菜单过窄

        Args:
            event: 显示事件对象
        """
        self.setMinimumWidth(max(self.width(), 160))
        super().showEvent(event)

    def changeEvent(self, event):
        """显式捕获国际化事件"""
        if event.type() == QEvent.LanguageChange:
            # 强制触发刷新
            self.retranslateUi()
        super().changeEvent(event)

    def clear(self):
        super().clear()
        self._action_keys.clear()

    def retranslateUi(self):
        """当语言切换或文本更新时调用"""
        if not self._action_keys:
            return
        actions = self.actions()
        for i, text_key in enumerate(self._action_keys):
            if text_key and i < len(actions):
                translated = XI18N.x_tr(text_key)
                actions[i].setText(translated)


