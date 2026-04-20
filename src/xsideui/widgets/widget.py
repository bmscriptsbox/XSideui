"""
XWidget 组件 - 基础容器组件

支持明暗主题切换的无边框窗口容器，带阴影效果和标题栏。
"""
import ctypes
from ctypes import windll, wintypes, byref, c_int, Structure, c_long, c_uint

from ..utils.qt_compat import QWidget, QVBoxLayout, QFrame, QIcon, Qt, QByteArray, QPoint, QPropertyAnimation, \
    QEasingCurve, QPushButton, QLabel, QApplication, QCursor, QGraphicsOpacityEffect, QTimer

from .title_bar import XTitleBar
from ..icon import IconName, XIcon


# Windows 结构体定义
class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


class RECT(Structure):
    _fields_ = [("left", c_long), ("top", c_long), ("right", c_long), ("bottom", c_long)]


class MINMAXINFO(Structure):
    _fields_ = [
        ("ptReserved", POINT),
        ("ptMaxSize", POINT),
        ("ptMaxPosition", POINT),
        ("ptMinTrackSize", POINT),
        ("ptMaxTrackSize", POINT),
    ]


class MONITORINFO(Structure):
    _fields_ = [
        ("cbSize", c_uint),
        ("rcMonitor", RECT),
        ("rcWork", RECT),
        ("dwFlags", c_uint),
    ]


class XWidget(QWidget):
    MINMAXINFO = MINMAXINFO
    MONITORINFO = MONITORINFO

    def __init__(self,
                 title: str = "",
                 logo: str = None,
                 show_min: bool = True,
                 show_max: bool = True,
                 show_close: bool = True,
                 show_dark: bool = True,
                 parent=None
                 ):
        """初始化自定义无边框窗口容器。

            Args:
                title: 窗口标题。
                logo: 图标路径或 IconName 枚举。
                show_min: 是否显示最小化按钮。
                show_max: 是否显示最大化/还原按钮。
                show_close: 是否显示关闭按钮。
                show_dark: 是否支持深色模式切换/适配。
                parent: 父组件。
            """
        super().__init__(parent)
        self.is_max = None
        self.setObjectName("xwidget")
        self._title = title
        self._logo = logo
        self._show_min = show_min
        self._show_max = show_max
        self._show_close = show_close
        self._show_dark = show_dark
        self._is_first_show = True  # 标记位
        self.title_bar = None

        self.setWindowFlags(Qt.Window | Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)

        self._setup_base_ui()

    def show(self):
        self._apply_native_style()
        super().show()
        self.setUpdatesEnabled(True)

    def _apply_native_style(self):
        hwnd = self.winId().__int__()


        # 调整窗口样式
        style = windll.user32.GetWindowLongW(hwnd, -16)
        # 保持 WS_MAXIMIZEBOX, WS_MINIMIZEBOX, WS_THICKFRAME (用于缩放和阴影)
        new_style = style | 0x00020000 | 0x00010000 | 0x00040000
        windll.user32.SetWindowLongW(hwnd, -16, new_style)

        # 开启阴影 (针对 Win10/11)
        class MARGINS(Structure):
            _fields_ = [("left", c_int), ("right", c_int), ("top", c_int), ("bottom", c_int)]

        margins = MARGINS(1, 1, 1, 1)
        windll.dwmapi.DwmExtendFrameIntoClientArea(hwnd, byref(margins))

        # 针对 Win11 的圆角
        try:
            windll.dwmapi.DwmSetWindowAttribute(hwnd, 33, byref(c_int(2)), 4)
        except:
            pass


        user32 = windll.user32
        style = user32.GetWindowLongW(hwnd, -16)  # GWL_STYLE
        # 移除标题栏和系统菜单，保留缩放边框
        style &= ~0x00C00000  # 移除 WS_CAPTION (TITLEBAR + SYSMENU)
        style |= 0x00040000  # 确保 WS_THICKFRAME 开启
        user32.SetWindowLongW(hwnd, -16, style)
        try:
            windll.dwmapi.DwmSetWindowAttribute(hwnd, 33, byref(c_int(2)), 4)
            windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, byref(c_int(1)), 4)
        except:
            pass
        # 刷新窗口样式
        user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x0027)


    def nativeEvent(self, event_type, message):
        """处理 Windows 原生消息，实现无边框窗口的缩放、拖拽及 Snap Layouts"""
        if event_type != QByteArray(b"windows_generic_MSG"):
            return super().nativeEvent(event_type, message)

        msg = wintypes.MSG.from_address(message.__int__())

        # 状态保护：窗口被禁用时不拦截消息
        if not self.isEnabled():
            return False, 0

        # 防止无边框窗口残影
        if msg.message == 0x0083:  # WM_NCCALCSIZE
            return True, 0
        if msg.message == 0x0086:  # WM_NCACTIVATE
            return True, 1

        # 最大化不遮挡任务栏
        if msg.message == 0x0024:  # WM_GETMINMAXINFO
            info = ctypes.cast(msg.lParam, ctypes.POINTER(self.MINMAXINFO)).contents

            # 获取显示器信息和工作区
            h_monitor = windll.user32.MonitorFromWindow(msg.hWnd, 2)
            monitor_info = self.MONITORINFO()
            monitor_info.cbSize = ctypes.sizeof(monitor_info)
            windll.user32.GetMonitorInfoW(h_monitor, byref(monitor_info))

            # 计算最大化位置
            work_rect = monitor_info.rcWork
            screen_rect = monitor_info.rcMonitor
            info.ptMaxPosition.x = work_rect.left - screen_rect.left
            info.ptMaxPosition.y = work_rect.top - screen_rect.top
            info.ptMaxSize.x = work_rect.right - work_rect.left
            info.ptMaxSize.y = work_rect.bottom - work_rect.top

            return True, 0

        # 判定鼠标在窗口哪个部位 (WM_NCHITTEST)
        if msg.message == 0x0084:
            # 获取屏幕物理坐标
            x = ctypes.c_short(msg.lParam & 0xFFFF).value
            y = ctypes.c_short(msg.lParam >> 16).value

            # 获取窗口物理矩形
            rect = wintypes.RECT()
            windll.user32.GetWindowRect(msg.hWnd, byref(rect))

            # 计算相对坐标
            lx = x - rect.left
            ly = y - rect.top
            w = rect.right - rect.left
            h = rect.bottom - rect.top

            # 获取缩放边距
            bw = windll.user32.GetSystemMetrics(32) + windll.user32.GetSystemMetrics(92)

            # 判定缩放边缘
            if ly < bw:
                if lx < bw: return True, 13  # HTTOPLEFT
                if lx >= w - bw: return True, 14  # HTTOPRIGHT
                return True, 12  # HTTOP
            if ly >= h - bw:
                if lx < bw: return True, 16  # HTBOTTOMLEFT
                if lx >= w - bw: return True, 17  # HTBOTTOMRIGHT
                return True, 15  # HTBOTTOM
            if lx < bw: return True, 10  # HTLEFT
            if lx >= w - bw: return True, 11  # HTRIGHT

            # 判定标题栏及子控件
            dpr = self.devicePixelRatioF()
            qt_local_pos = QPoint(int(lx / dpr), int(ly / dpr))

            if self.title_bar and self.title_bar.isVisible():
                title_rect = self.title_bar.geometry()

                if title_rect.contains(qt_local_pos):
                    # 检查鼠标下方的子控件
                    child_pos = self.title_bar.mapFromParent(qt_local_pos)
                    child = self.title_bar.childAt(child_pos)

                    # 如果是交互控件，交给 Qt 处理
                    if child and (isinstance(child, (QPushButton, QLabel)) or child.accessibleName()):
                        return False, 0

                    # 否则返回 HTCAPTION，触发系统拖拽
                    return True, 2

        # 处理 Snap Layouts 的点击模拟
        if msg.message in [0x00A1, 0x00A2]:  # WM_NCLBUTTONDOWN / UP
            if msg.wParam == 9:  # HTMAXBUTTON
                max_btn = getattr(self.title_bar, 'max_button', None)
                if max_btn and self.isEnabled():
                    if msg.message == 0x00A1:
                        max_btn.setDown(True)
                    else:
                        max_btn.setDown(False)
                        max_btn.click()
                return True, 0

        return super().nativeEvent(event_type, message)

    def changeEvent(self, event):
        if event.type() == event.Type.WindowStateChange:
            self.is_max = self.isMaximized()
            if self.title_bar:
                icon = IconName.OFF_SCREEN if self.is_max else IconName.FULL_SCREEN
                self.title_bar.max_button.setIcon(XIcon(icon).icon())
        super().changeEvent(event)

    def showEvent(self, event):
        if self._is_first_show:
            QTimer.singleShot(0, self._deferred_setup)
            self._is_first_show = False
        super().showEvent(event)

    def _deferred_setup(self):
        # 预计算尺寸
        content = getattr(self, '_main_content_proxy', None)
        if content:
            content.ensurePolished()
            size = content.sizeHint()
            self.resize(max(self.width(), size.width()), max(self.height(), size.height()))

        # 精准定位并显示
        self.move(self._get_centered_pos())
        self.setWindowOpacity(1.0)

        # 3. 延迟挂载内容
        QTimer.singleShot(100, self._final_mount_logic)

    def _final_mount_logic(self):
        content = getattr(self, '_main_content_proxy', None)
        if content:
            # 将组件放入布局
            self.base_container_layout.addWidget(content)
            # 执行淡入
            self._fade_in_widget(content, duration=500)
            self._main_content_proxy = None

    def _fade_in_widget(self, widget: QWidget, duration: int = 450):
        """为重型组件创建透明度淡入效果"""
        widget.setAttribute(Qt.WA_StaticContents, True)
        # 创建透明度效果器
        self.content_opacity_effect = QGraphicsOpacityEffect(widget)
        self.content_opacity_effect.setOpacity(0.0)  # 初始透明
        widget.setGraphicsEffect(self.content_opacity_effect)
        widget.show()

        # 设置动画
        self.content_fade_ani = QPropertyAnimation(self.content_opacity_effect, b"opacity")
        self.content_fade_ani.setDuration(duration)
        self.content_fade_ani.setStartValue(0.0)
        self.content_fade_ani.setEndValue(1.0)
        self.content_fade_ani.setEasingCurve(QEasingCurve.OutCubic)

        def on_finished():
            widget.setGraphicsEffect(None)
            widget.setAttribute(Qt.WA_StaticContents, False)

        self.content_fade_ani.finished.connect(on_finished)
        self.content_fade_ani.start()

    def _get_centered_pos(self) -> QPoint:
        """
        计算主窗口居中的目标坐标（静默计算，不执行移动）

        Returns:
            QPoint: 窗口左上角应该移动到的目标坐标
        """
        # 1. 确定目标屏幕：优先选择鼠标指针所在的屏幕，这比 primaryScreen 更智能
        screen = QApplication.screenAt(QCursor.pos())
        if not screen:
            screen = QApplication.primaryScreen()

        # 2. 获取该屏幕的可用几何区域（排除任务栏/工具栏）
        avail_geom = screen.availableGeometry()

        # 3. 智能尺寸自适应（安全检查）
        limit_w = int(avail_geom.width() * 0.9)
        limit_h = int(avail_geom.height() * 0.9)

        curr_w = self.width()
        curr_h = self.height()

        # 如果窗口预设尺寸太大，强制 resize 以适应屏幕
        if curr_w > limit_w or curr_h > limit_h:
            ratio = min(limit_w / curr_w, limit_h / curr_h)
            curr_w = int(curr_w * ratio)
            curr_h = int(curr_h * ratio)
            self.resize(curr_w, curr_h)

        # 4. 精准居中计算
        # 计算公式：屏幕起始点 + (屏幕宽度 - 窗口宽度) / 2
        target_x = avail_geom.x() + (avail_geom.width() - curr_w) // 2
        target_y = avail_geom.y() + (avail_geom.height() - curr_h) // 2

        # 5. 边界防御：确保标题栏不会被推到屏幕上方边缘之外（否则无法拖动）
        # 在 Windows 下，y 坐标至少应等于 avail_geom.y()
        final_x = max(avail_geom.x(), target_x)
        final_y = max(avail_geom.y(), target_y)

        return QPoint(final_x, final_y)

    def _setup_base_ui(self):
        self.base_main_layout = QVBoxLayout(self)
        self.base_main_layout.setContentsMargins(0, 0, 0, 0)
        self.base_main_layout.setSpacing(0)

        self.base_main_frame = QFrame(self)
        self.base_main_frame.setObjectName("MainFrame")
        self.base_main_layout.addWidget(self.base_main_frame)

        self.frame_layout = QVBoxLayout(self.base_main_frame)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_layout.setSpacing(0)

        # --- 自定义标题栏 ---
        self.title_bar = XTitleBar(
            title=self._title,
            logo=self._logo,
            show_min=self._show_min,
            show_max=self._show_max,
            show_close=self._show_close,
            show_dark=self._show_dark,
            parent=self
        )

        self.title_bar.windowMinimumed.connect(self.showMinimized)
        self.title_bar.windowsMaxOrNor.connect(self._handle_max_normal)
        self.title_bar.windowClosed.connect(self.close)
        self.frame_layout.addWidget(self.title_bar, 0)

        # 创建一个专门存放内容的容器
        base_container = QFrame(self.base_main_frame)
        self.base_container_layout = QVBoxLayout(base_container)
        self.base_container_layout.setContentsMargins(0, 0, 0, 0)
        self.base_container_layout.setSpacing(0)
        self.base_container_layout.setAlignment(Qt.AlignTop)
        self.frame_layout.addWidget(base_container, 1)

    def _handle_max_normal(self):
        if self.is_max:
            self.showNormal()
        else:
            self.showMaximized()

    def addWidget(self, widget: QWidget):
        if self._is_first_show:
            self._main_content_proxy = widget
            # 建立父子关系，这样 widget 就能拿到窗口的样式和 DPI
            widget.setParent(self)
            widget.hide()
        else:
            self.base_container_layout.addWidget(widget)
        return self

    def addLayout(self, layout):
        """添加布局到内容区域

        Args:
            layout: 要添加的布局

        Returns:
            self (支持链式调用)
        """
        if self._is_first_show:
            # 创建一个临时的透明容器来承载这个布局
            container = QWidget()
            container.setAttribute(Qt.WA_TransparentForMouseEvents, False)
            container.setLayout(layout)
            # 复用 addWidget 的逻辑
            return self.addWidget(container)
        else:
            self.base_container_layout.addLayout(layout)
        return self

    def set_title(self, title: str) -> 'XWidget':
        """设置窗口标题

        Args:
            title: 窗口标题

        Returns:
            self (支持链式调用)
        """
        self._title = title
        self.setWindowTitle(title)
        self.title_bar.set_title(title)
        return self

    def set_logo(self, icon) -> 'XWidget':
        """设置窗口图标

        Args:
            icon: 图标路径或 QIcon 对象

        Returns:
            self (支持链式调用)
        """
        self._logo = icon
        if isinstance(icon, str):
            self.setWindowIcon(QIcon(icon))
        elif isinstance(icon, QIcon):
            self.setWindowIcon(icon)
        self.title_bar.set_logo(icon)
        return self

    def hide_title_bar(self) -> 'XWidget':
        """隐藏标题栏

        Returns:
            self (支持链式调用)
        """
        self.title_bar.hide()
        return self

    def hide_minimize_button(self) -> 'XWidget':
        """隐藏最小化按钮

        Returns:
            self (支持链式调用)
        """
        if hasattr(self.title_bar, 'min_button'):
            self.title_bar.min_button.hide()
        return self

    def hide_maximize_button(self) -> 'XWidget':
        """隐藏最大化按钮

        Returns:
            self (支持链式调用)
        """
        if hasattr(self.title_bar, 'max_button'):
            self.title_bar.max_button.hide()
        return self

    def hide_theme_button(self) -> 'XWidget':
        """隐藏主题切换按钮

        Returns:
            self (支持链式调用)
        """
        if hasattr(self.title_bar, 'theme_btn'):
            self.title_bar.theme_btn.hide()
        return self

    def add_title_bar_widget(self, widget):
        if self.title_bar:
            self.title_bar.add_widget(widget)
        return self
