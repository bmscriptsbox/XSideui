"""
XCodeBlock 组件使用示例
展示代码块组件如何自动适配明暗主题切换
"""

import sys

try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from src.xsideui import XWidget, XLabel, XCodeBlock


class XCodeBlockDemo(XWidget):
    def __init__(self):
        super(XCodeBlockDemo, self).__init__()
        self._init_ui()

    def _init_ui(self):
        self.set_title('XCodeBlock Demo')
        self.resize(600, 800)
        content_widget = QWidget(self)
        self.addWidget(content_widget)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 20, 20, 20)

        content_layout.addWidget(XLabel("Python 代码示例", style=XLabel.Style.H3))
        python_code = '''def hello_world():
            """
            这是一个 Python 函数示例
            """
            name = "XmSideUI"
            print(f"Hello, {name}!")

            numbers = [1, 2, 3, 4, 5]
            total = sum(numbers)

            if total > 10:
                return "Total is greater than 10"
            else:
                return "Total is less than or equal to 10"

        result = hello_world()
        print(result)'''

        code_block1 = XCodeBlock(code=python_code)
        content_layout.addWidget(code_block1)
        content_layout.addWidget(XLabel("类定义示例", style=XLabel.Style.H3))

        class_code = '''class Calculator:
            """简单的计算器类"""

            def __init__(self, value=0):
                self.value = value

            def add(self, other):
                """加法运算"""
                return self.value + other

            def multiply(self, other):
                """乘法运算"""
                return self.value * other

            def __str__(self):
                return f"Calculator(value={self.value})"

        calc = Calculator(10)
        result = calc.add(5)
        print(f"Result: {result}")'''

        code_block2 = XCodeBlock(code=class_code)
        content_layout.addWidget(code_block2)

        content_layout.addWidget(XLabel("列表推导式示例", style=XLabel.Style.H3))

        list_code = '''# 使用列表推导式创建平方数列表
        numbers = [1, 2, 3, 4, 5]
        squares = [x ** 2 for x in numbers]

        # 使用列表推导式过滤偶数
        evens = [x for x in numbers if x % 2 == 0]

        # 使用字典推导式
        word_lengths = {word: len(word) for word in ["hello", "world", "python"]}

        print(f"Squares: {squares}")
        print(f"Evens: {evens}")
        print(f"Word lengths: {word_lengths}")'''

        code_block3 = XCodeBlock(code=list_code)
        content_layout.addWidget(code_block3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = XCodeBlockDemo()
    demo.show()
    sys.exit(app.exec_())
