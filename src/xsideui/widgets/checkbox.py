"""Checkbox Component 复选框组件

支持多种尺寸和颜色，自动适配主题切换，支持国际化。
"""
from typing import Union

from ..utils.qt_compat import QColor, QPainter, QPen, QPainterPath, QPixmap, Qt, Signal, QRectF, QSize, QTimer, \
    QCheckBox, QEvent

from ..theme.theme import theme_manager
from ..xenum import XColor, XSize
from ..i18n import XI18N

# 常量
BORDER_WIDTH = 2
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


class XCheckBoxCache:
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


class XCheckBox(QCheckBox):
    """复选框组件"""

    clicked = Signal(bool)

    def __init__(
            self,
            text: str = "",
            checked: bool = False,
            size: XSize = XSize.DEFAULT,
            color: Union[XColor, str] = XColor.PRIMARY,
            parent=None
    ):
        """初始化复选框组件。

            Args:
                text: 复选框显示的标签文本。
                checked: 初始选中状态。默认为 False（未选中）。
                size: 组件的尺寸规格。影响复选框图标的大小、间距以及字体大小。
                    通常对应 XSize.SMALL, XSize.DEFAULT, XSize.LARGE 等。
                color: 选中的主题颜色。支持 XColor 枚举或十六进制颜色字符串。
                parent: 父级组件。
            """
        super().__init__(text, parent)
        self.setObjectName("xcheckbox")
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

        self._update_size()
        theme_manager.theme_changed.connect(self._on_theme_changed)

        # 初始化国际化
        if text:
            self.retranslateUi()

    def retranslateUi(self):
        """当语言切换或文本更新时调用"""
        if not self._text_key:
            super().setText("")
            return

        # 调用我们刚刚写的适配函数
        translated = XI18N.x_tr(self._text_key)
        super().setText(translated)

    def changeEvent(self, event):
        """监听翻译事件"""
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi()
        super().changeEvent(event)

    def setText(self, text: str):
        """重写 setText，确保外部修改文本时同步更新翻译键"""
        self._text_key = text
        self.retranslateUi()

    def _update_size(self):
        """更新控件尺寸和字体"""
        config = self._get_size_config()
        if not config:
            return

        self.setFixedHeight(config['height'])

        font = theme_manager.get_font("size_s", "weight_medium")
        self.setFont(font)

    def _get_size_config(self):
        """获取尺寸配置"""
        return theme_manager.checkbox.get(self._size)

    def _schedule_update(self):
        """调度更新（节流）"""
        self._update_timer.start()

    def set_size(self, size):
        """设置复选框尺寸"""
        size = _parse_enum_value(size, XSize)
        if size in theme_manager.checkbox:
            self._size = size
            self._update_size()
            XCheckBoxCache.clear_cache()
            self._schedule_update()
        return self

    def set_color(self, color):
        """设置复选框颜色"""
        self._color_name = color
        self._color = _parse_color(color)
        XCheckBoxCache.clear_cache()
        self._schedule_update()
        return self

    def set_text(self, text: str = None):
        """
        设置复选框文本

        Args:
            text: 普通文本或翻译键

        """
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
                'bg': colors.text_disabled if self.isChecked() else colors.bg_2,
                'check': colors.bg_1 if self.isChecked() else None
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
                'text': colors.text_1,
                'border': display_color,
                'bg': display_color,
                'check': colors.bg_1
            }

        return {
            'text': display_color if self._is_hover else colors.text_1,
            'border': display_color if self._is_hover else colors.text_1,
            'bg': colors.bg_1,
            'check': None
        }

    def _get_text_margins(self, config):
        """计算文本边距"""
        box_margin = 3
        text_spacing = 6
        right_margin = 3
        text_left = box_margin + config['box_size'] + text_spacing
        return box_margin, text_left, right_margin

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
                self.clicked.emit(not self.isChecked())
                self.setChecked(not self.isChecked())
            self._schedule_update()

    def paintEvent(self, e):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        colors = self._get_colors()
        config = self._get_size_config()
        box_margin, text_left, _ = self._get_text_margins(config)
        dpr = self.devicePixelRatioF()

        # 绘制文本
        painter.setPen(QColor(colors['text']))
        painter.drawText(
            QRectF(text_left, 0, self.width() - text_left, self.height()),
            Qt.AlignLeft | Qt.AlignVCenter,
            self.text()
        )

        # 绘制复选框（使用缓存）
        checkbox_key = (self._size, self.isChecked(), self.isEnabled(), self._is_hover,
                        colors['bg'], colors['border'], colors['check'], dpr)
        pixmap = XCheckBoxCache.get_pixmap(
            checkbox_key,
            lambda: self._create_checkbox_pixmap(config, colors)
        )

        # 居中绘制 Pixmap
        pixmap_margin = 4
        py = (self.height() - pixmap.height() / pixmap.devicePixelRatio()) / 2
        px = box_margin - pixmap_margin
        painter.drawPixmap(px, py, pixmap)

    def _create_checkbox_pixmap(self, config, colors):
        """创建高清的复选框 Pixmap

        特性：
        - 支持高分屏（Retina/4K）
        - 使用抗锯齿
        - 圆角矩形
        - 黄金比例勾选标记
        """
        box_size = config['box_size']
        margin = 4
        total_size = box_size + margin * 2

        # 支持高分屏
        dpr = self.devicePixelRatioF()
        pixmap = QPixmap(total_size * dpr, total_size * dpr)
        pixmap.setDevicePixelRatio(dpr)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(margin, margin, box_size, box_size)

        # 绘制背景和边框
        if self.isChecked():
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(colors['bg']))
            painter.drawRoundedRect(rect, 3, 3)
        else:
            pen = QPen(QColor(colors['border']))
            pen.setWidthF(1.5)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(rect.adjusted(0.5, 0.5, -0.5, -0.5), 3, 3)

        # 绘制勾选标记（黄金比例）
        if self.isChecked() and colors['check']:
            # check_pen = QPen(QColor(colors['check']))
            check_pen = QPen(QColor('#F5F5F5'))
            check_pen.setWidthF(box_size * 0.16)
            check_pen.setCapStyle(Qt.RoundCap)
            check_pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(check_pen)

            path = QPainterPath()
            w, h = rect.width(), rect.height()
            lx, ly = rect.left(), rect.top()
            path.moveTo(lx + w * 0.24, ly + h * 0.5)
            path.lineTo(lx + w * 0.44, ly + h * 0.68)
            path.lineTo(lx + w * 0.74, ly + h * 0.32)
            painter.drawPath(path)

        painter.end()
        return pixmap

    def sizeHint(self):
        """返回建议的尺寸"""
        config = self._get_size_config()
        if not config:
            return QSize(100, 32)

        box_margin, text_left, right_margin = self._get_text_margins(config)

        fm = self.fontMetrics()
        text_width = fm.horizontalAdvance(self.text())
        total_width = text_left + text_width + right_margin

        return QSize(total_width, config['height'])

    def _on_theme_changed(self, theme_name):
        """处理主题变化事件"""
        XCheckBoxCache.clear_cache()
        self._color = _parse_color(self._color_name)
        self._update_size()
        self.update()
