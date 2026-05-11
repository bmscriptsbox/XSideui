"""XListView Component 基于 QListView 的列表视图组件

提供更灵活的 Model/View 架构支持的列表视图组件，支持自定义委托和高效渲染。
"""
from typing import Union, Optional

from ..utils.qt_compat import Qt, QListView, QAbstractItemView, set_selection_rect_visible
from ..xenum import XColor, XSize


class XListView(QListView):
    """ListView Component 基于 QListView 的列表视图组件

    一个基于 Qt Model/View 架构的列表视图组件，提供高性能的列表渲染，
    支持自定义委托、多种选择模式和拖拽操作。

    Features:
        - Model/View 架构支持（与 XListWidget 的区别）
        - 属性驱动样式 (QSS Property-driven)
        - 自动感知明暗主题切换
        - 支持链式调用 API
        - 多种选择模式支持

    Args:
        show_border: 是否显示组件外边框。默认 True。
        selection_mode: 选择模式，默认单选。
            - SingleSelection: 单选
            - MultiSelection: 多选
            - ExtendedSelection: 扩展多选（Ctrl/Shift）
            - NoSelection: 禁止选择
        drag_enabled: 是否启用拖拽。默认 False。
        parent: 父级组件。
    """

    def __init__(
            self,
            show_border: bool = True,
            selection_mode: QAbstractItemView.SelectionMode = QAbstractItemView.SingleSelection,
            drag_enabled: bool = False,
            show_alternating_colors: bool = False,
            parent=None
    ):
        """初始化列表视图组件

        Args:
            show_border: 是否显示边框。默认 True。
            selection_mode: 选择模式。可选值：
                - QAbstractItemView.SingleSelection（单选，默认）
                - QAbstractItemView.MultiSelection（多选）
                - QAbstractItemView.ExtendedSelection（扩展多选）
                - QAbstractItemView.ContiguousSelection（连续多选）
                - QAbstractItemView.NoSelection（禁止选择）
            drag_enabled: 是否启用拖拽。默认 False。
            show_alternating_colors: 是否显示交替行颜色。默认 False。
            parent: 父级组件。
        """
        super().__init__(parent)
        self._show_border = show_border
        self._selection_mode = selection_mode
        self._drag_enabled = drag_enabled
        self._show_alternating_colors = show_alternating_colors

        self.setObjectName("XListView")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._init_properties()
        self._apply_properties()

    def _init_properties(self):
        """初始化基本属性"""
        # 框架样式
        self.setFrameShape(QListView.NoFrame)

        # 滚动模式 - 像素级滚动，更平滑
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        # 滚动条策略
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 选择模式
        self.setSelectionMode(self._selection_mode)

        # 焦点策略
        self.setFocusPolicy(Qt.NoFocus)

        # 拖拽设置
        self.setDragEnabled(self._drag_enabled)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.NoDragDrop)

        # 交替行颜色
        self.setAlternatingRowColors(self._show_alternating_colors)

        # 网格线 - 不设置，使用默认无网格
        # 如需设置网格大小，调用 set_grid_size(w, h)

        # 拖拽选择矩形（兼容 PySide2/PySide6）
        set_selection_rect_visible(self, True)

    def _apply_properties(self):
        """应用属性到样式系统"""
        self.set_show_border(self._show_border)
        self.setProperty("alternatingColors", str(self._show_alternating_colors).lower())

    def _update_style(self):
        """刷新 QSS 样式"""
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    # ==================== 公共 API ====================

    def set_show_border(self, show: bool) -> 'XListView':
        """动态设置是否显示边框

        Args:
            show: 是否显示边框

        Returns:
            self，支持链式调用
        """
        self._show_border = show
        self.setProperty("hasBorder", str(show).lower())
        self._update_style()
        return self

    def show_border(self) -> bool:
        """获取当前边框显示状态

        Returns:
            True 表示显示边框，False 表示隐藏
        """
        return self._show_border

    def set_selection_mode(self, mode: QAbstractItemView.SelectionMode) -> 'XListView':
        """设置选择模式

        Args:
            mode: 选择模式，可选值：
                - QAbstractItemView.SingleSelection（单选）
                - QAbstractItemView.MultiSelection（多选）
                - QAbstractItemView.ExtendedSelection（扩展多选）
                - QAbstractItemView.ContiguousSelection（连续多选）
                - QAbstractItemView.NoSelection（禁止选择）

        Returns:
            self，支持链式调用
        """
        self._selection_mode = mode
        self.setSelectionMode(mode)
        return self

    def selection_mode(self) -> QAbstractItemView.SelectionMode:
        """获取当前选择模式

        Returns:
            当前的选择模式
        """
        return self._selection_mode

    def set_drag_enabled(self, enabled: bool) -> 'XListView':
        """设置是否启用拖拽

        Args:
            enabled: True 启用拖拽，False 禁用

        Returns:
            self，支持链式调用
        """
        self._drag_enabled = enabled
        self.setDragEnabled(enabled)

        # 根据拖拽启用状态自动调整拖放模式
        if enabled:
            self.setDragDropMode(QAbstractItemView.DragOnly)
        else:
            self.setDragDropMode(QAbstractItemView.NoDragDrop)
        return self

    def is_drag_enabled(self) -> bool:
        """获取当前拖拽启用状态

        Returns:
            True 表示启用拖拽
        """
        return self._drag_enabled

    def set_alternating_row_colors(self, enabled: bool) -> 'XListView':
        """设置是否显示交替行颜色

        Args:
            enabled: True 显示交替颜色，False 不显示

        Returns:
            self，支持链式调用
        """
        self._show_alternating_colors = enabled
        self.setAlternatingRowColors(enabled)
        self.setProperty("alternatingColors", str(enabled).lower())
        self._update_style()
        return self

    def is_alternating_row_colors(self) -> bool:
        """获取交替行颜色状态

        Returns:
            True 表示启用了交替行颜色
        """
        return self._show_alternating_colors

    def set_grid_size(self, width: int, height: Optional[int] = None) -> 'XListView':
        """设置网格尺寸（每个项的大小）

        Args:
            width: 网格宽度
            height: 网格高度，如果为 None，则使用与 width 相同的值

        Returns:
            self，支持链式调用
        """
        if height is None:
            height = width
        from ..utils.qt_compat import QSize
        self.setGridSize(QSize(width, height))
        return self

    def set_icon_size(self, width: int, height: Optional[int] = None) -> 'XListView':
        """设置图标大小

        Args:
            width: 图标宽度
            height: 图标高度，如果为 None，则使用与 width 相同的值

        Returns:
            self，支持链式调用
        """
        if height is None:
            height = width
        from ..utils.qt_compat import QSize
        self.setIconSize(QSize(width, height))
        return self

    def set_item_spacing(self, spacing: int) -> 'XListView':
        """设置项之间的间距

        Args:
            spacing: 间距值（像素）

        Returns:
            self，支持链式调用
        """
        self.setGridSize(self.gridSize())
        return self

    def set_view_mode(self, mode: str) -> 'XListView':
        """设置视图模式

        Args:
            mode: 'list' 列表模式 或 'icon' 图标模式

        Returns:
            self，支持链式调用
        """
        if mode.lower() == "icon":
            self.setViewMode(QListView.IconMode)
        else:
            self.setViewMode(QListView.ListMode)
        return self

    def set_resize_mode(self, mode: str) -> 'XListView':
        """设置调整大小模式

        Args:
            mode: 'fixed' 固定 或 'adjust' 可调整

        Returns:
            self，支持链式调用
        """
        if mode.lower() == "fixed":
            self.setResizeMode(QListView.Fixed)
        else:
            self.setResizeMode(QListView.Adjust)
        return self

    def set_word_wrap(self, wrap: bool) -> 'XListView':
        """设置是否自动换行

        Args:
            wrap: True 启用自动换行，False 禁用

        Returns:
            self，支持链式调用
        """
        self.setWordWrap(wrap)
        return self

    def clear_selection(self) -> 'XListView':
        """清空所有选择

        Returns:
            self，支持链式调用
        """
        self.clearSelection()
        return self

    def select_all(self) -> 'XListView':
        """选择所有项

        Returns:
            self，支持链式调用
        """
        self.selectAll()
        return self
