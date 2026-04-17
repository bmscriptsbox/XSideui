from enum import Enum
from ..utils.qt_compat import QLayout, QVBoxLayout, QHBoxLayout, QWidget, Qt, Signal
from .divider import XDivider
from .label import XLabel




class GroupProxy:
    """分组代理类，支持链式调用添加组件到分组"""

    def __init__(self, card: 'XGroupCard', index: int):
        self._card = card
        self._index = index

    @property
    def index(self) -> int:
        """获取分组索引"""
        return self._index

    def add(self, widget, stretch: int = 0, alignment=Qt.Alignment()) -> 'GroupProxy':
        """
        向分组添加组件（链式调用）

        Args:
            widget: 要添加的组件
            stretch: 伸缩因子
            alignment: 对齐方式

        Returns:
            GroupProxy: 返回自身以支持链式调用
        """
        self._card.group_layouts[self._index].addWidget(widget, stretch, alignment)
        return self

    def addLayout(self, layout, stretch: int = 0) -> 'GroupProxy':
        """
        向分组添加布局（链式调用）

        Args:
            layout: 要添加的布局
            stretch: 伸缩因子

        Returns:
            GroupProxy: 返回自身以支持链式调用
        """
        self._card.group_layouts[self._index].addLayout(layout, stretch)
        return self


class LayoutCleanerMixin:
    """布局清理 Mixin，提供递归清理布局中所有子组件的能力"""

    def clear_layout(self, layout: QLayout):
        """
        递归清理布局中的所有子组件

        Args:
            layout: 要清理的布局
        """
        if not layout:
            return
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
            del item


class XCardBase(QWidget, LayoutCleanerMixin):
    """
    卡片基础组件

    提供布局和组件的工厂方法，是 XCard、XHeaderCard、XGroupCard 的基类。

    Signals:
        clicked: 点击信号（子类需启用 clickable）
    """

    clicked = Signal()



    def __init__(self, parent=None):
        """
        Args:
            parent: 父组件
        """
        super().__init__(parent)
        self.setObjectName("xcard-base")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.layout = self.create_layout(self, is_vbox=True)
        self.container = self.create_widget("xcard-container")
        self.layout.addWidget(self.container)

    def create_layout(self, parent_or_layout, is_vbox=True, margins=(0, 0, 0, 0), spacing=2):
        """
        智能创建布局

        如果 parent_or_layout 是 QWidget，则作为其主布局；
        如果是 QLayout，则作为子布局添加。

        Args:
            parent_or_layout: 父组件或父布局
            is_vbox: True 为垂直布局，False 为水平布局
            margins: 内边距 (left, top, right, bottom)
            spacing: 组件间距

        Returns:
            QLayout: 创建的布局
        """
        if isinstance(parent_or_layout, QWidget):
            layout = QVBoxLayout(parent_or_layout) if is_vbox else QHBoxLayout(parent_or_layout)
        else:
            layout = QVBoxLayout() if is_vbox else QHBoxLayout()
            parent_or_layout.addLayout(layout)

        layout.setContentsMargins(*margins)
        layout.setSpacing(spacing)
        return layout

    def create_widget(self, name=None, style_attr=True):
        """
        创建组件

        Args:
            name: ObjectName
            style_attr: 是否启用 WA_StyledBackground 属性

        Returns:
            QWidget: 创建的组件
        """
        w = QWidget()
        if name:
            w.setObjectName(name)
        if style_attr:
            w.setAttribute(Qt.WA_StyledBackground, True)
        return w


class XCard(XCardBase):
    """
    基础卡片组件

    简单的容器卡片，支持添加组件和布局，可选择是否可点击。

    Example:
        >>> card = XCard(clickable=True)
        >>> card.addWidget(XLabel("内容"))
        >>> card.clicked.connect(lambda: print("点击"))
    """

    def __init__(self, padding=(11, 11, 11, 11), spacing=8, clickable=False, parent=None):
        """
        Args:
            padding: 内边距 (left, top, right, bottom)
            spacing: 组件间距
            clickable: 是否可点击
            parent: 父组件
        """
        super().__init__(parent)
        self._clickable = clickable
        self._layout = self.create_layout(self.container, is_vbox=False, margins=padding, spacing=spacing)
        self.setCursor(Qt.PointingHandCursor if clickable else Qt.ArrowCursor)
        self.setObjectName("xcard")
        if clickable:
            self.container.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def addWidget(self, widget, stretch=0, alignment=Qt.Alignment()):
        """
        添加组件

        Args:
            widget: 要添加的组件
            stretch: 伸缩因子
            alignment: 对齐方式
        """
        self._layout.addWidget(widget, stretch, alignment)

    def addLayout(self, layout: QLayout, stretch: int = 0):
        """
        添加布局

        Args:
            layout: 要添加的布局
            stretch: 伸缩因子
        """
        self._layout.addLayout(layout, stretch)

    def clear(self):
        """清空卡片内容"""
        self.clear_layout(self._layout)

    def set_clickable(self, clickable: bool) -> 'XCard':
        """
        设置是否可点击

        Args:
            clickable: 是否可点击

        Returns:
            XCard: 返回自身以支持链式调用
        """
        self._clickable = clickable
        self.setCursor(Qt.PointingHandCursor if clickable else Qt.ArrowCursor)
        return self

    def mousePressEvent(self, event):
        """处理鼠标点击事件"""
        if self._clickable and event.button() == Qt.LeftButton:
            self.clicked.emit()


class XHeaderCard(XCardBase):
    """
    标题卡片组件

    带标题栏的卡片，分为 HEADER 和 CONTENT 两个区域，
    支持链式调用添加组件。

    Example:
        >>> card = XHeaderCard(title="标题")
        >>> card.addWidget(btn, target=CardPosition.HEADER) \\
        ...     .addWidget(XLabel("内容"), target=CardPosition.CONTENT)
    """


    class CardPosition(Enum):
        """卡片目标区域枚举"""
        HEADER = 'header'
        CONTENT = 'content'
        GROUP = 'group'
    def __init__(self, title="", header_padding=(11, 11, 11, 11), content_padding=(11, 11, 11, 11), spacing=8,
                 parent=None):
        """
        Args:
            title: 标题文本
            header_padding: 标题栏内边距
            content_padding: 内容区内边距
            spacing: 内容区组件间距
            parent: 父组件
        """
        super().__init__(parent)
        container_layout = self.create_layout(self.container, is_vbox=True)

        self.header = self.create_widget("xcard-header")
        self.header_layout = self.create_layout(self.header, is_vbox=False, margins=header_padding)
        self.title_label = XLabel(title, style=XLabel.Style.H4)
        self.header_layout.addWidget(self.title_label, 1)
        container_layout.addWidget(self.header)

        container_layout.addWidget(XDivider())
        self._layout = self.create_layout(container_layout, is_vbox=False, margins=content_padding, spacing=spacing)

    def addWidget(self, widget, target=CardPosition.CONTENT, stretch=0, alignment=Qt.Alignment()) -> 'XHeaderCard':
        """
        添加组件（支持链式调用）

        Args:
            widget: 要添加的组件
            target: 目标区域 (CardPosition.HEADER 或 CardPosition.CONTENT)
            stretch: 伸缩因子
            alignment: 对齐方式

        Returns:
            XHeaderCard: 返回自身以支持链式调用
        """
        layout = self.header_layout if target == XHeaderCard.CardPosition.HEADER else self._layout
        layout.addWidget(widget, stretch, alignment)
        return self

    def addLayout(self, layout, target=CardPosition.CONTENT, stretch=0) -> 'XHeaderCard':
        """
        添加布局（支持链式调用）

        Args:
            layout: 要添加的布局
            target: 目标区域 (CardPosition.HEADER 或 CardPosition.CONTENT)
            stretch: 伸缩因子

        Returns:
            XHeaderCard: 返回自身以支持链式调用
        """
        _layout = self.header_layout if target == XHeaderCard.CardPosition.HEADER else self._layout
        _layout.addLayout(layout, stretch)
        return self

    def clear(self):
        """清空内容区域（保留标题栏）"""
        self.clear_layout(self._layout)

    def set_title(self, title: str):
        """
        设置标题

        Args:
            title: 标题文本
        """
        self.title_label.setText(title)

    def add_stretch(self):
        """底部添加弹性空间"""
        self.container.layout().addStretch()


class XGroupCard(XCardBase):
    """
    分组卡片组件

    支持多个分组的卡片，每个分组间自动添加分隔线。
    通过 GroupProxy 支持链式调用。

    Example:
        >>> card = XGroupCard(title="设置")
        >>> card.add_group() \\
        ...     .add(XLabel("分组1内容"))
        >>> card.add_group() \\
        ...     .add(XLabel("分组2内容"))
    """
    class CardPosition(Enum):
        """卡片目标区域枚举"""
        HEADER = 'header'
        CONTENT = 'content'
        GROUP = 'group'

    def __init__(self, title="", header_padding=(11, 11, 11, 11), group_padding=(11, 11, 11, 11), spacing=8,
                 parent=None):
        """
        Args:
            title: 标题文本
            header_padding: 标题栏内边距
            group_padding: 分组内边距
            spacing: 分组内组件间距
            parent: 父组件
        """
        super().__init__(parent)
        self._group_padding = group_padding
        self._spacing = spacing
        self.group_layouts = []

        main_layout = self.create_layout(self.container, is_vbox=True)
        self.header = self.create_widget("xcard-header")
        self.header_layout = self.create_layout(self.header, is_vbox=False, margins=header_padding)
        self.title_label = XLabel(title, style=XLabel.Style.H4)
        self.header_layout.addWidget(self.title_label, 1)
        self.header_layout.addStretch()
        main_layout.addWidget(self.header)
        self._header_divider = XDivider()
        main_layout.addWidget(self._header_divider)

    def add_group(self) -> GroupProxy:
        """
        添加新分组

        Returns:
            GroupProxy: 分组代理对象，支持链式调用
        """
        if self.group_layouts:
            self.container.layout().addWidget(XDivider())

        group_widget = self.create_widget(style_attr=True)
        group_layout = self.create_layout(group_widget, is_vbox=True, margins=self._group_padding,
                                          spacing=self._spacing)
        content_layout = self.create_layout(group_layout, is_vbox=False)

        self.container.layout().addWidget(group_widget)
        self.group_layouts.append(content_layout)
        return GroupProxy(self, len(self.group_layouts) - 1)

    def addWidget(self, widget, target=CardPosition.GROUP, group_index=0, stretch=0, alignment=Qt.Alignment()):
        """
        添加组件

        Args:
            widget: 要添加的组件
            target: 目标区域 (CardPosition.HEADER 或 CardPosition.GROUP)
            group_index: 分组索引（仅 target=GROUP 时有效）
            stretch: 伸缩因子
            alignment: 对齐方式
        """
        if target == XGroupCard.CardPosition.HEADER:
            self.header_layout.addWidget(widget, stretch, alignment)
        else:
            self.group_layouts[group_index].addWidget(widget, stretch, alignment)

    def addLayout(self, layout, target: CardPosition.GROUP, group_index: int = 0, stretch: int = 0):
        """
        添加布局

        Args:
            layout: 要添加的布局
            target: 目标区域 (CardPosition.HEADER 或 CardPosition.GROUP)
            group_index: 分组索引（仅 target=GROUP 时有效）
            stretch: 伸缩因子

        Raises:
            ValueError: 分组索引无效时抛出
        """
        if target == XGroupCard.CardPosition.HEADER:
            self.header_layout.addLayout(layout, stretch)
        elif target == XGroupCard.CardPosition.GROUP:
            if not (0 <= group_index < len(self.group_layouts)):
                raise ValueError(f"Invalid group index: {group_index}")
            self.group_layouts[group_index].addLayout(layout, stretch)

    def clear(self):
        """清空所有分组（保留标题栏和头部分割线）"""
        container = self.container.layout()
        i = container.count() - 1
        while i >= 0:
            item = container.itemAt(i)
            widget = item.widget()
            if widget and widget not in (self.header, self._header_divider):
                widget.deleteLater()
            i -= 1
        self.group_layouts.clear()

    def set_title(self, title: str):
        """
        设置标题

        Args:
            title: 标题文本
        """
        self.title_label.setText(title)

    def addStretch(self):
        """底部添加弹性空间"""
        self.container.layout().addStretch()
