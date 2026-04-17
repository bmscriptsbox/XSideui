from enum import Enum


class XColor(Enum):
    """Color enumeration 颜色枚举"""
    PRIMARY = "primary"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"
    TERTIARY = "tertiary"
    SECONDARY = "secondary"



class XSize(Enum):
    """Size enumeration 尺寸枚举"""
    LARGE = "large"
    DEFAULT = "default"
    SMALL = "small"
    MINI = "mini"


class XInputStatus(Enum):
    """Input status enumeration 输入框状态枚举"""
    ERROR = "error"
    SUCCESS = "success"


class XButtonVariant(Enum):
    """Button variant enumeration 按钮变体枚举"""
    SOLID = "solid"
    OUTLINED = "outlined"
    FILLED = "filled"
    TEXT = "text"
    LINK = "link"


