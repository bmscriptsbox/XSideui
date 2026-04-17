from typing import Union, Optional, List
from ..utils.qt_compat import QPixmap, QIcon
from .icon_name import IconName
from .xicon_engine import XIconEngine
from .xicon_theme import XIconThemeAdapter
from .xicon_theme import xicon_theme_adapter
from ..xenum import XColor, XSize


def _resolve_name(name: Union[str, IconName, None]) -> Optional[str]:
    """解析图标名称
    
    Args:
        name: 图标名称（IconName 枚举或字符串）
        
    Returns:
        图标名称字符串
    """
    if name is None:
        return None
    if hasattr(name, 'value'):
        return str(name.value)
    name_str = str(name)
    if "." in name_str and "IconName" in name_str:
        return name_str.split(".")[-1].lower()
    return name_str


class XIcon:
    """轻量级图标管理类
    
    用于创建和管理SVG图标，支持：
    - 尺寸自定义
    - 颜色自定义
    - 主题感知
    - 变换支持（旋转、翻转）
    - 链式调用
    - 多DPR支持（自动适应不同缩放比例）
    
    Features:
        - 高效渲染 (基于缓存)
        - 主题集成
        - 链式API
        - 多种尺寸支持
        - 自定义颜色
        - 多DPR自动适应
    """

    _default_size = 24
    _default_color = None
    _pool = {}

    def __init__(
        self,
        name: Union[str, IconName] = None,
        size: Union[int, XSize] = None,
        color: Union[str, XColor] = XColor.SECONDARY,
        theme_aware: bool = True,
        rotation: float = 0,
        flip_h: bool = False,
        flip_v: bool = False
    ):
        """
        Args:
            name: 图标名称 (如 IconName.ADD, "add", "user", "settings")
            size: 图标尺寸 (int, XSize 枚举)
            color: 图标颜色 (XColor 枚举, "#165dff", "primary", "success")
            theme_aware: 是否启用主题感知
            rotation:旋转角度 (0-360)
            flip_h: 水平翻转
            flip_v: 垂直翻转
        """
        self._name = self._resolve_name(name)
        self._size = self._default_size

        self._theme_aware = theme_aware
        if self._theme_aware and XIconThemeAdapter._instance is not None:
            XIconThemeAdapter._instance.theme_changed.connect(self._on_theme_changed)
        self._color = self._resolve_color(color)
        self._raw_color = color  # 新增：记录原始颜色（如 XColor.SUCCESS）
        self._rotation = rotation
        self._flip_h = flip_h
        self._flip_v = flip_v
        self._qicon = None

        if size is not None:
            self.set_size(size)

    @classmethod
    def add_resource_path(cls, prefix: str):
        """
        向图标系统添加自定义资源搜索路径

        Args:
            prefix: 资源前缀，例如 ":/custom/"
        """
        # 调用引擎执行底层注册
        XIconEngine.register_resource_package(prefix)

        # 清理 XIcon 的实例对象池
        cls._pool.clear()


    @classmethod
    def get(cls, name: Union[str, IconName], size=24, color=XColor.PRIMARY) -> 'XIcon':
        """
        获取图标实例的快捷方式（带内部缓存）
        """
        # 生成 key，注意：如果 color 是枚举，确保它也能被 hash
        key = (str(name), size, color)

        if key not in cls._pool:
            cls._pool[key] = cls(name, size, color)

        return cls._pool[key]

    def _resolve_name(self, name: Union[str, IconName, None]) -> Optional[str]:
        """解析图标名称
        
        Args:
            name: 图标名称（IconName 枚举或字符串）
            
        Returns:
            图标名称字符串
        """
        if name is None:
            return None
        if hasattr(name, 'value'):
            val = str(name.value)
            return val
        name_str = str(name)
        if "." in name_str and "IconName" in name_str:
            return name_str.split(".")[-1].lower()

        return name_str



    def _resolve_color(self, color: Union[str, XColor, None]) -> Optional[str]:
        """解析颜色值
        
        Args:
            color: 颜色值（XColor 枚举或字符串）
            
        Returns:
            颜色字符串
        """
        return xicon_theme_adapter.resolve_color(color, self._theme_aware)

    def _resolve_size(self, size: Union[int, XSize]) -> int:
        """解析尺寸值
        
        Args:
            size: 尺寸值（XSize 枚举或整数）
            
        Returns:
            尺寸整数值
        """
        if isinstance(size, XSize):
            size_map = {
                XSize.MINI: 12,
                XSize.SMALL: 16,
                XSize.DEFAULT: 24,
                XSize.LARGE: 32
            }
            return size_map.get(size, 24)
        
        return int(size)

    def _on_theme_changed(self, theme: str):
        """主题切换回调
        
        Args:
            theme: 新的主题标识符
        """
        if hasattr(self, '_raw_color'):
            self._color = self._resolve_color(self._raw_color)
        else:
            # 如果你没有保存 raw_color，建议在 __init__ 里存一份
            pass
        self._qicon = None

    def icon(self, dpr_values: List[float] = None) -> Optional[QIcon]:
        """转换为QIcon，支持多DPR
        
        Qt会根据当前DPR自动选择最合适的尺寸
        
        Args:
            dpr_values: DPR值列表，默认 [1.0, 1.25, 1.5, 1.75, 2.0]
            
        Returns:
            包含多个DPR尺寸的QIcon
        """
        if not self._name:
            return None

        if self._qicon is None:
            self._qicon = XIconEngine.create_multisize_icon(
                self._name,
                self._size,
                self._color,
                dpr_values
            )

        return self._qicon

    def pixmap(self, dpr: float = 1.0) -> Optional[QPixmap]:
        """转换为指定DPR的QPixmap
        
        Args:
            dpr: 设备像素比（Device Pixel Ratio）
            
        Returns:
            指定DPR的QPixmap
        """
        if not self._name:
            return None

        return XIconEngine.create_pixmap(
            self._name,
            self._size,
            self._color,
            self._rotation,
            self._flip_h,
            self._flip_v,
            dpr
        )

    def set_name(self, name: Union[str, IconName]):
        """设置图标名称"""
        resolved_name = self._resolve_name(name)
        if self._name != resolved_name:
            self._name = resolved_name
            self._qicon = None

    def set_size(self, size: Union[int, XSize]):
        """设置图标尺寸"""
        resolved_size = self._resolve_size(size)
        if self._size != resolved_size:
            self._size = resolved_size
            self._qicon = None

    def set_color(self, color: Union[str, XColor]):
        """设置图标颜色"""
        resolved_color = self._resolve_color(color)
        if self._color != resolved_color:
            self._color = resolved_color
            self._qicon = None

    def set_theme_aware(self, enabled: bool):
        """设置是否启用主题感知"""
        if self._theme_aware == enabled:
            return

        adapter = XIconThemeAdapter._instance
        if adapter is None:
            self._theme_aware = enabled
            return

        self._theme_aware = enabled

        if enabled:
            try:
                adapter.theme_changed.disconnect(self._on_theme_changed)
            except (TypeError, RuntimeError):
                pass
            adapter.theme_changed.connect(self._on_theme_changed)
        else:
            try:
                adapter.theme_changed.disconnect(self._on_theme_changed)
            except (TypeError, RuntimeError):
                pass

        self._qicon = None

    def set_rotation(self, rotation: float):
        """设置旋转角度"""
        if self._rotation != rotation:
            self._rotation = rotation
            self._qicon = None

    def set_flip_h(self, flip: bool):
        """设置水平翻转"""
        if self._flip_h != flip:
            self._flip_h = flip
            self._qicon = None

    def set_flip_v(self, flip: bool):
        """设置垂直翻转"""
        if self._flip_v != flip:
            self._flip_v = flip
            self._qicon = None

    def reset(self):
        """重置为默认状态"""
        self._name = None
        self._size = self._default_size
        self._color = self._default_color
        self._theme_aware = True
        self._rotation = 0
        self._flip_h = False
        self._flip_v = False
        self._qicon = None

    def name(self) -> Optional[str]:
        """获取图标名称"""
        return self._name

    def size(self) -> int:
        """获取图标尺寸"""
        return self._size

    def color(self) -> Optional[str]:
        """获取图标颜色"""
        return self._color

    def is_theme_aware(self) -> bool:
        """是否启用主题感知"""
        return self._theme_aware

    def rotation(self) -> float:
        """获取旋转角度"""
        return self._rotation

    def is_flipped_h(self) -> bool:
        """是否水平翻转"""
        return self._flip_h

    def is_flipped_v(self) -> bool:
        """是否垂直翻转"""
        return self._flip_v

    def is_valid(self) -> bool:
        """图标是否有效"""
        return bool(self._name)

    def to_svg_bytes(self, color: Union[str, XColor] = None) -> bytes:
        """导出为SVG字节数据"""
        if not self._name:
            return b""

        resolved_color = self._resolve_color(color) if color is not None else self._color
        resolved_color = resolved_color or "#000000"

        svg_content = XIconEngine.load_svg(self._name)
        if svg_content:
            return XIconEngine.svg_to_bytes(
                svg_content,
                self._size,
                resolved_color
            )

        return b""

    def with_name(self, name: Union[str, IconName]):
        """链式设置图标名称"""
        self.set_name(name)
        return self

    def with_size(self, size: Union[int, XSize]):
        """链式设置图标尺寸"""
        self.set_size(size)
        return self

    def with_color(self, color: Union[str, XColor]):
        """链式设置图标颜色"""
        self.set_color(color)
        return self

    def with_theme_aware(self, enabled: bool):
        """链式设置主题感知"""
        self.set_theme_aware(enabled)
        return self

    def with_rotate(self, degrees: float):
        """链式设置旋转角度"""
        self.set_rotation(degrees)
        return self

    def with_flip_h(self, flip: bool = True):
        """链式设置水平翻转"""
        self.set_flip_h(flip)
        return self

    def with_flip_v(self, flip: bool = True):
        """链式设置垂直翻转"""
        self.set_flip_v(flip)
        return self

    def with_primary(self):
        """链式设置为主题色"""
        self.set_color(XColor.PRIMARY)
        return self

    def with_success(self):
        """链式设置为成功色"""
        self.set_color(XColor.SUCCESS)
        return self

    def with_warning(self):
        """链式设置为警告色"""
        self.set_color(XColor.WARNING)
        return self

    def with_danger(self):
        """链式设置为危险色"""
        self.set_color(XColor.DANGER)
        return self

    def with_secondary(self):
        """链式设置为次要色"""
        self.set_color(XColor.SECONDARY)
        return self

    def with_mini(self):
        """链式设置为最小尺寸"""
        self.set_size(XSize.MINI)
        return self

    def with_small(self):
        """链式设置为小尺寸"""
        self.set_size(XSize.SMALL)
        return self

    def with_large(self):
        """链式设置为大尺寸"""
        self.set_size(XSize.LARGE)
        return self

    def with_default(self):
        """链式设置为默认尺寸"""
        self.set_size(XSize.DEFAULT)
        return self


