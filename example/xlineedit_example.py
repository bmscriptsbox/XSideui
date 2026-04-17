"""
XLineEdit 组件示例
模拟日常开发场景，展示输入框组件的各种功能
"""

import sys


try:
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QFormLayout, QMessageBox, QWidget
except ImportError:
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QFormLayout, QMessageBox, QWidget

from src.xsideui import XIcon, IconName, XSize, XHeaderCard, XColor
from src.xsideui import XWidget, XLabel, XLineEdit, XPushButton, XInputStatus, XNotif, XI18N


class XLineeditDemo(XWidget):
    def __init__(self):
        super(XLineeditDemo, self).__init__()
        self._users = {}  # 模拟用户数据库
        self._init_ui()

    def _init_ui(self):
        self.set_title("XLineEdit Demo")
        self.resize(400, 600)
        content_widget = QWidget()
        self.addWidget(content_widget)

        self.layout = QVBoxLayout(content_widget)
        self.layout.setContentsMargins(12,12,12,12)
        self.layout.setSpacing(15)

        self._register_card()
        self._login_card()
        self.layout.addStretch()



    def _login_card(self):
        """登录场景"""
        login_card = XHeaderCard('用户登录')
        self.layout.addWidget(login_card)

        login_form_layout = QFormLayout()
        login_form_layout.setSpacing(12)
        login_form_layout.setHorizontalSpacing(15)

        self.login_username = XLineEdit(
            prefix_icon=IconName.USER,
        )
        self.login_username.setStyleSheet("border-color:transparent")
        self.login_username.setPlaceholderText('Primary')
        self.login_username.textEdited.connect(lambda: self.login_username.set_status(None))

        self.login_password = XLineEdit(
            placeholder="请输入密码",
            show_password=True,
            prefix_icon=IconName.LOCK)
        self.login_password.textEdited.connect(lambda: self.login_password.set_status(None))

        self.btn_login = XPushButton(text='登 录', size=XSize.SMALL, color=XColor.SUCCESS)

        login_form_layout.addRow(XLabel('用户名：'), self.login_username)
        login_form_layout.addRow(XLabel('密码：'), self.login_password)
        login_form_layout.addRow(None, self.btn_login)

        login_card.addLayout(login_form_layout)
        self.btn_login.clicked.connect(self._handle_login)

    def _register_card(self):
        """注册场景"""
        register_card = XHeaderCard('用户注册')
        self.layout.addWidget(register_card)

        register_form_layout = QFormLayout()
        register_form_layout.setSpacing(12)

        self.nickname = XLineEdit(placeholder="请输入昵称", size=XSize.DEFAULT)
        self.nickname.textEdited.connect(lambda: self.nickname.set_status(None))

        self.email = XLineEdit(placeholder="请输入邮箱", size=XSize.DEFAULT)
        self.email.textEdited.connect(lambda: self.email.set_status(None))

        self.pwd = XLineEdit(placeholder="请输入密码", size=XSize.DEFAULT, show_password=True)
        self.pwd.textEdited.connect(lambda: self.pwd.set_status(None))

        self.confirm_pwd = XLineEdit(placeholder="请再次输入密码", size=XSize.DEFAULT, show_password=True)
        self.confirm_pwd.textEdited.connect(lambda: self.confirm_pwd.set_status(None))
        self.register_btn = XPushButton(text="注 册", size=XSize.SMALL, color=XColor.SUCCESS)

        register_form_layout.addRow(XLabel('昵称：'), self.nickname)
        register_form_layout.addRow(XLabel('邮箱：'), self.email)
        register_form_layout.addRow(XLabel('密码：'), self.pwd)
        register_form_layout.addRow(XLabel('确认密码：'), self.confirm_pwd)
        register_form_layout.addRow(None, self.register_btn)

        register_card.addLayout(register_form_layout)
        self.register_btn.clicked.connect(self._handle_register)

    def _handle_login(self):
        """处理登录"""
        username = self.login_username.text().strip()
        password = self.login_password.text()

        if not username:
            self.login_username.set_status(XInputStatus.ERROR)
            XNotif.warning('请输入用户名')
            return

        if not password:
            self.login_password.set_status(XInputStatus.ERROR)
            XNotif.warning('请输入密码')
            return

        # 模拟后端验证
        user = self._users.get(username)
        if not user:
            self.login_username.set_status(XInputStatus.ERROR)
            XNotif.warning('用户不存在，请先注册')
            return

        if user['password'] != password:
            self.login_password.set_status(XInputStatus.ERROR)
            XNotif.warning('密码错误')
            return

        self.login_username.set_status(XInputStatus.SUCCESS)
        self.login_password.set_status(XInputStatus.SUCCESS)
        XNotif.success('登录成功')


    def _handle_register(self):
        """处理注册"""
        nickname = self.nickname.text().strip()
        email = self.email.text().strip()
        pwd = self.pwd.text()
        confirm_pwd = self.confirm_pwd.text()

        # 验证昵称
        if not nickname:
            self.nickname.set_status(XInputStatus.ERROR)
            XNotif.warning('请输入昵称')
            return

        # 验证邮箱格式
        if not email:
            self.email.set_status(XInputStatus.ERROR)
            XNotif.warning('请输入邮箱')
            return
        if '@' not in email or '.' not in email:
            self.email.set_status(XInputStatus.ERROR)
            XNotif.warning('邮箱格式不正确')
            return

        # 检查邮箱是否已注册
        for user in self._users.values():
            if user['email'] == email:
                self.email.set_status(XInputStatus.ERROR)
                XNotif.warning('该邮箱已被注册')
                return

        # 验证密码
        if not pwd:
            self.pwd.set_status(XInputStatus.ERROR)
            XNotif.warning('请输入密码')
            return

        if len(pwd) < 6:
            self.pwd.set_status(XInputStatus.ERROR)
            XNotif.warning('密码长度至少6位')
            return

        # 验证确认密码
        if not confirm_pwd:
            self.confirm_pwd.set_status(XInputStatus.ERROR)
            XNotif.warning('请再次输入密码')
            return

        if pwd != confirm_pwd:
            self.pwd.set_status(XInputStatus.ERROR)
            self.confirm_pwd.set_status(XInputStatus.ERROR)
            XNotif.warning('两次密码不一致')
            return

        # 保存用户到模拟数据库
        self._users[nickname] = {
            'nickname': nickname,
            'email': email,
            'password': pwd
        }

        # 清空表单
        self.nickname.clear()
        self.email.clear()
        self.pwd.clear()
        self.confirm_pwd.clear()
        self.nickname.set_status(None)
        self.email.set_status(None)
        self.pwd.set_status(None)
        self.confirm_pwd.set_status(None)
        XNotif.success('注册成功')



if __name__ == "__main__":
    app = QApplication(sys.argv)
    XI18N.set_language("zh_CN")
    demo = XLineeditDemo()
    demo.show()
    sys.exit(app.exec_())
