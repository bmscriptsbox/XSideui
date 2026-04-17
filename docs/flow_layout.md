# XFlowLayout

流式布局组件，自动换行排列子组件。

## 导入

```python
from xsideui import XFlowLayout
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `parent` | QWidget | None | 父组件 |
| `margin` | int | 0 | 布局边距 |
| `spacing` | int | -1 | 项目间距（-1 表示使用系统默认） |

## 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `addItem(item)` | 添加布局项目 | None |
| `count()` | 获取项目数量 | int |
| `itemAt(index)` | 获取指定位置的项目 | QLayoutItem |
| `takeAt(index)` | 移除并返回指定位置的项目 | QLayoutItem |
| `expandingDirections()` | 获取可扩展方向 | Qt.Orientations |
| `hasHeightForWidth()` | 是否支持基于宽度计算高度 | bool |
| `heightForWidth(width)` | 根据宽度计算高度 | int |
| `setGeometry(rect)` | 设置布局几何区域 | None |
| `sizeHint()` | 获取建议大小 | QSize |
| `minimumSize()` | 获取最小大小 | QSize |
| `spacing()` | 获取项目间距 | int |
| `setSpacing(spacing)` | 设置项目间距 | None |
| `clear()` | 清空布局（删除所有子组件） | None |
| `invalidate()` | 使缓存失效 | None |

## 示例

```python
# 基础用法
layout = XFlowLayout(parent_widget, margin=10, spacing=5)
layout.addWidget(QPushButton("按钮 1"))
layout.addWidget(QPushButton("按钮 2"))
parent_widget.setLayout(layout)

# 添加多个按钮
for i in range(10):
    button = QPushButton(f"按钮 {i+1}")
    layout.addWidget(button)

# 不同宽度的项目
short_btn = QPushButton("短")
layout.addWidget(short_btn)

medium_btn = QPushButton("中等长度按钮")
layout.addWidget(medium_btn)

long_btn = QPushButton("这是一个非常长的按钮文本")
layout.addWidget(long_btn)

# 标签云
tags = ["Python", "JavaScript", "Java", "C++", "Go", "Rust"]
for tag in tags:
    button = QPushButton(tag)
    layout.addWidget(button)

# 动态添加和移除
layout.addWidget(QPushButton("新按钮"))
item = layout.takeAt(0)
if item and item.widget():
    item.widget().deleteLater()

# 清空布局
layout.clear()

# 获取布局信息
count = layout.count()
spacing = layout.spacing()
size = layout.sizeHint()
min_size = layout.minimumSize()
height = layout.heightForWidth(400)

# 设置间距和边距
layout.setSpacing(10)
layout.setContentsMargins(10, 10, 10, 10)

# 使缓存失效
layout.invalidate()
```

## 特性

- ✅ 自动换行
- ✅ 支持不同宽度的项目
- ✅ 可配置间距
- ✅ 缓存优化
- ✅ 支持高度计算
- ✅ 支持大小策略
