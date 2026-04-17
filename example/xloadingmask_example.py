"""
加载遮罩组件示例
"""
import sys

try:
    from PySide2.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                                   QTableWidgetItem)
    from PySide2.QtCore import Qt
    from PySide2.QtCore import QTimer
except ImportError:
    from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                                   QTableWidgetItem)
    from PySide6.QtCore import Qt
    from PySide6.QtCore import QTimer


from src.xsideui import (XLabel, XLoadingMask, XPushButton,
                         XWidget, XTableWidget)


class XLoadingMaskExample(XWidget):
    """XLoadingMask Example Window 加载遮罩示例窗口"""

    def __init__(self):
        super().__init__()
        self.set_title("XLoadingMask- 加载遮罩组件示例")
        self.resize(600, 800)
        self._loading_mask = None
        self._setup_ui()
        self.data = [
            ['刘备', '26', '皇室特供草鞋编织师'],
            ['关羽', '18', '战马销售顾问兼美髯养护'],
            ['张飞', '18', '屠夫转行声乐教练'],

            ['刘备', '27', '蜀汉集团创始人兼首席哭官'],
            ['关羽', '19', '青龙偃月刀代言人'],
            ['张飞', '19', '长板桥噪音测试员'],

            ['刘备', '28', '诸葛亮的老板兼眼泪表演家'],
            ['关羽', '20', '过五关斩六将快递员'],
            ['张飞', '20', '丈八蛇矛烧烤师傅'],

            ['刘备', '29', '荆州钉子户'],
            ['关羽', '21', '华容道放水管理员'],
            ['张飞', '21', '巴西太守兼吼叫教练'],

            ['刘备', '30', '阿斗摔跤教练'],
            ['关羽', '22', '麦城迷路导游'],
            ['张飞', '22', '阆中夜市屠夫'],
        ]*20

    def _setup_ui(self):
        """Setup user interface.
        设置用户界面。"""
        central_widget = QWidget()
        self.addWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        main_layout.addWidget(XLabel(
            "一个半透明的遮罩层，中间显示旋转的加载图标和文字。",
            style=XLabel.Style.H3
        ))

        self.table = XTableWidget(style="default")
        main_layout.addWidget(self.table)

        btn = XPushButton("加载数据")
        btn.clicked.connect(self._show_loading)
        main_layout.addWidget(btn,alignment=Qt.AlignRight)

    def add_table_bata(self):
        self.table.set_headers(['姓名', '年龄', '职业'])
        self.table.set_column_widths([100,100,-1])
        self.table.setRowCount(len(self.data))
        for row ,value in enumerate(self.data):
            for column , item in enumerate(value):
                table_item = QTableWidgetItem(item)
                self.table.setItem(row,column,table_item)

    def _show_loading(self):
        """Show loading mask.
        显示加载遮罩。"""
        self.loading = XLoadingMask.show_loading(self.table, text="正在处理...")
        self.add_table_bata()
        QTimer.singleShot(3000, self._hide_loading)

    def _hide_loading(self):
        """隐藏加载遮罩。"""
        self.loading.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = XLoadingMaskExample()
    window.show()
    sys.exit(app.exec_())
