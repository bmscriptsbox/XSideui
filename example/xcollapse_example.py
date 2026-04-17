"""
XCollapse 折叠面板组件使用示例
展示折叠面板组件的各种用法和主题适配
"""

import sys


try:
    from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
except ImportError:
    from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton


from src.xsideui import XLabel, XCollapse, XCollapseGroup, XWidget, XI18N

class XCollapseDemo(XWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.set_title(self.tr("XCollapse Demo"))
        self.resize(800, 600)
        content_widget = QWidget()
        self.addWidget(content_widget)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20,20,20,20)
        content_layout.setSpacing(20)

        content_layout.addWidget(XLabel(self.tr("Collapse Panel 1"), style=XLabel.Style.H4))
        panel1 = XCollapse(title=self.tr("Expand / Collapse Panel"), expanded=True)
        panel1.add_content_widget(XLabel(self.tr("The content area of the panel can have any components added"), style=XLabel.Style.BODY))
        panel1.state_changed.connect(lambda exp: print(f"面板1状态: {'展开' if exp else '折叠'}"))
        content_layout.addWidget(panel1)

        content_layout.addWidget(XLabel(self.tr("Panel Group - Accordion Mode"), style=XLabel.Style.H4))


        group2 = XCollapseGroup(accordion=True)

        group2_panel1 = group2.add_panel(self.tr("Option A"))
        group2_panel1.add_content_widget(XLabel(self.tr("Detailed content of option A"), style=XLabel.Style.BODY))

        group2_panel2 = group2.add_panel(self.tr("Option B"))
        group2_panel2.add_content_widget(XLabel(self.tr("Detailed content of option B"), style=XLabel.Style.BODY))

        group2_panel3 = group2.add_panel(self.tr("Option C"))
        group2_panel3.add_content_widget(XLabel(self.tr("Detailed content of option C"), style=XLabel.Style.BODY))

        content_layout.addWidget(group2)

    def tr(self, text):
        return text



if __name__ == "__main__":
    app = QApplication(sys.argv)
    # XI18N.add_custom_lang_path(r"D:\PythonCode\xsideui-new\src\xsideui\i18n\222", context='app')
    XI18N.set_language("zh_CN")
    demo = XCollapseDemo()
    demo.show()
    sys.exit(app.exec_())
