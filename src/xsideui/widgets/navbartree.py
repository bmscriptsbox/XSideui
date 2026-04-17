"""
Navigation Tree Component 导航树组件
基于 QTreeWidget 的树形导航菜单，支持多级菜单、图标显示和主题适配。
"""

from ..utils.qt_compat import QRect, QStyledItemDelegate, QStyle, QTreeWidget, QTreeWidgetItem, QFrame, QPainter, \
    QColor, QBrush, Qt, Signal, QSize, QRectF, QEvent

from ..theme import theme_manager
from ..icon import XIcon, IconName
from ..i18n import XI18N


class XNavTreeDelegate(QStyledItemDelegate):
    """导航树自定义绘制代理"""

    def __init__(self, tree_widget):
        super().__init__(tree_widget)
        self.tree = tree_widget

    def paint(self, painter: QPainter, option, index):
        """自定义绘制导航项"""
        painter.setRenderHint(QPainter.Antialiasing)

        # 计算层级深度
        level = 0
        p = index.parent()
        while p.isValid():
            level += 1
            p = p.parent()

        # 获取状态
        is_selected = option.state & QStyle.State_Selected
        is_hovered = option.state & QStyle.State_MouseOver
        is_expanded = option.state & QStyle.State_Open
        has_children = self.tree.model().hasChildren(index)

        icon_name = index.data(Qt.UserRole + 1)
        text_key = index.data(Qt.DisplayRole)
        text = XI18N.x_tr(text_key)

        # 背景区域
        bg_rect = option.rect.adjusted(4, 2, -4, -2)
        indent_val = level * 10

        # 绘制背景
        painter.save()
        if is_selected:
            bg_color = QColor(theme_manager.colors.primary)
            bg_color.setAlphaF(0.15)
            painter.setBrush(QBrush(bg_color))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(bg_rect, 6, 6)
        elif is_hovered:
            bg_color = QColor(theme_manager.colors.fill)
            bg_color.setAlphaF(0.3)
            painter.setBrush(QBrush(bg_color))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(bg_rect, 6, 6)
        painter.restore()

        # 绘制选中指示条
        if is_selected and not has_children:
            painter.save()
            painter.setBrush(QBrush(QColor(theme_manager.colors.primary)))
            painter.setPen(Qt.NoPen)
            bar_rect = QRectF(bg_rect.x(), bg_rect.y() + 8, 3, bg_rect.height() - 16)
            painter.drawRoundedRect(bar_rect, 1.5, 1.5)
            painter.restore()

        # 绘制文字
        painter.save()
        text_color = theme_manager.colors.primary if is_selected else theme_manager.colors.text_1
        painter.setPen(QColor(text_color))

        font = theme_manager.get_font(self.tree.text_size, "weight_medium")
        painter.setFont(font)

        icon_offset = (self.tree.icon_size + 8) if icon_name else 0
        text_x = bg_rect.x() + 6 + indent_val + icon_offset
        text_rect = bg_rect.adjusted(text_x - bg_rect.x(), 0, -30, 0)
        painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, text)
        painter.restore()

        # 绘制图标
        if icon_name:
            color = theme_manager.colors.primary if is_selected else theme_manager.colors.text_1
            icon = XIcon(name=icon_name, color=color, size=self.tree.icon_size).icon()
            if icon:
                icon_x = bg_rect.x() + 12 + indent_val
                icon_y = bg_rect.y() + (bg_rect.height() - self.tree.icon_size) / 2
                icon_rect = QRect(
                    int(icon_x),
                    int(icon_y),
                    self.tree.icon_size,
                    self.tree.icon_size
                )
                icon.paint(painter, icon_rect, Qt.AlignCenter)

        # 绘制展开/折叠箭头
        if has_children:
            arrow_icon_name = IconName.DOWN if is_expanded else IconName.RIGHT
            arrow_color = theme_manager.colors.primary if (is_hovered or is_selected) else theme_manager.colors.text_1
            arrow_size = 12
            q_arrow_icon = XIcon(name=arrow_icon_name, color=arrow_color, size=arrow_size).icon()

            if q_arrow_icon:
                ax = bg_rect.right() - arrow_size - 8
                ay = bg_rect.center().y() - (arrow_size / 2)
                arrow_rect = QRect(int(ax), int(ay), arrow_size, arrow_size)
                q_arrow_icon.paint(painter, arrow_rect, Qt.AlignCenter)

    def sizeHint(self, option, index):
        """返回推荐尺寸"""
        return QSize(200, 42)


class XNavTree(QTreeWidget):
    """导航树组件"""
    changed = Signal(str)

    def __init__(self, indent: int = 16, icon_size: int = 16, text_size: int = 13, parent=None):
        super().__init__(parent)
        self.indent = indent
        self.icon_size = icon_size
        self.text_size = text_size
        self._items = {}
        self._current_id = None
        self._item_keys = {}  # 存储每个 item 的翻译键

        self._init_ui()
        theme_manager.theme_changed.connect(self._on_theme_updated)

    def _init_ui(self):
        """初始化界面"""
        self.setObjectName("xnavtree")
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setIndentation(self.indent)
        self.setMouseTracking(True)

        # 禁用系统自带渲染，使用 Delegate
        self.setRootIsDecorated(False)
        self.setUniformRowHeights(True)

        # 挂载 Delegate
        self.delegate = XNavTreeDelegate(self)
        self.setItemDelegate(self.delegate)

        self.itemClicked.connect(self._on_item_clicked)

    def _on_theme_updated(self, theme_name):
        """主题切换处理"""
        self.viewport().update()

    def _on_item_clicked(self, item, column):
        """导航项点击处理"""
        item_id = item.data(0, Qt.UserRole)
        if item.childCount() > 0:
            item.setExpanded(not item.isExpanded())
        elif item_id:
            self._current_id = item_id
            self.changed.emit(item_id)
            self.viewport().update()

    def add_item_batch(self, items: list) -> 'XNavTree':
        """批量添加导航项"""
        self.clear()
        self._items.clear()
        for cfg in items:
            self._add_node(cfg, self)
        return self

    def _add_node(self, cfg, parent):
        """添加单个节点"""
        item = QTreeWidgetItem(parent)
        text = cfg.get('text', '')
        item.setText(0, text)
        item.setData(0, Qt.UserRole, cfg.get('id', ''))
        item.setData(0, Qt.UserRole + 1, cfg.get('icon', ''))

        # 存储翻译键
        item_id = cfg.get('id', '')
        self._items[item_id] = item
        self._item_keys[item_id] = text

        for child_cfg in cfg.get('children', []):
            self._add_node(child_cfg, item)

        if cfg.get('children'):
            item.setExpanded(True)

    def set_current_id(self, item_id: str):
        """设置当前选中的导航项"""
        if item_id in self._items:
            item = self._items[item_id]
            self.setCurrentItem(item)
            self._current_id = item_id
            # 自动展开父级
            p = item.parent()
            while p:
                p.setExpanded(True)
                p = p.parent()
            self.viewport().update()

    def refresh_i18n(self):
        """刷新所有导航项的翻译"""
        # 强制重绘所有项
        self.viewport().update()

    def changeEvent(self, event):
        """响应语言切换事件"""
        super().changeEvent(event)
        if event.type() == QEvent.LanguageChange:
            self.refresh_i18n()
