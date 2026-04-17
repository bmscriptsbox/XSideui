"""
Group Box Component 分组框组件
支持明暗主题切换的分组框组件
"""
from ..utils.qt_compat import QGroupBox, Qt, QEvent
from ..i18n import XI18N

class XGroupBox(QGroupBox):
    """Group Box Component 分组框组件
    
    一个用于组织相关组件的主题化分组框。
    
    Features 功能:
        - Custom title 自定义标题
        - Theme integration 主题适配
        - Rounded corners 圆角边框
        - Disabled state 禁用状态
    """
    
    def __init__(
        self,
        title: str = "",
        parent=None
    ):
        """
        Initialize group box.
        
        初始化分组框。
        
        Args:
            title: Group title 分组标题
            parent: Parent widget 父组件
        """
        super().__init__(title, parent)
        self.setObjectName("xgroupbox")
        self._text_key =title
        self.retranslateUi()
        self.setAttribute(Qt.WA_StyledBackground, True)

    def retranslateUi(self):
        """当语言切换或文本更新时调用"""
        if not self._text_key:
            super().setTitle('')
            return
        translated = XI18N.x_tr(self._text_key)
        super().setTitle(translated)

    def changeEvent(self, event):
        """显式捕获事件，确保 Mixin 的逻辑被执行"""
        if event.type() == QEvent.LanguageChange:
            # 强制触发刷新
            self.retranslateUi()
        super().changeEvent(event)