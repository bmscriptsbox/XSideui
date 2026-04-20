from ..utils.qt_compat import QLayout, QStyle, QPoint, QRect, QSize, Qt, QSizePolicy


class XFlowLayout(QLayout):
    """流式布局组件"""

    def __init__(self, parent=None, margin: int = 0, spacing: int = -1):
        """初始化流式布局。

            Args:
                parent: 父级组件或父布局。
                margin: 布局的外边距（四周留白像素）。
                spacing: 组件之间的间距（像素）。若为 -1，则尝试从父组件获取系统默认间距。
            """
        super().__init__(parent)
        self._items = []
        self._spacing = spacing
        self._cached_width = -1
        self._cached_height = -1
        self._cache_dirty = True
        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

    def addItem(self, item):
        """添加布局项目"""
        self._items.append(item)
        self._cache_dirty = True
        self.invalidate()

    def count(self):
        """获取项目数量"""
        return len(self._items)

    def itemAt(self, index):
        """获取指定位置的项目"""
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def takeAt(self, index):
        """移除并返回指定位置的项目"""
        if 0 <= index < len(self._items):
            item = self._items.pop(index)
            self._cache_dirty = True
            return item
        return None

    def expandingDirections(self):
        """获取可扩展方向"""
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        """是否支持基于宽度计算高度"""
        return True

    def heightForWidth(self, width):
        """根据宽度计算高度"""
        if self._cache_dirty or self._cached_width != width:
            self._cached_height = self._do_layout(QRect(0, 0, width, 0), True)
            self._cached_width = width
            self._cache_dirty = False
        return self._cached_height

    def setGeometry(self, rect):
        """设置布局几何区域"""
        super().setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):
        """获取建议大小"""
        return self.minimumSize()

    def minimumSize(self):
        """获取最小大小"""
        if not self._items:
            margin = self.contentsMargins()
            return QSize(margin.left() + margin.right(), margin.top() + margin.bottom())

        width = 0
        height = 0
        for item in self._items:
            size = self._get_item_size(item)
            width = max(width, size.width())
            height = max(height, size.height())

        margin = self.contentsMargins()
        return QSize(width + margin.left() + margin.right(), height + margin.top() + margin.bottom())

    def spacing(self):
        """获取项目间距"""
        if self._spacing >= 0:
            return self._spacing
        return self.style().pixelMetric(QStyle.PM_DefaultLayoutSpacing)

    def setSpacing(self, spacing):
        """设置项目间距"""
        self._spacing = spacing
        self._cache_dirty = True
        self.update()

    def clear(self):
        """清空布局中的所有组件"""
        item = self.takeAt(0)
        while item:
            if item.widget():
                item.widget().deleteLater()
            item = self.takeAt(0)
        self._cache_dirty = True

    def invalidate(self):
        """使缓存失效"""
        self._cache_dirty = True
        super().invalidate()

    def _get_item_size(self, item):
        """获取项目的实际大小，考虑 sizePolicy"""
        size = item.sizeHint()
        widget = item.widget()

        if widget:
            policy = widget.sizePolicy()
            if policy.horizontalPolicy() == QSizePolicy.Policy.Expanding:
                size = size.expandedTo(item.minimumSize())

        return size

    def _do_layout(self, rect, test_only=False):
        """执行实际的布局计算"""
        if not self._items:
            return 0

        margin = self.contentsMargins()
        available_width = rect.width() - margin.left() - margin.right()
        spacing = self.spacing()

        x = rect.x() + margin.left()
        y = rect.y() + margin.top()
        row_height = 0
        row_width = 0

        for item in self._items:
            item_size = self._get_item_size(item)

            if row_width > 0:
                row_width += spacing

            if row_width + item_size.width() > available_width and row_width > 0:
                x = rect.x() + margin.left()
                y += row_height + spacing
                row_height = 0
                row_width = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item_size))

            row_height = max(row_height, item_size.height())
            x += item_size.width() + spacing
            row_width += item_size.width()

        return y + row_height - rect.y() + margin.bottom()
