"""
一个轻量级的通知提示组件，支持多种类型、位置和自动消失控制。
"""
from enum import Enum
from typing import Union

from ..utils.qt_compat import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSizePolicy,
                               Qt, QPropertyAnimation, QEasingCurve, QTimer, QPoint, QSize, QApplication)
from ..icon import IconName, XIcon
from ..theme import theme_manager
from ..xenum import XColor, XButtonVariant, XSize
from .pushbutton import XPushButton
from .label import XLabel


class XNotif(QWidget):
    """通知提示组件
    
    一个轻量级的通知提示组件，支持多种类型、位置和自动消失控制。
    支持淡入淡出动画和平滑移动动画。
    
    Features:
        - 5种显示位置（居中、四角）
        - 4种通知类型（信息、成功、警告、错误）
        - 自动消失控制
        - 淡入淡出动画
        - 平滑移动动画
        - 主题适配
        - 通知堆叠管理
    """

    class Pos(Enum):
        """通知位置枚举"""
        CENTER = "center"
        TOP_LEFT = "top_left"
        TOP_RIGHT = "top_right"
        BOTTOM_LEFT = "bottom_left"
        BOTTOM_RIGHT = "bottom_right"

    # ========== 配置常量 ==========
    DURATION = 2000
    SPACING = 16
    MARGIN = 20
    MAX_TEXT_LENGTH = 500
    MAX_WIDTH = 600

    # ========== 动画配置 ==========
    ANIMATION_ENABLED = True
    FADE_IN_DURATION = 300
    FADE_OUT_DURATION = 300
    EASING_CURVE = QEasingCurve.OutCubic

    # ========== 类变量 ==========
    _notifications = []

    def __init__(
            self,
            text: str = "",
            parent=None,
            position: Union[Pos, str] = Pos.CENTER,
            duration: int = DURATION,
            show_close: bool = True,
            in_window: bool = True,
            animated: bool = None
    ):
        """初始化通知组件
        
        Args:
            text: 通知文本内容
            parent: 父组件
            position: 显示位置，支持枚举或字符串
            duration: 自动消失时间（毫秒），0表示不自动消失
            show_close: 是否显示关闭按钮
            in_window: 是否在父窗口内显示
            animated: 是否启用动画，None表示使用全局配置
        """
        super().__init__(parent)

        # 处理位置参数（支持字符串和枚举）
        if isinstance(position, str):
            self.position = XNotif.Pos(position.lower())
        else:
            self.position = position

        # 保存配置
        self.duration = duration
        self.in_window = in_window
        self._animated = animated if animated is not None else self.ANIMATION_ENABLED

        # 初始化状态变量
        self._is_closing = False
        self._timer = None
        self._fade_in_anim = None
        self._fade_out_anim = None
        self._move_anim = None

        # 设置窗口属性
        if in_window:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow)
        else:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("xnotification")
        self.show_close = show_close

        # 初始化界面
        self._setup_ui(text)

    def _setup_ui(self, text: str):
        """初始化界面
        
        Args:
            text: 通知文本
        """
        self.setMinimumWidth(100)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 创建容器
        self.container = QWidget(self)
        self.container.setObjectName('notification-container')
        main_layout.addWidget(self.container)

        # 创建水平布局
        layout = QHBoxLayout(self.container)
        layout.setContentsMargins(6, 6, 0, 6)
        layout.setSpacing(8)

        self.icon_button = QPushButton()
        # 1. 拦截点击事件
        self.icon_button.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.icon_button.setFocusPolicy(Qt.NoFocus)

        self.icon_button.setObjectName("notification-icon")
        layout.addWidget(self.icon_button, 0, Qt.AlignVCenter)

        # 文本标签
        self.text_label = XLabel(self._truncate_text(text))
        self.text_label.setWordWrap(False)
        layout.addWidget(self.text_label, 1, Qt.AlignVCenter)

        # 关闭按钮
        if self.show_close:
            self.close_button = XPushButton(variant=XButtonVariant.LINK, icon=IconName.CLOSE, size=XSize.SMALL,
                                            color=XColor.SECONDARY)
            self.close_button.setCursor(Qt.PointingHandCursor)
            self.close_button.clicked.connect(self.close_notification)
            layout.addWidget(self.close_button, 0, Qt.AlignVCenter)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setMaximumWidth(self.MAX_WIDTH)

    def _truncate_text(self, text: str) -> str:
        """截断超长文本
        
        Args:
            text: 原始文本
            
        Returns:
            截断后的文本（如果超长则添加省略号）
        """
        if len(text) <= self.MAX_TEXT_LENGTH:
            return text
        return text[:self.MAX_TEXT_LENGTH - 3] + "..."

    def _set_icon(self, icon_name: IconName, color: str):
        """设置通知图标
        
        Args:
            icon_name: 图标名称
            color: 图标颜色
        """
        self.icon_button.setIcon(XIcon.get(name=icon_name, size=20, color=color).icon())
        self.icon_button.setIconSize(QSize(20, 20))

    def _fade_in(self):
        """执行淡入动画
        
        从透明度0渐变到1，持续时间为FADE_IN_DURATION毫秒。
        动画对象绑定到实例，防止被垃圾回收。
        """
        self.setWindowOpacity(0.0)
        self.show()

        # 创建淡入动画
        self._fade_in_anim = QPropertyAnimation(self, b"windowOpacity")
        self._fade_in_anim.setDuration(self.FADE_IN_DURATION)
        self._fade_in_anim.setStartValue(0.0)
        self._fade_in_anim.setEndValue(1.0)
        self._fade_in_anim.setEasingCurve(self.EASING_CURVE)
        self._fade_in_anim.finished.connect(self._on_fade_in_finished)
        self._fade_in_anim.start()

    def _on_fade_in_finished(self):
        """淡入动画完成回调
        
        清理动画对象引用，释放内存。
        """
        if self._fade_in_anim:
            self._fade_in_anim.deleteLater()
            self._fade_in_anim = None

    def _fade_out(self):
        """执行淡出动画
        
        从透明度1渐变到0，持续时间为FADE_OUT_DURATION毫秒。
        动画完成后自动关闭窗口。
        """
        # 创建淡出动画
        self._fade_out_anim = QPropertyAnimation(self, b"windowOpacity")
        self._fade_out_anim.setDuration(self.FADE_OUT_DURATION)
        self._fade_out_anim.setStartValue(1.0)
        self._fade_out_anim.setEndValue(0.0)
        self._fade_out_anim.setEasingCurve(self.EASING_CURVE)
        self._fade_out_anim.finished.connect(self._on_fade_out_finished)

        # 停止自动关闭定时器
        self._is_closing = True
        if self._timer:
            self._timer.stop()

        self._fade_out_anim.start()

    def _on_fade_out_finished(self):
        """淡出动画完成回调
        
        清理动画对象引用并关闭窗口。
        """
        if self._fade_out_anim:
            self._fade_out_anim.deleteLater()
            self._fade_out_anim = None
        self.close()

    def _slide_to(self, target_pos: QPoint, duration: int = 300):
        """平滑移动到目标位置
        
        使用位置动画实现平滑移动效果，用于通知堆叠时的位置调整。
        
        Args:
            target_pos: 目标位置
            duration: 动画时长（毫秒），默认300ms
        """
        # 如果已经在目标位置，不需要动画
        if self.pos() == target_pos:
            return

        # 如果有正在进行的移动动画，停止它
        if self._move_anim:
            self._move_anim.stop()
            self._move_anim.deleteLater()

        # 创建位置动画
        self._move_anim = QPropertyAnimation(self, b"pos")
        self._move_anim.setDuration(duration)
        self._move_anim.setStartValue(self.pos())
        self._move_anim.setEndValue(target_pos)
        self._move_anim.setEasingCurve(self.EASING_CURVE)
        self._move_anim.finished.connect(self._on_move_finished)
        self._move_anim.start()

    def _on_move_finished(self):
        """移动动画完成回调
        
        清理动画对象引用，释放内存。
        """
        if self._move_anim:
            self._move_anim.deleteLater()
            self._move_anim = None

    def _calculate_position(self, parent_rect):
        """计算通知的显示位置
        
        根据通知的位置配置和父窗口/屏幕尺寸计算目标位置。
        
        Args:
            parent_rect: 父窗口或屏幕的矩形区域
            
        Returns:
            QPoint: 目标位置坐标
        """
        self.adjustSize()
        width, height = self.width(), self.height()

        if self.in_window:
            # 在父窗口内显示
            if self.position == XNotif.Pos.CENTER:
                return QPoint((parent_rect.width() - width) // 2, (parent_rect.height() - height) // 2)
            elif self.position == XNotif.Pos.TOP_LEFT:
                return QPoint(self.MARGIN, self.MARGIN)
            elif self.position == XNotif.Pos.TOP_RIGHT:
                return QPoint(parent_rect.width() - width - self.MARGIN, self.MARGIN)
            elif self.position == XNotif.Pos.BOTTOM_LEFT:
                return QPoint(self.MARGIN, parent_rect.height() - height - self.MARGIN)
            else:
                return QPoint(parent_rect.width() - width - self.MARGIN, parent_rect.height() - height - self.MARGIN)
        else:
            # 在屏幕上显示
            screen_geometry = QApplication.primaryScreen().availableGeometry()
            if self.position == XNotif.Pos.CENTER:
                return QPoint((screen_geometry.width() - width) // 2, (screen_geometry.height() - height) // 2)
            elif self.position == XNotif.Pos.TOP_LEFT:
                return QPoint(self.MARGIN, self.MARGIN)
            elif self.position == XNotif.Pos.TOP_RIGHT:
                return QPoint(screen_geometry.width() - width - self.MARGIN, self.MARGIN)
            elif self.position == XNotif.Pos.BOTTOM_LEFT:
                return QPoint(self.MARGIN, screen_geometry.height() - height - self.MARGIN)
            else:
                return QPoint(screen_geometry.width() - width - self.MARGIN,
                              screen_geometry.height() - height - self.MARGIN)

    def show_notification(self):
        """显示通知
        
        将通知添加到通知列表，计算显示位置，调整已有通知的位置，
        然后显示通知并启动自动关闭定时器。
        """
        # 添加到通知列表
        self.__class__._notifications.append(self)

        # 计算目标位置
        if self.parent() and self.in_window:
            target_pos = self._calculate_position(self.parent().rect())
        else:
            screen_geometry = QApplication.primaryScreen().availableGeometry()
            target_pos = self._calculate_position(screen_geometry)

        # 为已有的通知腾出空间（使用平滑移动动画）
        for notification in self.__class__._notifications[:-1]:
            if notification.position == self.position:
                pos = notification.pos()
                if self.position in [XNotif.Pos.TOP_LEFT, XNotif.Pos.TOP_RIGHT]:
                    # 顶部位置：向下移动
                    new_pos = QPoint(pos.x(), pos.y() + self.height() + self.SPACING)
                else:
                    # 底部位置：向上移动
                    new_pos = QPoint(pos.x(), pos.y() - self.height() - self.SPACING)

                # 使用动画平滑移动
                if notification._animated:
                    notification._slide_to(new_pos)
                else:
                    notification.move(new_pos)

        # 移动到目标位置并置顶
        self.move(target_pos)
        self.raise_()

        # 使用动画或直接显示
        if self._animated:
            self._fade_in()
        else:
            self.show()

        # 如果duration大于0，启动自动关闭定时器
        if self.duration > 0:
            self._timer = QTimer(self)
            self._timer.timeout.connect(self.close_notification)
            self._timer.start(self.duration)

    def close_notification(self):
        """关闭通知
        
        如果正在关闭中，直接返回。
        根据动画配置使用淡出动画或直接关闭。
        """
        if self._is_closing:
            return

        # 使用动画或直接关闭
        if self._animated:
            self._fade_out()
        else:
            self._is_closing = True
            if self._timer:
                self._timer.stop()
            self.close()

    def closeEvent(self, event):
        """窗口关闭事件
        
        从通知列表中移除自己，然后调用父类的关闭事件。
        
        Args:
            event: 关闭事件对象
        """
        if self in self.__class__._notifications:
            self.__class__._notifications.remove(self)
        super().closeEvent(event)

    @classmethod
    def _create_notification(cls, text: str, icon: IconName, color: Union[XColor, str], parent=None,
                             position: Union[Pos, str] = "center",
                             duration=DURATION, show_close=False, in_window=True, animated=None):
        """创建通知的通用方法
        
        Args:
            text: 通知文本
            icon: 图标名称
            color: 图标颜色
            parent: 父组件
            position: 显示位置
            duration: 自动消失时间
            show_close: 是否显示关闭按钮
            in_window: 是否在父窗口内显示
            animated: 是否启用动画
            
        Returns:
            XNotif: 创建的通知实例
        """
        w = cls(text, parent, position, duration, show_close, in_window, animated)
        w._set_icon(icon, color)
        w.show_notification()
        return w

    @classmethod
    def info(cls, text: str, parent=None, position: Union[Pos, str] = "center",
             duration=DURATION, show_close=True, in_window=True, animated=None):
        """显示信息通知
        
        Args:
            text: 通知文本
            parent: 父组件
            position: 显示位置
            duration: 自动消失时间
            show_close: 是否显示关闭按钮
            in_window: 是否在父窗口内显示
            animated: 是否启用动画
            
        Returns:
            XNotif: 创建的通知实例
        """
        return cls._create_notification(text, IconName.INFO, XColor.PRIMARY, parent, position,
                                        duration, show_close, in_window, animated)

    @classmethod
    def success(cls, text: str, parent=None, position: Union[Pos, str] = "center",
                duration=DURATION, show_close=True, in_window=True, animated=None):
        """显示成功通知
        
        Args:
            text: 通知文本
            parent: 父组件
            position: 显示位置
            duration: 自动消失时间
            show_close: 是否显示关闭按钮
            in_window: 是否在父窗口内显示
            animated: 是否启用动画
            
        Returns:
            XNotif: 创建的通知实例
        """
        return cls._create_notification(text, IconName.CHECK_CIRCLE, theme_manager.colors.success, parent, position,
                                        duration, show_close, in_window, animated)

    @classmethod
    def warning(cls, text: str, parent=None, position: Union[Pos, str] = "center",
                duration=DURATION, show_close=True, in_window=True, animated=None):
        """显示警告通知
        
        Args:
            text: 通知文本
            parent: 父组件
            position: 显示位置
            duration: 自动消失时间
            show_close: 是否显示关闭按钮
            in_window: 是否在父窗口内显示
            animated: 是否启用动画
            
        Returns:
            XNotif: 创建的通知实例
        """
        return cls._create_notification(text, IconName.WARNING, theme_manager.colors.warning, parent, position,
                                        duration, show_close, in_window, animated)

    @classmethod
    def error(cls, text: str, parent=None, position: Union[Pos, str] = "center",
              duration=DURATION, show_close=True, in_window=True, animated=None):
        """显示错误通知
        
        Args:
            text: 通知文本
            parent: 父组件
            position: 显示位置
            duration: 自动消失时间
            show_close: 是否显示关闭按钮
            in_window: 是否在父窗口内显示
            animated: 是否启用动画
            
        Returns:
            XNotif: 创建的通知实例
        """
        return cls._create_notification(text, IconName.CLOSE_CIRCLE, theme_manager.colors.danger, parent, position,
                                        duration, show_close, in_window, animated)
