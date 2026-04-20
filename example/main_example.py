# conding utf-8
import ctypes
import sys

try:
    from PySide6.QtCore import Qt, QTimer, QPoint
    from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QFrame, \
        QTableWidgetItem, QFormLayout, QListWidgetItem
except ImportError:
    from PySide2.QtCore import Qt, QTimer, QPoint
    from PySide2.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QFrame, \
        QTableWidgetItem, QFormLayout, QListWidgetItem

from src.xsideui import XWidget, XLabel, XPushButton, XColor, XButtonVariant, IconName, XPushButtonGroup, \
    XPushButtonDropdown, XSwitch, XRadioButton, XCheckBox, XHeaderCard, XLineEdit, XIcon, XDateEdit, XDateTimeEdit, \
    XTimeEdit, XComboBox, XTextEdit, XCodeBlock, XCarousel, XTableWidget, XLoadingMask, XPagination, XSpinBox, \
    XDoubleSpinBox, XSlider, XProgressBar, XCircleProgress, XNotif, XMessageBox, XSize, XMenu, XPopover, \
    XTextBadge, XIconBadge, XTabWidget, XUpload, XListWidget, XNavSimple, XI18N, XScrollArea, tr
from src.xsideui.utils.qt_compat import exec_app


class XSideUiDemo(XWidget):
    def __init__(self, parent=None):
        super(XSideUiDemo, self).__init__(parent=parent)
        self.timer = QTimer(self)
        self._init_ui()

    def _init_ui(self):
        self.set_title('XSideUi样式示例')
        self.set_logo(r'..\resources\logo.png')
        self.resize(1000, 600)
        # 标题栏增加语言切换按钮
        btn_translation = XPushButton(icon=IconName.TRANSLATE, variant=XButtonVariant.TEXT, size=XSize.SMALL,
                                      color=XColor.SECONDARY)
        btn_translation.clicked.connect(self._on_translation)
        self.add_title_bar_widget(btn_translation)

        main_widget = QFrame()
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(11)
        main_widget.setLayout(self.main_layout)
        self.addWidget(main_widget)

        self._init_navbar()

        # 左右布局
        self.scroll_area = XScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.set_scrollbar_visible(True, False)

        context_widget = QFrame()
        self.scroll_area.setWidget(context_widget)
        self.main_layout.addWidget(self.scroll_area)
        context_layout = QHBoxLayout(context_widget)

        self.left_frame = QFrame()
        self.left_layout = QVBoxLayout(self.left_frame)
        self.left_layout.setAlignment(Qt.AlignTop)

        # 滑动区域
        self.right_frame = QFrame()
        self.right_layout = QVBoxLayout(self.right_frame)
        self.right_layout.setAlignment(Qt.AlignTop)

        context_layout.addWidget(self.left_frame, 9)
        context_layout.addWidget(self.right_frame, 3)

        self._init_layout()

    def _init_navbar(self):
        self.navbar = XNavSimple(icon_size=22)  # 导航栏
        self.main_layout.addWidget(self.navbar, 0)

        # 添加导航项
        self.navbar.add_item("home", icon_name=IconName.HOME, text=tr("Home"))
        self.navbar.add_item("dashboard", icon_name=IconName.DASHBOARD, text=tr("Dashboard"))
        self.navbar.add_item("ai", icon_name=IconName.SYSTEM, text=tr("Ai"))
        self.navbar.add_item("chart", icon_name=IconName.CHART, text=tr("Statistics"))
        self.navbar.add_item("settings", icon_name=IconName.SETTING, text=tr("Settings"))

        self.navbar.add_item("user", icon_name=IconName.USER, text=tr('User'), position='bottom')
        self.navbar.add_item("logout", icon_name=IconName.LOGOUT, text=tr('Exit'), position='bottom')

    def _init_layout(self):
        self._banner_layout()
        self._theme_button_layout()
        self._button_layout()
        self._notif_layout()
        self._badge_layout()
        self._table_layout()
        self._check_layout()
        self._progressbar_layout()
        self._input_layout()

    def _banner_layout(self):
        carousel = XCarousel(interval=3000, min_height=160)
        carousel.setMaximumHeight(320)

        # 添加示例图片
        carousel.add_image_page(r".\img\banner1.png", scale_mode="cover")
        carousel.add_image_page(r".\img\banner2.png", scale_mode="cover")
        carousel.add_image_page(r".\img\banner3.png", scale_mode="cover")

        self.left_layout.addWidget(carousel)

    def _theme_button_layout(self):
        """主题颜色演示"""
        theme_card = XHeaderCard(tr('Theme color'))
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(XPushButton(tr('Primary'), color=XColor.PRIMARY))
        theme_layout.addWidget(XPushButton(tr('Success'), color=XColor.SUCCESS, variant=XButtonVariant.SOLID))
        theme_layout.addWidget(XPushButton(tr('Warning'), color=XColor.WARNING, variant=XButtonVariant.SOLID))
        theme_layout.addWidget(XPushButton(tr('Danger'), color=XColor.DANGER, variant=XButtonVariant.SOLID))
        theme_layout.addWidget(XPushButton(tr('Secondary'), color=XColor.SECONDARY, variant=XButtonVariant.SOLID))
        theme_layout.addWidget(XPushButton(tr('Tertiary'), color=XColor.TERTIARY, variant=XButtonVariant.SOLID))

        theme_layout.addStretch()
        theme_card.addLayout(theme_layout)
        self.left_layout.addWidget(theme_card)

    def _button_layout(self):
        """按钮演示"""
        button_card = XHeaderCard(tr('Button style'))
        card_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout2 = QHBoxLayout()
        card_layout.addLayout(button_layout)
        card_layout.addLayout(button_layout2)

        button_layout.addWidget(XPushButton('SOLID', variant=XButtonVariant.SOLID))
        button_layout.addWidget(XPushButton('FILLED', variant=XButtonVariant.FILLED))
        button_layout.addWidget(XPushButton('OUTLINED', variant=XButtonVariant.OUTLINED))
        button_layout.addWidget(XPushButton('TEXT', variant=XButtonVariant.TEXT))
        button_layout.addWidget(XPushButton('LINK', variant=XButtonVariant.LINK))
        button_layout.addWidget(XPushButton(icon=IconName.CHECK))
        button_layout.addWidget(XPushButton(icon=IconName.CLOSE, color=XColor.DANGER))
        button_layout.addStretch()

        btn_loading = XPushButton(tr('Loading'))
        btn_loading.set_loading(True)
        button_layout2.addWidget(btn_loading)

        group_btn1 = XPushButtonGroup(spacing=1, vertical=False)
        fist_btn = XPushButton(tr('Last page'), icon=IconName.LEFT_ARROW)
        right_btn = XPushButton(tr('Next page'), icon=IconName.RIGHT_ARROW).set_icon_position('right')
        group_btn1.add_button(fist_btn)
        group_btn1.add_button(right_btn)
        button_layout2.addWidget(group_btn1)

        items = [
            {"text": tr("Test"), "value": "center"},
            {"text": tr("Test"), "value": "top_right"},
            {"text": tr("Test"), "value": "top_left"},
            {"text": tr("Test"), "value": "bottom_right"},
            {"text": tr("Test"), "value": "bottom_left"},
        ]

        dropdown = XPushButtonDropdown(
            text=tr('Operation'),
            menu_items=items,  # 传入数据
            variant=XButtonVariant.SOLID,
            color=XColor.PRIMARY,
            icon=IconName.TOOL
        )
        button_layout2.addWidget(dropdown)
        button_layout2.addStretch()
        button_card.addLayout(card_layout)
        self.left_layout.addWidget(button_card)

    def _notif_layout(self):
        """通知/窗口/气泡/菜单"""
        notif_card = XHeaderCard(tr('Notice/Window/Popover/Menu'))
        card_layout = QVBoxLayout()
        notif_layout = QHBoxLayout()
        menu_layout = QHBoxLayout()

        card_layout.addLayout(notif_layout)
        card_layout.addLayout(menu_layout)

        btn_notif = XPushButton(text=tr('General Notice'), icon=IconName.MESSAGE, variant=XButtonVariant.OUTLINED)
        btn_notif.clicked.connect(
            lambda: XNotif.info(tr('General Notice'), animated=True, position=XNotif.Pos.BOTTOM_RIGHT, parent=self))
        notif_layout.addWidget(btn_notif)

        btn_notif_success = XPushButton(text=tr('Success Notice'), icon=IconName.MESSAGE,
                                        variant=XButtonVariant.OUTLINED, color=XColor.SUCCESS)
        btn_notif_success.clicked.connect(
            lambda: XNotif.success(tr('Success Notice'), animated=True, position=XNotif.Pos.TOP_RIGHT, parent=self))
        notif_layout.addWidget(btn_notif_success)

        btn_notif_error = XPushButton(text=tr('Error Notice'), icon=IconName.MESSAGE, variant=XButtonVariant.OUTLINED,
                                      color=XColor.DANGER)
        btn_notif_error.clicked.connect(
            lambda: XNotif.error(tr('Error Notice'), animated=True, position=XNotif.Pos.CENTER, parent=self))
        notif_layout.addWidget(btn_notif_error)

        btn_notif_warning = XPushButton(text=tr('Warning Notice'), icon=IconName.MESSAGE,
                                        variant=XButtonVariant.OUTLINED, color=XColor.WARNING)
        btn_notif_warning.clicked.connect(
            lambda: XNotif.warning(tr('Warning Notice'), animated=True, position=XNotif.Pos.BOTTOM_LEFT, parent=self))
        notif_layout.addWidget(btn_notif_warning)

        btn_info = XPushButton(tr('Information Dialog'), icon=IconName.COMMENT, color=XColor.SUCCESS)
        menu_layout.addWidget(btn_info)
        btn_info.clicked.connect(lambda: XMessageBox.information(self, tr('Information'), tr('Information Dialog')))

        btn_ask = XPushButton(tr('Ask Dialog'), icon=IconName.COMMENT, color=XColor.SUCCESS)
        menu_layout.addWidget(btn_ask)
        btn_ask.clicked.connect(lambda: XMessageBox.ask(self, tr('Ask'), tr('Ask Dialog')))

        btn_form = XPushButton(tr('Form Dialog'), icon=IconName.COMMENT, color=XColor.SUCCESS)
        btn_form.clicked.connect(lambda: _form())
        menu_layout.addWidget(btn_form)

        def _form():
            form_layout = QFormLayout()
            form_layout.setSpacing(10)

            name_input = XLineEdit(size=XSize.SMALL, placeholder=tr("Input username"))
            email_input = XLineEdit(size=XSize.SMALL, placeholder=tr("Input email"))

            form_layout.addRow(XLabel(tr('User:')), name_input)
            form_layout.addRow(XLabel(tr('Email:')), email_input)

            def on_confirm(msg_box):
                print(f"姓名: {name_input.text()}, 邮箱: {email_input.text()}")

            XMessageBox.information(self, tr('Form Dialog'), tr('Please fill out the form below'), layout=form_layout,
                                    on_confirm=on_confirm)

        btn_menu = XPushButton('点击弹出菜单', icon=IconName.LIST, color=XColor.PRIMARY)
        menu_layout.addWidget(btn_menu)
        btn_menu.clicked.connect(lambda: _show_menu())

        def _show_menu():
            """Show basic menu 显示基本菜单"""
            menu = XMenu(tr("Menu"), self)

            menu.add_action(tr("New"), icon=XIcon(IconName.FILE_ADD).icon(), triggered=lambda: print('点击了新建'))
            menu.add_action(tr("Open"), icon=XIcon(IconName.FOLDER_ADD).icon(), triggered=lambda: print('点击了打开'))
            menu.add_action(tr("Save"), icon=XIcon(IconName.SAVE).icon(), shortcut='ctrl+s',
                            triggered=lambda: print('点击了保存'))
            menu.addSeparator()
            menu.add_action(tr("Export"), icon=XIcon(IconName.EXPORT).icon(), triggered=lambda: print('点击了导出'))
            menu.add_action(tr("Download"), icon=XIcon(IconName.DOWNLOAD).icon(), triggered=lambda: print('点击了下载'))
            menu.add_action(tr("Delete"), icon=XIcon(IconName.DELETE, color=XColor.DANGER).icon(),
                            triggered=lambda: print('点击了删除'))
            more_menu = menu.add_submenu(tr("More"), icon=XIcon(IconName.MORE).icon())
            more_menu.add_action(tr('Share'), icon=XIcon(IconName.SHARE).icon())
            more_menu.add_action(tr('Test'), icon=XIcon(IconName.EDIT).icon())

            menu.exec_at_widget(btn_menu)

        btn_popover = XPushButton(tr('Popover'), icon=IconName.MESSAGE, variant=XButtonVariant.FILLED,
                                  color=XColor.PRIMARY)
        XPopover.show_popover(btn_popover, tr('Bubble hover trigger; displayed at the top of the parent component'),
                              placement=XPopover.Placement.TOP)
        menu_layout.addWidget(btn_popover)

        notif_layout.addStretch()
        menu_layout.addStretch()
        notif_card.addLayout(card_layout)
        self.left_layout.addWidget(notif_card)

    def _badge_layout(self):
        """徽章 / 图标"""
        badge_card = XHeaderCard(tr('Badge'))
        badge_layout = QHBoxLayout()
        badge_layout.setSpacing(20)
        texts = ["1", "99", tr("Hot"), tr('Sale'), tr('Free')]
        self.text_buttons = []
        for text in texts:
            btn = XPushButton(text)
            self.text_buttons.append(btn)
            badge_layout.addWidget(btn)

        self.dot_btn = XPushButton(text=tr('Messages'), variant=XButtonVariant.SOLID, color=XColor.SECONDARY)
        badge_layout.addWidget(self.dot_btn)

        badge_layout.addStretch()
        badge_card.addLayout(badge_layout)
        self.left_layout.addWidget(badge_card)

        self.timer.singleShot(100, self._create_badges)

    def _create_badges(self):
        """创建徽章"""
        texts = ["1", "99", tr("Hot"), tr('Sale'), tr('Free')]
        for count, btn in enumerate(self.text_buttons):
            XTextBadge(btn, texts[count], color=XColor.DANGER)

        nav_item_widget = self.navbar.get_item('user')
        XIconBadge(self.dot_btn, icon_name=IconName.PIN_FILL, color=XColor.WARNING, size=14, offset=QPoint(-10, 10))
        XIconBadge(nav_item_widget, icon_name=IconName.DOT, color=XColor.DANGER, size=16, offset=QPoint(-5, 5))

    def _table_layout(self):
        """表格 / 分页器 / 遮罩"""
        tab_widget_capsule = XTabWidget()
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        tab1.setLayout(tab1_layout)
        tab_widget_capsule.addTab(tab1, tr("Upload"))
        upload = XUpload(
            mode=XUpload.MODE_BOTH,
            mini_height=200,
            title=tr('Drag and drop files into this area or click the upload button'),
            description=tr('Supports file restrictions, size limits, and more'),
        )
        tab1_layout.addWidget(upload)
        self.left_layout.addWidget(tab_widget_capsule)

        tab2 = QWidget()
        tab2_layout = QVBoxLayout()
        tab2.setLayout(tab2_layout)
        tab_widget_capsule.addTab(tab2, tr("Tabel"))
        self.table = XTableWidget(style=XTableWidget.Style.STRIPED)
        tab2_layout.addWidget(self.table)
        self.table.set_headers([tr('Name'), tr('Age'), tr('Job')])
        self.table.set_column_widths([100, 100, -1])

        self.pagination = XPagination(total=500, page_size=30, current_page=1)
        tab2_layout.addWidget(self.pagination)

        btn = XPushButton(str("Add data"))
        btn.clicked.connect(self._loading_mask)
        tab2_layout.addWidget(btn, alignment=Qt.AlignRight)
        QTimer.singleShot(500, self._add_table_bata)

        tab3 = QWidget()
        tab3_layout = QVBoxLayout()
        tab3.setLayout(tab3_layout)
        tab_widget_capsule.addTab(tab3, tr("List"))
        default_list = XListWidget()
        default_list.addItems([
            "选项 1：默认列表项",
            "选项 2：带边框和圆角",
            "选项 3：支持悬停效果",
            "选项 4：支持选中效果",
            "选项 5：自定义滚动条样式",
            "选项 7：支持明暗切换",
            "选项 8：继承QListWidget",
            "选项 9：QSS样式控制",
        ])
        item = QListWidgetItem('带图标的Item')
        item.setIcon(XIcon(IconName.SHARE).icon())
        default_list.addItem(item)
        tab3_layout.addWidget(default_list)

    def _loading_mask(self):
        self.loading = XLoadingMask.show_loading(self.table, text=tr("Loading"))
        self._add_table_bata()
        QTimer.singleShot(3000, lambda: self.loading.hide())

    def _add_table_bata(self):
        data = [
                   ['刘备', '26', '皇室特供草鞋编织师'],
                   ['关羽', '18', '战马销售顾问兼美髯养护'],
                   ['张飞', '18', '屠夫转行声乐教练'],

                   ['刘备', '27', '蜀汉集团创始人兼首席哭官'],
                   ['关羽', '19', '青龙偃月刀代言人'],
                   ['张飞', '19', '长板桥噪音测试员'],
               ] * 50
        self.table.setRowCount(0)

        self.table.setRowCount(len(data))
        for row, value in enumerate(data):
            for column, item in enumerate(value):
                table_item = QTableWidgetItem(item)
                self.table.setItem(row, column, table_item)

    def _check_layout(self):
        """选择器演示"""
        check_card = XHeaderCard(tr('Selector'))
        check_layout = QHBoxLayout()
        switch = XSwitch(checked=False, color=XColor.PRIMARY, text_on=tr('On'), text_off=tr('Off'))
        check_layout.addWidget(switch)
        switch.setChecked(True)
        check_layout.addWidget(XRadioButton(tr("Check"), color=XColor.PRIMARY, checked=False))
        check_layout.addWidget(XCheckBox(color=XColor.PRIMARY, text=tr("Check"), checked=False))
        check_layout.addStretch()
        check_card.addLayout(check_layout)
        self.right_layout.addWidget(check_card)

    def _progressbar_layout(self):
        """滑块 / 进度条"""
        progressbar_card = XHeaderCard(tr('Slider/ Progress'))
        progressbar_layout = QVBoxLayout()
        progressbar_layout.addWidget(XSlider(value=20, minimum=0, maximum=100))

        progressbar_h = XProgressBar(text_visible=False, value=20)
        progressbar_layout.addWidget(progressbar_h)

        progressbar_c = XCircleProgress(value=20)
        progressbar_layout.addWidget(progressbar_c, alignment=Qt.AlignCenter)

        progressbar_layout.addStretch()
        progressbar_card.addLayout(progressbar_layout)
        self.right_layout.addWidget(progressbar_card)

        self.timer.timeout.connect(lambda: update_progress(progressbar_h, progressbar_c))
        self.timer.start(500)

        def update_progress(progress_bar, circle_progress):
            """更新进度条值"""
            current_value = progress_bar.value()
            new_value = current_value + 5
            if new_value >= 100:
                progress_bar.setValue(100)
                circle_progress.setValue(100)

                self.timer.singleShot(200, lambda: progress_bar.setValue(0))
                self.timer.singleShot(200, lambda: circle_progress.setValue(0))
            else:
                progress_bar.setValue(new_value)
                circle_progress.setValue(new_value)

    def _input_layout(self):
        """输入框样式"""
        input_card = XHeaderCard(tr('Input'))
        input_layout = QVBoxLayout()
        input_layout.addWidget(XLineEdit(placeholder=tr("Input username"), prefix_icon=IconName.USER))
        input_layout.addWidget(XLineEdit(placeholder=tr("Input password"), show_password=True))

        input_layout.addWidget(XDateEdit())
        input_layout.addWidget(XTimeEdit())
        input_layout.addWidget(XDateTimeEdit())
        input_layout.addWidget(XSpinBox())
        input_layout.addWidget(XDoubleSpinBox())

        combox = XComboBox()
        combox.addItems([tr('Hamburg'), tr('French fries'), tr('Fried chicken'), tr('Coca-Cola')])
        input_layout.addWidget(combox)

        text_edit = XTextEdit(
            placeholder="请输入文本...",
            max_length=100
        )
        text_edit.append("""独立寒秋，湘江北去，橘子洲头。看万山红遍，层林尽染；漫江碧透，百舸争流。""")
        input_layout.addWidget(text_edit)

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

        code_block = XCodeBlock(code=python_code)
        input_layout.addWidget(code_block)

        input_layout.addStretch()
        input_card.addLayout(input_layout)
        self.right_layout.addWidget(input_card)

    def _on_translation(self):
        langs = XI18N.current_lang
        if langs == 'zh_CN':
            XI18N.set_language('en_US')
            print(f'当前：{langs}, 已设置为:en_US')
        else:
            XI18N.set_language("zh_CN")
            print(f'当前：{langs}, 已设置为:zh_CN')


if __name__ == '__main__':
    if sys.platform == 'win32':
        # 确保windows任务栏能正确显示图标，字符串标识符（格式：公司名.产品名.子模块.版本号）
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('mycompany.myproduct.subelement.version')
    app = QApplication(sys.argv)
    XI18N.add_custom_lang_path(r"./custom_langs", context='XSideUiDemo')
    XI18N.set_language("zh_CN")
    ui = XSideUiDemo()
    ui.show()
    sys.exit(exec_app(app))
