"""
XNavTree Example 导航树组件示例
演示导航树的基本用法，包括图标支持、层级结构和页面切换。
"""
import sys

from xsideui import XI18N

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import (
        QApplication, QWidget, QHBoxLayout, QVBoxLayout,
        QStackedWidget
    )
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import (
        QApplication, QWidget, QHBoxLayout, QVBoxLayout,
        QStackedWidget
    )

from src.xsideui import XDivider, XLabel, IconName, XNavTree, XWidget, XPushButton, XButtonVariant, XSize, XColor


class XNavTreeExample(XWidget):
    """导航树示例窗口"""

    def __init__(self):
        super().__init__()
        # self.set_title("XNavTree 示例")
        self.resize(1000, 800)

        # 页面 ID 到索引的映射
        self.page_index_map = {}

        self.setup_ui()

    def setup_ui(self):
        """初始化界面"""
        # 创建主布局
        content_widget = QWidget()
        self.addWidget(content_widget)
        main_layout = QHBoxLayout(content_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        btn_translation = XPushButton(icon=IconName.TRANSLATE, variant=XButtonVariant.TEXT, size=XSize.SMALL, color=XColor.SECONDARY)
        btn_translation.clicked.connect(self._on_translation)
        self.add_title_bar_widget(btn_translation)
        # 创建导航树
        nav_tree = self._create_nav_tree()

        # 创建内容区域（包含页面堆叠）
        content_area = self._create_content_area()

        # 添加到主布局
        main_layout.addWidget(nav_tree, 1)
        main_layout.addWidget(XDivider(vertical=True), 0)  # 分割线
        main_layout.addWidget(content_area, 4)

    def _create_nav_tree(self):
        """创建导航树"""
        nav_tree = XNavTree(
            indent=20,
            icon_size=20,
            text_size=14
        )
        nav_tree.setMinimumWidth(180)
        nav_tree.setMaximumWidth(180)

        # 添加菜单项
        menu_items = self._get_menu_items()
        nav_tree.add_item_batch(menu_items)

        # 监听切换事件
        nav_tree.changed.connect(self.on_nav_changed)

        # 设置默认选中
        nav_tree.set_current_id('home')

        return nav_tree

    def _get_menu_items(self):
        """获取菜单项数据
        
        Returns:
            list: 菜单项列表
        """
        return [
            # 首页
            {
                'icon': IconName.HOME,
                'text': 'New',
                'id': 'home'
            },
            # 仪表盘
            {
                'icon': IconName.DASHBOARD,
                'text': 'Save',
                'id': 'dashboard'
            },
            # 系统设置（包含子菜单）
            {
                'icon': IconName.SETTING,
                'text': '系统设置',
                'children': [
                    {
                        'icon': IconName.USER,
                        'text': '用户管理',
                        'id': 'user_management'
                    },
                    {
                        'icon': 'lock',
                        'text': '权限管理',
                        'id': 'permission_management'
                    }
                ]
            },
            # 数据分析（包含子菜单）
            {
                'icon': IconName.CHART,
                'text': '数据分析',
                'children': [
                    {
                        'icon': IconName.CHART_LINE,
                        'text': '销售统计',
                        'id': 'sales_stats'
                    },
                    {
                        'icon': IconName.CHART_LINE,
                        'text': '用户统计',
                        'id': 'user_stats'
                    }
                ]
            }
        ]

    def _create_content_area(self):
        """创建内容区域（包含页面堆叠）
        
        Returns:
            QWidget: 内容区域组件
        """
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(0)

        # 创建页面堆叠
        self.stacked_widget = QStackedWidget()

        # 添加各个页面
        self._add_home_page()
        self._add_dashboard_page()
        self._add_user_management_page()
        self._add_permission_management_page()
        self._add_sales_stats_page()
        self._add_user_stats_page()

        content_layout.addWidget(self.stacked_widget)

        return content_area

    def _add_home_page(self):
        """添加首页"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(XLabel("首页", style=XLabel.Style.H1))
        layout.addWidget(XLabel("欢迎使用 XNavTree 导航树组件,配合QStackedWidget可实现复杂的窗口"))

        # 添加到堆叠并记录索引
        index = self.stacked_widget.addWidget(page)
        self.page_index_map['home'] = index

    def _add_dashboard_page(self):
        """添加仪表盘页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(XLabel("仪表盘", style=XLabel.Style.H1))
        layout.addWidget(XLabel("这里是仪表盘页面，可以展示各种数据概览和图表。"))

        # 添加到堆叠并记录索引
        index = self.stacked_widget.addWidget(page)
        self.page_index_map['dashboard'] = index

    def _add_user_management_page(self):
        """添加用户管理页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(XLabel("用户管理", style=XLabel.Style.H1))
        layout.addWidget(XLabel("这里是用户管理页面，可以管理系统的用户信息。"))

        # 添加到堆叠并记录索引
        index = self.stacked_widget.addWidget(page)
        self.page_index_map['user_management'] = index

    def _add_permission_management_page(self):
        """添加权限管理页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(XLabel("权限管理", style=XLabel.Style.H1))
        layout.addWidget(XLabel("这里是权限管理页面，可以配置系统的权限规则。"))

        # 添加到堆叠并记录索引
        index = self.stacked_widget.addWidget(page)
        self.page_index_map['permission_management'] = index

    def _add_sales_stats_page(self):
        """添加销售统计页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(XLabel("销售统计", style=XLabel.Style.H1))
        layout.addWidget(XLabel("这里是销售统计页面，可以查看销售数据的统计和分析。"))

        # 添加到堆叠并记录索引
        index = self.stacked_widget.addWidget(page)
        self.page_index_map['sales_stats'] = index

    def _add_user_stats_page(self):
        """添加用户统计页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(XLabel("用户统计", style=XLabel.Style.H1))
        layout.addWidget(XLabel("这里是用户统计页面，可以查看用户数据的统计和分析。"))

        # 添加到堆叠并记录索引
        index = self.stacked_widget.addWidget(page)
        self.page_index_map['user_stats'] = index

    def on_nav_changed(self, item_id):
        """导航切换事件处理
        
        Args:
            item_id: 切换后的导航项 ID
        """
        # 切换到对应的页面
        if item_id in self.page_index_map:
            index = self.page_index_map[item_id]
            self.stacked_widget.setCurrentIndex(index)


    def _on_translation(self):
        langs = XI18N.current_lang
        if langs == 'zh_CN':
            XI18N.set_language('en_US')
            print(f'当前：{langs}, 已设置为:en_US')
        else:
            XI18N.set_language("zh_CN")
            print(f'当前：{langs}, 已设置为:zh_CN')

if __name__ == '__main__':
    # 开启了高分屏支持 适用于PySide2
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    XI18N.set_language("zh_CN")
    window = XNavTreeExample()
    window.show()
    sys.exit(app.exec_())
