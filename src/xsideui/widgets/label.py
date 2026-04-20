import sys
from enum import Enum
from typing import Union

from ..utils.qt_compat import Qt, QGuiApplication, QLabel, QSizePolicy, QEvent
from ..theme.theme import theme_manager, Theme
from ..xenum import XColor
from ..i18n import XI18N


class XLabel(QLabel):
    """高级标签组件

    支持预设样式、自定义颜色、字号、字重、文字装饰等功能
    """

    class Style(Enum):
        """预设样式"""
        H1 = "h1"
        H2 = "h2"
        H3 = "h3"
        H4 = "h4"
        BODY = "body"
        CAPTION = "caption"
        SECONDARY = "secondary"
        DISABLED = "disabled"

    FONT_FAMILIES = [
        "Microsoft YaHei UI",
        "PingFang SC",
        "HarmonyOS Sans SC"
    ]

    STYLE_MAP = {
        Style.H1: {"size": 20, "weight": 700, "color_key": "text_0"},
        Style.H2: {"size": 18, "weight": 600, "color_key": "text_0"},
        Style.H3: {"size": 16, "weight": 600, "color_key": "text_0"},
        Style.H4: {"size": 14, "weight": 600, "color_key": "text_0"},
        Style.BODY: {"size": 14, "weight": 400, "color_key": "text_1"},
        Style.CAPTION: {"size": 12, "weight": 400, "color_key": "text_1"},
        Style.SECONDARY: {"size": 10, "weight": 400, "color_key": "text_2"},
        Style.DISABLED: {"size": 10, "weight": 400, "color_key": "text_3"},
    }

    @staticmethod
    def _get_dpi_scale() -> float:
        """获取 DPI 缩放因子"""
        try:
            return QGuiApplication.primaryScreen().devicePixelRatio()
        except:
            return 1.0

    @staticmethod
    def _scale_font_size(size: int) -> int:
        """根据 DPI 缩放字体大小"""
        scale = XLabel._get_dpi_scale()
        return int(size * scale)

    def __init__(
            self,
            text: str = "",
            style: 'XLabel.Style' = None,
            color: Union[XColor, str] = None,
            size: int = None,
            weight: int = None,
            letter_spacing: float = 0.3,
            underline: bool = False,
            strike_out: bool = False,
            elide_mode: bool = False,
            alignment: Qt.Alignment = Qt.AlignLeft | Qt.AlignVCenter,
            selectable: bool = True,
            word_wrap: bool = False,
            theme: Theme = None,
            parent=None
    ):
        """初始化文本标签组件。

            Args:
                text: 显示的文本内容。
                style: 预设样式（如 H1, H2, Body, Caption 等）。
                color: 文本颜色。支持 XColor 枚举或十六进制字符串。
                size: 字体大小（像素）。
                weight: 字体粗细（如 QFont.Bold 或数值 50-900）。
                letter_spacing: 字符间距（像素）。默认 0.3px 以提升易读性。
                underline: 是否启用下划线。
                strike_out: 是否启用删除线。
                elide_mode: 是否启用省略模式。若为 True，当宽度不足时文本末尾显示 "..."。
                alignment: 文本对齐方式。默认左对齐且垂直居中。
                selectable: 是否允许用户鼠标拖拽选中文字并复制。
                word_wrap: 是否允许自动换行。
                theme: 显式指定的主题对象。若为 None 则跟随系统全局主题。
                parent: 父级组件。
            """
        super().__init__(parent)
        self._full_text = text
        self._theme = theme or theme_manager
        self._style = style or self.Style.BODY
        self._custom_color = color.value if isinstance(color, XColor) else color
        self._size = size
        self._weight = weight
        self._letter_spacing = letter_spacing
        self._underline = underline
        self._strike_out = strike_out
        self._elide_mode = elide_mode
        self._alignment = alignment
        self._word_wrap = word_wrap

        self._text_key = text
        self._i18n_context = self.__class__.__name__

        # 初始翻译
        self.retranslateUi()


        self._has_custom_style = (
                color is not None or
                size is not None or
                weight is not None or
                underline or
                strike_out or
                letter_spacing != 0.3
        )

        self._apply_base_style()
        self._apply_interaction(selectable)
        self.update_elided_text()

        self._theme.theme_changed.connect(self._update_theme)

    def retranslateUi(self):
        """当语言切换或文本更新时调用"""
        if not self._text_key:
            super().setText("")
            return

        # 调用我们刚刚写的适配函数
        translated = XI18N.x_tr(self._text_key)
        self._full_text = translated
        if self._elide_mode:
            self.update_elided_text()
        else:
            super().setText(translated)

    def changeEvent(self, event):
        """监听国际化事件"""
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi()
        super().changeEvent(event)

    def setText(self, text: str):
        """重写 setText，确保外部修改文本时同步更新翻译键"""
        self._text_key = text
        self.retranslateUi()

    def _apply_base_style(self):
        """应用基础样式"""
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAlignment(self._alignment)
        self.setWordWrap(self._word_wrap)

        if not self._has_custom_style:
            self.setObjectName(f"label-{self._style.value}")
        else:
            self.setObjectName("")

        self._update_style()

    def _apply_interaction(self, selectable: bool):
        """设置交互模式"""
        flags = Qt.TextBrowserInteraction if selectable else Qt.NoTextInteraction
        self.setTextInteractionFlags(flags)
        self.setOpenExternalLinks(selectable)

    def _update_style(self):
        """更新样式：智能合并预设样式与自定义参数"""
        # 如果既没有自定义属性，也没有设置 Style，则不处理（交给 QSS 运行）
        if not self._has_custom_style:
            return

        # 1. 获取当前预设样式的基础配置 (若无匹配则回退到 BODY)
        base_config = self.STYLE_MAP.get(self._style, self.STYLE_MAP[self.Style.BODY])

        # 2. 确定颜色 (优先级: 手动 color > 预设 color_key > 默认黑)
        color = self._custom_color
        if not color:
            color_key = base_config["color_key"]
            # 尝试从主题对象中获取对应的颜色值
            color = getattr(self._theme.colors, color_key, "#000000")

        # 如果 color 仍然是一个 key 字符串，递归转换一次
        if isinstance(color, str) and hasattr(self._theme.colors, color):
            color = getattr(self._theme.colors, color)

        # 3. 确定字号 (优先级: 手动 size > 预设 size)
        target_size = self._size if self._size is not None else base_config["size"]
        scaled_size = self._scale_font_size(target_size)

        # 4. 确定字重 (优先级: 手动 weight > 预设 weight)
        target_weight = self._weight if self._weight is not None else base_config["weight"]

        # 5. 处理装饰线
        decorations = []
        if self._underline:
            decorations.append("underline")
        if self._strike_out:
            decorations.append("line-through")
        decoration_str = " ".join(decorations) if decorations else "none"

        # 6. 生成并应用 QSS
        qss = f"""
            QLabel {{
                font-family: {", ".join(self.FONT_FAMILIES)};
                font-size: {scaled_size}px;
                font-weight: {target_weight};
                color: {color};
                text-decoration: {decoration_str};
                letter-spacing: {self._letter_spacing}px;
                background: transparent;
            }}
        """
        self.setStyleSheet(qss)

    def _update_theme(self):
        """主题更新处理"""
        if self._has_custom_style:
            self._update_style()
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._elide_mode and event.oldSize().width() != event.size().width():
            self.update_elided_text()



    def set_elide_mode(self, enable: bool):
        """启用/禁用文本省略模式"""
        self._elide_mode = enable
        if enable:
            self.update_elided_text()
        else:
            self.setToolTip("")
            super().setText(self._full_text)
        return self

    def update_elided_text(self):
        """更新省略文本"""
        if self.textFormat() == Qt.RichText:
            return

        if not self._elide_mode or not self._full_text:
            if super().text() != self._full_text:
                super().setText(self._full_text)
            return

        metrics = self.fontMetrics()
        available_width = max(20, self.width() - 4)

        elided_text = metrics.elidedText(
            self._full_text,
            Qt.ElideRight,
            available_width
        )

        if elided_text != super().text():
            super().setText(elided_text)

        self.setToolTip(self._full_text if elided_text != self._full_text else "")

    def set_style(self, style: 'XLabel.Style'):
        """设置预设样式"""
        self._style = style
        self._has_custom_style = False
        self.setStyleSheet("")
        self.setObjectName(f"label-{self._style.value}")
        self._update_style()
        return self

    def set_color(self, color: Union[XColor, str]):
        """设置自定义颜色"""
        self._custom_color = color.value if isinstance(color, XColor) else color
        self._has_custom_style = True
        self.setObjectName("")
        self._update_style()
        return self

    def set_font_size(self, size: int):
        """设置字号"""
        self._size = size
        self._has_custom_style = True
        self.setObjectName("")
        self._update_style()
        return self

    def set_weight(self, weight: int):
        """设置字重（100-900）"""
        if 100 <= weight <= 900:
            self._weight = weight
            self._has_custom_style = True
            self.setObjectName("")
            self._update_style()
        return self

    def set_letter_spacing(self, spacing: float):
        """设置字间距"""
        self._letter_spacing = spacing
        self._has_custom_style = True
        self.setObjectName("")
        self._update_style()
        return self

    def set_underline(self, enable: bool):
        """启用/禁用下划线"""
        self._underline = enable
        self._has_custom_style = True
        self.setObjectName("")
        self._update_style()
        return self

    def set_strike_out(self, enable: bool):
        """启用/禁用删除线"""
        self._strike_out = enable
        self._has_custom_style = True
        self.setObjectName("")
        self._update_style()
        return self

    def set_alignment(self, alignment: Qt.Alignment):
        """设置文本对齐方式"""
        self._alignment = alignment
        self.setAlignment(alignment)
        return self

    def set_word_wrap(self, enable: bool):
        """设置是否自动换行"""
        self._word_wrap = enable
        self.setWordWrap(enable)
        return self

    def set_rich_text(self, html: str):
        """设置富文本内容"""
        self.setTextFormat(Qt.RichText)
        self.setText(html)
        return self

    def set_link(self, url: str):
        """设置为可点击链接"""
        self.setText(f'<a href="{url}">{self.text()}</a>')
        self.setTextFormat(Qt.RichText)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setFocusPolicy(Qt.NoFocus)
        self.setAttribute(Qt.WA_Hover, False)
        self.setOpenExternalLinks(True)
        return self

    def set_selectable(self, enable: bool):
        """启用文本选择"""
        flags = Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard if enable else Qt.NoTextInteraction
        self.setTextInteractionFlags(flags)
        return self

    def set_theme(self, theme: Theme):
        """设置主题"""
        try:
            self._theme.theme_changed.disconnect(self._update_theme)
        except (RuntimeError, TypeError):
            pass

        self._theme = theme
        self._theme.theme_changed.connect(self._update_theme)
        self._update_style()
        return self

    @property
    def theme(self) -> Theme:
        """获取当前使用的主题"""
        return self._theme
