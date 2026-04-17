# XCarousel

走马灯/轮播组件，支持自动播放、滑动切换动画、高 DPI 适配、底部指示器。

## 示例

![XCarousel示例](./images/XCarousel.png "XCarousel示例")

## 导入

```python
from xsideui import XCarousel
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `interval` | int | 3000 | 轮播间隔(毫秒) |
| `min_height` | int | 200 | 最小高度 |
| `parent` | QWidget | None | 父组件 |

## 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `add_image_page(source, scale_mode)` | 添加图片页面 | XImage |
| `set_current_page(index)` | 切换到指定页面 | None |
| `get_current_page()` | 获取当前页索引 | int |
| `get_page_count()` | 获取总页数 | int |

## 信号

| 信号 | 说明 |
|------|------|
| `image_clicked(index)` | 图片点击时发出 |
| `current_page_changed(index)` | 页面切换时发出 |

## 缩放模式

| 模式 | 字符串值 | 说明 |
|------|----------|------|
| 填充容器 | "cover" | 保持比例，填充整个容器（可能裁剪） |
| 完整显示 | "contain" | 保持比例，完整显示在容器内 |
| 拉伸填充 | "fill" | 拉伸填充容器（不保持比例） |

## 示例

```python
# 创建
carousel = XCarousel(interval=3000, min_height=300)

# 添加图片 (支持路径、QPixmap、bytes)
carousel.add_image_page("image1.jpg", scale_mode="cover")
carousel.add_image_page("image2.jpg", scale_mode="cover")

# 监听事件
carousel.image_clicked.connect(lambda idx: print(f"点击第{idx}张"))
carousel.current_page_changed.connect(lambda idx: print(f"切换到第{idx}页"))

# 本地图片
carousel.add_image_page(r"D:\photos\banner.jpg", scale_mode="cover")

# QPixmap
from PySide2.QtGui import QPixmap
pixmap = QPixmap(":/images/logo.png")
carousel.add_image_page(pixmap, scale_mode="contain")

# bytes
with open("image.jpg", "rb") as f:
    carousel.add_image_page(f.read(), scale_mode="cover")

# 手动控制
carousel.set_current_page(0)  # 跳转到第一页
```

## 特性

- ✅ 基于 XImage 组件，自动获得所有图片特性
- ✅ **滑动切换动画（500ms，OutCubic 缓动）**
- ✅ 鼠标悬停时暂停播放
- ✅ 底部指示器点击切换
- ✅ 窗口 resize 时自动重绘
- ✅ **高 DPI 适配（Retina/4K）**
- ✅ **跨显示器 DPR 切换支持**
- ✅ **图片加载淡入动画**
- ✅ **智能缩放缓存**

## 高级特性

### 滑动切换动画

页面切换时自动播放滑动动画：

```python
# 自动播放，无需配置
carousel = XCarousel()
carousel.add_image_page("photo1.jpg", scale_mode="cover")
carousel.add_image_page("photo2.jpg", scale_mode="cover")

# 动画特性：
# - 持续时间：500ms
# - 缓动曲线：OutCubic
# - 方向：根据切换方向自动判断（左滑/右滑）
```

### 高 DPI 适配

基于 XImage 组件，自动适配高 DPI 显示器（Retina/4K）：

```python
# 无需额外配置，自动适配
carousel = XCarousel()
carousel.add_image_page("photo.jpg", scale_mode="cover")
```

### DPR 切换支持

窗口在不同 DPI 显示器间拖动时，自动检测并重新渲染：

```python
# DPR 1.0 显示器 → DPR 1.25 显示器
# 自动检测变化，重新渲染，保持清晰
```

### 图片加载动画

每张图片加载完成后自动播放淡入动画（300ms）：

```python
# 自动播放，无需配置
carousel.add_image_page("photo.jpg", scale_mode="cover")
```

### 智能缩放缓存

大图缩放后自动缓存，避免重复计算，提升性能：

```python
# 首次加载：计算缩放并缓存
# 后续绘制：直接使用缓存
# 窗口 resize：自动更新缓存
```

## 架构说明

XCarousel 内部使用 XImage 组件作为页面，因此自动继承 XImage 的所有特性：

- 懒加载
- 图片缓存
- 右键菜单（保存、复制、刷新）
- 圆角处理
- 主题适配
- 错误处理
- 占位图
