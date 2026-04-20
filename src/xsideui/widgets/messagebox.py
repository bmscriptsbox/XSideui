from ..utils.qt_compat import QVBoxLayout, QHBoxLayout, QWidget, Qt
from ..icon import IconName
from ..xenum import XButtonVariant, XColor, XSize
from .dialog import XDialog
from .pushbutton import XPushButton
from .label import XLabel
from ..icon import XIcon


class XMessageBox(XDialog):
    """
    消息提示框,支持原生调用方式及自定义组件嵌入
    """

    def __init__(self, title="提示", text="", icon: IconName = None, color: XColor = XColor.SECONDARY, parent=None):
        """初始化消息提示框。

            Args:
                title: 弹窗标题。
                text: 提示的正文内容。支持富文本格式。
                icon: 提示图标。传入 IconName 枚举，若为 None 则不显示图标。
                color: 主题颜色。主要影响图标颜色或顶部装饰条，默认为次要（Secondary）灰色。
                parent: 父窗口。
            """
        super().__init__(title=title, parent=parent)
        self._text = text
        self._on_confirm_callback = None

        # 1. 基础配置：消息框通常不需要最大化和最小化
        self.hide_maximize_button()
        self.hide_minimize_button()
        self.hide_theme_button()
        self.setMinimumWidth(300)
        if icon:
            print(icon)
            self.set_logo(XIcon.get(name=icon, color=color).icon())

        # 2. 初始化UI结构
        self._setup_message_ui()

    def _setup_message_ui(self):
        """初始化消息框内部布局结构"""
        # 主垂直布局
        self.container_layout = QVBoxLayout()
        self.container_layout.setContentsMargins(20, 20, 20, 20)
        self.container_layout.setSpacing(20)

        # --- A. 顶部内容区：文字/图标 ---
        self.content_hbox = QHBoxLayout()
        self.content_hbox.setSpacing(12)

        self.msg_label = XLabel(self._text)
        self.msg_label.setWordWrap(True)
        # 允许鼠标选择文字以便复制错误信息
        self.msg_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.content_hbox.addWidget(self.msg_label, 1)
        self.container_layout.addLayout(self.content_hbox)

        # --- B. 中间自定义区：预留给 add_custom_widget/layout ---
        self.custom_layout = QVBoxLayout()
        self.custom_layout.setSpacing(10)
        # 初始为空，不占空间
        self.container_layout.addLayout(self.custom_layout)

        # --- C. 底部按钮区 ---
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(10)
        self.button_layout.addStretch(1)

        # 默认创建确定按钮
        self.yes_btn = XPushButton("Ok", variant=XButtonVariant.SOLID, size=XSize.SMALL)
        self.yes_btn.setMinimumWidth(70)  # 保证按钮不会太窄
        self.yes_btn.clicked.connect(self._on_yes_clicked)

        self.button_layout.addWidget(self.yes_btn)
        self.container_layout.addStretch()
        self.container_layout.addLayout(self.button_layout)

        # 将最终布局交给 XDialog 渲染
        self.addLayout(self.container_layout)

    def _on_yes_clicked(self):
        """确定按钮点击处理"""
        # 如果有回调函数，先调用回调函数
        if self._on_confirm_callback:
            self._on_confirm_callback(self)
        # 再关闭对话框
        self.accept()

    # --- 自定义扩展接口 ---

    def add_custom_widget(self, widget: QWidget):
        """在文字下方动态添加自定义组件"""
        self.custom_layout.addWidget(widget)
        return self

    def add_custom_layout(self, layout):
        """在文字下方动态添加自定义布局"""
        self.custom_layout.addLayout(layout)
        return self

    def set_on_confirm(self, callback):
        """设置确定按钮的回调函数
        
        Args:
            callback: 回调函数，接收对话框实例作为参数
        """
        self._on_confirm_callback = callback
        return self

    # --- 静态方法（对齐原生 QMessageBox 接口） ---

    @classmethod
    def information(cls, parent, title, text, widget=None, layout=None, on_confirm=None):
        """
        信息提示框：XMessageBox.information(self, '标题', '内容')
        
        Args:
            parent: 父组件
            title: 标题
            text: 消息文本
            widget: 自定义组件
            layout: 自定义布局
            on_confirm: 确定按钮回调函数，接收对话框实例作为参数
        """
        if not widget and not layout:
            dlg = cls(title, text, icon=IconName.INFO, color=XColor.SECONDARY, parent=parent)
        else:
            dlg = cls(title, text, icon=IconName.EDITOR, color=XColor.SECONDARY, parent=parent)
        # 添加自定义内容
        if widget:
            dlg.add_custom_widget(widget)
        if layout:
            dlg.add_custom_layout(layout)
        # 设置回调函数
        if on_confirm:
            dlg.set_on_confirm(on_confirm)
        return dlg.exec_()

    @classmethod
    def ask(cls, parent, title, text, widget=None, layout=None, on_confirm=None):
        """
        询问对话框：提供确定和取消按钮
        
        Args:
            parent: 父组件
            title: 标题
            text: 消息文本
            widget: 自定义组件
            layout: 自定义布局
            on_confirm: 确定按钮回调函数，接收对话框实例作为参数
        """
        dlg = cls(title, text, icon=IconName.HELP, color=XColor.SECONDARY, parent=parent)
        # 添加自定义内容
        if widget:
            dlg.add_custom_widget(widget)
        if layout:
            dlg.add_custom_layout(layout)

        # 创建取消按钮
        # 使用 OUTLINED 变体区分主次按钮
        cancel_btn = XPushButton(
            "Cancel",
            color=XColor.TERTIARY,
            variant=XButtonVariant.OUTLINED,
            size=XSize.SMALL,
        )
        cancel_btn.setMinimumWidth(70)
        cancel_btn.clicked.connect(dlg.reject)

        # 插入到确定按钮左侧（弹簧之后，确定按钮之前）
        dlg.button_layout.insertWidget(1, cancel_btn)

        # 设置回调函数
        if on_confirm:
            dlg.set_on_confirm(on_confirm)

        return dlg.exec_()
