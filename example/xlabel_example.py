"""
XLabel 组件使用示例
展示 XLabel 组件的预设样式、自定义参数和方法
"""

import sys



try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from src.xsideui import XWidget, XLabel, XColor, XSize, XHeaderCard, XI18N, XPushButton, IconName, XButtonVariant



class XLabelDemo(XWidget):
    def __init__(self, parent=None):
        super(XLabelDemo, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self.set_title("XLabel Demo")
        self.resize(600, 600)

        context_widget = QWidget()
        self.addWidget(context_widget)
        content_layout = QVBoxLayout(context_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        btn_translation = XPushButton(icon=IconName.TRANSLATE, variant=XButtonVariant.TEXT, size=XSize.SMALL, color=XColor.SECONDARY)
        btn_translation.clicked.connect(self._on_translation)
        self.add_title_bar_widget(btn_translation)

        content_layout.addWidget(XLabel("XLabel 组件示例", style=XLabel.Style.H2))

        preset_card = XHeaderCard('预设样式')
        content_layout.addWidget(preset_card)
        preset_layout = QVBoxLayout()
        preset_layout.addWidget(XLabel("H1 - 一级标题", style=XLabel.Style.H1))
        preset_layout.addWidget(XLabel("H2 - 二级标题", style=XLabel.Style.H2))
        preset_layout.addWidget(XLabel("H3 - 三级标题", style=XLabel.Style.H3))
        preset_layout.addWidget(XLabel("H4 - 强调正文", style=XLabel.Style.H4))
        preset_layout.addWidget(XLabel("BODY - 常规正文", style=XLabel.Style.BODY))
        preset_layout.addWidget(XLabel("CAPTION - 说明文字", style=XLabel.Style.CAPTION))
        preset_layout.addWidget(XLabel("SECONDARY - 次要文字", style=XLabel.Style.SECONDARY))
        preset_layout.addWidget(XLabel("DISABLED - 禁用状态", style=XLabel.Style.DISABLED))
        preset_card.addLayout(preset_layout)

        color_card = XHeaderCard('自定义颜色')
        content_layout.addWidget(color_card)
        color_card.addWidget(XLabel("Primary", style=XLabel.Style.BODY, color=XColor.PRIMARY))
        color_card.addWidget(XLabel("Success", style=XLabel.Style.BODY, color=XColor.SUCCESS))
        color_card.addWidget(XLabel("Warning", style=XLabel.Style.BODY, color=XColor.WARNING))
        color_card.addWidget(XLabel("Danger", style=XLabel.Style.BODY, color=XColor.DANGER), stretch=1)



        decoration_card = XHeaderCard('文字装饰')
        content_layout.addWidget(decoration_card)
        underline_label = XLabel("下划线文字", style=XLabel.Style.H4)
        underline_label.set_underline(True)
        decoration_card.addWidget(underline_label)
        strikethrough_label = XLabel("删除线文字", style=XLabel.Style.H4)
        strikethrough_label.set_strike_out(True)
        decoration_card.addWidget(strikethrough_label)
        both_label = XLabel("下划线 + 删除线", style=XLabel.Style.H4)
        both_label.set_underline(True).set_strike_out(True)
        decoration_card.addWidget(both_label)


        interaction_card = XHeaderCard('文本交互')
        content_layout.addWidget(interaction_card)
        selectable_label = XLabel("这段文字可以选择", style=XLabel.Style.BODY)
        selectable_label.set_selectable(True)
        interaction_card.addWidget(selectable_label)
        wrap_label = XLabel("这段文字会自动换行，当文字长度超过标签宽度时，会自动换行显示。", style=XLabel.Style.BODY)
        wrap_label.set_word_wrap(True)
        interaction_card.addWidget(wrap_label)

        elide_card = XHeaderCard('文本省略')
        content_layout.addWidget(elide_card)
        elide_label = XLabel("这是一段很长的文字，当启用省略模式时，如果文字长度超过标签宽度，会自动用省略号截断显示。", style=XLabel.Style.BODY)
        elide_label.set_elide_mode(True)
        elide_card.addWidget(elide_label)

        rich_card = XHeaderCard('富文本')
        content_layout.addWidget(rich_card)
        rich1_label = XLabel("", style=XLabel.Style.BODY)
        rich1_label.set_rich_text("这是<b>粗体</b>和<i>斜体</i>文字")
        rich_card.addWidget(rich1_label)
        rich2_label = XLabel("", style=XLabel.Style.BODY)
        rich2_label.set_rich_text('这是<span style="color: #FF0000">红色</span>文字')
        rich_card.addWidget(rich2_label)
        link_label = XLabel("点击访问 GitHub", style=XLabel.Style.BODY)
        link_label.set_link("https://github.com")
        rich_card.addWidget(link_label)


    def _on_translation(self):
        langs = XI18N.current_lang
        if langs == 'zh_CN':
            XI18N.set_language('en_US')
            print(f'当前：{langs}, 已设置为:en_US')
        else:
            XI18N.set_language("zh_CN")
            print(f'当前：{langs}, 已设置为:zh_CN')




if __name__ == "__main__":
    app = QApplication(sys.argv)
    XI18N.set_language("zh_CN")
    demo = XLabelDemo()
    demo.show()
    sys.exit(app.exec_())
