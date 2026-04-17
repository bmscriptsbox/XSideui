"""
XTableWidget 表格组件示例
"""

import sys

from xsideui import XI18N

try:
    from PySide2.QtCore import QTimer
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QTableWidgetItem, QWidget
except ImportError:
    from PySide6.QtCore import QTimer
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QTableWidgetItem, QWidget

from src.xsideui import XWidget, XTableWidget, XLabel



class TableExample(XWidget):
    """动态切换样式示例 (Dynamic Style Switch Example)"""

    def __init__(self):
        super().__init__()


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
        self._init_ui()

    def _init_ui(self):
        self.set_title("XTableWidget Demo ")
        self.resize(600, 800)
        self.content_widget = QWidget()
        self.addWidget(self.content_widget)
        self.layout = QVBoxLayout(self.content_widget)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.setup_table()



    def setup_table(self):
        self.layout.addWidget(XLabel('默认表格', style=XLabel.Style.H2))
        table = XTableWidget(style="default")
        self.layout.addWidget(table)


        self.layout.addWidget(XLabel('斑马纹表格', style=XLabel.Style.H2))
        table_striped = XTableWidget(style="striped")
        self.layout.addWidget(table_striped)


        # QTimer.singleShot(100, lambda: self.add_table_bata(table))
        QTimer.singleShot(200, lambda: self.add_table_bata(table_striped))



    def add_table_bata(self, table:XTableWidget):
        table.set_headers(['Name', 'Age', 'Job'])
        table.set_column_widths([100,100,-1])
        table.setRowCount(len(self.data))
        for row ,value in enumerate(self.data):
            for column , item in enumerate(value):
                table_item = QTableWidgetItem(item)
                table.setItem(row,column,table_item)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    XI18N.set_language("zh_CN")
    window = TableExample()
    window.show()
    sys.exit(app.exec_())
