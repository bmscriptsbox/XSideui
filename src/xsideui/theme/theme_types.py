"""Theme type definitions
主题类型定义

This module contains shared type definitions used across the theme system.
本模块包含主题系统中使用的共享类型定义。
"""

from dataclasses import dataclass
from enum import Enum


class ThemeType(Enum):
    """Theme types
    主题类型
    """
    LIGHT = "light"
    DARK = "dark"


@dataclass
class ThemeColors:
    """Theme color configuration
    主题颜色配置
    """
    primary: str
    secondary: str
    tertiary: str
    success: str
    warning: str
    danger: str
    link: str
    text_0: str
    text_1: str
    text_2: str
    text_3: str
    text_disabled: str
    bg_0: str
    bg_1: str
    bg_2: str
    fill: str
    border: str
    shadow: str
    code_keyword: str
    code_string: str
    code_comment: str
    code_function: str
    code_number: str
    code_operator: str
    
    def with_updates(self, **updates) -> 'ThemeColors':
        """创建一个新的颜色配置，并更新指定的颜色值"""
        data = self.__dict__.copy()
        data.update(updates)
        return ThemeColors(**data)
