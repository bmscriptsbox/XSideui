"""Radio Button Component 单选按钮组件

支持多种尺寸和颜色，自动适配主题切换。
"""
from typing import Union

from ..utils.qt_compat import QColor, QPainter, QPen, QPixmap, QFontMetrics, Qt, Signal, QRectF, QPointF, QSize, \
    QTimer, QRadioButton, QEvent
from ..theme.theme import theme_manager
from ..xenum import XColor, XSize
from ..i18n import XI18N

# 常量
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

    return color_map.get(str(color).lower(), color)


class XRadioButtonCache:
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


class XRadioButton(QRadioButton):
    """单选按钮组件

    Example:
        >>> radio = XRadioButton("选项", checked=True)
        >>> radio.clicked.connect(lambda checked: print(f"Checked: {checked}"))
    """

    clicked = Signal(bool)

    def __init__(
        self,
        text: str = "",
        checked: bool = False,
        size: XSize = XSize.DEFAULT,
        color:Union[XColor, str]=XColor.PRIMARY,
        parent=None
    ):
        super().__init__(text, parent)
        self.setObjectName("xradio")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._text_key = text
        self._is_pressed = False
        self._is_hover = False
        self._size = _parse_enum_value(size, XSize)
        self._color_name = color
        self._color = _parse_color(color)

        self.setChecked(checked)
        self.setCursor(Qt.PointingHandCursor)

        # 节流定时器
        self._update_timer = QTimer(self)
        self._update_timer.setSingleShot(True)
        self._update_timer.setInterval(UPDATE_INTERVAL)
        self._update_timer.timeout.connect(self.update)

        # 初始化国际化
        self.retranslateUi()

        self._update_size()
        theme_manager.theme_changed.connect(self._on_theme_changed)

    def _update_size(self):
        """更新控件尺寸和字体"""
        config = self._get_size_config()
        if not config:
            return

        self.setFixedHeight(config['height'])
        font = theme_manager.get_font(config['font_size'], "weight_medium")
        self.setFont(font)

    def _get_size_config(self):
        """获取尺寸配置"""
        return theme_manager.radio.get(self._size)

    def _schedule_update(self):
        """调度更新（节流）"""
        self._update_timer.start()

    def set_size(self, size):
        """设置单选按钮尺寸"""
        size = _parse_enum_value(size, XSize)
        if size in theme_manager.radio:
            self._size = size
            self._update_size()
            XRadioButtonCache.clear_cache()
            self._schedule_update()
        return self

    def set_color(self, color):
        """设置单选按钮颜色"""
        self._color_name = color
        self._color = _parse_color(color)
        XRadioButtonCache.clear_cache()
        self._schedule_update()
        return self


    def retranslateUi(self):
        """当语言切换或文本更新时调用"""
        if not self._text_key:
            super().setText("")
            return
        translated = XI18N.x_tr(self._text_key)
        super().setText(translated)
        self.updateGeometry()
        self.update()

    def changeEvent(self, event):
        """监听国际化事件"""
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi()
        super().changeEvent(event)

    def setText(self, text: str):
        """重写 setText，确保外部修改文本时同步更新翻译键"""
        self._text_key = text
        self.retranslateUi()

    def _get_colors(self):
        """获取当前状态的颜色

        颜色状态：
        - 禁用：使用灰色
        - 按下：颜色加深 15%
        - 悬停：颜色变亮 10%
        - 选中：使用主题色
        """
        colors = theme_manager.colors

        if not self.isEnabled():
            return {
                'text': colors.text_disabled,
                'border': colors.text_disabled,
                'dot': colors.text_disabled if self.isChecked() else None
            }

        base_color = QColor(self._color)
        if self._is_pressed:
            display_color = base_color.darker(115).name()
        elif self._is_hover:
            display_color = base_color.lighter(110).name()
        else:
            display_color = self._color

        if self.isChecked():
            return {
                'text': display_color,
                'border': display_color,
                'dot': display_color
            }

        if self._is_hover:
            return {
                'text': display_color,
                'border': display_color,
                'dot': None
            }

        return {
            'text': colors.text_1,
            'border': colors.text_1,
            'dot': None
        }

    def enterEvent(self, e):
        """鼠标进入事件"""
        if not self._is_hover:
            self._is_hover = True
            self._schedule_update()

    def leaveEvent(self, e):
        """鼠标离开事件"""
        if self._is_hover:
            self._is_hover = False
            self._schedule_update()

    def mousePressEvent(self, e):
        """鼠标按下事件"""
        if e.button() == Qt.LeftButton:
            self._is_pressed = True
            self._schedule_update()

    def mouseReleaseEvent(self, e):
        """鼠标释放事件"""
        if e.button() == Qt.LeftButton:
            self._is_pressed = False
            if self.rect().contains(e.pos()):
                self.setChecked(True)
                self.clicked.emit(True)
            self._schedule_update()

    def paintEvent(self, e):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        colors = self._get_colors()
        config = self._get_size_config()

        # 计算文本位置
        margin, spacing = 4, 8
        text_left = margin + (config['radius'] * 2) + spacing

        # 绘制文本
        painter.setPen(QColor(theme_manager.colors.text_1))
        painter.setFont(self.font())
        painter.drawText(
            QRectF(text_left, 0, self.width() - text_left, self.height()),
            Qt.AlignLeft | Qt.AlignVCenter,
            self.text()
        )

        # 绘制单选按钮（使用缓存）
        radio_key = (self._size, self.isChecked(), self.isEnabled(), self._is_hover,
                    self._is_pressed, colors['border'], colors['dot'],self.devicePixelRatioF())
        pixmap = XRadioButtonCache.get_pixmap(
            radio_key,
            lambda: self._create_radio_pixmap(config, colors)
        )

        # 居中绘制 Pixmap
        pw, ph = pixmap.width() / pixmap.devicePixelRatio(), pixmap.height() / pixmap.devicePixelRatio()
        px = margin - (pw - config['radius'] * 2) / 2
        py = (self.height() - ph) / 2
        painter.drawPixmap(QRectF(px, py, pw, ph), pixmap, QRectF(pixmap.rect()))

    def _create_radio_pixmap(self, config, colors):
        """创建高清、不裁剪的单选按钮 Pixmap

        特性：
        - 支持高分屏（Retina/4K）
        - 使用抗锯齿
        - 内圆半径为外圆半径的 50%
        - 按下时内圆缩放 85%
        """
        radius = config['radius']
        draw_margin = 4
        total_size = (radius + draw_margin) * 2

        # 支持高分屏
        dpr = self.devicePixelRatioF()
        pixmap = QPixmap(total_size * dpr, total_size * dpr)
        pixmap.setDevicePixelRatio(dpr)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        center = QPointF(total_size / 2, total_size / 2)

        # 绘制外圆
        pen = QPen(QColor(colors['border']))
        pen.setWidthF(2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(center, radius - 0.5, radius - 0.5)

        # 绘制内点（Checked 状态）
        if self.isChecked() and colors['dot']:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(colors['dot']))
            dot_r = radius * 0.5
            if self._is_pressed:
                dot_r *= 0.85
            painter.drawEllipse(center, dot_r, dot_r)

        painter.end()
        return pixmap

    def sizeHint(self):
        """返回建议的尺寸"""
        config = self._get_size_config()
        if not config:
            return QSize(100, 32)

        fm = QFontMetrics(self.font())
        w = 4 + (config['radius'] * 2) + 8 + fm.horizontalAdvance(self.text()) + 6

        return QSize(w, config['height'])

    def _on_theme_changed(self, theme_name):
        """处理主题变化事件"""
        XRadioButtonCache.clear_cache()
        self._color = _parse_color(self._color_name)
        self._update_size()
        self.update()
