import threading
from typing import Dict, Optional, OrderedDict
from ..utils.qt_compat import QPixmap, QIcon


class _LRUCache:
    """自定义LRU缓存实现
    
    简单的LRU (Least Recently Used) 缓存实现
    """

    def __init__(self, max_size: int = 100):
        if max_size <= 0:
            max_size = 1
        self._max_size = max_size
        self._cache: OrderedDict = OrderedDict()

    def __contains__(self, key) -> bool:
        return key in self._cache

    def __getitem__(self, key):
        if key not in self._cache:
            raise KeyError(key)
        self._cache.move_to_end(key)
        return self._cache[key]

    def __setitem__(self, key, value):
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        if len(self._cache) > self._max_size:
            self._cache.popitem(last=False)

    def __len__(self) -> int:
        return len(self._cache)

    def get(self, key, default=None):
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        return default

    def set(self, key, value):
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        if len(self._cache) > self._max_size:
            self._cache.popitem(last=False)

    def clear(self):
        self._cache.clear()

    def items(self):
        return self._cache.items()

    def keys(self):
        return self._cache.keys()

    def values(self):
        return self._cache.values()


class XIconCache:
    """高性能图标缓存管理器
    
    采用三级缓存策略：
    - L1: 内存缓存 (QPixmap)
    - L2: 主题缓存 (按主题分片)
    - L3: QIcon缓存 (常用尺寸)
    
    Features:
        - LRU淘汰策略
        - 线程安全
        - 主题隔离
        - 批量操作支持
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_cache()
        return cls._instance

    def _init_cache(self):
        self._l1_cache = _LRUCache(200)
        self._l2_light_cache = _LRUCache(100)
        self._l2_dark_cache = _LRUCache(100)
        self._l3_cache = _LRUCache(100)
        self._current_theme = "light"
        self._stats = {"hits": 0, "misses": 0}

    def get_cache_key(
        self,
        name: str,
        size: int,
        color: str,
        rotation: float,
        flip_h: bool,
        flip_v: bool,
        dpr: float = 1.0
    ) -> str:
        """生成缓存键"""
        return f"{name}|{size}|{color}|{rotation}|{flip_h}|{flip_v}|{dpr}"

    def get_theme_key(
        self,
        name: str,
        size: int,
        color: str
    ) -> str:
        """生成主题相关的缓存键"""
        return f"{name}|{size}|{color}"

    def get(
        self,
        name: str,
        size: int = 24,
        color: str = None,
        fill_type: str = None,
        rotation: float = 0,
        flip_h: bool = False,
        flip_v: bool = False,
        theme_aware: bool = True,
        dpr: float = 1.0
    ) -> Optional[QPixmap]:
        """从缓存获取图标"""
        cache_key = self.get_cache_key(name, size, color or "", rotation, flip_h, flip_v, dpr)

        if theme_aware and color is None:
            cache = self._l2_light_cache if self._current_theme == "light" else self._l2_dark_cache
        else:
            cache = self._l1_cache

        result = cache.get(cache_key)
        if result is not None:
            self._stats["hits"] += 1
            return result

        self._stats["misses"] += 1
        return None

    def set(
        self,
        pixmap: QPixmap,
        name: str,
        size: int = 24,
        color: str = None,
        fill_type: str = None,
        rotation: float = 0,
        flip_h: bool = False,
        flip_v: bool = False,
        theme_aware: bool = True,
        dpr: float = 1.0
    ):
        """存入缓存"""
        cache_key = self.get_cache_key(name, size, color or "", rotation, flip_h, flip_v, dpr)

        if theme_aware and color is None:
            cache = self._l2_light_cache if self._current_theme == "light" else self._l2_dark_cache
        else:
            cache = self._l1_cache

        cache.set(cache_key, pixmap)

    def get_qicon(
        self,
        name: str,
        size: int = 24,
        color: str = None,
        theme_aware: bool = True
    ) -> Optional[QIcon]:
        """获取QIcon缓存"""
        key = (name, size, color or "", theme_aware)
        # key = (name, size, color or "", theme_aware, rotation, flip_h, flip_v)

        if key in self._l3_cache:
            self._stats["hits"] += 1
            return self._l3_cache.get(key)

        self._stats["misses"] += 1
        return None

    def set_qicon(
        self,
        icon: QIcon,
        name: str,
        size: int = 24,
        color: str = None,
        theme_aware: bool = True
    ):
        """存入QIcon缓存"""
        key = (name, size, color or "", theme_aware)
        self._l3_cache.set(key, icon)

    def set_theme(self, theme: str):
        """设置当前主题"""
        self._current_theme = theme

    def clear_theme_cache(self, theme: str = None):
        """清理主题缓存"""
        target_theme = theme or self._current_theme

        if target_theme == "light":
            self._l2_light_cache.clear()
        else:
            self._l2_dark_cache.clear()

        if theme is None:
            self._l1_cache.clear()
            self._l3_cache.clear()

    def clear_all(self):
        """清理所有缓存"""
        self._l1_cache.clear()
        self._l2_light_cache.clear()
        self._l2_dark_cache.clear()
        self._l3_cache.clear()
        self._stats = {"hits": 0, "misses": 0}

    def get_stats(self) -> Dict:
        """获取缓存统计"""
        total = self._stats["hits"] + self._stats["misses"]
        hit_rate = (self._stats["hits"] / total * 100) if total > 0 else 0

        return {
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "hit_rate": f"{hit_rate:.1f}%",
            "l1_size": len(self._l1_cache),
            "l2_light_size": len(self._l2_light_cache),
            "l2_dark_size": len(self._l2_dark_cache),
            "l3_size": len(self._l3_cache)
        }

    def preload(
        self,
        icon_names: list,
        sizes: list = None,
        colors: list = None
    ):
        """预加载图标到缓存"""
        sizes = sizes or [16, 24, 32, 48]
        colors = colors or []

        for name in icon_names:
            for size in sizes:
                self._l1_cache.set(
                    self.get_cache_key(name, size, "", 0, False, False),
                    None
                )

xicon_cache = XIconCache()
