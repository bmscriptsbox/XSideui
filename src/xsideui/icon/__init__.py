"""XIcon Component 图标组件系统

高性能SVG图标库，支持：
- 高效渲染 (基于缓存)
- 主题感知
- 链式API
- 自定义颜色
- 尺寸变换
- 旋转/翻转
- 图标名称枚举（支持 IDE 自动补全）

Example:
    >>> # 基础使用（使用枚举）
    >>> from xsideui import XIcon
    >>> qicon = XIcon.get(IconName.SETTING, size=24).icon()

"""

from .xicon import XIcon
from .xicon_engine import XIconEngine, xicon_engine
from .xicon_cache import XIconCache, xicon_cache
from .xicon_theme import (
    XIconThemeAdapter,
    xicon_theme_adapter
)
from .icon_name import IconName





def preload_icons(
    names: list,
    sizes: list = None,
    colors: list = None,
    theme_aware: bool = True
):
    """预加载图标到缓存
    
    在使用前预加载图标，提高首次显示速度
    
    Args:
        names: 图标名称列表
        sizes: 尺寸列表 (默认 [16, 24, 32, 48])
        colors: 颜色列表
        theme_aware: 是否启用主题感知
        
    Example:
        >>> from src.icon import preload_icons
        >>> preload_icons(["add", "edit", "delete", "search"])
    """
    return XIconEngine.preload_icons(
        names,
        sizes=sizes,
        colors=colors,
    )


def clear_icon_cache():
    """清理图标缓存"""
    XIconEngine.clear_cache()


def get_icon_names() -> list:
    """获取所有已加载的图标名称"""
    return XIconEngine.get_icon_names()


def search_icons(keyword: str) -> list:
    """搜索图标
    
    通过关键词搜索图标名称
    
    Args:
        keyword: 搜索关键词
        
    Returns:
        list: 匹配的图标名称列表
        
    Example:
        >>> from src.icon import search_icons
        >>> results = search_icons("add")
        >>> # ["add", "add-c", "add-c-f", "add-o", ...]
    """
    from .xicon_engine import XIconEngine

    all_names = XIconEngine.get_icon_names()
    keyword = keyword.lower()

    return [
        name for name in all_names
        if keyword in name.lower()
    ]


def has_icon(name: str) -> bool:
    """检查图标是否存在
    
    Args:
        name: 图标名称
        
    Returns:
        bool: 图标是否存在
    """
    from .xicon_engine import XIconEngine

    svg_content = XIconEngine.load_svg(name)
    return svg_content is not None


__all__ = [
    "XIcon",
    "XIconEngine",
    "XIconCache",
    "XIconThemeAdapter",
    "xicon_cache",
    "xicon_engine",
    "xicon_theme_adapter",
    "IconName",
    "preload_icons",
    "clear_icon_cache",
    "get_icon_names",
    "search_icons",
    "has_icon",
]
