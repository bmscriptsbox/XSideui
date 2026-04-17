import enum
from typing import Union, Dict

from ..utils.qt_compat import (
    QWidget, Qt, QPoint, QVBoxLayout, QApplication, QTimer, QCursor, QEvent, QGraphicsDropShadowEffect, QColor
)
from .label import XLabel


class XPopover(QWidget):
    """
    高级气泡卡片组件
    
    提供轻量级的提示信息展示，支持多种显示位置和触发方式。
    可用于显示提示信息、帮助文本、下拉菜单等场景。
    """

    _popover_instances: Dict[int, 'XPopover'] = {}

    class Placement(enum.Enum):
        """气泡显示位置枚举"""
        TOP = "top"
        BOTTOM = "bottom"
        LEFT = "left"
        RIGHT = "right"

    class Trigger(enum.Enum):
        """气泡触发方式枚举"""
        HOVER = "hover"
        CLICK = "click"

    def __init__(
            self,
            parent: QWidget = None,
            title: str = None,
            content: str = None,
            placement: Union[Placement, str] = Placement.TOP,
            trigger: Union[Trigger, str] = Trigger.HOVER,
    ):
        """
        初始化气泡卡片组件
        
        Args:
            parent: 父组件
            title: 标题文本
            content: 内容文本
            placement: 显示位置，支持枚举或字符串（top/bottom/left/right）
            trigger: 触发方式，支持枚举或字符串（hover/click）
        """
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("xpopover")

        self._target = None
        self._title = title
        self._content = content
        self._safe_margin = 8

        self._placement = self.Placement(placement.lower()) if isinstance(placement, str) else placement
        self._trigger = self.Trigger(trigger.lower()) if isinstance(trigger, str) else trigger

        self.setMouseTracking(True)
        self._init_ui()
        QApplication.instance().installEventFilter(self)

    def _init_ui(self):
        """初始化用户界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)

        self.container = QWidget(self)
        self.container.setObjectName("popover-container")

        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(12, 8, 12, 8)
        container_layout.setSpacing(4)

        if self._title:
            self.title_label = XLabel(text=self._title)
            self.title_label.setObjectName("title")
            container_layout.addWidget(self.title_label)

        if self._content:
            self.content_label = XLabel(text=self._content)
            self.content_label.setObjectName("content")
            container_layout.addWidget(self.content_label)

        main_layout.addWidget(self.container)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 65))
        shadow.setOffset(0, 2)
        self.container.setGraphicsEffect(shadow)

        self.adjustSize()

    def set_target(self, widget: QWidget):
        """
        设置触发气泡的目标组件
        
        Args:
            widget: 目标组件
        """
        self._target = widget
        self._target.setMouseTracking(True)
        self._target.installEventFilter(self)

    def eventFilter(self, obj, event):
        """
        事件过滤器，处理气泡的显示和隐藏逻辑
        
        Args:
            obj: 事件源对象
            event: 事件对象
            
        Returns:
            bool: 是否拦截事件
        """
        try:
            if not self._target: return False
            self._target.parent()
        except (RuntimeError, AttributeError):
            return False

        if obj == self._target:
            if self._trigger == self.Trigger.HOVER:
                if event.type() == QEvent.Enter:
                    self.show_at_target()
                elif event.type() == QEvent.Leave:
                    QTimer.singleShot(100, self._check_mouse_position)

            elif self._trigger == self.Trigger.CLICK:
                if event.type() == QEvent.MouseButtonPress:
                    if self.isVisible():
                        self.hide()
                    else:
                        self.show_at_target()
                    return True

        elif event.type() == QEvent.MouseButtonPress:
            if self.isVisible():
                cursor_pos = QCursor.pos()
                if not self.geometry().contains(cursor_pos):
                    target_rect = self._target.rect()
                    target_global_pos = self._target.mapToGlobal(QPoint(0, 0))
                    target_global_rect = target_rect.translated(target_global_pos)

                    if not target_global_rect.contains(cursor_pos):
                        self.hide()

        return super().eventFilter(obj, event)

    def _check_mouse_position(self):
        """检查鼠标位置，决定是否隐藏气泡"""
        try:
            if not self._target or not self.isVisible(): return

            cursor_pos = QCursor.pos()
            target_global_rect = self._target.rect().translated(self._target.mapToGlobal(QPoint(0, 0)))

            if not target_global_rect.contains(cursor_pos) and not self.geometry().contains(cursor_pos):
                self.hide()
        except RuntimeError:
            self.hide()

    def show_at_target(self):
        """在目标组件位置显示气泡"""
        try:
            if not self._target or not self._target.isVisible(): return

            for p in list(self._popover_instances.values()):
                if p != self and p.isVisible():
                    p.hide()

            self.adjustSize()
            target_rect = self._target.rect()
            target_pos = self._target.mapToGlobal(QPoint(0, 0))

            if self._placement == self.Placement.TOP:
                x = target_pos.x() + (target_rect.width() - self.width()) // 2
                y = target_pos.y() - self.height() - self._safe_margin
            elif self._placement == self.Placement.BOTTOM:
                x = target_pos.x() + (target_rect.width() - self.width()) // 2
                y = target_pos.y() + target_rect.height() + self._safe_margin
            elif self._placement == self.Placement.LEFT:
                x = target_pos.x() - self.width() - self._safe_margin
                y = target_pos.y() + (target_rect.height() - self.height()) // 2
            else:
                x = target_pos.x() + target_rect.width() + self._safe_margin
                y = target_pos.y() + (target_rect.height() - self.height()) // 2

            screen = QApplication.screenAt(QCursor.pos()) or QApplication.primaryScreen()
            if screen:
                geo = screen.availableGeometry()
                x = max(geo.left(), min(x, geo.right() - self.width()))
                y = max(geo.top(), min(y, geo.bottom() - self.height()))

            self.move(x, y)
            super().show()
        except RuntimeError:
            pass

    def cleanup(self):
        """安全清理资源"""
        for tid, inst in list(self._popover_instances.items()):
            if inst == self:
                self._popover_instances.pop(tid, None)
                break

        try:
            if self._target:
                self._target.removeEventFilter(self)
        except (RuntimeError, TypeError, AttributeError):
            pass

        QApplication.instance().removeEventFilter(self)
        self._target = None
        self.deleteLater()

    @classmethod
    def show_popover(cls, target: QWidget, content: str, title: str = None,
                     placement: Union[Placement, str] = "top",
                     trigger: Union[Trigger, str] = "hover") -> "XPopover":
        """
        显示气泡卡片（类方法）
        
        Args:
            target: 目标组件
            content: 内容文本
            title: 标题文本
            placement: 显示位置，支持枚举或字符串（top/bottom/left/right）
            trigger: 触发方式，支持枚举或字符串（hover/click）
            
        Returns:
            XPopover: 气泡实例
        """
        target_id = id(target)

        if target_id in cls._popover_instances:
            inst = cls._popover_instances[target_id]
            try:
                inst.parent()
                inst._title = title
                inst._content = content
                for i in reversed(range(inst.layout().count())):
                    inst.layout().itemAt(i).widget().setParent(None)
                inst._init_ui()
                return inst
            except (RuntimeError, AttributeError):
                cls._popover_instances.pop(target_id)

        popover = cls(
            parent=target.window(),
            title=title,
            content=content,
            placement=placement,
            trigger=trigger
        )
        popover.set_target(target)
        cls._popover_instances[target_id] = popover

        if popover._trigger == popover.Trigger.HOVER:
            pass

        return popover
