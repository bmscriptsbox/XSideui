"""
轮播图组件
"""

from ..utils.qt_compat import (QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
                               QLabel, Qt, QTimer, Signal, QPropertyAnimation, QEasingCurve, QRect, QApplication)

from .image import XImage


class XCarousel(QWidget):
    """轮播图组件"""
    image_clicked = Signal(int)
    current_page_changed = Signal(int)

    def __init__(self, interval: int = 3000, min_height: int = 200, parent=None):
        """初始化轮播图组件。

            Args:
                interval: 自动轮播的时间间隔（毫秒）。默认 3000ms (3秒)。
                min_height: 组件的最小高度（像素）。用于确保轮播图在布局中有足够的视觉占位。
                parent: 父组件。
            """
        super().__init__(parent)
        self.interval = interval
        self.min_height = min_height
        self.auto_play = True
        self._is_animating = False

        self._init_ui()
        self._setup_timer()

    def _init_ui(self):
        """初始化UI"""
        self.setObjectName("xcarousel")
        self.setMinimumHeight(self.min_height)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.stack_widget = QStackedWidget(self)
        self.stack_widget.currentChanged.connect(self._on_current_page_changed)
        self.main_layout.addWidget(self.stack_widget)

        self.indicator_container = QWidget(self)
        self.indicator_container.setObjectName("indicator_container")
        self.indicator_layout = QHBoxLayout(self.indicator_container)
        self.indicator_layout.setContentsMargins(0, 0, 0, 15)
        self.indicator_layout.setSpacing(8)
        self.indicator_layout.setAlignment(Qt.AlignCenter)

    def add_image_page(self, source, scale_mode: str = "cover"):
        """添加图片页面"""
        fit_mode = {
            "cover": XImage.FitMode.COVER,
            "contain": XImage.FitMode.CONTAIN,
            "fill": XImage.FitMode.FILL
        }.get(scale_mode, XImage.FitMode.COVER)

        image_widget = XImage(
            source=source,
            fit=fit_mode,
            lazy=False,
            min_size=self.min_height,
            parent=self
        )
        image_widget.clicked.connect(lambda: self.image_clicked.emit(self.stack_widget.indexOf(image_widget)))

        idx = self.stack_widget.addWidget(image_widget)

        dot = QLabel()
        dot.setObjectName("carousel_indicator")
        dot.setFixedSize(8, 4)
        dot.setCursor(Qt.PointingHandCursor)
        dot.mousePressEvent = lambda e, i=idx: self.set_current_page(i)
        self.indicator_layout.addWidget(dot)

        if idx == 0:
            self._update_indicator_style(0)

        return image_widget

    def _switch_to_page(self, index: int):
        """切换到指定页面（带滑动动画）"""
        if self._is_animating or index == self.stack_widget.currentIndex():
            return

        current_idx = self.stack_widget.currentIndex()
        direction = 1 if index > current_idx else -1

        current_widget = self.stack_widget.widget(current_idx)
        new_widget = self.stack_widget.widget(index)

        self._is_animating = True
        width = self.width()
        start_pos_current = 0
        end_pos_current = -width * direction
        start_pos_new = width * direction
        end_pos_new = 0

        current_widget.setGeometry(start_pos_current, 0, width, self.height())
        new_widget.setGeometry(start_pos_new, 0, width, self.height())

        current_widget.show()
        new_widget.show()
        # current_widget.raise_()

        self.current_anim = QPropertyAnimation(current_widget, b"geometry")
        self.current_anim.setDuration(500)
        self.current_anim.setStartValue(QRect(start_pos_current, 0, width, self.height()))
        self.current_anim.setEndValue(QRect(end_pos_current, 0, width, self.height()))
        self.current_anim.setEasingCurve(QEasingCurve.OutCubic)

        self.new_anim = QPropertyAnimation(new_widget, b"geometry")
        self.new_anim.setDuration(500)
        self.new_anim.setStartValue(QRect(start_pos_new, 0, width, self.height()))
        self.new_anim.setEndValue(QRect(end_pos_new, 0, width, self.height()))
        self.new_anim.setEasingCurve(QEasingCurve.OutCubic)

        def on_finished():
            self._is_animating = False
            current_widget.setGeometry(0, 0, width, self.height())
            new_widget.setGeometry(0, 0, width, self.height())
            self.stack_widget.setCurrentIndex(index)
            self.stack_widget.currentWidget().show()
            # self.stack_widget.currentWidget().raise_()
            current_widget.hide()

        self.new_anim.finished.connect(on_finished)

        self.current_anim.start()
        self.new_anim.start()

        self._update_indicator_style(index)

    def _update_indicator_style(self, active_index: int):
        """更新指示器样式"""
        for i in range(self.indicator_layout.count()):
            dot = self.indicator_layout.itemAt(i).widget()
            if dot:
                is_active = (i == active_index)
                dot.setProperty("active", "true" if is_active else "false")
                dot.setFixedSize(24 if is_active else 8, 4)
                dot.style().unpolish(dot)
                dot.style().polish(dot)

    def _next_page(self):
        """切换图片-自动感知焦点"""
        if self.get_page_count() <= 1:
            return

        # 获取当前正拥有焦点的控件
        focus_widget = QApplication.focusWidget()
        # 只要是开启了输入法支持的控件在处理焦点，就保持安静
        if focus_widget and focus_widget.testAttribute(Qt.WA_InputMethodEnabled):
            return

        next_idx = (self.stack_widget.currentIndex() + 1) % self.get_page_count()
        self._switch_to_page(next_idx)

    def set_current_page(self, index: int):
        """设置当前页"""
        self._switch_to_page(index)
        if self.auto_play:
            self.timer.stop()
            self.timer.start(self.interval)

    def get_page_count(self):
        """获取总页数"""
        return self.stack_widget.count()

    def get_current_page(self):
        """获取当前页索引"""
        return self.stack_widget.currentIndex()

    def _setup_timer(self):
        """设置自动播放定时器"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._next_page)
        if self.auto_play:
            self.timer.start(self.interval)

    def resizeEvent(self, event):
        """处理尺寸变化"""
        super().resizeEvent(event)
        self.indicator_container.setGeometry(0, self.height() - 45, self.width(), 45)
        self.indicator_container.raise_()

    def enterEvent(self, event):
        """鼠标进入，暂停播放"""
        if self.auto_play:
            self.timer.stop()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开，恢复播放"""
        if self.auto_play:
            self.timer.start(self.interval)
        super().leaveEvent(event)

    def _on_current_page_changed(self, index: int):
        """页面切换回调"""
        self.current_page_changed.emit(index)
