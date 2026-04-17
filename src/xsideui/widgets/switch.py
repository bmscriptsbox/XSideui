"""Switch Component 开关组件

支持多种尺寸和颜色，自动适配主题切换。
"""
from typing import Union
from ..utils.qt_compat import QColor, QPainter, QPixmap, QAbstractButton, QWidget, QHBoxLayout, Qt, Signal, Property, \
    QPropertyAnimation, QEasingCurve, QTimer

from .label import XLabel
from ..theme import theme_manager
from ..xenum import XColor, XSize
from ..i18n import XI18N

# 常量
THUMB_COLOR_ENABLED = "#f5f5f5"
ANIMATION_DURATION = 200
PADDING = 3
TRACK_MARGIN = 3
MAX_CACHE_SIZE = 50
UPDATE_INTERVAL = 16  # ~60fps


def _parse_enum_value(value, enum_class):
    """解析枚举值"""
    return value.value if isinstance(value, enum_class) else value


def _parse_color(color):
    """解析颜色"""
    if not color:
        return theme_manager.colors.primary

    if isinstance(color, XColor):
        color = color.value

    colors = theme_manager.colors
    color_map = {
        'primary': colors.primary,
        'secondary': colors.secondary,
        'tertiary': colors.tertiary,
        'success': colors.success,
        'warning': colors.warning,
        'danger': colors.danger,
    }

    return color_map.get(color.lower(), color)


class XSwitchCache:
    """全局缓存管理器（带大小限制）"""
    _cache = {}

    @classmethod
    def get_pixmap(cls, key, draw_func):
        """获取或创建缓存的 QPixmap"""
        if key in cls._cache:
            return cls._cache[key]

        if len(cls._cache) >= MAX_CACHE_SIZE:
            cls._cache.clear()

        pixmap = draw_func()
        cls._cache[key] = pixmap
        return pixmap

    @classmethod
    def clear_cache(cls):
        """清除所有缓存"""
        cls._cache.clear()


class OnlySwitch(QAbstractButton):
    """内部开关组件"""

    def __init__(self, checked=False, color=XColor.PRIMARY, size=XSize.DEFAULT, parent=None):
        super().__init__(parent)
        self.setObjectName("onlyswitch")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._color_name = color
        self._color = _parse_color(color)
        self._size = _parse_enum_value(size, XSize)

        self._handle_position = 1.0 if checked else 0.0
        self._thumb_scale = 1.0

        # 节流定时器，减少频繁重绘
        self._update_timer = QTimer(self)
        self._update_timer.setSingleShot(True)
        self._update_timer.setInterval(UPDATE_INTERVAL)
        self._update_timer.timeout.connect(self.update)

        self._update_size()
        self._setup_animations()

        self.setCheckable(True)
        self.setChecked(checked)
        theme_manager.theme_changed.connect(self._on_theme_changed)

    def _setup_animations(self):
        """初始化动画"""
        self._handle_anim = QPropertyAnimation(self, b"handle_position", self)
        self._handle_anim.setDuration(ANIMATION_DURATION)
        self._handle_anim.setEasingCurve(QEasingCurve.InOutCubic)

    def _update_size(self):
        """更新尺寸"""
        config = self._get_config()
        if config:
            self.setFixedSize(config["width"], config["height"])

    def _get_config(self):
        """获取当前尺寸配置"""
        return theme_manager.switch.get(self._size)

    def setChecked(self, checked: bool):
        # 1. 调用父类原始方法，确保逻辑状态改变
        super().setChecked(checked)

        # 2. 同步更新动画位置属性
        # 如果当前没有动画在跑（比如界面初始化或外部直接设置），直接跳到目标点
        if not self._handle_anim.state() == QPropertyAnimation.Running:
            self._handle_position = 1.0 if checked else 0.0
            self.update()
        else:
            # 如果正在动画中，则让动画飞向新目标
            self._handle_anim.stop()
            self._handle_anim.setEndValue(1.0 if checked else 0.0)
            self._handle_anim.start()

    def set_size(self, size):
        """设置尺寸"""
        size = _parse_enum_value(size, XSize)
        if size in theme_manager.switch:
            self._size = size
            self._update_size()
            XSwitchCache.clear_cache()
            self._schedule_update()
        return self

    def set_color(self, color):
        """设置开关颜色"""
        self._color_name = color
        self._color = _parse_color(color)
        XSwitchCache.clear_cache()
        self._schedule_update()
        return self

    @Property(float)
    def handle_position(self) -> float:
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos: float):
        self._handle_position = pos
        self.update()

    def _schedule_update(self):
        """调度更新（节流）"""
        self._update_timer.start()

    def _update_thumb_scale(self, scale):
        """更新滑块缩放"""
        if self._thumb_scale != scale:
            self._thumb_scale = scale
            self._schedule_update()

    def enterEvent(self, event):
        """鼠标进入事件"""
        if self.isEnabled():
            self.setCursor(Qt.PointingHandCursor)
            self._update_thumb_scale(1.1)

    def leaveEvent(self, event):
        """鼠标离开事件"""
        self._update_thumb_scale(1.0)

    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self._update_thumb_scale(0.9)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self._update_thumb_scale(1.1 if self.underMouse() else 1.0)
        super().mouseReleaseEvent(event)

    def nextCheckState(self):
        """切换状态"""
        super().nextCheckState()
        checked = self.isChecked()
        self._handle_anim.setStartValue(self._handle_position)
        self._handle_anim.setEndValue(1.0 if checked else 0.0)
        self._handle_anim.start()

    def _get_colors(self):
        """获取当前状态的颜色"""
        colors = theme_manager.colors

        if not self.isEnabled():
            return {'track': colors.fill, 'thumb': colors.text_1}

        return {
            'track': self._color if self.isChecked() else colors.fill,
            'thumb': THUMB_COLOR_ENABLED if self.isChecked() else colors.text_1
        }

    def paintEvent(self, event):
        """绘制事件"""
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        config = self._get_config()
        if not config:
            return

        colors = self._get_colors()
        dpr = self.devicePixelRatioF()

        # 绘制轨道
        track_key = (self._size, self.isChecked(), self.isEnabled(), colors['track'], dpr)
        track_pixmap = XSwitchCache.get_pixmap(track_key, lambda: self._create_track_pixmap(config, colors['track']))
        track_x = (self.width() - config["track_width"]) // 2
        p.drawPixmap(track_x, 0, track_pixmap)

        # 绘制滑块
        thumb_size = int((self.height() - TRACK_MARGIN * 2) * self._thumb_scale)
        thumb_key = (self._size, self.isEnabled(), colors['thumb'], thumb_size, dpr)
        thumb_pixmap = XSwitchCache.get_pixmap(thumb_key,
                                               lambda: self._create_thumb_pixmap(colors['thumb'], thumb_size))

        max_thumb_x = config["track_width"] - thumb_size - PADDING * 2
        thumb_x = track_x + PADDING + max_thumb_x * self._handle_position
        thumb_y = (self.height() - thumb_size) / 2
        p.drawPixmap(int(thumb_x), int(thumb_y), thumb_pixmap)

    def _create_track_pixmap(self, config, color):
        """创建轨道 QPixmap"""
        dpr = self.devicePixelRatioF()  # 获取当前屏幕缩放倍率
        pixmap = QPixmap(int(config["track_width"] * dpr), int(config["height"] * dpr))
        pixmap.setDevicePixelRatio(dpr)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(color))
        painter.drawRoundedRect(0, 0, config["track_width"], config["height"], config["height"] / 2,
                                config["height"] / 2)
        painter.end()

        return pixmap

    def _create_thumb_pixmap(self, color, size):
        """创建滑块 QPixmap"""
        dpr = self.devicePixelRatioF()
        pixmap = QPixmap(int(size * dpr), int(size * dpr))
        pixmap.setDevicePixelRatio(dpr)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(color))
        painter.drawEllipse(0, 0, size, size)
        painter.end()

        return pixmap

    def _on_theme_changed(self):
        """处理主题变化事件"""
        XSwitchCache.clear_cache()
        self._color = _parse_color(self._color_name)
        self._update_size()
        self.update()


class XSwitch(QWidget):
    """带标签的开关组件

    Example:
        >>> switch = XSwitch("开启", "关闭", checked=True)
        >>> switch.clicked.connect(lambda checked: print(f"Switch: {checked}"))
    """

    clicked = Signal(bool)

    def __init__(
            self,
            text_on: str = "On",
            text_off: str = "Off",
            checked: bool = False,
            color: Union[XColor, str] = XColor.PRIMARY,
            size: XSize = XSize.DEFAULT,
            parent=None
    ):
        super().__init__(parent)
        self.setObjectName("xswitch")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._text_on_key = text_on
        self._text_off_key = text_off

        self.switch = OnlySwitch(checked=checked, color=color, size=size)

        current_key = self._text_on_key if checked else self._text_off_key
        self.label = XLabel(current_key)

        layout = QHBoxLayout(self)
        layout.addWidget(self.switch)
        layout.addWidget(self.label)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        XI18N.language_changed.connect(self._update_label_text)
        self.switch.clicked.connect(self._on_switch_clicked)
        theme_manager.theme_changed.connect(self._on_theme_changed)

    def _update_label_text(self):
        """
        同步逻辑：根据 Check 状态决定 Label 应该持有的 Key
        """
        is_checked = self.switch.isChecked()
        target_key = self._text_on_key if is_checked else self._text_off_key

        self.label.setText(target_key)

    def _on_switch_clicked(self, checked):
        """处理开关点击事件"""
        self._update_label_text()
        self.clicked.emit(checked)

    def setChecked(self, checked: bool):
        """设置开关状态"""
        if self.switch.isChecked() != checked:
            self.switch.setChecked(checked)
            # 必须调用这个，否则 XLabel 里的 key 永远是旧的
            self._update_label_text()
            self.switch.update()

    def set_checked(self, checked: bool):
        """设置开关状态（链式调用）"""
        self.setChecked(checked)
        return self

    def isChecked(self) -> bool:
        """获取开关状态"""
        return self.switch.isChecked()

    def setEnabled(self, enabled: bool):
        """设置开关启用/禁用状态"""
        super().setEnabled(enabled)
        self.switch.setEnabled(enabled)
        self.label.setEnabled(enabled)

    def set_size(self, size):
        """设置尺寸"""
        size = _parse_enum_value(size, XSize)
        if size in theme_manager.switch:
            self.switch.set_size(size)
        return self

    def set_color(self, color):
        """设置开关颜色"""
        color = _parse_enum_value(color, XColor)
        self.switch.set_color(color)
        return self

    def _on_theme_changed(self, theme_name):
        """处理主题变化事件"""
        self.label.update()
