"""
XPagination 组件使用示例
展示分页器如何自动适配明暗主题切换，以及如何使用翻页信号
"""

import sys

from xsideui import XI18N

try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QTableWidgetItem, QWidget
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QTableWidgetItem, QWidget

from src.xsideui import XLabel, XPagination, XWidget, XTableWidget


class PaginationExample(XWidget):
    """分页器示例窗口"""
    
    def __init__(self):
        super().__init__()
        
        # 模拟数据
        self.all_data = self._generate_data(500)

        # 设置布局（先创建UI组件）
        self._setup_ui()
        
        # 连接翻页信号
        self.pagination.prevClicked.connect(self._on_prev_page)
        self.pagination.nextClicked.connect(self._on_next_page)
        self.pagination.pageClicked.connect(self._on_page_clicked)
        self.pagination.jumped.connect(self._on_jumped)
        self.pagination.pageChanged.connect(self._on_page_changed)
        self.pagination.pageSizeChanged.connect(self._on_page_size_changed)
        
        # 初始化显示（在UI创建后）
        self._load_page_data()
    
    def _setup_ui(self):
        """设置UI"""
        self.resize(800,600)
        content_widget = QWidget()
        self.addWidget(content_widget)

        layout = QVBoxLayout(content_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20,20,20,20)
        
        # 添加标题
        layout.addWidget(XLabel("XPagination 分页组件示例", style=XLabel.Style.H1))

        # 创建表格
        self.table = XTableWidget()
        self.table.set_headers(["姓名", "年龄", "职位"])
        self.table.set_column_widths([100,100,-1])
        layout.addWidget(self.table)

        # 创建分页器
        self.pagination = XPagination(total=500, page_size=30, current_page=1)
        layout.addWidget(self.pagination)


    
    def _generate_data(self, count: int) -> list:
        """生成模拟数据"""
        data = []
        positions = ["软件工程师", "产品经理", "UI设计师", "测试工程师", "前端开发", "后端开发"]
        for i in range(count):
            data.append({
                "name": f"张{i+1}",
                "age": str(20 + (i % 30)),
                "position": positions[i % len(positions)]
            })
        return data
    
    def _load_page_data(self):
        """加载当前页数据"""
        start, end = self.pagination.get_page_range()
        page_data = self.all_data[start:end]
        
        # 更新表格
        self.table.setRowCount(len(page_data))
        for row, item in enumerate(page_data):
            self.table.setItem(row, 0, QTableWidgetItem(item["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(item["age"]))
            self.table.setItem(row, 2, QTableWidgetItem(item["position"]))

    
    def _on_prev_page(self, page: int):
        """上一页"""
        print(f"[信号] 点击上一页按钮，跳转到第 {page} 页")
        self._load_page_data()
    
    def _on_next_page(self, page: int):
        """下一页"""
        print(f"[信号] 点击下一页按钮，跳转到第 {page} 页")
        self._load_page_data()
    
    def _on_page_clicked(self, page: int):
        """点击页码"""
        print(f"[信号] 点击页码按钮，跳转到第 {page} 页")
        self._load_page_data()
    
    def _on_jumped(self, page: int):
        """跳转页码"""
        print(f"[信号] 输入框跳转，跳转到第 {page} 页")
        self._load_page_data()
    
    def _on_page_changed(self, page: int):
        """页码变化"""
        print(f"[信号] 页码变化到第 {page} 页")
    
    def _on_page_size_changed(self, page_size: int):
        """每页数量变化"""
        print(f"[信号] 每页数量变化为 {page_size}")
        self._load_page_data()
    
    def _change_page_size(self):
        """修改每页数量"""
        self.pagination.set_page_size(20)
    
    def _reset_page_size(self):
        """恢复每页数量"""
        self.pagination.set_page_size(10)


def main():
    app = QApplication(sys.argv)
    # 创建主窗口
    XI18N.set_language("zh_CN")
    window = PaginationExample()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
