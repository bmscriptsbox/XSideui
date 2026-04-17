import re

from typing import Optional, Dict, List
import xml.etree.ElementTree as ET
from ..utils.qt_compat import QSvgRenderer, QPixmap, QIcon, QPainter, QTransform, Qt, QByteArray, QResource, QRect
from .xicon_cache import xicon_cache
from . import xicons_rc

class XIconEngine:
    """图标引擎 - 负责SVG图标的加载和处理
    
    Features:
        - 高效SVG解析
        - 颜色替换 (基于路径替换，非像素操作)
        - 尺寸变换
        - 旋转/翻转支持
        - 批量处理优化
    """

    _svg_cache: Dict[str, str] = {}
    _svg_renderer_cache: Dict[str, QSvgRenderer] = {}
    _search_prefixes = [":/xsidiui/"]
    _icons_initialized: bool = False
    _svg_directory: str = ""

    _fill_pattern = re.compile(r'fill="[^"]*"', re.IGNORECASE)

    @classmethod
    def _init_icons(cls):
        """初始化图标索引"""
        if cls._icons_initialized:
            return

        # 遍历所有注册的路径前缀
        for prefix in cls._search_prefixes:
            # 去掉冒号和结尾斜杠，以便 QResource 识别
            res_path = prefix.rstrip('/')
            resource = QResource(res_path)

            if resource.isValid():
                for child in resource.children():
                    if child.endswith(".svg"):
                        # 提取文件名作为图标名
                        name = child.split("/")[-1][:-4]
                        # 如果已存在（被更高优先级的路径占坑），则不覆盖
                        if name not in cls._svg_cache:
                            cls._svg_cache[name] = None

        cls._icons_initialized = True

    @classmethod
    def load_svg(cls, name: str) -> Optional[str]:
        """从资源系统中检索并加载内容"""

        # 1. 如果已经缓存了源码，直接返回
        if cls._svg_cache.get(name):
            return cls._svg_cache[name]

        # 2. 核心：按优先级在所有前缀中查找文件
        for prefix in cls._search_prefixes:
            full_path = f"{prefix}{name}.svg"
            resource = QResource(full_path)

            if resource.isValid():
                data = resource.data()
                if data:
                    try:
                        content = bytes(data).decode('utf-8')
                        # 自动兼容某些极致压缩的 QRC 资源
                        if not content.startswith('<'):
                            import zlib
                            content = zlib.decompress(bytes(data)).decode('utf-8')

                        cls._svg_cache[name] = content
                        return content
                    except Exception as e:
                        print(f"Load SVG Error ({full_path}): {e}")


        return None

    @classmethod
    def get_renderer(cls, name: str) -> Optional[QSvgRenderer]:
        """获取SVG渲染器"""
        if name in cls._svg_renderer_cache:
            return cls._svg_renderer_cache[name]

        svg_content = cls.load_svg(name)
        if svg_content is None:
            return None

        renderer = QSvgRenderer(QByteArray(svg_content.encode()))
        if renderer.isValid():
            cls._svg_renderer_cache[name] = renderer
            return renderer

        return None



    @classmethod
    def recolor_svg(cls, svg_content: str, color: str) -> str:
        """替换颜色"""
        if not color or color.lower() == "currentcolor":
            return svg_content

        try:
            # 1. 注册命名空间，防止生成 ns0:svg 这种奇怪的前缀
            ET.register_namespace('', "http://www.w3.org/2000/svg")

            # 2. 解析 SVG 字符串
            # 使用 BytesIO 处理编码，防止特殊字符报错
            tree = ET.ElementTree(ET.fromstring(svg_content))
            root = tree.getroot()

            # 3. 定义需要处理的形状标签
            tags_to_fix = ['{*}path', '{*}rect', '{*}circle', '{*}ellipse', '{*}line', '{*}polyline', '{*}polygon']

            # 4. 递归遍历所有元素
            for elem in root.iter():
                # 获取去除命名空间后的标签名
                tag_name = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag

                # 只处理形状相关的标签
                if any(elem.tag.endswith(t.replace('{*}', '')) for t in tags_to_fix):

                    # 情况 A：处理描边 (Stroke)
                    stroke = elem.get('stroke')
                    if stroke and stroke.lower() != 'none':
                        elem.set('stroke', color)

                    # 情况 B：处理填充 (Fill)
                    fill = elem.get('fill')
                    # 注意：如果 fill 没写，默认通常是黑色，我们要把它揪出来
                    if fill:
                        if fill.lower() != 'none':
                            elem.set('fill', color)
                    else:
                        # 如果该标签既没有 stroke 也没有 fill
                        # 按照 SVG 规范，它会默认填充黑色，所以我们强制给它颜色
                        if not stroke:
                            elem.set('fill', color)

                    # 情况 C：处理 Style 属性 (比如 style="fill:#333")
                    style = elem.get('style')
                    if style:
                        # 替换 style 字符串中的颜色
                        style = re.sub(r'(fill|stroke):\s*[^;]+', r'\1:' + color, style)
                        elem.set('style', style)

            # 5. 将处理后的 XML 转回字符串
            return ET.tostring(root, encoding='unicode', method='xml')

        except Exception as e:
            # 如果解析失败（说明不是标准 XML），返回原内容
            print(f"SVG Recolor Error: {e}")
            return svg_content



    @classmethod
    def create_pixmap(
            cls,
            name: str,
            size: int = 24,
            color: str = None,
            rotation: float = 0,
            flip_h: bool = False,
            flip_v: bool = False,
            dpr: float = 1.0
    ) -> Optional[QPixmap]:
        # 1. 尝试从缓存获取
        cached = xicon_cache.get(
            name, size, color, None,
            rotation, flip_h, flip_v, True, dpr
        )
        if cached is not None and not cached.isNull():
            return cached

        # 2. 准备基础资源
        svg_content = cls.load_svg(name)
        if svg_content is None: return None

        # color 已经是解析后的颜色值，直接使用
        svg_content = cls.recolor_svg(svg_content, color)

        # 3. 初始化画布
        # 核心修改：强制物理像素向上取整，避免 1.25dpr 下出现 29.5px 这种非法尺寸
        physical_pixel_size = int(size * dpr + 0.5)
        pixmap = QPixmap(physical_pixel_size, physical_pixel_size)

        # 必须先填充透明，否则会有随机底色噪声
        pixmap.fill(Qt.transparent)
        # 设置逻辑比例
        pixmap.setDevicePixelRatio(dpr)

        painter = QPainter(pixmap)
        # 高清渲染必备三件套
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        # 4. 坐标变换 (统一使用逻辑尺寸 size)
        if rotation != 0 or flip_h or flip_v:
            transform = QTransform()
            center = size / 2.0
            transform.translate(center, center)
            if rotation != 0: transform.rotate(rotation)
            if flip_h: transform.scale(-1, 1)
            if flip_v: transform.scale(1, -1)
            transform.translate(-center, -center)
            painter.setTransform(transform)

        # 5. 渲染 SVG
        svg_bytes = QByteArray(svg_content.encode())
        temp_renderer = QSvgRenderer(svg_bytes)

        if temp_renderer.isValid():
            target_rect = QRect(0, 0, size, size)
            temp_renderer.render(painter, target_rect)

        painter.end()

        # 6. 存入缓存
        xicon_cache.set(
            pixmap, name, size, color, None,
            rotation, flip_h, flip_v, dpr
        )

        return pixmap


    @classmethod
    def create_icon(
        cls,
        name: str,
        size: int = 24,
        color: str = None
    ) -> Optional[QIcon]:
        """创建图标QIcon"""
        cached = xicon_cache.get_qicon(name, size, color, True)
        if cached is not None:
            return cached

        pixmap = cls.create_pixmap(name, size, color)
        if pixmap is None or pixmap.isNull():
            return None

        icon = QIcon(pixmap)
        xicon_cache.set_qicon(icon, name, size, color, True)

        return icon

    @classmethod
    def preload_icons(
        cls,
        names: List[str],
        sizes: List[int] = None,
        colors: List[str] = None
    ):
        """预加载图标到缓存"""
        sizes = sizes or [16, 24, 32, 48]
        colors = colors or []

        for name in names:
            for size in sizes:
                if name not in cls._svg_cache:
                    cls.load_svg(name)

                pixmap = cls.create_pixmap(
                    name, size, None,
                    theme_aware=True
                )

        xicon_cache.preload(names, sizes, colors)

    @classmethod
    def clear_cache(cls):
        """清理所有缓存"""
        cls._svg_cache.clear()
        cls._svg_renderer_cache.clear()
        xicon_cache.clear_all()

    @classmethod
    def get_icon_names(cls) -> List[str]:
        """获取所有已加载的图标名称"""
        cls._init_icons()
        return list(cls._svg_cache.keys())

    @classmethod
    def svg_to_bytes(cls, svg_content: str, size: int, color: str = None) -> bytes:
        """将SVG转换为指定颜色和大小的字节数据"""
        if color:
            svg_content = cls.recolor_svg(svg_content, color)

        svg_content = re.sub(
            r'width="[^"]*"',
            f'width="{size}"',
            svg_content
        )
        svg_content = re.sub(
            r'height="[^"]*"',
            f'height="{size}"',
            svg_content
        )

        return svg_content.encode('utf-8')

    @classmethod
    def create_multisize_icon(
        cls,
        name: str,
        size: int,
        color: str = None,
        dpr_values: list = None
    ) -> Optional[QIcon]:
        """创建多尺寸图标，支持多个 DPR 值
        
        Qt会根据当前DPR自动选择最合适的尺寸
        
        Args:
            name: 图标名称
            size: 图标逻辑尺寸
            color: 图标颜色（已解析）
            dpr_values: DPR值列表，默认 [1.0, 1.25, 1.5, 1.75, 2.0]
            
        Returns:
            包含多个DPR尺寸的QIcon
        """

        if dpr_values is None:
            dpr_values = [1.0, 1.25, 1.5, 1.75, 2.0]
        
        icon = QIcon()
        
        for dpr in dpr_values:
            pixmap = cls.create_pixmap(
                name, size, color,
                dpr=dpr
            )
            if pixmap and not pixmap.isNull():
                # 关键：明确指定逻辑尺寸，让Qt正确处理DPR
                icon.addPixmap(pixmap)
        
        return icon if not icon.isNull() else None

    @classmethod
    def create_animated_pixmap(
        cls,
        name: str,
        size: int,
        color: str = None,
        frame: int = 0,
        total_frames: int = 1
    ) -> QPixmap:
        """创建动画帧Pixmap (用于加载动画等)"""
        rotation = (360 / total_frames) * frame
        return cls.create_pixmap(
            name, size, color,
            rotation=rotation,
            # theme_aware=True
        ) or QPixmap(size, size)

    @classmethod
    def register_resource_package(cls, prefix: str):
        """
        供用户调用：注册自定义图标资源前缀
        需要先导入_rc.py资源文件
        例如：XIconEngine.register_resource_package(":/custom/")
        """
        if not prefix.endswith('/'):
            prefix += '/'
        if prefix not in cls._search_prefixes:
            # 插入到最前面，实现“用户优先”的覆盖逻辑
            cls._search_prefixes.insert(0, prefix)

        # 重置初始化状态，以便下次调用时重新扫描新注册的图标
        cls._icons_initialized = False



xicon_engine = XIconEngine()
