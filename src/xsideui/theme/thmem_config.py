from dataclasses import dataclass
from typing import Dict

from .theme_types import ThemeColors, ThemeType


@dataclass
class ThemeConfig:
    """主题配置

    使用组合模式，将主题名称、显示名称和颜色配置组合在一起
    """
    name: str
    display_name: str
    colors: ThemeColors
    theme_type: ThemeType = ThemeType.LIGHT
    fonts: Dict[str, str] = None
    spacing: Dict[str, str] = None
    height: Dict[str, str] = None
    border_radius: Dict[str, str] = None
    border_width: Dict[str, str] = None
    opacity: Dict[str, str] = None
    shadow: Dict[str, str] = None
    radio: Dict[str, Dict[str, int]] = None
    checkbox: Dict[str, Dict[str, int]] = None
    switch: Dict[str, Dict[str, int]] = None

    def __post_init__(self):
        """初始化后处理，确保所有配置都有默认值"""
        if self.fonts is None:
            self.fonts = {}
        if self.spacing is None:
            self.spacing = {}
        if self.height is None:
            self.height = {}
        if self.border_radius is None:
            self.border_radius = {}
        if self.border_width is None:
            self.border_width = {}
        if self.opacity is None:
            self.opacity = {}
        if self.shadow is None:
            self.shadow = {}
        if self.radio is None:
            self.radio = {}
        if self.checkbox is None:
            self.checkbox = {}
        if self.switch is None:
            self.switch = {}

    def with_primary_color(self, primary_color: str) -> 'ThemeConfig':
        """创建一个新的主题配置，使用指定的主题色"""
        new_colors = self.colors.with_updates(primary=primary_color)
        return ThemeConfig(
            name=self.name,
            display_name=self.display_name,
            colors=new_colors,
            theme_type=self.theme_type,
            fonts=self.fonts,
            spacing=self.spacing,
            height=self.height,
            border_radius=self.border_radius,
            border_width=self.border_width,
            opacity=self.opacity,
            shadow=self.shadow,
            radio=self.radio,
            checkbox=self.checkbox,
            switch=self.switch
        )

