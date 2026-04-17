"""
XCarousel Example 走马灯组件示例
"""
import sys

from xsideui import XLineEdit

try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from src.xsideui import XWidget, XLabel, XCarousel



class XCarouselDemo(XWidget):
    """XCarousel Example Window"""

    def __init__(self):
        super().__init__()
        self.set_title("XCarousel Demo")
        self.resize(800, 600)
        self._init_ui()

    def _init_ui(self):
        """构建主界面布局"""

        content_widget = QWidget()
        self.addWidget(content_widget)
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(11)

        # 标题
        layout.addWidget(XLabel("图片轮播组件", style=XLabel.Style.H2))
        layout.addWidget(XLabel("支持自动播放、鼠标悬停暂停、图片点击信号，切换信号，详情请看文档", style=XLabel.Style.BODY))

        # 走马灯
        self.carousel = XCarousel(interval=3000, min_height=460)

        # 添加示例图片
        self.carousel.add_image_page(r".\img\banner1.png", scale_mode="cover")
        self.carousel.add_image_page(r".\img\banner2.png", scale_mode="cover")
        self.carousel.add_image_page(r".\img\banner3.png", scale_mode="cover")


        # 连接信号
        self.carousel.image_clicked.connect(self.on_image_clicked)
        self.carousel.current_page_changed.connect(self.on_page_changed)


        layout.addWidget(self.carousel)
        input = XLineEdit()
        # input.focusInEvent = lambda e: (
        #     self.carousel.timer.stop(),
        #     type(input).focusInEvent(input, e)
        # )
        # input.focusOutEvent = lambda e: (
        #     self.carousel.timer.start(self.carousel.interval) if self.carousel.auto_play else None,
        #     type(input).focusOutEvent(input, e)
        # )
        layout.addWidget(input)


    def on_image_clicked(self, index):
        """图片点击事件"""
        print(f"点击了第 {index + 1} 张图片")

    def on_page_changed(self, index):
        """页面切换事件"""
        print(f"切换到第 {index + 1} 页")


def main():
    app = QApplication(sys.argv)
    window = XCarouselDemo()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
