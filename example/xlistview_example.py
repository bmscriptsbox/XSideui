"""
XListView 组件使用示例
展示基于 Model/View 架构的列表视图组件
"""

import sys
try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget
    from PySide2.QtGui import QStandardItemModel, QStandardItem
    from PySide2.QtCore import Qt
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
    from PySide6.QtGui import QStandardItemModel, QStandardItem
    from PySide6.QtCore import Qt

from src.xsideui import XLabel, XListView, XWidget, XPushButton, XPushButtonGroup, XCard, XGroupBox
from src.xsideui.xenum import XSize


class XListViewDemo(XWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.set_title('XListView Demo')
        self.resize(600, 600)

        content_widget = QWidget()
        self.addWidget(content_widget)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # 基础示例
        content_layout.addWidget(XLabel("基础列表示例", style=XLabel.Style.H3))
        self.list_view = XListView(show_border=True)
        self._setup_model()
        content_layout.addWidget(self.list_view)

        # 控制按钮
        controls = XPushButtonGroup(spacing=10)
        btn_clear = XPushButton("清空选择", size=XSize.SMALL)
        btn_clear.clicked.connect(self.list_view.clear_selection)
        btn_select_all = XPushButton("全选", size=XSize.SMALL)
        btn_select_all.clicked.connect(self.list_view.select_all)
        controls.add_buttons([btn_clear, btn_select_all])
        content_layout.addWidget(controls)

        # 选项组
        options_group = XGroupBox("选项")
        options_layout = QVBoxLayout(options_group)
        options_layout.setSpacing(10)

        from src.xsideui import XCheckBox
        self.check_alternating = XCheckBox("交替行颜色")
        self.check_alternating.stateChanged.connect(self._toggle_alternating)
        options_layout.addWidget(self.check_alternating)

        from src.xsideui import XComboBox
        self.mode_combo = XComboBox()
        self.mode_combo.addItems(["单选", "多选", "扩展选择", "禁止选择"])
        self.mode_combo.currentIndexChanged.connect(self._change_selection_mode)
        options_layout.addWidget(XLabel("选择模式"))
        options_layout.addWidget(self.mode_combo)

        content_layout.addWidget(options_group)

    def _setup_model(self):
        """设置数据模型"""
        model = QStandardItemModel()

        # 添加分组
        fruits = ["苹果", "香蕉", "橙子", "葡萄", "草莓", "西瓜"]
        for i, fruit in enumerate(fruits):
            item = QStandardItem(f"水果 - {fruit}")
            item.setEditable(False)
            model.appendRow(item)

        animals = ["猫", "狗", "鸟", "鱼", "兔子"]
        for animal in animals:
            item = QStandardItem(f"动物 - {animal}")
            item.setEditable(False)
            model.appendRow(item)

        techs = ["Python", "JavaScript", "Rust", "Go", "Java"]
        for tech in techs:
            item = QStandardItem(f"技术 - {tech}")
            item.setEditable(False)
            model.appendRow(item)

        self.list_view.setModel(model)
        self.list_view.set_icon_size(20)

    def _toggle_alternating(self, state):
        """切换交替行颜色"""
        enabled = state == Qt.Checked
        self.list_view.set_alternating_row_colors(enabled)

    def _change_selection_mode(self, index):
        """改变选择模式"""
        # from PySide6.QtWidgets import QAbstractItemView
        try:
            from PySide2.QtWidgets import QAbstractItemView as AIV
        except ImportError:
            from PySide6.QtCore import Qt as p6Qt
            # PySide6 方式
            modes = [
                QAbstractItemView.SingleSelection,
                QAbstractItemView.MultiSelection,
                QAbstractItemView.ExtendedSelection,
                QAbstractItemView.NoSelection
            ]
        else:
            modes = [
                AIV.SingleSelection,
                AIV.MultiSelection,
                AIV.ExtendedSelection,
                AIV.NoSelection
            ]

        if index < len(modes):
            self.list_view.set_selection_mode(modes[index])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = XListViewDemo()
    demo.show()
    sys.exit(app.exec_())
