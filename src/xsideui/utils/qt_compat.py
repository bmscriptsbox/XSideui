"""Qt 兼容模块

处理 PySide2 和 PySide6 的兼容性
"""

import sys
import importlib

# 尝试导入 PySide6，如果失败则导入 PySide2
try:
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    from PySide6.QtSvg import *
    QT_VERSION = 6
    QT_MODULE = "PySide6"
except ImportError:
    try:
        from PySide2.QtCore import *
        from PySide2.QtGui import *
        from PySide2.QtWidgets import *
        from PySide2.QtSvg import *
        QT_VERSION = 2
        QT_MODULE = "PySide2"
    except ImportError:
        raise ImportError("Neither PySide6 nor PySide2 is installed")

# 导入 QEvent 用于事件类型判断
if QT_VERSION == 6:
    from PySide6.QtCore import QEvent
else:
    from PySide2.QtCore import QEvent


def safe_translate(context: str, text: str) -> str:
    """跨版本兼容的翻译函数"""
    try:
        # 尝试标准调用 (PySide6)
        res = QCoreApplication.translate(context, text)
    except TypeError:
        # 回退到字节调用 (PySide2)
        res = QCoreApplication.translate(context.encode('utf-8'), text.encode('utf-8'))

    # 统一确保返回 str
    if isinstance(res, (bytes, bytearray)):
        return res.decode('utf-8')
    return res







def get_qt_module():
    """获取当前使用的 Qt 模块"""
    return QT_MODULE


def exec_app(app):
    """兼容 PySide2 和 PySide6 的应用程序执行方法
    
    Args:
        app: QApplication 实例
    """
    if hasattr(app, 'exec'):
        return app.exec()
    return app.exec_()

def get_text_width(font_metrics, text: str) -> int:
    """获取文本宽度（兼容 PySide2 和 PySide6）"""
    if hasattr(font_metrics, 'horizontalAdvance'):
        return font_metrics.horizontalAdvance(text)
    return font_metrics.width(text)



class FontHelper:
    @staticmethod
    def set_weight(font: QFont, weight: int):
        """兼容 PySide2 和 PySide6 的字重设置"""
        try:
            # PySide6 强制要求枚举
            if hasattr(QFont, "Weight") and isinstance(QFont.Weight, type(QFont.Weight)):
                font.setWeight(QFont.Weight(weight))
            else:
                # 某些老版本环境处理
                font.setWeight(weight)
        except (TypeError, AttributeError):
            # 兜底 PySide2，直接传 int
            font.setWeight(weight)


def set_selection_rect_visible(widget, visible: bool):
    """兼容 PySide2 和 PySide6 的选择矩形可见性设置

    Args:
        widget: QAbstractItemView 子类实例
        visible: 是否显示选择矩形
    """
    if hasattr(widget, 'setSelectionRectVisible'):
        # PySide6
        widget.setSelectionRectVisible(visible)
    # PySide2 不支持此方法，静默忽略

# 获取所有导入的名称
_locals = locals()
__all__ = [name for name in _locals if not name.startswith('_')]
__all__.extend(['QT_VERSION', 'QT_MODULE', 'get_qt_module', 'set_font_families', 'set_font_weight', 'exec_app'])
