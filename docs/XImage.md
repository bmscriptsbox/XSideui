# XImage

图片组件，支持多种适应模式、懒加载、缓存和高 DPI 适配。

## 示例

![XImage示例](./images/XImage.png "XImage示例")

## 导入

```python
from xsideui import XImage
```

## 参数

| 参数         | 类型 | 默认值                    | 说明      |
|------------|------|------------------------|---------|
| `source`   | str / QPixmap / QImage / bytes | ""                     | 图片源     |
| `fit`      | XImage.FitMode 或 str | XImage.FitMode.CONTAIN | 适应模式    |
| `alt`      | str | ""                     | 图片描述    |
| `min_size` | int | 32                     | 最小尺寸    |
| `lazy`     | bool | True                   | 是否启用懒加载 |
| `parent`   | QWidget | None                   | 父组件     |

## 适应模式

| 模式 | 枚举值 | 字符串值 | 说明 |
|------|--------|----------|------|
| 完整显示 | XImage.FitMode.CONTAIN | "contain" | 保持比例，完整显示在容器内 |
| 填充容器 | XImage.FitMode.COVER | "cover" | 保持比例，填充整个容器（可能裁剪） |
| 拉伸填充 | XImage.FitMode.FILL | "fill" | 拉伸填充容器（不保持比例） |
| 原始大小 | XImage.FitMode.NONE | "none" | 原始大小，不缩放 |

## 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `set_source(source)` | 设置图片源 | None |
| `set_fit(fit)` | 设置适应模式 | None |

## 信号

| 信号 | 说明 |
|------|------|
| `loaded` | 图片加载完成时发出 |
| `error` | 图片加载失败时发出 |
| `clicked` | 图片被点击时发出 |

## 缓存

图片组件支持自动缓存，提升加载性能：

```python
from xsideui.widgets.image import clear_image_cache

# 清空图片缓存
clear_image_cache()
```

## 右键菜单

图片加载成功后，右键点击可显示菜单：

- **保存图片**：保存到本地文件
- **复制图片**：复制到剪贴板
- **刷新**：重新加载图片

## 示例

```python
# 基础用法
image = XImage(source="path/to/image.jpg")

# 使用枚举设置适应模式
image = XImage(source="photo.jpg", fit=XImage.FitMode.CONTAIN)
image = XImage(source="photo.jpg", fit=XImage.FitMode.COVER)
image = XImage(source="photo.jpg", fit=XImage.FitMode.FILL)
image = XImage(source="photo.jpg", fit=XImage.FitMode.NONE)

# 使用字符串设置适应模式
image = XImage(source="photo.jpg", fit="contain")
image = XImage(source="photo.jpg", fit="cover")
image = XImage(source="photo.jpg", fit="fill")
image = XImage(source="photo.jpg", fit="none")

# 使用 Base64
image = XImage(source="data:image/png;base64,iVBORw0KG...")

# 使用 QPixmap
from PySide2.QtGui import QPixmap
image = XImage(source=QPixmap("photo.jpg"))

# 使用 QImage
from PySide2.QtGui import QImage
image = XImage(source=QImage("photo.jpg"))

# 使用 bytes
image = XImage(source=open("photo.jpg", "rb").read())

# 动态更换图片
image = XImage(source="image1.jpg")
image.set_source("image2.jpg")

# 更改适应模式
image.set_fit(XImage.FitMode.COVER)
image.set_fit("cover")

# 监听事件
image.loaded.connect(lambda: print("图片加载完成"))
image.error.connect(lambda: print("图片加载失败"))
image.clicked.connect(lambda: print("图片被点击"))

# 禁用懒加载
image = XImage(source="photo.jpg", lazy=False)

# 设置最小高度
image = XImage(source="photo.jpg", min_height=200)
```

## 特性

- ✅ 多种图片源（文件路径、QPixmap、QImage、bytes、Base64）
- ✅ 四种适应模式（contain/cover/fill/none）
- ✅ 懒加载
- ✅ 图片缓存
- ✅ 右键菜单（保存、复制、刷新）
- ✅ 圆角处理
- ✅ 主题适配
- ✅ 错误处理
- ✅ 占位图
- ✅ 点击事件
- ✅ **加载淡入动画**
- ✅ **高 DPI 适配（Retina/4K）**
- ✅ **智能缩放缓存**
- ✅ **跨显示器 DPR 切换支持**

## 高级特性

### 高 DPI 适配

组件自动适配高 DPI 显示器（Retina/4K），确保图片清晰：

```python
# 无需额外配置，自动适配
image = XImage(source="photo.jpg")

# 跨显示器拖动窗口时，自动重新渲染适配新 DPI
```

### 智能缩放缓存

大图缩放后自动缓存，避免重复计算，提升性能：

```python
# 首次加载：计算缩放并缓存
# 后续绘制：直接使用缓存
# 窗口 resize：自动更新缓存
```

### DPR 切换支持

窗口在不同 DPI 显示器间拖动时，自动检测并重新渲染：

```python
# DPR 1.0 显示器 → DPR 1.25 显示器
# 自动检测变化，重新渲染，保持清晰
```

### 加载动画

图片加载完成后自动播放淡入动画（300ms）：

```python
# 自动播放，无需配置
image = XImage(source="photo.jpg")
```
