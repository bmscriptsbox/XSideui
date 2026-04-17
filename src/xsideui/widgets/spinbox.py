"""Number Input Component 数字输入框组件

提供整数和小数输入框，支持步进按钮。
"""

from typing import Union
from ..utils.qt_compat import QSpinBox, QDoubleSpinBox, Qt, QTimer
from .xarrowbutton import XArrowButton
from .. import IconName
from ..theme import theme_manager
from ..xenum import XSize

# 常量
MAX_CACHE_SIZE = 50
UPDATE_INTERVAL = 16  # ~60fps


def _parse_size_value(size: Union[XSize, str]) -> str:
    """解析尺寸值"""
    return size.value if isinstance(size, XSize) else size

class XSpinBoxBase:
    """SpinBox 基类，提供公共方法"""

    def _parse_size(self, size: Union[XSize, str]) -> str:
        """解析尺寸"""
        return _parse_size_value(size)

    def _init_buttons(self):
        """初始化自定义步进按钮"""
        self._up_btn = XArrowButton(icon_name=IconName.UP_CARET, parent=self)
        self._down_btn = XArrowButton(icon_name=IconName.DOWN_CARET, parent=self)

        self._up_btn.clicked.connect(self.stepUp)
        self._down_btn.clicked.connect(self.stepDown)

    def _get_size_config(self) -> dict:
        """获取尺寸配置"""
        size_map = {
            'large': 28,
            'default': 24,
            'small': 22,
            'mini': 20
        }

        if self._size_value not in size_map:
            raise ValueError(f"Invalid size value: {self._size_value}. "
                           f"Expected one of: {list(size_map.keys())}")

        return {'btn_width': size_map[self._size_value]}

    def _update_style(self):
        """更新样式"""
        self.setProperty("componentSize", self._size_value)
        self._schedule_update()

    def _schedule_update(self):
        """调度更新（节流）"""
        self._update_timer.start()

    def _update_button_positions(self):
        """同步 XTimeEdit 的成功逻辑：动态获取 rect"""
        if not hasattr(self, '_up_btn'): return

        config = self._get_size_config()
        btn_width = config['btn_width']

        # 使用 self.rect() 确保获取的是布局完成后的真实几何尺寸
        r = self.rect()
        width = r.width()
        height = r.height()
        btn_height = height // 2

        self._up_btn.setFixedSize(btn_width, btn_height)
        self._down_btn.setFixedSize(btn_width, btn_height)

        # 确保按钮停留在最右侧
        self._up_btn.move(width - btn_width, 0)
        self._down_btn.move(width - btn_width, btn_height)

        self._up_btn.raise_()
        self._down_btn.raise_()

        # 必须设置边距，否则输入框文字会和按钮重叠
        self.setContentsMargins(0, 0, btn_width, 0)

    def handle_resize(self, event):
        """手动处理函数，避免 Mixin 的 super() 迷路"""
        self._update_button_positions()



    def closeEvent(self, event):
        """处理关闭事件，断开信号连接"""
        try:
            theme_manager.theme_changed.disconnect(self._on_theme_changed)
        except (TypeError, RuntimeError):
            pass
        super().closeEvent(event)

    def set_size(self, size: Union[XSize, str]):
        """设置尺寸"""
        self._size_value = self._parse_size(size)
        self._update_style()
        return self

    def size(self) -> str:
        """获取当前尺寸"""
        return self._size_value

    def _on_theme_changed(self, theme_name):
        """处理主题变化事件"""
        self._up_btn.update()
        self._down_btn.update()


class XSpinBox(QSpinBox, XSpinBoxBase):
    """带步进按钮的整数输入框"""

    def __init__(
            self,
            value: int = 0,
            minimum: int = 0,
            maximum: int = 999999999,
            step: int = 1,
            prefix: str = "",
            suffix: str = "",
            size: Union[XSize, str] = XSize.DEFAULT,
            parent=None
    ):
        """
        初始化整数输入框

        Args:
            value: 初始值，默认 0
            minimum: 最小值，默认 0
            maximum: 最大值，默认 999999999
            step: 步长，默认 1
            prefix: 前缀文本，默认 ""
            suffix: 后缀文本，默认 ""
            size: 组件尺寸，支持枚举或字符串，默认 XSize.DEFAULT
                  - XSize.LARGE 或 "large": 大尺寸
                  - XSize.DEFAULT 或 "default": 默认尺寸
                  - XSize.SMALL 或 "small": 小尺寸
                  - XSize.MINI 或 "mini": 迷你尺寸
            parent: 父组件，默认 None
        """
        super().__init__(parent)

        self.setObjectName("xspinbox")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._size_value = self._parse_size(size)

        self.setAlignment(Qt.AlignCenter)
        self.setMinimumWidth(120)
        self.setButtonSymbols(QSpinBox.NoButtons)

        self.setRange(minimum, maximum)
        self.setValue(value)
        self.setSingleStep(step)
        self.setPrefix(prefix)
        self.setSuffix(suffix)

        self._update_timer = QTimer(self)
        self._update_timer.setSingleShot(True)
        self._update_timer.setInterval(UPDATE_INTERVAL)
        self._update_timer.timeout.connect(self._update_button_positions)

        self._init_buttons()
        self._update_style()
        theme_manager.theme_changed.connect(self._on_theme_changed)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_button_positions()

    def showEvent(self, event):
        super().showEvent(event)
        self._update_button_positions()


class XDoubleSpinBox(QDoubleSpinBox, XSpinBoxBase):
    """带步进按钮的小数输入框"""

    def __init__(
            self,
            value: float = 0.0,
            minimum: float = 0.0,
            maximum: float = 99.99,
            step: float = 0.1,
            decimals: int = 2,
            prefix: str = "",
            suffix: str = "",
            size: Union[XSize, str] = XSize.DEFAULT,
            parent=None
    ):
        """
        初始化小数输入框

        Args:
            value: 初始值，默认 0.0
            minimum: 最小值，默认 0.0
            maximum: 最大值，默认 99.99
            step: 步长，默认 0.1
            decimals: 小数位数，默认 2
            prefix: 前缀文本，默认 ""
            suffix: 后缀文本，默认 ""
            size: 组件尺寸，支持枚举或字符串，默认 XSize.DEFAULT
                  - XSize.LARGE 或 "large": 大尺寸
                  - XSize.DEFAULT 或 "default": 默认尺寸
                  - XSize.SMALL 或 "small": 小尺寸
                  - XSize.MINI 或 "mini": 迷你尺寸
            parent: 父组件，默认 None
        """
        super().__init__(parent)

        self.setObjectName("xspinbox")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._size_value = self._parse_size(size)

        self.setAlignment(Qt.AlignCenter)
        self.setMinimumWidth(120)
        self.setButtonSymbols(QDoubleSpinBox.NoButtons)

        self.setRange(minimum, maximum)
        self.setValue(value)
        self.setSingleStep(step)
        self.setDecimals(decimals)
        self.setPrefix(prefix)
        self.setSuffix(suffix)

        self._update_timer = QTimer(self)
        self._update_timer.setSingleShot(True)
        self._update_timer.setInterval(UPDATE_INTERVAL)
        self._update_timer.timeout.connect(self._update_button_positions)

        self._init_buttons()
        self._update_style()
        theme_manager.theme_changed.connect(self._on_theme_changed)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_button_positions()

    def showEvent(self, event):
        super().showEvent(event)
        self._update_button_positions()

    def set_decimals(self, decimals: int):
        """设置小数位数"""
        self.setDecimals(decimals)
        return self
