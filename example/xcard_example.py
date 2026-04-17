"""
XCard 组件使用示例
展示卡片组件如何自动适配明暗主题切换
"""

import sys
try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from src.xsideui import XPushButton, XSize, XButtonVariant, IconName, XColor
from src.xsideui import XLabel, XCard, XHeaderCard, XGroupCard, XWidget



class XCardDemo(XWidget):
    def __init__(self):
        super(XCardDemo, self).__init__()
        self._initUI()

    def _initUI(self):
        self.set_title('XCard Demo')
        self.resize(800, 600)
        content_widget = QWidget()
        self.addWidget(content_widget)
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(20,20,20,20)
        main_layout.setSpacing(20)

        main_layout.addWidget(XLabel("XCard 组件示例", style=XLabel.Style.H1))
        main_layout.addWidget(XLabel("点击下方按钮切换明暗主题，观察卡片样式变化", style=XLabel.Style.CAPTION))

        # 基础卡片
        main_layout.addWidget(XLabel("基础卡片 (XCard)", style=XLabel.Style.H3))
        basic_card = XCard(clickable=True )
        basic_card.addWidget(XLabel("这是一个可点击的基础卡片", style=XLabel.Style.BODY))
        basic_card.clicked.connect(lambda: print("基础卡片被点击"))
        main_layout.addWidget(basic_card)

        # 标题卡片
        main_layout.addWidget(XLabel("标题卡片 (XHeaderCard)", style=XLabel.Style.H3))
        header_card = XHeaderCard(title="卡片标题")
        btn_clear_header_card = XPushButton(icon=IconName.DELETE, size=XSize.SMALL, color=XColor.DANGER,
                                             variant=XButtonVariant.TEXT)
        btn_clear_header_card.clicked.connect(lambda: header_card.clear())
        header_card.addWidget(btn_clear_header_card, target=header_card.CardPosition.HEADER, stretch=0)
        header_card.addWidget(XLabel("这是标题卡片的内容区域", style=XLabel.Style.BODY), target=header_card.CardPosition.CONTENT)
        main_layout.addWidget(header_card)

        # 分组卡片
        main_layout.addWidget(XLabel("分组卡片 (XGroupCard)", style=XLabel.Style.H3))
        group_card = XGroupCard(title="分组设置")
        btn_add_group = XPushButton(icon=IconName.PLUS, size=XSize.DEFAULT, color=XColor.PRIMARY,
                                    variant=XButtonVariant.TEXT)
        btn_clear_group = XPushButton(icon=IconName.DELETE, size=XSize.DEFAULT, color=XColor.DANGER,
                                      variant=XButtonVariant.TEXT)
        btn_add_group.clicked.connect(
            lambda: group_card.add_group().add(XLabel('新增分组', style=XLabel.Style.BODY)))
        btn_clear_group.clicked.connect(lambda: group_card.clear())
        group_card.addWidget(btn_add_group, target=group_card.CardPosition.HEADER, stretch=0)
        group_card.addWidget(btn_clear_group, target=group_card.CardPosition.HEADER, stretch=0)

        # 链式添加
        group_card.add_group() \
            .add(XLabel("分组一文本内容", style=XLabel.Style.BODY), stretch=1) \
            .add(XPushButton(variant=XButtonVariant.TEXT, icon=IconName.RIGHT, size=XSize.DEFAULT,
                             color=XColor.TERTIARY), stretch=0)

        # 常规添加
        group2 = group_card.add_group()
        group_card.addWidget(XLabel("分组二文本内容"), group_index=group2.index, stretch=0)
        group_card.addWidget(XPushButton(variant=XButtonVariant.TEXT, icon=IconName.RIGHT, size=XSize.DEFAULT,
                                         color=XColor.TERTIARY), group_index=group2.index, stretch=0)

        main_layout.addWidget(group_card)



def main():
    app = QApplication(sys.argv)
    xcardDemo = XCardDemo()
    xcardDemo.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
