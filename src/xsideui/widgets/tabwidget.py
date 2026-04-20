from typing import List

from ..utils.qt_compat import (Qt, QTabWidget, QTabBar, QEasingCurve, QPropertyAnimation, QRect, QPainter, Property,
                               QColor, QRectF, QEvent, QSize)
from ..theme import theme_manager
from ..i18n import XI18N


class XTabBar(QTabBar):
    """标签栏组件 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("xtabbar")
        self.setMinimumHeight(40)
        self.setExpanding(False)
        self.setTabsClosable(False)

        self._ani_rect = QRect()
        self._ani = QPropertyAnimation(self, b"indicatorRect", self)
        self._ani.setDuration(300)
        self._ani.setEasingCurve(QEasingCurve.OutCubic)

        self.currentChanged.connect(self._on_current_changed)

    def get_indicatorRect(self):
        return self._ani_rect

    def set_indicatorRect(self, rect):
        self._ani_rect = rect
        self.update()

    indicatorRect = Property(QRect, fget=get_indicatorRect, fset=set_indicatorRect)

    def tabSizeHint(self, index: int):
        size = super().tabSizeHint(index)
        font_metrics = self.fontMetrics()
        text = self.tabText(index)

        # 兼容性处理
        if hasattr(font_metrics, 'horizontalAdvancement'):
            text_width = font_metrics.horizontalAdvancement(text)
        else:
            text_width = font_metrics.width(text)

        # 加上图标宽度（如果有图标的话）
        icon = self.tabIcon(index)
        icon_width = self.iconSize().width() + 10 if not icon.isNull() else 0

        # 40 是左右预留的内边距 (Padding)
        new_width = text_width + icon_width + 40

        # 保持原有的高度，更新宽度
        size.setWidth(new_width)
        return size

    def showEvent(self, event):
        super().showEvent(event)
        if self.currentIndex() >= 0:
            self._ani_rect = self.tabRect(self.currentIndex())
            self.update()

    def _on_current_changed(self, index):
        """处理标签切换事件"""
        if index < 0:
            return
        target_rect = self.tabRect(index)
        self._ani.stop()
        self._ani.setStartValue(self._ani_rect)
        self._ani.setEndValue(target_rect)
        self._ani.start()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.count() <= 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        indicator_color = QColor(theme_manager.colors.primary)
        painter.setBrush(indicator_color)
        painter.setPen(Qt.NoPen)


        rect = QRectF(self._ani_rect)
        h = 3
        padding = 10
        line_width = max(0.0, rect.width() - 2 * padding)
        line_rect = QRectF(
            rect.x() + padding,
            self.height() - h,
            line_width,
            h
        )

        painter.drawRoundedRect(line_rect, 1.5, 1.5)


class XTabWidget(QTabWidget):
    """标签页组件
    支持平滑的底部指示器动画，自动适配主题切换。
    """

    def __init__(self, parent=None):
        """初始化标签页组件

        Args:
            parent: 父组件
        """
        super().__init__(parent)
        self._i18n_tab_keys: List[str] = []
        self.setObjectName("xtabwidget")
        self.setContentsMargins(0, 0, 0, 0)
        self.tabBar().setContentsMargins(0, 0, 0, 0)
        self._tab_bar = XTabBar(parent=self)
        self.setTabBar(self._tab_bar)

        self.setLayoutDirection(Qt.LeftToRight)
        self.setTabPosition(QTabWidget.North)

        self.tabBar().setExpanding(False)
        self.setUsesScrollButtons(True)

        self.retranslateUi()

    def _extract_and_translate(self, args):
        """
        内部辅助：从不确定的参数中提取 label 并翻译
        addTab(widget, str) -> args 为 (widget, str)
        addTab(widget, icon, str) -> args 为 (widget, icon, str)
        """
        new_args = list(args)
        label_index = -1

        # 寻找参数中的字符串部分（通常是最后一个或倒数第一个）
        for i, arg in enumerate(args):
            if isinstance(arg, str):
                label_index = i
                break

        if label_index != -1:
            label_key = args[label_index]
            # 翻译
            translated = XI18N.x_tr(label_key)
            new_args[label_index] = translated
            return label_key, new_args

        return None, new_args

    def addTab(self, *args) -> int:
        """重写 addTab，记录 Key"""
        label_key, translated_args = self._extract_and_translate(args)
        self._i18n_tab_keys.append(label_key if label_key else "")
        return super().addTab(*translated_args)

    def insertTab(self, index: int, *args) -> int:
        """重写 insertTab，在指定位置插入 Key"""
        label_key, translated_args = self._extract_and_translate(args)
        self._i18n_tab_keys.insert(index, label_key if label_key else "")
        return super().insertTab(index, *translated_args)

    def setTabText(self, index: int, label: str):
        """更新翻译键并刷新 UI"""
        if 0 <= index < len(self._i18n_tab_keys):
            self._i18n_tab_keys[index] = label

        translated = XI18N.x_tr(label)
        super().setTabText(index, translated)

    def removeTab(self, index: int):
        if 0 <= index < len(self._i18n_tab_keys):
            self._i18n_tab_keys.pop(index)
        super().removeTab(index)

    def retranslateUi(self):
        """当语言切换或文本更新时调用"""
        if not self._i18n_tab_keys:
            return

        for index, key in enumerate(self._i18n_tab_keys):
            if key:
                translated = XI18N.x_tr(key)
                super().setTabText(index, translated)

        # 强制让 TabBar 重新计算所有 Tab 的宽度
        self.tabBar().updateGeometry()
        # 动画重置到当前选中的位置，防止文字撑开后指示器位置偏离
        curr = self.currentIndex()
        if curr >= 0:
            self._tab_bar.set_indicatorRect(self._tab_bar.tabRect(curr))

    def changeEvent(self, event):
        """监听国际化事件"""
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi()
        super().changeEvent(event)
