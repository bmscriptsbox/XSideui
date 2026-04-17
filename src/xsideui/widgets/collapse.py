
from ..utils.qt_compat import QWidget, QVBoxLayout, QHBoxLayout, QFrame, Qt, Signal, QPropertyAnimation, QEasingCurve
from .pushbutton import XPushButton
from ..xenum import XButtonVariant, XSize, XColor
from .label import XLabel
from ..icon import XIcon, IconName


class XCollapse(QWidget):
    """优化版：修复残影与抖动的折叠面板"""

    state_changed = Signal(bool)

    def __init__(self, title: str = "", expanded: bool = False, parent=None):
        super().__init__(parent)
        self.collapsed = not expanded
        self._setup_ui(title)

        # 初始状态同步
        if self.collapsed:
            self.content.setMaximumHeight(0)
            self.content.hide()

        self._update_arrow()

    def _setup_ui(self, title):
        self.setObjectName("xcollapse-base")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.container = QFrame()
        self.container.setObjectName("xcollapse-container")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(0)
        self.main_layout.addWidget(self.container)

        self.header = QFrame()
        self.header.setObjectName("xcollapse-header")
        self.header.setCursor(Qt.PointingHandCursor)
        self.header.setFixedHeight(40)
        h_layout = QHBoxLayout(self.header)
        h_layout.setContentsMargins(12, 0, 0, 0)

        self.title_label = XLabel(title)
        self.title_label.setObjectName("xcollapse-title")
        self.arrow = XPushButton(icon=IconName.RIGHT, variant=XButtonVariant.LINK, size=XSize.MINI, color=XColor.TERTIARY)
        h_layout.addWidget(self.title_label)
        h_layout.addStretch()
        h_layout.addWidget(self.arrow)

        self.content = QFrame()
        self.content.setObjectName("xcollapse-content")
        self.content.setAttribute(Qt.WA_StyledBackground, True)
        self.content.setAttribute(Qt.WA_OpaquePaintEvent, False)

        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(11,11,11,11)
        self.content_layout.setSpacing(10)

        self.container_layout.addWidget(self.header)
        self.container_layout.addWidget(self.content)

        self.anim_height = QPropertyAnimation(self.content, b"maximumHeight")
        self.anim_height.setDuration(250)
        self.anim_height.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim_height.valueChanged.connect(self.content.update)

        self.header.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.header and event.type() == 2:  # MouseButtonPress
            if event.button() == Qt.LeftButton:
                self.toggle_panel()
                return True
        return super().eventFilter(obj, event)

    def _update_arrow(self):
        icon_name = XIcon.get(IconName.RIGHT, color=XColor.TERTIARY).icon() if self.collapsed else XIcon.get(IconName.DOWN, color=XColor.TERTIARY).icon()
        self.arrow.setIcon(icon_name)

    def toggle_panel(self):
        if self.anim_height.state() == QPropertyAnimation.Running:
            return

        self.content.layout().activate()
        target_h = self.content.layout().sizeHint().height()

        if self.collapsed:
            self.content.show()
            self.anim_height.setStartValue(0)
            self.anim_height.setEndValue(target_h)
            self.collapsed = False
        else:
            self.anim_height.setStartValue(self.content.height())
            self.anim_height.setEndValue(0)
            self.collapsed = True

        self._update_arrow()

        self.header.setProperty("active", str(not self.collapsed).lower())
        self.header.style().polish(self.header)

        self.anim_height.finished.connect(self._on_anim_finished)
        self.anim_height.start()
        self.state_changed.emit(not self.collapsed)

    def _on_anim_finished(self):
        try:
            self.anim_height.finished.disconnect(self._on_anim_finished)
        except:
            pass

        if self.collapsed:
            self.content.hide()
        else:
            self.content.setMaximumHeight(16777215)

    def add_content_widget(self, widget):
        """内容添加组件"""
        self.content_layout.addWidget(widget)

    def add_content_layout(self, layout):
        """内容添加布局"""
        self.content_layout.addLayout(layout)

    def expand(self):
        if self.collapsed:
            self.toggle_panel()

    def collapse(self):
        if not self.collapsed:
            self.toggle_panel()


class XCollapseGroup(QWidget):
    """折叠面板组"""

    def __init__(self, accordion=False, parent=None):
        super().__init__(parent)
        self.accordion = accordion
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(8)
        self.panels = []

    def add_panel(self, title):
        panel = XCollapse(title)
        self.panels.append(panel)
        self.main_layout.addWidget(panel)
        if self.accordion:
            panel.state_changed.connect(lambda exp: self._handle_accordion(panel, exp))
        return panel

    def _handle_accordion(self, sender, expanded):
        if expanded and self.accordion:
            for p in self.panels:
                if p != sender and not p.collapsed:
                    p.toggle_panel()
