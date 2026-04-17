"""
XProgressBar 组件使用示例
展示进度条组件如何自动适配明暗主题切换
"""

import sys
try:
    from PySide2.QtCore import QTimer, Qt
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget
except ImportError:
    from PySide6.QtCore import QTimer, Qt
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget


from src.xsideui import XWidget, XLabel, XDivider, XProgressBar, XCircleProgress, XColor


class XProgressBarDemo(XWidget):
    def __init__(self):
        super(XProgressBarDemo, self).__init__()
        self._init_ui()


    def _init_ui(self):
        self.set_title("XProgressBar Demo")
        self.resize(800, 600)

        content_widget = QWidget()
        self.addWidget(content_widget)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20,20,20,20)

        content_layout.addWidget(XLabel("XProgressBar 组件示例", style=XLabel.Style.H1))
        content_layout.addWidget(XDivider())

        content_layout.addWidget(XLabel("线性进度条", style=XLabel.Style.H3))
        color_layout = QVBoxLayout()
        progress_primary = XProgressBar(value=30, color=XColor.PRIMARY, text_visible=False, height=4)
        color_layout.addWidget(progress_primary)
        progress_success = XProgressBar(value=50, color=XColor.SUCCESS, text_visible=False, height=6)
        color_layout.addWidget(progress_success)
        progress_warning = XProgressBar(value=70, color=XColor.WARNING, text_visible=False, height=8)
        color_layout.addWidget(progress_warning)
        progress_danger = XProgressBar(value=90, color=XColor.DANGER, text_visible=True, height=12, text_position='right')
        color_layout.addWidget(progress_danger)
        content_layout.addLayout(color_layout)

        content_layout.addWidget(XLabel("环形进度条", style=XLabel.Style.H3))
        circle_color_layout = QHBoxLayout()
        circle_primary = XCircleProgress(value=30, size=60, color="primary")
        circle_color_layout.addWidget(circle_primary)
        circle_success = XCircleProgress(value=50, size=80, color="success")
        circle_color_layout.addWidget(circle_success)
        circle_warning = XCircleProgress(value=70, size=100, color="warning")
        circle_color_layout.addWidget(circle_warning)
        circle_danger = XCircleProgress(value=90, size=120, color="danger")
        circle_color_layout.addWidget(circle_danger)
        content_layout.addLayout(circle_color_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.update_progress(progress_danger, circle_danger))
        self.timer.start(50)


    def update_progress(self,progress_bar, circle_progress):
        """更新进度条值"""
        current_value = progress_bar.value()
        new_value = current_value + 1
        if new_value > 100:
            new_value = 0
        progress_bar.setValue(new_value)
        circle_progress.setValue(new_value)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = XProgressBarDemo()
    demo.show()
    sys.exit(app.exec_())
