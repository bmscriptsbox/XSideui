from typing import Tuple

from ..utils.qt_compat import (Qt, Signal, QIntValidator, QWidget, QHBoxLayout, QPushButton)
from ..xenum import XSize, XButtonVariant, XColor
from .label import XLabel
from .lineedit import XLineEdit
from .pushbutton import XPushButton
from ..icon import IconName


class XPagination(QWidget):
    """
    分页器组件 (Pagination Component)

    提供分页器的基础功能实现，包括页码导航、上一页/下一页、页码跳转和主题适配。

    Signals 信号:
        pageChanged(int): 当前页改变时发出
        pageSizeChanged(int): 每页数量改变时发出
        prevClicked(int): 点击上一页按钮时发出
        nextClicked(int): 点击下一页按钮时发出
        pageClicked(int): 点击页码按钮时发出
        jumped(int): 输入框跳转时发出

    Properties 属性:
        page_size (int): 每页显示数量
        current_page (int): 当前页码
        total (int): 总条目数
        can_go_prev (bool): 是否可以上一页
        can_go_next (bool): 是否可以下一页
    """
    pageChanged = Signal(int)
    pageSizeChanged = Signal(int)
    prevClicked = Signal(int)
    nextClicked = Signal(int)
    pageClicked = Signal(int)
    jumped = Signal(int)

    def __init__(
            self,
            total: int = 0,
            page_size: int = 10,
            current_page: int = 1,
            parent=None
    ):
        """初始化分页组件

        Args:
            total: 总条目数
            page_size: 每页显示数量
            current_page: 初始页码
            parent: 父组件
        """
        super().__init__(parent)

        self._total = total
        self._page_size = page_size
        self._current_page = current_page
        self.page_buttons = []

        self._setup_ui()
        self._init_connections()

    def _init_connections(self):
        """初始化信号连接"""
        self.prev_btn.clicked.connect(self._on_prev_page)
        self.next_btn.clicked.connect(self._on_next_page)
        self.jump_edit.returnPressed.connect(self._on_jump_page)

    @property
    def page_size(self) -> int:
        """获取每页显示数量"""
        return self._page_size

    @property
    def current_page(self) -> int:
        """获取当前页码"""
        return self._current_page

    @property
    def total(self) -> int:
        """获取总条目数"""
        return self._total

    @property
    def can_go_prev(self) -> bool:
        """是否可以上一页"""
        return self._current_page > 1

    @property
    def can_go_next(self) -> bool:
        """是否可以下一页"""
        return self._current_page < self.get_total_pages()

    def _setup_ui(self):
        """初始化用户界面"""
        self.setObjectName("xpagination")
        self.setAttribute(Qt.WA_StyledBackground, True)

        layout = QHBoxLayout()
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # 总数显示
        self.total_label = XLabel(f"共计 {self._total}")

        # 上一页/下一页按钮
        self.prev_btn = XPushButton(icon=IconName.LEFT_ARROW, variant=XButtonVariant.TEXT, size=XSize.SMALL,
                                    color=XColor.TERTIARY)
        self.next_btn = XPushButton(icon=IconName.RIGHT_ARROW, variant=XButtonVariant.TEXT, size=XSize.SMALL,
                                    color=XColor.TERTIARY)

        # 跳转输入框
        self.jump_edit = XLineEdit(placeholder='Page', size=XSize.SMALL)
        self.jump_edit.setMaximumWidth(80)
        self.jump_edit.setValidator(QIntValidator(1, self.get_total_pages()))

        # 添加到布局
        layout.addStretch()
        layout.addWidget(self.total_label)
        layout.addWidget(self.prev_btn)
        self._update_page_buttons()
        layout.addWidget(self.next_btn)

        self.jump_label = XLabel('Jump')
        layout.addWidget(self.jump_label)
        layout.addWidget(self.jump_edit)

    def get_total_pages(self) -> int:
        """获取总页数"""
        return max(1, (self._total + self._page_size - 1) // self._page_size)

    def get_page_range(self) -> Tuple[int, int]:
        """
        获取当前页的数据范围
        
        Returns:
            Tuple[int, int]: 起始索引和结束索引（0-based）
        """
        start = (self._current_page - 1) * self._page_size
        end = min(start + self._page_size, self._total)
        return (start, end)

    def set_current_page(self, page: int) -> None:
        """
        设置当前页码
        
        Args:
            page: 要设置的页码（会自动限制在有效范围内）
        """
        page = max(1, min(page, self.get_total_pages()))
        if page != self._current_page:
            self._current_page = page
            self._update_page_buttons()
            self.pageChanged.emit(page)

    def set_page_size(self, page_size: int) -> None:
        """
        设置每页数量
        
        Args:
            page_size: 每页显示数量
        """
        if page_size != self._page_size:
            self._page_size = page_size
            self.jump_edit.setValidator(QIntValidator(1, self.get_total_pages()))
            self._update_page_buttons()
            self.pageSizeChanged.emit(page_size)

    def set_total(self, total: int) -> None:
        """
        设置总条目数
        
        Args:
            total: 总条目数
        """
        self._total = max(0, total)
        self.total_label.setText(f"共计 {self._total}")
        self.jump_edit.setValidator(QIntValidator(1, self.get_total_pages()))
        self._update_page_buttons()

    def go_to_page(self, page: int) -> None:
        """
        跳转到指定页码
        
        Args:
            page: 目标页码
        """
        self.set_current_page(page)

    def go_to_first_page(self) -> None:
        """跳转到第一页"""
        self.set_current_page(1)

    def go_to_last_page(self) -> None:
        """跳转到最后一页"""
        self.set_current_page(self.get_total_pages())

    def _update_page_buttons(self) -> None:
        """更新页码按钮"""
        for btn in self.page_buttons:
            self.layout().removeWidget(btn)
            btn.deleteLater()
        self.page_buttons.clear()

        total_pages = self.get_total_pages()

        if total_pages <= 7:
            for i in range(1, total_pages + 1):
                self._add_page_button(i)
        else:
            if self._current_page <= 4:
                for i in range(1, 6):
                    self._add_page_button(i)
                self._add_ellipsis()
                self._add_page_button(total_pages)
            elif self._current_page >= total_pages - 3:
                self._add_page_button(1)
                self._add_ellipsis()
                for i in range(total_pages - 4, total_pages + 1):
                    self._add_page_button(i)
            else:
                self._add_page_button(1)
                self._add_ellipsis()
                for i in range(self._current_page - 1, self._current_page + 2):
                    self._add_page_button(i)
                self._add_ellipsis()
                self._add_page_button(total_pages)

    def _add_page_button(self, page: int) -> None:
        """
        添加页码按钮
        
        Args:
            page: 页码
        """
        btn = QPushButton(str(page))
        btn.setObjectName("xpagination-page-btn")
        btn.setCheckable(True)
        btn.setChecked(page == self._current_page)
        btn.clicked.connect(lambda: self._on_page_clicked(page))
        self.page_buttons.append(btn)
        self.layout().insertWidget(self.layout().indexOf(self.next_btn), btn)

    def _add_ellipsis(self) -> None:
        """添加省略号"""
        label = XLabel("...")
        self.page_buttons.append(label)
        self.layout().insertWidget(self.layout().indexOf(self.next_btn), label)

    def _on_page_clicked(self, page: int) -> None:
        """
        页码按钮点击处理
        
        Args:
            page: 点击的页码
        """
        self.set_current_page(page)
        self.pageClicked.emit(page)

    def _on_prev_page(self) -> None:
        """上一页按钮点击处理"""
        if self._current_page > 1:
            self.set_current_page(self._current_page - 1)
            self.prevClicked.emit(self._current_page)

    def _on_next_page(self) -> None:
        """下一页按钮点击处理"""
        if self._current_page < self.get_total_pages():
            self.set_current_page(self._current_page + 1)
            self.nextClicked.emit(self._current_page)

    def _on_jump_page(self) -> None:
        """跳转输入框回车处理"""
        try:
            page = int(self.jump_edit.text())
            if 1 <= page <= self.get_total_pages():
                self.set_current_page(page)
                self.jump_edit.setText(str(page))
                self.jumped.emit(page)
        except ValueError:
            pass
