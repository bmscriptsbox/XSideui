"""
XBadge - 徽章组件模块

提供圆点徽章和文本徽章两种类型，支持自动跟随目标组件定位。
"""
from enum import Enum
from typing import Union, Optional
from ..utils.qt_compat import (QObject, QEvent, Qt, QTimer, QPoint, QRectF, QSize, QPainter, QColor, QFont,
                               QFontMetrics, QLabel, QWidget)

from ..xenum import XColor
from ..theme import theme_manager
from ..i18n import XI18N
from ..icon import XIcon, IconName


class XBadgeManager(QObject):
    def __init__(self, target: QWidget, badge: QWidget, offset: QPoint):
        super().__init__(target)
        self.target = target
        self.badge = badge
        self.offset = offset
        self._parents = []  # 用于记录监听了哪些父容器

        # 监听目标组件
        self.target.installEventFilter(self)

        # 只要任何一级父容器大小变化，target 的绝对位置就可能变
        p = self.target.parentWidget()
        while p:
            p.installEventFilter(self)
            self._parents.append(p)
            p = p.parentWidget()

        # 节流定时器：限制更新频率到 ~60fps
        self._update_timer = QTimer(self)
        self._update_timer.setSingleShot(True)
        self._update_timer.setInterval(16)
        self._update_timer.timeout.connect(self._do_update_position)

        # 初始定位
        QTimer.singleShot(0, self.update_position)

    def cleanup(self):
        """彻底释放监听"""
        if self.target:
            self.target.removeEventFilter(self)
        for p in self._parents:
            try:
                p.removeEventFilter(self)
            except:
                pass
        self._parents.clear()
        self._update_timer.stop()

    def eventFilter(self, obj, event):
        # 只要是移动、缩放、显示、隐藏或者布局请求，都调度更新（带节流）
        if event.type() in [
            QEvent.Move,
            QEvent.Resize,
            QEvent.Show,
            QEvent.LayoutRequest,
            QEvent.WindowStateChange
        ]:
            self._schedule_update()

        # 目标销毁处理
        if obj is self.target and event.type() == QEvent.Destroy:
            if self.badge and not self.badge.isHidden():
                self.badge.deleteLater()
            self.deleteLater()

        return super().eventFilter(obj, event)

    def _schedule_update(self):
        """调度位置更新（带节流）"""
        self._update_timer.start()

    def _do_update_position(self):
        """实际执行位置更新"""
        self.update_position()

    def update_position(self):
        """精准更新徽章位置"""
        # 1. 检查有效性
        if not self.target or not self.badge or self.target.isHidden():
            if self.badge: self.badge.hide()
            return

        target_visible = self.target.isVisible()
        if target_visible:
            p = self.target.parentWidget()
            while p:
                if not p.isVisible():
                    target_visible = False
                    break
                if p.isWindow(): break
                p = p.parentWidget()

        if not target_visible:
            self.badge.hide()
            return

        # 2. 获取徽章相对于其父窗口的坐标
        win = self.badge.parentWidget()
        if not win: return

        # 使用全局坐标中转，消除所有嵌套布局产生的偏移
        rect = self.target.rect()
        anchor_func_name = self.badge.anchor.value
        local_anchor_pos = getattr(rect, anchor_func_name)()
        global_pos = self.target.mapToGlobal(local_anchor_pos)

        # 再将这个屏幕位置转换回窗口内部的相对位置
        anchor = win.mapFromGlobal(global_pos)

        badge_size = self.badge.size()
        custom_offset = self.badge.get_anchor_offset()

        # 3. 计算最终位置
        x = anchor.x() - (badge_size.width() // 2) + custom_offset.x() + self.offset.x()
        y = anchor.y() - (badge_size.height() // 2) + custom_offset.y() + self.offset.y()

        self.badge.move(int(x), int(y))
        self.badge.show()
        self.badge.raise_()


class XBadgeBase(QLabel):
    """
    徽章基类

    提供徽章的通用功能：
    - 自动挂载管理器
    - 颜色解析（带缓存优化）
    - 鼠标事件穿透

    Example:
        >>> class MyBadge(XBadgeBase):
        ...     pass
    """
    # 结构: { target_id: { tag_name: badge_instance } }
    _registry = {}

    class Anchor(Enum):
        TOP_LEFT = "topLeft"
        TOP_RIGHT = "topRight"
        BOTTOM_LEFT = "bottomLeft"
        BOTTOM_RIGHT = "bottomRight"
        CENTER = "center"

    def __init__(self,
                 target: QWidget,
                 tag: str = "default",
                 offset=QPoint(0, 0),
                 anchor=Anchor.TOP_RIGHT,
                 ):
        """初始化徽章

        Args:
            target: 目标组件
            offset: 位置偏移量
            tag: 徽章标识符。如果相同 tag 的徽章已存在，则替换它。
        """
        XBadgeBase.remove_tag_from(target, tag)
        super().__init__(target.window())
        self.target = target
        self.anchor = anchor
        self.tag = tag
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.manager = XBadgeManager(target, self, offset)
        self.show()

        self._color_cache = {}
        theme_manager.theme_changed.connect(self._on_theme_changed)

        tid = id(target)
        if tid not in XBadgeBase._registry:
            XBadgeBase._registry[tid] = {}
        XBadgeBase._registry[tid][tag] = self

    @classmethod
    def remove_tag_from(cls, target: QWidget, tag: str):
        """删除指定 tag 的徽章"""
        tid = id(target)
        if tid in cls._registry and tag in cls._registry[tid]:
            badge = cls._registry[tid].pop(tag)
            badge.detach()
            # 如果该 target 没徽章了，清理掉空字典
            if not cls._registry[tid]:
                cls._registry.pop(tid)

    @classmethod
    def remove_all_from(cls, target: QWidget):
        """删除该组件上所有的徽章"""
        tid = id(target)
        if tid in cls._registry:
            # 必须转成 list 遍历，因为 detach 会修改字典
            tags = list(cls._registry[tid].keys())
            for tag in tags:
                cls.remove_tag_from(target, tag)

    def detach(self):
        """从注册表中把自己摘除并销毁"""
        try:
            theme_manager.theme_changed.disconnect(self._on_theme_changed)
        except:
            pass

        if hasattr(self, 'manager'):
            self.manager.cleanup()

        tid = id(self.target)
        if tid in XBadgeBase._registry and self.tag in XBadgeBase._registry[tid]:
            XBadgeBase._registry[tid].pop(self.tag)
            if not XBadgeBase._registry[tid]:
                XBadgeBase._registry.pop(tid)

        self.hide()
        self.deleteLater()

    def _on_theme_changed(self, theme_name):
        """主题切换回调，清除颜色缓存"""
        self._color_cache.clear()
        self.update()

    def _get_color(self, color: Union[XColor, str, None]) -> QColor:
        """获取颜色（带缓存优化）

        Args:
            color: 颜色值，支持 XColor 枚举、十六进制字符串、颜色名称

        Returns:
            QColor 对象
        """
        if color is None:
            return QColor()

        cache_key = color.value if isinstance(color, XColor) else color

        if cache_key not in self._color_cache:
            resolved = self._resolve_color(color)
            self._color_cache[cache_key] = QColor(resolved) if resolved else QColor()

        return self._color_cache[cache_key]

    def get_anchor_offset(self) -> QPoint:
        """获取锚点偏移

        子类可重写此方法返回自定义偏移量。

        Returns:
            QPoint: 偏移量
        """
        return QPoint(0, 0)

    def _resolve_color(self, color: Union[XColor, str, None]) -> Optional[str]:
        """解析颜色值

        Args:
            color: 颜色值，支持 XColor 枚举、十六进制字符串、颜色名称

        Returns:
            解析后的颜色字符串，如果输入为 None 则返回 None
        """
        if color is None:
            return None

        if isinstance(color, XColor):
            return getattr(theme_manager.colors, color.value, color.value)

        if color.startswith("#"):
            return color

        return getattr(theme_manager.colors, color, color)


class XTextBadge(XBadgeBase):
    """
    文本徽章

    显示为圆角矩形容器包裹的文字，常用于显示数量（如购物车数量、消息未读数）。
    宽度会根据文字内容自动调整。
    支持国际化。

    Example:
        >>> badge = XTextBadge(button, "5", color=XColor.DANGER)
        >>> badge.set_content("99+")
    """

    def __init__(self,
                 target: QWidget,
                 text: str = "0",
                 color: Union[XColor, str] = XColor.SUCCESS,
                 offset: QPoint = QPoint(0, 0),
                 anchor=XBadgeBase.Anchor.TOP_RIGHT,
                 tag: str = "default"):
        """创建并初始化一个带文本内容的徽章组件。

            Args:
                target: 目标组件。徽章将悬浮并定位在该组件之上。
                text: 徽章显示的文字内容（如数字 "99+" 或标签文本）。支持国际化翻译键。
                color: 徽章的背景颜色。支持 XColor 枚举或十六进制颜色字符串。
                offset: 位置偏移量。用于在锚点定位的基础上进行微调，QPoint(x, y)。
                anchor: 锚点位置。决定徽章相对于 target 的对齐方式（如右上、左下等）。
                tag: 唯一标识符。用于在同一个 target 上管理多个不同的徽章。
            """
        super().__init__(target=target, tag=tag, offset=offset, anchor=anchor)
        self._color = color
        self._text_key = text
        self.padding = 12
        self.text_content = ""  # 先给个默认值防止 paintEvent 报错
        self.retranslateUi()

    def sizeHint(self):
        """计算徽章尺寸

        根据文字宽度自动计算合适的尺寸，保证文字不超出徽章边界。

        Returns:
            QSize: 徽章尺寸
        """
        if not hasattr(self, 'text_content') or not self.text_content:
            return QSize(24, 24)
        font = theme_manager.get_font("size_xs", "weight_medium", )
        fm = QFontMetrics(font)
        text_width = fm.horizontalAdvance(self.text_content)
        return QSize(max(26, int(text_width + self.padding + 10)), 24)

    def paintEvent(self, e):
        """绘制文本徽章

        绘制流程：
        1. 底层白色圆角矩形作为边框
        2. 中层彩色圆角矩形作为背景
        3. 顶层白色文字居中显示

        Args:
            e: 绘制事件
        """
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        radius = rect.height() / 3

        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.white)
        painter.drawRoundedRect(rect, radius, radius)

        inner_rect = rect.adjusted(1.5, 1.5, -1.5, -1.5)
        painter.setBrush(self._get_color(self._color))
        painter.drawRoundedRect(inner_rect, radius - 1.5, radius - 1.5)

        painter.setPen(Qt.white)
        font = theme_manager.get_font("size_s", "weight_medium")
        painter.setFont(font)

        painter.drawText(inner_rect, Qt.AlignCenter, self.text_content)

    def set_content(self, text_key: str):
        """更新徽章文字内容

        Args:
            text: 新的文字内容或翻译键
        """
        self._text_key = text_key
        self.retranslateUi()

    def retranslateUi(self):
        """当语言切换或文本更新时调用"""
        if not self._text_key:
            return

        translated = XI18N.x_tr(self._text_key)
        self.text_content = translated

        # 重新计算尺寸
        self.setFixedSize(self.sizeHint())

        # 尺寸变了 通知管理器重新定位
        if hasattr(self, 'manager'):
            # 建议加一个微小的 offset 确保在 Qt 布局生效后执行
            QTimer.singleShot(0, self.manager.update_position)

        self.update()

    def changeEvent(self, event):
        """监听国际化事件"""
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi()
        super().changeEvent(event)


class XIconBadge(XBadgeBase):
    """
    图标徽章

    显示为一个圆角容器包裹的图标。常用于表示某种状态类型（如：警告图标、锁定图标）。
    """

    def __init__(self,
                 target: QWidget,
                 icon_name: Union[str, 'IconName'],  # 直接接收图标名
                 color: Union[XColor, str] = XColor.PRIMARY,
                 size: int = 18,
                 offset: QPoint = QPoint(0, 0),
                 anchor=XBadgeBase.Anchor.TOP_RIGHT,
                 tag: str = "default"):
        """创建并初始化一个带文本内容的徽章组件。

            Args:
                target: 目标组件。徽章将悬浮并定位在该组件之上。
                icon_name: 图标名，枚举IconName的值或字符串。
                color: 徽章的背景颜色。支持 XColor 枚举或十六进制颜色字符串。
                offset: 位置偏移量。用于在锚点定位的基础上进行微调，QPoint(x, y)。
                anchor: 锚点位置。决定徽章相对于 target 的对齐方式（如右上、左下等）。
                tag: 唯一标识符。用于在同一个 target 上管理多个不同的徽章。
            """
        super().__init__(target=target, tag=tag, offset=offset, anchor=anchor)
        self._color = color
        self._icon_name = icon_name
        self.setFixedSize(size, size)

    def set_icon(self, icon_name: Union[str, 'IconName']):
        """动态更新图标名"""
        self._icon_name = icon_name
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        icon_obj = XIcon(self._icon_name, size=self.width(), color=self._color)
        # 根据当前设备的 DPR 获取高清 Pixmap
        pixmap = icon_obj.pixmap(dpr=self.devicePixelRatioF())

        if not pixmap or pixmap.isNull():
            return

        target_rect = self.rect()
        painter.drawPixmap(target_rect, pixmap)
