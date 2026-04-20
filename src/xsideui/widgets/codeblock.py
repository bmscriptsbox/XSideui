"""
代码块组件，带有语法高亮和主题适配。
"""
import re
from ..utils.qt_compat import QFont, QSyntaxHighlighter, QTextCharFormat, QColor, QPlainTextEdit, Qt
from ..theme import theme_manager


class XCodeBlock(QPlainTextEdit):
    """代码块组件，支持语法高亮和主题适配"""

    def __init__(self, code: str = "", language: str = "python", parent=None):
        """初始化代码块。

            Args:
                code: 初始显示的代码文本。
                language: 编程语言类型（如 'python', 'cpp', 'javascript'），用于匹配高亮规则。
                parent: 父级组件。
            """
        super().__init__(parent)
        self.setObjectName("xcodeblock")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._language = language
        self.setReadOnly(True)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setPlainText(code)
        self.setFont(self._get_code_font())
        self.highlighter = PythonHighlighter(self.document())


    def _get_code_font(self):
        """获取代码字体"""
        font = QFont()
        font.setFamilies([
            "JetBrains Mono",
            "Fira Code",
            "Source Code Pro",
            "Cascadia Code",
            "Monaco",
            "Consolas"
        ])
        font.setPointSize(10)
        return font


    def add_code(self, code: str):
        """添加代码到代码块"""
        self.clear_code()
        self.appendPlainText(code)
        return self

    def clear_code(self):
        """清除代码块中的代码"""
        self.setPlainText("")
        return self

    def set_language(self, language: str):
        """设置编程语言"""
        self._language = language
        self.highlighter = PythonHighlighter(self.document())


class PythonHighlighter(QSyntaxHighlighter):
    """Python 语法高亮器，支持明暗主题"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []
        theme_manager.theme_changed.connect(self._update_formats)
        self._setup_formats()

    def _setup_formats(self):
        """设置语法高亮格式"""
        colors = theme_manager.colors

        self.colors = {
            "keyword": QColor(colors.code_keyword),
            "string": QColor(colors.code_string),
            "comment": QColor(colors.code_comment),
            "function": QColor(colors.code_function),
            "number": QColor(colors.code_number),
            "operator": QColor(colors.code_operator),
        }

        self.highlighting_rules.clear()

        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'False', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'None',
            'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'True',
            'try', 'while', 'with', 'yield', 'const'
        ]
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(self.colors["keyword"])
        for word in keywords:
            pattern = f'\\b{word}\\b'
            self.highlighting_rules.append((re.compile(pattern), keyword_format))

        string_format = QTextCharFormat()
        string_format.setForeground(self.colors["string"])
        self.highlighting_rules.extend([
            (re.compile('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'), string_format),
            (re.compile("'[^'\\\\]*(\\\\.[^'\\\\]*)*'"), string_format),
        ])

        comment_format = QTextCharFormat()
        comment_format.setForeground(self.colors["comment"])
        self.highlighting_rules.append((re.compile('#.*'), comment_format))

        function_format = QTextCharFormat()
        function_format.setForeground(self.colors["function"])
        self.highlighting_rules.append((re.compile('\\b[A-Za-z0-9_]+(?=\\()'), function_format))

        number_format = QTextCharFormat()
        number_format.setForeground(self.colors["number"])
        self.highlighting_rules.append((re.compile('\\b\\d+\\b'), number_format))

        operator_format = QTextCharFormat()
        operator_format.setForeground(self.colors["operator"])
        operators = ['=', '==', '!=', '<', '<=', '>', '>=', '\\+', '-', '\\*', '/', '//', '%', '\\*\\*', '\\+=', '-=',
                     '\\*=', '/=', '%=', '\\^', '\\|', '\\&', '\\~', '>>', '<<']
        for op in operators:
            pattern = re.compile(re.escape(op))
            self.highlighting_rules.append((pattern, operator_format))

        self.rehighlight()

    def _update_formats(self, theme_name):
        """主题变化时更新格式"""
        self._setup_formats()

    def highlightBlock(self, text):
        """对当前文本块应用高亮规则"""
        for pattern, format in self.highlighting_rules:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), format)
