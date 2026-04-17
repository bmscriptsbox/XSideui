"""Slider Component 滑块组件

A customizable slider component with advanced features.
一个功能丰富的可自定义滑块组件。
"""

from typing import Union
from collections import OrderedDict
from ..utils.qt_compat import Qt, QPropertyAnimation, Property, QPoint, QRectF, QSize, QEasingCurve, QPainter, QColor, QPen, QPixmap, QSlider, QToolTip
from ..theme import theme_manager
from ..xenum import XColor

MAX_CACHE_SIZE = 50


class XSliderCache:
    """滑块全局缓存管理器（LRU 缓存）"""
    _cache = OrderedDict()

    @classmethod
    def get_cache_key(cls, color: QColor, fill_color: QColor, bg_color: QColor, enabled: bool, size: float) -> tuple:
        return (color.name(), fill_color.name(), bg_color.name(), enabled, size)

    @classmethod
    def get_handle_pixmap(cls, color: QColor, fill_color: QColor, bg_color: QColor, enabled: bool,
                          size: float) -> QPixmap:
        key = cls.get_cache_key(color, fill_color, bg_color, enabled, size)
        if key in cls._cache:
            cls._cache.move_to_end(key)
            return cls._cache[key]

        pix_size = int(size + 4)
        pixmap = QPixmap(pix_size, pix_size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHints(QPainter.Antialiasing)

        rect = QRectF(2, 2, size, size)

        if not enabled:
            painter.setBrush(fill_color)
            painter.setPen(Qt.NoPen)
        else:
            painter.setBrush(bg_color)
            pen = QPen(color)
            pen.setWidth(2)
            painter.setPen(pen)

        painter.drawEllipse(rect)
        painter.end()

        cls._cache[key] = pixmap
        if len(cls._cache) > MAX_CACHE_SIZE:
            cls._cache.popitem(last=False)
        return pixmap

    @classmethod
    def get_highlight_pixmap(cls, color: QColor, size: float, scale: float) -> QPixmap:
        alpha = int(60 * (scale - 1.0) * 4)
        key = (color.name(), size, alpha)

        if key in cls._cache:
            cls._cache.move_to_end(key)
            return cls._cache[key]

        margin = int(size * 0.6)
        pix_size = int(size + margin * 2)
        pixmap = QPixmap(pix_size, pix_size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHints(QPainter.Antialiasing)

        c = QColor(color)
        c.setAlpha(min(alpha, 50))
        painter.setBrush(c)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(0, 0, pix_size, pix_size))
        painter.end()

        cls._cache[key] = pixmap
        return pixmap


class XSlider(QSlider):
    """滑块组件"""

    def __init__(self, orientation=Qt.Horizontal, value=0, minimum=0, maximum=100,
                 step=1, color: Union[XColor, str] = XColor.PRIMARY, groove_height=6, show_tooltip=True, parent=None):
        """初始化滑块组件

        Args:
            orientation: 滑块方向（Qt.Horizontal/Qt.Vertical）
            value: 初始值
            minimum: 最小值
            maximum: 最大值
            step: 步长
            color: 滑块颜色（XColor 枚举或字符串）
            groove_height: 轨道高度（像素）
            show_tooltip: 是否显示值提示
            parent: 父组件
        """
        super().__init__(orientation, parent)

        self.setAttribute(Qt.WA_StyledBackground, False)
        self.setContentsMargins(0, 0, 0, 0)

        self._color_name = color.value if isinstance(color, XColor) else color
        self._color = self._parse_color(color)
        self._show_tooltip = show_tooltip
        self.groove_height = groove_height
        self._handle_scale = 1.0

        self.setRange(minimum, maximum)
        self.setValue(value)
        self.setSingleStep(step)
        self.setCursor(Qt.PointingHandCursor)

        self._handle_animation = QPropertyAnimation(self, b"handle_scale", self)
        self._handle_animation.setDuration(250)
        self._handle_animation.setEasingCurve(QEasingCurve.OutQuint)

        theme_manager.theme_changed.connect(self._on_theme_changed)

    def _parse_color(self, color):
        colors = theme_manager.colors
        if not color: return QColor(colors.primary)
        c_name = color.value if isinstance(color, XColor) else str(color).lower()
        color_map = {
            'primary': colors.primary, 'secondary': colors.secondary,
            'success': colors.success, 'warning': colors.warning, 'danger': colors.danger
        }
        return QColor(color_map.get(c_name, c_name))

    @Property(float)
    def handle_scale(self):
        return self._handle_scale

    @handle_scale.setter
    def handle_scale(self, scale):
        self._handle_scale = scale
        self.update()

    def sizeHint(self):
        # 增加垂直空间，确保 1.2 倍手柄放大后不会在上下方向溢出
        h_size = self.groove_height * 3
        # 增加一点 padding，比如 2.5 倍
        needed = int(h_size * 2.5)
        return QSize(200, needed) if self.orientation() == Qt.Horizontal else QSize(needed, 200)

    def paintEvent(self, e):
        painter = QPainter(self)
        render_hints = QPainter.Antialiasing
        if hasattr(QPainter, 'HighQualityAntialiasing'):
            render_hints |= QPainter.HighQualityAntialiasing

        painter.setRenderHints(render_hints)

        colors = theme_manager.colors
        is_hor = self.orientation() == Qt.Horizontal

        W, H = self.width(), self.height()
        gh = self.groove_height
        hd = gh * 3

        # --- 核心策略：轨道彻底铺满 ---
        # 不再留 margin，轨道左右直接顶到 0 和 W
        if is_hor:
            groove_rect = QRectF(0, (H - gh) / 2, W, gh)
            available_len = W
        else:
            groove_rect = QRectF((W - gh) / 2, 0, gh, H)
            available_len = H

        # 1. 绘制背景轨道
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(colors.fill))
        painter.drawRoundedRect(groove_rect, gh / 2, gh / 2)
        # 2. 计算位置
        slider_pos = self.style().sliderPositionFromValue(
            self.minimum(), self.maximum(), self.sliderPosition(), int(available_len)
        )
        # 3. 绘制激活部分
        painter.setBrush(self._color)
        if is_hor:
            active_rect = QRectF(0, groove_rect.y(), slider_pos, gh)
            # 限制 center，防止手柄中心跑到 0 或 W 导致切边
            # 这里的 0.6 是为了给动画预留空间
            handle_margin = (hd / 2) * 1.2
            cx = max(handle_margin, min(slider_pos, W - handle_margin))
            center = QPoint(int(cx), int(H / 2))
        else:
            active_y = H - slider_pos
            active_rect = QRectF(groove_rect.x(), active_y, gh, slider_pos)
            handle_margin = (hd / 2) * 1.2
            cy = max(handle_margin, min(active_y, H - handle_margin))
            center = QPoint(int(W / 2), int(cy))

        painter.drawRoundedRect(active_rect, gh / 2, gh / 2)


        if self._handle_scale > 1.0:
            halo_radius = (hd / 2) * (1 + (self._handle_scale - 1.0) * 1.5)
            halo_color = QColor(self._color)
            halo_color.setAlpha(int(45 * (self._handle_scale - 1.0) * 5))
            painter.setBrush(halo_color)
            painter.setPen(Qt.NoPen)  # 确保光晕没有描边
            painter.drawEllipse(center, halo_radius, halo_radius)


        current_radius = (hd / 2) * self._handle_scale
        if not self.isEnabled():
            painter.setBrush(QColor(colors.fill))
            painter.setPen(Qt.NoPen)
        else:
            painter.setBrush(QColor(colors.bg_1))
            pen = QPen(self._color)
            pen.setWidthF(2.0 * self._handle_scale)
            painter.setPen(pen)

        painter.drawEllipse(center, current_radius, current_radius)



    def _update_value_from_pos(self, pos):
        is_hor = self.orientation() == Qt.Horizontal
        # 必须与 paintEvent 中的计算逻辑完全一致
        max_handle_radius = (self.groove_height * 3 / 2) * 1.2
        margin = max_handle_radius

        total_len = self.width() if is_hor else self.height()
        available = total_len - (margin * 2)

        if is_hor:
            val_pos = pos.x() - margin
        else:
            val_pos = (self.height() - pos.y()) - margin

        # 边界约束：防止点击 margin 区域时数值越界
        val_pos = max(0, min(val_pos, available))

        value = self.style().sliderValueFromPosition(
            self.minimum(), self.maximum(), int(val_pos), int(available)
        )
        self.setValue(value)

        if self._show_tooltip:
            # 这里的 center_px 是相对于起点 margin 的偏移
            pixel_offset = self.style().sliderPositionFromValue(
                self.minimum(), self.maximum(), value, int(available)
            )
            self._show_tooltip_at_position(value, pixel_offset + margin)

    def _show_tooltip_at_position(self, value, center_px):
        if not self._show_tooltip: return
        is_hor = self.orientation() == Qt.Horizontal

        if is_hor:
            local_center = QPoint(int(center_px), int(self.height() / 2))
        else:
            local_center = QPoint(int(self.width() / 2), int(self.height() - center_px))

        global_center = self.mapToGlobal(local_center)

        if is_hor:
            show_pos = global_center - QPoint(0, 65)
        else:
            show_pos = global_center + QPoint(60, 0)

        QToolTip.showText(show_pos, str(value), self)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton: self._update_value_from_pos(e.pos())
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.LeftButton: self._update_value_from_pos(e.pos())
        super().mouseMoveEvent(e)

    def enterEvent(self, e):
        if self.isEnabled():
            self._handle_animation.stop()
            self._handle_animation.setEndValue(1.2)
            self._handle_animation.start()

    def leaveEvent(self, e):
        self._handle_animation.stop()
        self._handle_animation.setEndValue(1.0)
        self._handle_animation.start()

    def _on_theme_changed(self, theme_name):
        self._color = self._parse_color(self._color_name)
        self.update()

    def set_color(self, color: Union[XColor, str]) -> 'XSlider':
        """设置滑块颜色

        Args:
            color: 颜色值（XColor 枚举或字符串）

        Returns:
            XSlider: 返回自身用于链式调用
        """
        self._color_name = color.value if isinstance(color, XColor) else color
        self._color = self._parse_color(color)
        self.update()
        return self

    def set_show_tooltip(self, show: bool) -> 'XSlider':
        """设置是否显示提示框

        Args:
            show: 是否显示提示框

        Returns:
            XSlider: 返回自身用于链式调用
        """
        self._show_tooltip = show
        if not show:
            self.setToolTip("")
        return self
