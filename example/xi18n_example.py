import sys

from PySide2.QtWidgets import QWidget, QVBoxLayout, QApplication

from xsideui import XWidget, XPushButton, tr, XLabel, XI18N


class Xi18nDemo(XWidget):
    def __init__(self, parent=None):
        super(Xi18nDemo, self).__init__(parent)
        self._init_ui()


    def _init_ui(self):
        context_widget = QWidget()
        self.addWidget(context_widget)
        layout = QVBoxLayout(context_widget)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(20)

        # 基础使用
        # 使用 tr() 仅为了方便让 lupdate 工具能静态提取该字符串到 .ts 文件
        btn = XPushButton(tr('Download'))  # 从组件库语言包获取的翻译
        label = XLabel(tr('Coca-Cola'))   # 从自定义语言包获取的翻译

        # # 占位使用（占位符本身是不需要翻译的）
        raw_key = tr("User %1 has %2 messages. ")
        text = XI18N.x_tr(raw_key, args=['Tom','15'])  # 调用x_tr()执行占位符变量替换，并完成翻译
        label_2 = XLabel(text=text)

        layout.addWidget(btn)
        layout.addWidget(label)
        layout.addWidget(label_2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    XI18N.set_language('zh_CN')
    XI18N.add_custom_lang_path(r'./custom_langs', context='XSideUiDemo')  # 从自定义语言包获取的翻译
    demo = Xi18nDemo()
    demo.show()
    app.exec_()