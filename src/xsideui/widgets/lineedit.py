"""Line Edit Component 输入框组件"""
from typing import Union
from ..utils.qt_compat import (QLineEdit, QAction, Signal, QIcon, Qt, QEvent)
from ..icon import XIcon, IconName
from ..xenum import XColor, XSize, XInputStatus
from ..theme import theme_manager
from ..i18n import XI18N


class XLineEdit(QLineEdit):
    """Line Edit Component 输入框组件
    
    A customizable input component with icons and various states.
    """

    iconClicked = Signal(str)

    def __init__(
            self,
            placeholder: str = "",
            size: Union[XSize, str] = XSize.DEFAULT,
            clearable: bool = False,
            show_password: bool = False,
            prefix_icon: Union[str, IconName] = None,
            suffix_icon: Union[str, IconName] = None,
            status: Union[XInputStatus, str] = None,
            parent=None
    ):
        """Initialize line edit.
        初始化输入框。

        Args:
            placeholder: Placeholder text 占位文本
            size: Input size 输入框大小
            clearable: Whether to show clear button 是否显示清空按钮
            show_password: Whether to show password toggle 是否显示密码切换
            prefix_icon: Prefix icon name or IconName enum 前缀图标名称或枚举
            suffix_icon: Suffix icon name or IconName enum 后缀图标名称或枚举
            status: Input status 输入框状态
            parent: Parent widget 父组件
        """
        super().__init__(parent)

        self._prefix_icon = None
        self._suffix_icon = None
        # 1. 记录原始数据（用于重绘）
        self._raw_prefix = None  # 存储前缀图标信息
        self._raw_suffix = None  # 存储后缀图标信息
        self._text_key = placeholder
        self._clearable = clearable
        self._show_password = show_password
        self._password_visible = False
        self._status = status

        self.setObjectName("xlineedit")
        self.setAttribute(Qt.WA_MacShowFocusRect, False)
        self._setup_actions()
        self.set_size(size)

        if prefix_icon:
            self.set_prefix_icon(prefix_icon)
        if suffix_icon:
            self.set_suffix_icon(suffix_icon)
        if clearable:
            self.set_clearable(True)
        if show_password:
            self.set_show_password(True)
        if status:
            self.set_status(status)

        theme_manager.theme_changed.connect(self._on_theme_changed)
        self.retranslateUi()
    def _on_theme_changed(self):
        """主题切换时，重新刷新所有内部图标"""
        # 刷新前缀
        if self._raw_prefix:
            icon_info = self._raw_prefix
            icon = XIcon.get(
                icon_info['name'],
                size=icon_info['size'],
                color=icon_info['color']
            ).icon()
            self._update_prefix_icon(icon)

        # 刷新后缀
        if self._raw_suffix:
            icon_info = self._raw_suffix
            icon = XIcon.get(
                icon_info['name'],
                size=icon_info['size'],
                color=icon_info['color']
            ).icon()
            self._update_suffix_icon(icon)

        # 刷新状态图标（Error/Success）
        if self._status:
            self.set_status(self._status)

        # 刷新清除按钮和密码按钮
        self._update_action_icons()

    def _update_prefix_icon(self, icon: QIcon):
        """更新前缀图标（内部方法，避免重复存储）"""
        if self._prefix_icon:
            self.removeAction(self._prefix_icon)

        if icon:
            action = self._create_icon_action(icon, 'prefix')
            self._prefix_icon = action
            self.addAction(action, QLineEdit.LeadingPosition)

    def _update_suffix_icon(self, icon: QIcon):
        """更新后缀图标（内部方法，避免重复存储）"""
        if self._suffix_icon:
            self.removeAction(self._suffix_icon)

        if icon:
            action = self._create_icon_action(icon, 'suffix')
            self._suffix_icon = action
            self.addAction(action, QLineEdit.TrailingPosition)

    def _update_action_icons(self):
        """更新内置动作（清除、密码）的图标"""
        # 更新清除图标
        self._clear_action.setIcon(XIcon(IconName.CLOSE).icon())
        # 更新密码图标
        icon_color = XColor.PRIMARY if self._password_visible else XColor.SECONDARY
        name = IconName.EYE_ON if self._password_visible else IconName.EYE_OFF
        self._password_action.setIcon(XIcon(name, color=icon_color).icon())

    def _setup_actions(self):
        """Initialize actions 初始化动作"""
        self._clear_action = QAction(XIcon(IconName.CLOSE).icon(), "", self)
        self._clear_action.triggered.connect(self.clear)
        self._clear_action.setVisible(False)

        self._password_action = QAction(XIcon(IconName.EYE_OFF).icon(), "", self)
        self._password_action.triggered.connect(self._toggle_password_visible)

        self.textChanged.connect(self._update_clear_button)

    def set_size(self, size: Union[XSize, str]) -> 'XLineEdit':
        """Set input size 设置输入框尺寸"""
        if isinstance(size, XSize):
            size = size.value
        elif size not in ["large", "default", "small", "mini"]:
            size = "default"
        self.setProperty("input-size", size)
        self.style().unpolish(self)
        self.style().polish(self)
        return self
    def retranslateUi(self):
        """当语言切换或文本更新时调用"""
        if not self._text_key:
            super().setPlaceholderText('')
            return
        translated = XI18N.x_tr(self._text_key)
        super().setPlaceholderText(translated)

    def changeEvent(self, event):
        """显式捕获事件，确保 Mixin 的逻辑被执行"""
        if event.type() == QEvent.LanguageChange:
            # 强制触发刷新
            self.retranslateUi()
        super().changeEvent(event)

    def setPlaceholderText(self, arg__1):
        translated = XI18N.x_tr(arg__1)
        super().setPlaceholderText(translated)


    def set_clearable(self, clearable: bool) -> 'XLineEdit':
        """Set whether to show clear button 设置是否显示清空按钮"""
        self._clearable = clearable
        if clearable:
            self.addAction(self._clear_action, QLineEdit.TrailingPosition)
        else:
            self.removeAction(self._clear_action)
        return self

    def set_show_password(self, show: bool) -> 'XLineEdit':
        """Set whether to show password toggle 设置是否显示密码切换"""
        self._show_password = show
        if show:
            self.setEchoMode(QLineEdit.Password)
            self.addAction(self._password_action, QLineEdit.TrailingPosition)
        else:
            self.setEchoMode(QLineEdit.Normal)
            self.removeAction(self._password_action)
        return self

    def set_prefix_icon(self, icon: Union[str, IconName], size: int = 16, color: Union[str, XColor] = XColor.SECONDARY) -> 'XLineEdit':
        """Set prefix icon 设置前缀图标

        Args:
            icon: Icon name or IconName enum 图标名称或枚举
            size: Icon size 图标大小（默认16）
            color: Icon color 图标颜色（默认SECONDARY）

        Returns:
            self: 支持链式调用
        """
        self._raw_prefix = {
            'name': icon,
            'size': size,
            'color': color
        }

        if self._prefix_icon:
            self.removeAction(self._prefix_icon)

        if icon:
            qicon = XIcon.get(icon, size=size, color=color).icon()
            action = self._create_icon_action(qicon, 'prefix')
            self._prefix_icon = action
            self.addAction(action, QLineEdit.LeadingPosition)
        return self

    def set_suffix_icon(self, icon: Union[str, IconName], size: int = 16, color: Union[str, XColor] = XColor.SECONDARY) -> 'XLineEdit':
        """Set suffix icon 设置后缀图标

        Args:
            icon: Icon name or IconName enum 图标名称或枚举
            size: Icon size 图标大小（默认16）
            color: Icon color 图标颜色（默认SECONDARY）

        Returns:
            self: 支持链式调用
        """
        self._raw_suffix = {
            'name': icon,
            'size': size,
            'color': color
        }

        if self._suffix_icon:
            self.removeAction(self._suffix_icon)

        if icon:
            qicon = XIcon.get(icon, size=size, color=color).icon()
            action = self._create_icon_action(qicon, 'suffix')
            self._suffix_icon = action
            self.addAction(action, QLineEdit.TrailingPosition)
        return self

    def set_status(self, status: Union[XInputStatus, str]) -> 'XLineEdit':
        """Set input status 设置输入框状态

        Args:
            status: XInputStatus.ERROR / XInputStatus.SUCCESS / None
        """
        if isinstance(status, XInputStatus):
            status_value = status.value
        else:
            status_value = status if status else ""

        if self.property("color") == status_value:
            return self

        if self.inputMethodQuery(Qt.ImMicroFocus):
            pass

        # 移除已有的状态图标
        if hasattr(self, '_status_icon'):
            self.removeAction(self._status_icon)
            del self._status_icon

        self._status = status

        if status_value:
            # 只有在没有前缀图标时才添加状态图标，避免视觉拥挤
            if not self._prefix_icon:
                icon_name = IconName.CLOSE_CIRCLE if status_value == 'error' else IconName.CHECK_CIRCLE
                icon_color = XColor.DANGER if status_value == 'error' else XColor.SUCCESS

                # 创建并添加图标动作
                action = QAction(XIcon(icon_name, color=icon_color).icon(), "", self)
                self._status_icon = action
                self.addAction(action, QLineEdit.LeadingPosition)

        # 5. 更新属性并触发样式重绘
        self.setProperty("color", status_value)

        # 只有在必要时才调用 polish，这是确保 IME 不断开的关键
        self.style().unpolish(self)
        self.style().polish(self)

        return self



    def _create_icon_action(self, icon: QIcon, position: str) -> QAction:
        """Create icon action 创建图标动作"""
        action = QAction(icon, "", self)
        action.triggered.connect(lambda: self.iconClicked.emit(position))
        return action

    def _update_clear_button(self, text: str):
        """更新清除按钮显示状态"""
        if not self._clearable:
            return

        should_visible = bool(text)

        # 增加判断：只有显隐状态发生切换时才操作
        if self._clear_action.isVisible() != should_visible:
            # 如果正在输入拼音，尽量延迟切换，直到用户空格上屏
            if self.inputMethodQuery(Qt.ImMicroFocus) and should_visible:
                return

            self._clear_action.setVisible(should_visible)



    def _toggle_password_visible(self):
        """Toggle password visibility 切换密码显示状态"""
        self._password_visible = not self._password_visible
        self.setEchoMode(QLineEdit.Normal if self._password_visible else QLineEdit.Password)

        icon_color = XColor.PRIMARY if self._password_visible else XColor.SECONDARY
        self._password_action.setIcon(XIcon(IconName.EYE_ON).with_color(icon_color).icon() if self._password_visible else XIcon(IconName.EYE_OFF).with_color(icon_color).icon() )
