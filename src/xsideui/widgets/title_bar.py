from typing import Union

from ..utils.qt_compat import QFrame, QHBoxLayout, QLabel, QSizePolicy, QIcon, Signal, QPoint, Qt, QEvent

from .pushbutton import XPushButton
from ..icon import IconName, XIcon
from ..theme import theme_manager
from ..xenum import XButtonVariant, XSize, XColor
from .label import XLabel


class XTitleBar(QFrame):
    """标题栏组件"""

    windowMinimumed = Signal()
    windowMaximumed = Signal()
    windowsMaxOrNor = Signal()
    windowNormaled = Signal()
    windowClosed = Signal()
    windowMoved = Signal(QPoint)

    def __init__(
        self,
        title: str = "XSideUI",
        logo: str = '',
        show_min: bool = True,
        show_max: bool = True,
        show_close: bool = True,
        show_dark: bool = True,
        parent=None
    ):
        """初始化标题栏

        Args:
            title: 窗口标题
            logo: 窗口图标路径
            show_min: 是否显示最小化按钮
            show_max: 是否显示最大化按钮
            show_dark: 是否显示明暗主题切换按钮
            show_close: 是否显示关闭按钮
            parent: 父组件
        """
        super().__init__(parent)
        self.setObjectName("xtitlebar")
        self._title = title
        self._logo = logo or XIcon(name=IconName.XSIDEUI, color=XColor.PRIMARY).icon()
        self._show_min = show_min
        self._show_max = show_max
        self._show_dark = show_dark
        self._show_close = show_close
        self._drag_pos = QPoint()
        self._is_dragging = False
        self.setMinimumHeight(36)
        
        theme_manager.initialize()
        self._init_ui()

    def _init_ui(self):
        """初始化用户界面"""
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 左侧：图标 + 标题
        self.left_layout = QHBoxLayout()
        self.left_layout.setContentsMargins(10, 0, 0, 0)
        self.left_layout.setSpacing(8)

        if self._logo:
            self.icon_label = QLabel()
            self.icon_label.setObjectName("xtitlebarlogo")
            self.icon_label.setFixedSize(18, 18)
            self.left_layout.addWidget(self.icon_label)

            self.set_logo(self._logo)

        self.title_label = XLabel(self._title)
        self.left_layout.addWidget(self.title_label)

        # 中间区：用来接收用户 add_widget 的组件
        self.middle_layout = QHBoxLayout()
        self.middle_layout.addStretch(1)

        # 右侧：按钮组
        self.right_layout = QHBoxLayout()
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(0)

        self._setup_window_buttons()

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.middle_layout, 1)
        self.main_layout.addLayout(self.right_layout)

    def add_widget(self, widget):
        """标题栏添加自定义组件"""
        widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        if self.middle_layout.count() == 0:
            self.middle_layout.addStretch(1)
        self.middle_layout.addWidget(widget)

    def _setup_window_buttons(self):
        """设置窗口控制按钮"""
        if self._show_dark:
            self.theme_btn = XPushButton(icon=IconName.MOON if theme_manager.is_dark else IconName.SUN, variant=XButtonVariant.TEXT, size=XSize.SMALL, color=XColor.SECONDARY)
            self.theme_btn.clicked.connect(self._toggle_theme)
            self.theme_btn.setFixedSize(36,36)
            self.theme_btn.setContentsMargins(0, 0, 0, 0)
            self.right_layout.addWidget(self.theme_btn)

        if self._show_min:
            self.min_button = XPushButton(icon=IconName.MINUS, variant=XButtonVariant.TEXT, size=XSize.SMALL, color=XColor.SECONDARY)
            self.min_button.clicked.connect(self.windowMinimumed.emit)
            self.min_button.setFixedSize(36, 36)
            self.min_button.setContentsMargins(0, 0, 0, 0)
            self.right_layout.addWidget(self.min_button)

        if self._show_max:
            self.max_button = XPushButton(icon=IconName.FULL_SCREEN, variant=XButtonVariant.TEXT, size=XSize.SMALL, color=XColor.SECONDARY)
            self.max_button.setMouseTracking(True)
            self.max_button.setAttribute(Qt.WA_Hover, True)  # 确保支持悬停属性
            self.max_button.clicked.connect(self._toggle_maximize)
            self.max_button.setFixedSize(36, 36)
            self.max_button.setContentsMargins(0, 0, 0, 0)
            self.right_layout.addWidget(self.max_button)

        if self._show_close:
            self.close_button = XPushButton(icon=IconName.CLOSE, variant=XButtonVariant.TEXT, size=XSize.SMALL, color=XColor.SECONDARY)
            self.close_button.clicked.connect(self.windowClosed.emit)
            self.close_button.setFixedSize(36, 36)
            self.close_button.setContentsMargins(0, 0, 0, 0)
            self.close_button.installEventFilter(self)
            self.right_layout.addWidget(self.close_button)

    def _toggle_theme(self, name):
        """切换主题"""

        theme_manager.toggle_theme()
        if theme_manager.is_dark:
            self.theme_btn.setIcon(XIcon(IconName.MOON).icon())
        else:
            self.theme_btn.setIcon(XIcon(IconName.SUN).icon())

    def _toggle_maximize(self):
        """切换最大化状态"""
        self.windowsMaxOrNor.emit()


    def set_logo(self, icon: Union[str, QIcon]):
        """设置图标"""
        if not self._logo:
            self.icon_label = QLabel()
            self.icon_label.setObjectName("xtitlebarlogo")
            self.icon_label.setFixedSize(18, 18)
            self.left_layout.insertWidget(0, self.icon_label)

        if icon:
            try:
                if isinstance(icon, str):
                    if icon.startswith(":") or icon.endswith((".png", ".svg", ".jpg", ".jpeg")):
                        pix = QIcon(icon).pixmap(18, 18)
                    else:
                        from src.xsideui.icon import get_icon
                        pix = get_icon(icon).pixmap(18, 18)
                elif isinstance(icon, QIcon):
                    pix = icon.pixmap(18, 18)
                else:
                    return
                self.icon_label.setPixmap(pix)
            except Exception as e:
                print(f"Failed to set logo: {e}")

    def set_title(self, title: str):
        """设置标题"""
        if title:
            self.title_label.setText(title)



    def eventFilter(self, obj, event):
        """事件过滤器，用于处理关闭按钮的悬浮效果"""
        if not self.window().isEnabled():  # 核心保护：窗口禁用时不处理
            return super().eventFilter(obj, event)
        if obj == self.close_button:
            if event.type() == QEvent.Enter:
                self.close_button.set_color(XColor.DANGER).set_variant(XButtonVariant.SOLID)
            elif event.type() == QEvent.Leave:
                self.close_button.set_color(XColor.SECONDARY).set_variant(XButtonVariant.TEXT)
        return super().eventFilter(obj, event)
