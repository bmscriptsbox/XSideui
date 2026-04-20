from ..utils.qt_compat import QGroupBox, Qt, QEvent
from ..i18n import XI18N

class XGroupBox(QGroupBox):
    """组框组件"""
    
    def __init__(
        self,
        title: str = "",
        parent=None
    ):
        """初始化分组框组件。

            Args:
                title: 分组框顶部的标题文本。
                parent: 父级组件。
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