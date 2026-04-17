import threading
from typing import Dict, Union
from ..utils.qt_compat import Signal, QObject
from .xicon_cache import xicon_cache
from ..theme import theme_manager
from ..xenum import XColor


class XIconThemeAdapter(QObject):
    """图标主题适配器
    
    与全局主题系统集成，提供：
    - 自动主题切换
    - 主题颜色映射
    - 批量更新通知
    - 统一颜色解析
    
    Features:
        - 信号通知
        - 缓存清理
        - 从 theme_manager 获取颜色
        - 统一颜色解析接口
    """

    theme_changed = Signal(str)
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init()
        return cls._instance



    def _init(self):
        self._current_theme = "light"
        self._connected = False
        self.connect_to_theme_manager()

    def resolve_color(self, color: Union[str, XColor], theme_aware: bool = True) -> str:
        """统一颜色解析
        
        将各种形式的颜色值统一解析为实际颜色值：
        - XColor 枚举（如 XColor.PRIMARY）→ 主题色值
        - 主题色名称（如 "primary"）→ 主题色值
        - 具体颜色值（如 "#165dff"）→ 直接返回
        
        Args:
            color: 颜色值（XColor 枚举、主题色名称或具体颜色值）
            theme_aware: 是否启用主题感知
            
        Returns:
            解析后的颜色值（如 "#165dff"）
        """
        if not color:
            return ""

        # 解析 XColor 枚举
        if hasattr(color, 'value'):
            color = str(color.value)
        else:
            color = str(color)

        # 如果不启用主题感知，直接返回
        if not theme_aware:
            return color

        # 检查是否是主题色名称
        theme_colors = ["primary", "secondary", "tertiary", "success", "warning", "danger"]
        if color.lower() in theme_colors:
            return self.get_theme_color(color.lower())
        return color

    def get_color(
        self,
        role,
        theme: str = None
    ) -> str:
        """获取图标颜色
        
        Args:
            role: 颜色角色 (XColor 枚举或字符串)
            theme: 指定主题，不指定则使用当前主题
            
        Returns:
            颜色值 (如 "#165dff")
        """
        try:
            if theme is None:
                theme = theme_manager.theme_name
            theme_config = theme_manager.registry.get_theme(theme)
            if theme_config is None:
                return ""

            color_attr = role.value if hasattr(role, 'value') else str(role)
            return getattr(theme_config.colors, color_attr, "")
        except Exception:
            return ""

    def get_theme_color(self, color_name: str, theme: str = None) -> str:
        """获取主题中的指定颜色"""
        try:
            if theme is None:
                theme = theme_manager.theme_name

            theme_config = theme_manager.registry.get_theme(theme)
            if theme_config is None:
                return ""

            return getattr(theme_config.colors, color_name, "")
        except Exception:
            return ""

    def _on_theme_changed(self, theme: str):
        """主题切换时的回调"""
        self._current_theme = theme
        xicon_cache.set_theme(theme)
        self.theme_changed.emit(theme)

    def connect_to_theme_manager(self):
        """连接到全局主题管理器"""
        theme_manager.theme_changed.connect(self._on_theme_changed)


    def get_stats(self) -> Dict:
        """获取适配器状态"""
        return {
            "current_theme": self._current_theme,
            "connected": self._connected,
        }


xicon_theme_adapter = XIconThemeAdapter()
