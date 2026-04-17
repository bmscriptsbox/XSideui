"""进度条组件"""

from typing import Union
from collections import OrderedDict
from ..utils.qt_compat import (QPainter, QColor, QPen, QProgressBar, Qt, QRectF, QPixmap, QTimer, QVariantAnimation,
                               QEasingCurve)
from ..theme import theme_manager
from ..xenum import XColor

MAX_CACHE_SIZE = 50
UPDATE_INTERVAL = 16
ANIMATION_DURATION = 300


def _parse_color_value(color, color_map: dict) -> str:
    """解析颜色值，支持枚举和字符串格式"""
    if isinstance(color, XColor):
        return color_map.get(color.value, color)
    elif color in color_map:
        return color_map[color]
    else:
        return color


class XProgressBarCache:
    """线性进度条全局缓存管理器（LRU 缓存）"""

    _cache = OrderedDict()

    @classmethod
    def get_cache_key(cls, width: int, height: int, radius: int, progress: float,
                      enabled: bool, color: str, dpr: float) -> tuple:
        """生成缓存键（不包含文本以提高缓存命中率）"""
        return (width, height, radius, progress, enabled, color, dpr)

    @classmethod
    def get_pixmap(cls, width: int, height: int, radius: int, progress: float,
                   enabled: bool, color: str, theme, dpr: float) -> QPixmap:
        """获取或创建缓存的 QPixmap（不包含文本）"""
        key = cls.get_cache_key(width, height, radius, progress, enabled, color, dpr)

        if key in cls._cache:
            cls._cache.move_to_end(key)
            return cls._cache[key]

        pixmap = QPixmap(int(width * dpr), int(height * dpr))
        pixmap.setDevicePixelRatio(dpr)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        bg_color = QColor(color)
        bg_color.setAlphaF(0.1)
        painter.setBrush(bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, width, height, radius, radius)

        if progress > 0:
            progress_width = int(width * progress)
            if progress_width < height:
                progress_width = height
            painter.setBrush(QColor(color))
            painter.drawRoundedRect(0, 0, progress_width, height, radius, radius)

        painter.end()

        if len(cls._cache) >= MAX_CACHE_SIZE:
            cls._cache.popitem(last=False)

        cls._cache[key] = pixmap
        return pixmap

    @classmethod
    def clear_cache(cls):
        """清除所有缓存"""
        cls._cache.clear()


class XCircleProgressCache:
    """圆形进度条全局缓存管理器（LRU 缓存）"""

    _cache = OrderedDict()

    @classmethod
    def get_cache_key(cls, size: int, stroke_width: int, progress: float,
                      enabled: bool, color: str, bg_color: str, dpr: float) -> tuple:
        """生成缓存键（不包含文本以提高缓存命中率）"""
        return (size, stroke_width, progress, enabled, color, bg_color, dpr)

    @classmethod
    def get_pixmap(cls, size: int, stroke_width: int, progress: float,
                   enabled: bool, color: str, bg_color: str, theme, dpr: float) -> QPixmap:
        """获取或创建缓存的 QPixmap（不包含文本）"""
        key = cls.get_cache_key(size, stroke_width, progress, enabled, color, bg_color, dpr)

        if key in cls._cache:
            cls._cache.move_to_end(key)
            return cls._cache[key]

        pixmap = QPixmap(int(size * dpr), int(size * dpr))
        pixmap.setDevicePixelRatio(dpr)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHints(
            QPainter.Antialiasing |
            QPainter.SmoothPixmapTransform |
            QPainter.TextAntialiasing
        )

        rotate_angle = 360 * progress
        margin = stroke_width + 1
        rect = QRectF(margin, margin, size - 2 * margin, size - 2 * margin)

        pen = QPen()
        pen.setWidth(stroke_width)
        pen.setCapStyle(Qt.RoundCap)
        pen.setStyle(Qt.SolidLine)

        bg_pen_color = QColor(bg_color)
        bg_pen_color.setAlphaF(0.2)
        pen.setColor(bg_pen_color)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(rect)

        progress_color = QColor(color if enabled else theme.colors.text_3)
        pen.setColor(progress_color)
        painter.setPen(pen)
        painter.drawArc(rect, 90 * 16, -rotate_angle * 16)

        painter.end()

        if len(cls._cache) >= MAX_CACHE_SIZE:
            cls._cache.popitem(last=False)

        cls._cache[key] = pixmap
        return pixmap

    @classmethod
    def clear_cache(cls):
        """清除所有缓存"""
        cls._cache.clear()


class XProgressBarBase:
    """进度条基类"""

    def _get_color_map(self) -> dict:
        """获取颜色映射字典"""
        return {
            'primary': theme_manager.colors.primary,
            'success': theme_manager.colors.success,
            'warning': theme_manager.colors.warning,
            'danger': theme_manager.colors.danger,
            'tertiary': theme_manager.colors.tertiary,
            'secondary': theme_manager.colors.secondary,
        }

    def _parse_color(self, color) -> str:
        """解析颜色参数，支持枚举和字符串"""
        return _parse_color_value(color, self._get_color_map())

    def _on_theme_changed(self, theme_name):
        """主题变化时清除缓存并更新显示"""
        self._clear_cache()
        self.update()

    def _schedule_update(self):
        """调度更新（节流）"""
        if hasattr(self, '_update_timer'):
            self._update_timer.start()

    def closeEvent(self, event):
        """处理关闭事件，断开信号连接"""
        try:
            theme_manager.theme_changed.disconnect(self._on_theme_changed)
        except (TypeError, RuntimeError):
            pass
        super().closeEvent(event)


class XProgressBar(QProgressBar, XProgressBarBase):
    """线性进度条组件
    支持不同颜色、尺寸、文本位置和动画的可自定义线性进度条。
    """

    DEFAULT_HEIGHT = 6

    def __init__(
            self,
            value: int = 0,
            minimum: int = 0,
            maximum: int = 100,
            height: int = DEFAULT_HEIGHT,
            color: Union[XColor, str] = 'primary',
            text_visible: bool = True,
            text_position: str = 'center',
            animation_enabled: bool = True,
            parent=None
    ):
        """初始化进度条

        Args:
            value: 初始值
            minimum: 最小值
            maximum: 最大值
            height: 进度条高度（像素）
            color: 进度条颜色（Color枚举、预设名称或颜色值）
            text_visible: 是否显示百分比文本
            text_position: 文本位置（'center'居中, 'right'右侧）
            animation_enabled: 是否启用动画
            parent: 父组件
        """
        super().__init__(parent)
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.setAttribute(Qt.WA_StaticContents, True)
        self._height = height
        self._color = self._parse_color(color)
        self._text_position = text_position
        self._animation_enabled = animation_enabled
        self._current_progress = value / maximum if maximum > 0 else 0
        self._target_progress = self._current_progress
        self._animation = None

        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.setValue(value)
        self.setTextVisible(text_visible)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(self._height)
        self.setMaximumHeight(self._height)

        self.setObjectName("xprogressbar")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._update_timer = QTimer(self)
        self._update_timer.setSingleShot(True)
        self._update_timer.setInterval(UPDATE_INTERVAL)
        self._update_timer.timeout.connect(self.update)

        theme_manager.theme_changed.connect(self._on_theme_changed)

    def _clear_cache(self):
        """清除缓存"""
        XProgressBarCache.clear_cache()

    def _start_animation(self, target_value: int):
        """启动动画"""
        if not self._animation_enabled:
            self._current_progress = target_value / self.maximum() if self.maximum() > 0 else 0
            self._schedule_update()
            return

        if self._animation is not None:
            self._animation.stop()

        target_progress = target_value / self.maximum() if self.maximum() > 0 else 0
        self._animation = QVariantAnimation(self)
        self._animation.setDuration(ANIMATION_DURATION)
        self._animation.setStartValue(self._current_progress)
        self._animation.setEndValue(target_progress)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        self._animation.valueChanged.connect(self._on_animation_value_changed)
        self._animation.finished.connect(self._on_animation_finished)
        self._animation.start()

    def _on_animation_value_changed(self, value):
        """动画值变化回调"""
        self._current_progress = value
        if not self._update_timer.isActive():
            self._schedule_update()
        # self._schedule_update()

    def _on_animation_finished(self):
        """动画完成回调"""
        self._current_progress = self._target_progress
        self._animation = None
        self.update()

    def set_color(self, color: Union[XColor, str]):
        """设置进度条颜色

        Args:
            color: 颜色值，支持以下格式：
                - Color 枚举：XColor.PRIMARY, XColor.SUCCESS 等
                - 预设颜色：'primary', 'success', 'warning', 'danger' 等
                - 自定义颜色值：'#FF0000', 'rgb(255, 0, 0)' 等

        Returns:
            self: 返回自身，支持链式调用

        Examples:
            >>> progress.set_color(XColor.SUCCESS)  # 使用枚举
            >>> progress.set_color('success')  # 使用预设字符串
            >>> progress.set_color('#FF0000')  # 使用自定义红色
        """
        self._color = self._parse_color(color)
        self._schedule_update()
        return self

    def set_height(self, height: int):
        """设置进度条高度

        Args:
            height: 进度条高度（像素），最小值为 4px
                    推荐值：6px（无文本），16px（带文本）

        Returns:
            self: 返回自身，支持链式调用

        Examples:
            >>> progress = XProgressBar()
            >>> progress.set_height(6)              # 无文本的小型进度条
            >>> progress.set_height(16)             # 带文本的标准进度条
            >>> progress.set_height(6).set_color('success')  # 链式调用

        Note:
            高度设置会影响进度条的圆角大小，圆角为高度的一半
        """
        self._height = max(4, height)
        self.setMinimumHeight(self._height)
        self.setMaximumHeight(self._height)
        self._schedule_update()
        return self

    def set_text_position(self, position: str):
        """设置文本位置

        Args:
            position: 文本位置
                - 'center': 居中显示（默认）
                - 'right': 右侧显示

        Returns:
            self: 返回自身，支持链式调用

        Examples:
            >>> progress = XProgressBar()
            >>> progress.set_text_position('center')  # 居中
            >>> progress.set_text_position('right')   # 右侧
        """
        if position in ('center', 'right'):
            self._text_position = position
            self._schedule_update()
        return self

    def set_animation_enabled(self, enabled: bool):
        """设置是否启用动画

        Args:
            enabled: 是否启用动画

        Returns:
            self: 返回自身，支持链式调用

        Examples:
            >>> progress = XProgressBar()
            >>> progress.set_animation_enabled(True)   # 启用动画
            >>> progress.set_animation_enabled(False)  # 禁用动画
        """
        self._animation_enabled = enabled
        return self

    def _get_border_radius(self) -> int:
        """计算圆角大小"""
        return self._height // 2

    def resizeEvent(self, event):
        """重写 resizeEvent，确保窗口大小改变时重新绘制"""
        super().resizeEvent(event)
        self.update()

    def setValue(self, value: int):
        # 如果值没变，不做操作
        if value == self.value():
            return self

        super().setValue(value)
        self._target_progress = value / self.maximum() if self.maximum() > 0 else 0

        # --- 优化逻辑 ---
        # 如果目标是 100% 或者是 0%，且你希望立即重置不被打断
        # 我们可以判断：如果当前值是最大值，强制让当前进度等于目标
        if value == self.maximum() or value == self.minimum():
            if self._animation:
                self._animation.stop()
            self._current_progress = self._target_progress
            self.update()
        else:
            self._start_animation(value)

        return self

    # def setValue(self, value: int):
    #     """重写 setValue 方法，支持动画"""
    #     super().setValue(value)
    #     self._target_progress = value / self.maximum() if self.maximum() > 0 else 0
    #     self._start_animation(value)
    #     return self

    def paintEvent(self, event):
        """重写绘制事件，使用全局缓存"""
        width = self.width()
        height = self.height()
        radius = self._get_border_radius()
        enabled = self.isEnabled()
        text_visible = self.isTextVisible()
        dpr = self.devicePixelRatioF()

        display_progress = round(self._current_progress, 3)
        if self.value() == self.maximum():
            display_progress = 1.0
        pixmap = XProgressBarCache.get_pixmap(
            width, height, radius, display_progress,
            self.isEnabled(), self._color, theme_manager, dpr
        )

        painter = QPainter(self)
        painter.drawPixmap(0, 0, pixmap)

        if text_visible:
            text = f"{int(self._current_progress * 100)}%"
            text_color = QColor(theme_manager.colors.text_2 if enabled else theme_manager.text_3)
            painter.setPen(text_color)

            font = theme_manager.get_font("size_s", "weight_medium")
            painter.setFont(font)

            if self._text_position == 'center':
                painter.drawText(pixmap.rect(), Qt.AlignCenter, text)
            else:
                text_rect = QRectF(width - 60, 0, 60, height)
                painter.drawText(text_rect, Qt.AlignCenter, text)


class XCircleProgress(QProgressBar, XProgressBarBase):
    """圆形进度条组件
    支持不同颜色、尺寸和动画的可自定义圆形进度条。
    """

    DEFAULT_SIZE = 100

    def __init__(
            self,
            value: int = 0,
            minimum: int = 0,
            maximum: int = 100,
            size: int = DEFAULT_SIZE,
            color: Union[XColor, str] = 'primary',
            text_visible: bool = True,
            animation_enabled: bool = True,
            parent=None
    ):
        """初始化圆形进度条

        Args:
            value: 初始值
            minimum: 最小值
            maximum: 最大值
            size: 直径（像素）
            color: 进度颜色（Color枚举、预设名称或颜色值）
            text_visible: 是否显示百分比文本
            animation_enabled: 是否启用动画
            parent: 父组件
        """
        super().__init__(parent)
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.setAttribute(Qt.WA_StaticContents, True)
        self._size = size
        self._color = self._parse_color(color)
        self._bg_color = theme_manager.colors.fill
        self._animation_enabled = animation_enabled
        self._current_progress = value / maximum if maximum > 0 else 0
        self._target_progress = self._current_progress
        self._animation = None

        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.setValue(value)
        self.setTextVisible(text_visible)
        self.setFixedSize(self._size, self._size)

        self.setObjectName("xcircleprogress")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._update_timer = QTimer(self)
        self._update_timer.setSingleShot(True)
        self._update_timer.setInterval(UPDATE_INTERVAL)
        self._update_timer.timeout.connect(self.update)

        theme_manager.theme_changed.connect(self._on_theme_changed)

    def _clear_cache(self):
        """清除缓存"""
        XCircleProgressCache.clear_cache()

    def _start_animation(self, target_value: int):
        """启动动画"""
        if not self._animation_enabled:
            self._current_progress = target_value / self.maximum() if self.maximum() > 0 else 0
            self._schedule_update()
            return

        if self._animation is not None:
            self._animation.stop()

        target_progress = target_value / self.maximum() if self.maximum() > 0 else 0
        self._animation = QVariantAnimation(self)
        self._animation.setDuration(ANIMATION_DURATION)
        self._animation.setStartValue(self._current_progress)
        self._animation.setEndValue(target_progress)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        self._animation.valueChanged.connect(self._on_animation_value_changed)
        self._animation.finished.connect(self._on_animation_finished)
        self._animation.start()

    def _on_animation_value_changed(self, value):
        """动画值变化回调"""
        # self._current_progress = value
        # self._schedule_update()
        self._current_progress = value
        if not self._update_timer.isActive():
            self._schedule_update()

    def _on_animation_finished(self):
        """动画完成回调"""
        self._current_progress = self._target_progress
        self._animation = None
        self.update()

    def _get_stroke_width(self) -> int:
        """根据尺寸计算圆环宽度"""
        if self._size >= 100:
            return 6
        elif self._size >= 60:
            return 4
        else:
            return 3

    def paintEvent(self, event):
        """重写绘制事件，使用全局缓存"""
        size = self._size
        stroke_width = self._get_stroke_width()
        enabled = self.isEnabled()
        color = self._color
        bg_color = self._bg_color
        text_visible = self.isTextVisible()
        dpr = self.devicePixelRatioF()

        pixmap = XCircleProgressCache.get_pixmap(
            size, stroke_width, self._current_progress, enabled, color, bg_color, theme_manager, dpr
        )

        painter = QPainter(self)
        painter.drawPixmap(0, 0, pixmap)

        if text_visible:
            text = f"{int(self._current_progress * 100)}%"
            font = theme_manager.get_font('size_m', "weight_semibold")
            painter.setFont(font)
            painter.setPen(QColor(theme_manager.colors.text_2))

            text_rect = QRectF(
                stroke_width * 2, stroke_width * 2,
                size - 4 * stroke_width,
                size - 4 * stroke_width
            )
            painter.drawText(text_rect, Qt.AlignCenter, text)

    def set_color(self, color: Union[XColor, str]):
        """设置进度颜色

        Args:
            color: 颜色值，支持以下格式：
                - Color 枚举：XColor.PRIMARY, XColor.SUCCESS 等
                - 预设颜色：'primary', 'success', 'warning', 'danger' 等
                - 自定义颜色：'#FF0000', 'rgb(255, 0, 0)' 等

        Returns:
            XCircleProgress: 返回自身，支持链式调用

        Examples:
            >>> progress.set_color(XColor.SUCCESS)  # 使用枚举
            >>> progress.set_color('success')  # 使用预设字符串
            >>> progress.set_color('#FF0000')  # 使用自定义红色
        """
        self._color = self._parse_color(color)
        self._schedule_update()
        return self

    def set_size(self, size: int):
        """设置进度条尺寸

        Args:
            size: 直径（像素），最小值为 40px
                    推荐值：100px（默认），80px（中等），60px（小型）

        Returns:
            XCircleProgress: 返回自身，支持链式调用

        Examples:
            >>> progress = XCircleProgress()
            >>> progress.set_size(100)  # 默认尺寸
            >>> progress.set_size(80)   # 中等尺寸
            >>> progress.set_size(60)   # 小型尺寸
        """
        self._size = max(40, size)
        self.setFixedSize(self._size, self._size)
        self._schedule_update()
        return self

    def set_animation_enabled(self, enabled: bool):
        """设置是否启用动画

        Args:
            enabled: 是否启用动画

        Returns:
            self: 返回自身，支持链式调用

        Examples:
            >>> progress = XCircleProgress()
            >>> progress.set_animation_enabled(True)   # 启用动画
            >>> progress.set_animation_enabled(False)  # 禁用动画
        """
        self._animation_enabled = enabled
        return self

    def setValue(self, value: int):
        """重写 setValue 方法，支持动画"""
        super().setValue(value)
        self._target_progress = value / self.maximum() if self.maximum() > 0 else 0
        self._start_animation(value)
        return self
