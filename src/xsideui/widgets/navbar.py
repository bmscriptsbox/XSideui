"""
Navigation Bar Component 导航栏组件
简单高效的导航栏组件，支持主题切换、图标缓存、悬停提示等功能。

主要组件：
- NavItemIconCache: 图标缓存管理类
- NavItem: 导航项组件
- XNavSimple: 导航栏容器组件
"""
from typing import Optional

from ..utils.qt_compat import QFrame, QWidget, QPushButton, QVBoxLayout, QToolTip, Qt, Signal, QSize, QRectF, QPoint, \
    QPainter, QColor, QBrush, QTimer, QEvent
from ..icon import XIcon
from ..theme import theme_manager
from ..i18n import XI18N


class NavItem(QWidget):
    """导航项组件

    单个导航项，支持图标显示、选中状态、悬停效果和提示文本。

    Features:
        - 图标显示（支持主题色切换）
        - 选中指示条（左侧圆角矩形）
        - 悬停高亮效果
        - 工具提示（ToolTip）
        - 图标缓存优化

    Signals:
        clicked: 点击信号
    """
    clicked = Signal()

    def __init__(self, icon_name, text=None, icon_size=18, parent=None):
        """初始化导航项

        Args:
            icon_name: 图标名称（支持字符串或 IconName 枚举）
            text: 提示文本（作为 ToolTip 显示）
            icon_size: 图标尺寸（像素）
            parent: 父组件
        """
        super().__init__(parent)
        self.icon_name = icon_name
        self.icon_size = icon_size
        self._text_key = text  # 作为 ToolTip 显示
        self._is_selected = False
        self._is_hovered = False

        # 初始化界面
        self._init_ui()

        # 设置鼠标样式
        self.setCursor(Qt.PointingHandCursor)

        # 设置工具提示
        if self._text_key:
            self.retranslateUi()

        # 更新图标
        self.update_icon()

    def retranslateUi(self):
        """当语言切换或文本更新时调用"""
        if not self._text_key:
            return
        translated = XI18N.x_tr(self._text_key)
        super().setToolTip(translated)

    def changeEvent(self, event):
        """监听翻译事件"""
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi()
        super().changeEvent(event)

    def _init_ui(self):
        """初始化界面布局"""
        self.setObjectName("navitem")
        self.setAttribute(Qt.WA_StyledBackground, True)

        # 导航项通常为正方形或稍微高一点
        self.setFixedSize(40, 40)

        # 创建垂直布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        # 创建图标标签
        self.icon_btn = QPushButton()
        self.icon_btn.setAttribute(Qt.WA_TransparentForMouseEvents)  # 核心：让点击穿透到 NavItem
        self.icon_btn.setFocusPolicy(Qt.NoFocus)
        self.icon_btn.setFlat(True)
        self.icon_btn.setStyleSheet("background: transparent; border: none; padding: 0px;")
        self.icon_btn.setIconSize(QSize(self.icon_size, self.icon_size))
        layout.addWidget(self.icon_btn)

    def setSelected(self, selected: bool):
        """设置选中状态

        Args:
            selected: 是否选中
        """
        if self._is_selected != selected:
            self._is_selected = selected

            # 更新 QSS 属性
            self.setProperty("selected", "true" if selected else "false")
            self.style().unpolish(self)
            self.style().polish(self)

            # 更新图标和重绘指示条
            self.update_icon()
            self.update()

    def update_icon(self):
        """更新图标（根据选中/悬停状态）

        选中或悬停时使用主题色，否则使用文本色。
        """
        if not self.icon_name:
            return

        # 根据状态选择颜色
        color = theme_manager.colors.primary if (self._is_selected or self._is_hovered) else theme_manager.colors.text_1
        icon = XIcon(name=self.icon_name, color=color, size=self.icon_size).icon()
        if icon:
            self.icon_btn.setIcon(icon)

    def enterEvent(self, event):
        """鼠标进入事件：显示悬停效果和工具提示

        Args:
            event: 鼠标进入事件
        """
        self._is_hovered = True
        self.update_icon()

        # 显示工具提示（固定在右侧）
        if self._text_key:
            # 获取翻译后的文本
            translated_text = XI18N.x_tr(self._text_key)

            # 1. 获取组件左上角相对于屏幕的绝对位置
            global_pos = self.mapToGlobal(QPoint(0, 0))

            # 2. 计算气泡显示的固定坐标
            # x: 组件宽度 + 6px 的间距 (显示在右侧)
            # y: 组件高度的 1/8 (稍微偏上)
            fixed_x = global_pos.x() + self.width() + 6
            fixed_y = global_pos.y() + (self.height() / 8)

            # 3. 在固定位置弹出
            QToolTip.showText(QPoint(fixed_x, fixed_y), translated_text, self)

        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开事件：取消悬停效果并隐藏工具提示

        Args:
            event: 鼠标离开事件
        """
        self._is_hovered = False
        self.update_icon()

        # 鼠标离开时立即隐藏气泡，防止残留
        QToolTip.hideText()

        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """鼠标点击事件：发送点击信号

        Args:
            event: 鼠标点击事件
        """
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        """绘制左侧选中指示条

        选中时在左侧绘制一个圆角矩形指示条。

        Args:
            event: 绘制事件
        """
        super().paintEvent(event)  # 绘制 QSS 背景

        # 仅在选中时绘制指示条
        if self._is_selected:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)  # 高分辨率清晰

            # 设置指示条颜色（主色）
            color = QColor(theme_manager.colors.primary)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)

            # 绘制指示条：位于左侧，高度为 18px，宽度 3px，圆角
            indicator_w = 3
            indicator_h = 18
            x = 2  # 距离左边边缘 2px
            y = (self.height() - indicator_h) / 2

            painter.drawRoundedRect(QRectF(x, y, indicator_w, indicator_h), 1.5, 1.5)


class XNavSimple(QWidget):
    """简单导航栏组件

    支持顶部和底部两个区域的导航项布局，自动管理选中状态。

    Features:
        - 顶部/底部布局
        - 选中状态管理
        - 主题切换支持
        - 图标缓存优化
        - 链式调用 API

    Signals:
        changed: 导航项切换信号（参数：item_id）
    """
    changed = Signal(str)

    def __init__(self, icon_size=18, parent=None):
        """初始化简单导航栏组件。

            Args:
                icon_size: 导航项图标的显示尺寸（像素）。
                parent: 父级组件。
            """
        super().__init__(parent)
        self.icon_size = icon_size
        self._items = {}
        self._current_item_id = None

        # 初始化界面
        self._init_ui()

        # 监听主题切换
        theme_manager.theme_changed.connect(self._on_theme_changed)

    def showEvent(self, event):
        """窗口显示时绑定屏幕切换信号"""
        super().showEvent(event)
        window = self.window().windowHandle()
        if window:
            # 确保只连接一次
            try:
                window.screenChanged.disconnect(self._on_screen_changed)
            except:
                pass
            window.screenChanged.connect(self._on_screen_changed)

    def _on_screen_changed(self):
        """当窗口从一个屏幕拖到另一个屏幕时触发"""
        QTimer.singleShot(100, self.refresh_ui)

    def refresh_ui(self):
        """强制刷新所有导航项"""
        for item in self._items.values():
            if hasattr(item, 'update_icon'):
                item.update_icon()
                item.update()  # 强制触发重绘
        self.update()

    def _init_ui(self):
        """初始化界面布局"""
        self.setObjectName("xnavsimple")
        self.setFixedWidth(46)  # 纯图标模式下固定宽度

        # 根布局
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # 容器组件
        self.container = QFrame()
        self.container.setObjectName("container")
        root_layout.addWidget(self.container)

        # 主布局
        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setContentsMargins(4, 4, 4, 4)  # 左右边距仅留 4px
        self.main_layout.setSpacing(6)

        # 顶部布局（主要导航）
        self.top_layout = QVBoxLayout()
        self.top_layout.setSpacing(6)
        self.main_layout.addLayout(self.top_layout)

        # 弹簧（将底部布局推到底部）
        self.main_layout.addStretch(1)

        # 底部布局（辅助功能）
        self.bottom_layout = QVBoxLayout()
        self.bottom_layout.setSpacing(6)
        self.main_layout.addLayout(self.bottom_layout)

    def add_item(self, item_id, icon_name=None, text=None, position="top"):
        """添加导航项

        Args:
            item_id: 导航项唯一标识
            icon_name: 图标名称（支持字符串或 IconName 枚举）
            text: 提示文本（作为 ToolTip 显示）
            position: 添加位置（"top" 或 "bottom"）

        Returns:
            self: 支持链式调用
        """
        # 创建导航项
        item = NavItem(icon_name, text, self.icon_size, self)
        item.clicked.connect(lambda: self._on_item_clicked(item_id))
        self._items[item_id] = item

        # 添加到对应布局
        target = self.top_layout if position == "top" else self.bottom_layout
        target.addWidget(item)

        return self

    def set_current_item(self, item_id):
        """设置当前选中的导航项

        Args:
            item_id: 导航项 ID
        """
        # 如果设置的项不存在，不做处理
        if item_id not in self._items:
            return

        # 如果设置的项已经是当前项，不做处理
        if self._current_item_id == item_id:
            return

        # 取消之前的选中状态
        if self._current_item_id in self._items:
            self._items[self._current_item_id].setSelected(False)

        # 设置新的选中状态
        self._current_item_id = item_id
        self._items[item_id].setSelected(True)

    def current_item(self):
        """获取当前选中的导航项 ID

        Returns:
            str: 当前选中的导航项 ID，如果没有选中则返回 None
        """
        return self._current_item_id

    def _on_item_clicked(self, item_id):
        """导航项点击处理

        Args:
            item_id: 被点击的导航项 ID
        """
        # 如果点击的是当前项，不做处理
        if self._current_item_id == item_id:
            return

        # 取消之前的选中状态
        if self._current_item_id in self._items:
            self._items[self._current_item_id].setSelected(False)

        # 设置新的选中状态
        self._current_item_id = item_id
        self._items[item_id].setSelected(True)

        # 发送切换信号
        self.changed.emit(item_id)

    def _on_theme_changed(self, theme_name):
        """主题切换处理"""
        for item in self._items.values():
            item.update_icon()
            item.update()

    def get_item(self, item_id: str) -> Optional[NavItem]:
        """根据 ID 获取对应的导航项 Widget 实例

        Args:
            item_id: 导航项唯一标识

        Returns:
            NavItem: 导航项实例，如果不存在则返回 None
        """
        return self._items.get(item_id)
