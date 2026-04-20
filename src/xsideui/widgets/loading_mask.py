"""
加载遮罩组件

"""
from ..utils.qt_compat import QFrame, QVBoxLayout, QLabel, QPainter, QColor, QPen, QPixmap, QTimer, Qt, QEvent
from ..theme import theme_manager
from .label import XLabel


class XLoadingMask(QFrame):
    """加载遮罩组件"""

    def __init__(
            self,
            text: str = "加载中...",
            icon_size: int = 42,
            spacing: int = 16,
            speed: str = "fast",
            parent=None
    ):
        """初始化加载遮罩组件。

            Args:
                text: 加载提示文本。若为空则只显示加载动画。
                icon_size: 旋转加载图标的尺寸（像素）。
                spacing: 旋转图标与下方文字之间的垂直间距。
                speed: 动画旋转速度。支持 'slow' (1s/r), 'medium' (0.8s/r), 'fast' (0.5s/r)。
                parent: 遮罩附着的父组件。遮罩将自动覆盖该组件的整个区域。
            """
        super().__init__(parent)
        self.setObjectName("xloadingmask")

        # 保存配置参数
        self._icon_size = icon_size
        self._text = text
        self._speed = speed
        self._angle = 0

        # 速度映射：每帧旋转的角度
        speed_map = {
            "slow": 3,  # 慢速：每帧旋转 3 度
            "medium": 5,  # 中速：每帧旋转 5 度
            "fast": 8  # 快速：每帧旋转 8 度
        }
        self._step = speed_map.get(self._speed, 5)

        # 初始化界面
        self._setup_ui(spacing)

        # 设置父组件
        if parent:
            self.resize(parent.size())
            parent.installEventFilter(self)

    @classmethod
    def show_loading(
            cls,
            parent,
            text: str = "加载中...",
            icon_size: int = 42,
            spacing: int = 16,
            speed: str = "fast"
    ):
        """在父组件上显示加载遮罩（便捷方法）
        
        Args:
            parent: 父组件
            text: 加载文字
            icon_size: 图标大小（像素）
            spacing: 图标和文字间距（像素）
            speed: 动画速度（slow/medium/fast）
            
        Returns:
            XLoadingMask: 加载遮罩实例
            
        Example:
            loading = XLoadingMask.show_loading(my_widget, text="正在处理...")
            # 隐藏: loading.hide()
        """
        loading = cls(
            text=text,
            icon_size=icon_size,
            spacing=spacing,
            speed=speed,
            parent=parent
        )
        loading.show()
        loading.raise_()
        return loading

    def hide(self):
        """隐藏加载遮罩"""
        super().hide()

    def _setup_ui(self, spacing: int):
        """初始化界面布局
        
        Args:
            spacing: 图标和文字间距（像素）
        """
        # 创建垂直布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(spacing)
        layout.setAlignment(Qt.AlignCenter)

        # 创建旋转图标标签
        self.spinner_label = QLabel()
        self.spinner_label.setObjectName("loading-spinner")
        self.spinner_label.setFixedSize(self._icon_size, self._icon_size)
        layout.addWidget(self.spinner_label, 0, Qt.AlignCenter)

        # 创建加载文字标签
        self.text_label = XLabel(self._text)
        layout.addWidget(self.text_label, 0, Qt.AlignCenter)

        # 创建动画定时器（60fps）
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._rotate)
        self._update_spinner()

    def _update_spinner(self):
        """绘制旋转动画（每帧调用）
        
        使用 QPainter 绘制双层圆弧，实现流畅的旋转效果。
        主圆弧使用主题色，次圆弧使用半透明主题色（残影效果）。
        """
        primary_color = theme_manager.colors.primary

        # 创建透明背景的 pixmap
        pixmap = QPixmap(self._icon_size, self._icon_size)
        pixmap.fill(Qt.transparent)

        # 创建绘制器
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        # 计算圆心和半径
        center_x = self._icon_size // 2
        center_y = self._icon_size // 2
        radius = min(center_x, center_y) - 4

        # 绘制主色圆弧（270度）
        pen = QPen(QColor(primary_color))
        pen.setWidth(4)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

        painter.drawArc(
            center_x - radius,
            center_y - radius,
            radius * 2,
            radius * 2,
            self._angle * 16,
            270 * 16
        )

        # 绘制次色圆弧（半透明，与主色圆弧相对 180 度）
        pen.setWidth(3)
        secondary_color = QColor(primary_color)
        secondary_color.setAlpha(80)
        pen.setColor(secondary_color)
        painter.setPen(pen)

        painter.drawArc(
            center_x - radius,
            center_y - radius,
            radius * 2,
            radius * 2,
            (self._angle + 180) * 16,
            270 * 16
        )

        # 结束绘制
        painter.end()

        # 设置图标到标签
        self.spinner_label.setPixmap(pixmap)

    def _rotate(self):
        """旋转动画回调（每 16ms 调用一次）
        
        更新旋转角度并重新绘制图标。
        """
        self._angle = (self._angle + self._step) % 360
        self._update_spinner()

    def set_text(self, text: str):
        """设置加载文字
        
        Args:
            text: 加载文字
        """
        self.text_label.setText(text)

    def text(self) -> str:
        """获取当前文字
        
        Returns:
            str: 当前文字
        """
        return self.text_label.text()

    def set_speed(self, speed: str):
        """设置动画速度
        
        Args:
            speed: 动画速度（slow/medium/fast）
        """
        self._speed = speed
        speed_map = {
            "slow": 3,
            "medium": 5,
            "fast": 8
        }
        self._step = speed_map.get(self._speed, 5)

    def showEvent(self, event):
        """显示事件处理：启动动画
        
        Args:
            event: 显示事件对象
        """
        super().showEvent(event)
        if not self._timer.isActive():
            self._timer.start(16)  # 60fps

    def hideEvent(self, event):
        """隐藏事件处理：停止动画
        
        Args:
            event: 隐藏事件对象
        """
        super().hideEvent(event)
        self._timer.stop()

    def eventFilter(self, obj, event):
        """事件过滤器：监听父组件大小变化
        
        当父组件大小变化时，自动调整遮罩大小以保持覆盖。
        
        Args:
            obj: 事件对象
            event: 事件对象
            
        Returns:
            bool: 是否处理了事件
        """
        if obj == self.parent() and event.type() == QEvent.Resize:
            self.resize(event.size())
        return super().eventFilter(obj, event)

    def setParent(self, parent):
        """设置父组件并调整大小匹配
        
        Args:
            parent: 父组件
        """
        super().setParent(parent)
        if parent:
            self.resize(parent.size())
            parent.installEventFilter(self)
