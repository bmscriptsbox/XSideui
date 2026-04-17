"""
XmNavSimple Example 导航栏组件示例 (纯图标 + 气泡模式)
"""
import sys

from xsideui import XPushButton, XSize, XButtonVariant, XI18N, XLineEdit

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QStackedWidget
except ImportError:
    from PySide6.QtCore import Qt, QTimer
    from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QStackedWidget

from src.xsideui import XWidget, IconName, XLabel, XNavSimple




class XmNavSimpleExample(XWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()


    def _setup_ui(self):
        self.set_title("XNavSimple Demo-导航栏示例")
        self.resize(500, 700)
        # 1. 基础布局
        central_widget = QWidget()
        self.addWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # 顶部边距需设置为0，导航栏和标题栏视觉上才会贴合
        main_layout.setSpacing(0)

        # 2. 左侧导航 (Rails)
        self.navbar = XNavSimple(icon_size=22)
        main_layout.addWidget(self.navbar)

        # 3. 右侧容器 (包含标题 + Stack)
        right_container = QFrame()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addWidget(right_container, 1)

        # 4. 核心：堆叠窗口
        self.stack = QStackedWidget()
        right_layout.addWidget(self.stack)

        # --- 注册页面 ---
        # 可以通过一个字典来建立 ID 和 Stack 索引的映射
        self.pages = {}
        self._add_page("home", self._create_placeholder(IconName.HOME, "首页中心"))
        self._add_page("dashboard", self._create_placeholder(IconName.DASHBOARD, "数据分析仪表盘"))
        # self._add_page("chart", self._create_placeholder(IconName.AREA_CHART, "数据统计看板"))
        # self._add_page("settings", self._create_placeholder(IconName.SETTING, "系统参数设置"))
        # self._add_page("user", self._create_placeholder(IconName.USER, "用户个人中心"))
        # self._add_page("ai", self._create_placeholder(IconName.OPEN_A_I, "AI 助手预览"))
        # self._add_page("logout", self._create_placeholder(IconName.LOGOUT, "账号注销确认"))


        # 添加导航项
        self.navbar.add_item("home", icon_name=IconName.HOME, text="New")
        self.navbar.add_item("dashboard", icon_name=IconName.DASHBOARD, text="仪表台")
        # self.navbar.add_item("ai", icon_name=IconName.OPEN_A_I, text="AI")
        # self.navbar.add_item("chart", icon_name=IconName.AREA_CHART, text="统计")
        # self.navbar.add_item("settings", icon_name=IconName.SETTING, text="设置")
        #
        # self.navbar.add_item("user", icon_name=IconName.USER, text="用户", position='bottom')
        # self.navbar.add_item("logout", icon_name=IconName.LOGOUT, text="退出", position='bottom')



        # 信号连接
        self.navbar.changed.connect(self.on_nav_changed)

        self.navbar.set_current_item("home")

    def _add_page(self, item_id: str, widget: QWidget):
        """注册页面并记录索引"""
        index = self.stack.addWidget(widget)
        self.pages[item_id] = index

    def on_nav_changed(self, item_id: str):
        """点击导航，自动翻页"""
        if item_id in self.pages:
            self.stack.setCurrentIndex(self.pages[item_id])

    def _create_placeholder(self, icon_name: IconName, title: str):
        """创建一个带图标的占位页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        # 2. 主标题
        title_label = XLabel(title, style=XLabel.Style.H2)
        title_label.setAlignment(Qt.AlignCenter)

        # 3. 装饰性副标题
        desc_label = XLabel("功能模块正在建设中...", style=XLabel.Style.BODY)

        input = XLineEdit()
        btn = XPushButton('测试按钮')


        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addWidget(input)
        layout.addWidget(btn)

        return page


if __name__ == "__main__":
    # 开启了高分屏支持 适用于PySide2
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    XI18N.set_language("zh_CN")
    window = XmNavSimpleExample()
    window.show()
    sys.exit(app.exec_())