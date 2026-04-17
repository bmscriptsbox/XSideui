
from pathlib import Path
from typing import List, Optional, Dict

from ..utils.qt_compat import (
    QObject, QTranslator, QCoreApplication,
    QEvent, QLibraryInfo, Signal
)




def tr(text: str) -> str:
    """
    仅用于静态标记，不执行实际翻译。
    作用：让 lupdate 能够提取到这个字符串，但在运行时它原样返回。
    """
    return text

class I18nManager(QObject):
    """
    国际化管理器（单例模式）

    职责：
    1. 管理和加载 .qm 翻译文件（包括组件库、Qt 标准库、用户自定义库）。
    2. 提供全局语言切换接口。
    3. 维护自定义翻译路径和上下文（Context）映射。
    4. 触发全局 UI 刷新事件。
    """

    _instance = None
    _initialized = False

    # 当语言改变时发送此信号 (可选，供非 Widget 类逻辑使用)
    language_changed = Signal(str)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(I18nManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if I18nManager._initialized:
            return
        super().__init__()

        # 核心翻译器
        self.app_translator = QTranslator()  # 组件库翻译器
        self.qt_translator = QTranslator()  # Qt 官方翻译器
        self.custom_translators: List[QTranslator] = []  # 自定义翻译器池

        self.current_lang = "zh_CN"

        # 默认语言文件存放路径 (假设在当前文件的 custom_langs 目录下)
        self.base_lang_path = Path(__file__).parent / "custom_langs"

        # 存储自定义路径: [{"path": str, "context": str}, ...]
        self._custom_paths = []

        I18nManager._initialized = True

    def x_tr(self, text: str, context: str = None, args: list = None) -> str:
        """
        智能翻译函数 (支持占位符填充)

        :param text: 翻译键 (Key)，如 "Export %1 Download"
        :param context: 翻译上下文
        :param args: 占位符填充值列表，按顺序对应 %1, %2...
        """

        # 1. 构造搜索链
        search_chain = []
        if context:
            search_chain.append(str(context))

        for info in self.custom_lang_paths:
            ctx = info.get("context")
            if ctx and ctx not in search_chain:
                search_chain.append(ctx)

        if "XSideUI" not in search_chain:
            search_chain.append("XSideUI")

        # 2. 依次执行翻译尝试
        translated_text = text
        for ctx in search_chain:
            try:
                res = QCoreApplication.translate(ctx, text)
            except TypeError:
                res = QCoreApplication.translate(ctx.encode('utf-8'), text.encode('utf-8'))

            if isinstance(res, (bytes, bytearray)):
                res = res.decode('utf-8')

            # 只要翻译结果和原文不等，说明找到了！
            if res != text:
                translated_text = res
                break

        # 3. 核心改进：处理 args 填充
        # 即使翻译失败返回了原文，也要尝试填充占位符
        if args:
            print(f"[Args Processing]: Replacing with {args}")
            for i, val in enumerate(args):
                # 将 %1, %2 ... 替换为 args 列表中的内容
                placeholder = f"%{i + 1}"
                translated_text = translated_text.replace(placeholder, str(val))
        return translated_text



    def _get_storage(self) -> List[Dict]:
        """获取存储自定义路径的列表，确保跨模块单例数据同步"""
        app = QCoreApplication.instance()
        if not app:
            return self._custom_paths
        if not hasattr(app, "_global_i18n_paths"):
            app._global_i18n_paths = self._custom_paths
        return app._global_i18n_paths

    def add_custom_lang_path(self, dir_path: str, context: str = "Global") -> bool:
        """
        注册外部翻译目录
        :param dir_path: 存放 .qm 文件的文件夹
        :param context: 翻译所属的上下文
        """
        path_obj = Path(dir_path)
        if not path_obj.is_dir():
            return False

        storage = self._get_storage()
        path_info = {"path": str(dir_path), "context": context}

        if path_info not in storage:
            storage.append(path_info)
            # 立即尝试加载当前语言对应的自定义翻译
            self._load_custom_translators(self.current_lang)
            self.refresh_ui()
            return True
        return False

    def _load_custom_translators(self, lang_code: str):
        """加载所有已注册路径下的指定语言文件"""
        app = QCoreApplication.instance()
        if not app:
            return

        # 卸载旧的自定义翻译器
        for t in self.custom_translators:
            app.removeTranslator(t)
        self.custom_translators.clear()

        # 遍历注册路径加载新的
        for info in self._get_storage():
            qm_file = Path(info["path"]) / f"{lang_code}.qm"
            if qm_file.exists():
                t = QTranslator()
                if t.load(str(qm_file)):
                    app.installTranslator(t)
                    self.custom_translators.append(t)

    def set_language(self, lang_code: str) -> bool:
        """
        切换全局语言
        :param lang_code: 如 'zh_CN', 'en_US'
        """
        app = QCoreApplication.instance()
        if not app:
            return False

        self.current_lang = lang_code

        # 1. 加载组件库自身翻译
        lib_qm = self.base_lang_path / f"{lang_code}.qm"
        app.removeTranslator(self.app_translator)
        if lib_qm.exists():
            if self.app_translator.load(str(lib_qm)):
                app.installTranslator(self.app_translator)

        # 2. 加载 Qt 标准对话框等翻译
        app.removeTranslator(self.qt_translator)
        # 兼容 Qt5/Qt6 获取路径的方法
        func = getattr(QLibraryInfo, 'path', getattr(QLibraryInfo, 'location', None))
        qt_trans_path = func(QLibraryInfo.TranslationsPath)

        for name in [f"qt_{lang_code}", f"qtbase_{lang_code}"]:
            if self.qt_translator.load(name, qt_trans_path):
                app.installTranslator(self.qt_translator)
                break

        # 3. 加载第三方自定义翻译
        self._load_custom_translators(lang_code)

        # 4. 触发全局刷新
        self.refresh_ui()
        self.language_changed.emit(lang_code)
        return True

    def refresh_ui(self):
        """
        核心通知机制：发送 LanguageChange 事件
        Qt 所有的 Widget 收到此事件后，如果重写了 changeEvent，就会触发刷新
        """
        app = QCoreApplication.instance()
        if app:
            QCoreApplication.sendEvent(app, QEvent(QEvent.LanguageChange))

    @property
    def custom_lang_paths(self):
        return self._get_storage()


# 全局单例对象
XI18N = I18nManager()