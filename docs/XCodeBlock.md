# XCodeBlock

代码块组件（继承QPlainTextEdit），带有语法高亮和主题适配。

## 示例

![XCodeBlock示例](./images/XCodeBlock.png "XCodeBlock示例")

## 导入

```python
from xsideui import XCodeBlock
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `code` | str | "" | 初始代码文本 |
| `language` | str | "python" | 编程语言（目前仅支持 Python） |
| `parent` | QWidget | None | 父组件 |

## 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `add_code(code)` | 添加代码到代码块（会先清空现有内容） | XCodeBlock |
| `clear_code()` | 清除代码块中的代码 | XCodeBlock |
| `set_language(language)` | 设置编程语言 | None |

## 示例

```python
# 基础用法
code_block = XCodeBlock()
```

```python
# 带初始代码
python_code = '''def hello_world():
    print("Hello, World!")

hello_world()'''

code_block = XCodeBlock(code=python_code)
```

```python
# 添加代码
code_block = XCodeBlock()
code_block.add_code('''
def calculate_sum(a, b):
    return a + b

result = calculate_sum(10, 20)
print(f"结果: {result}")
''')
```

```python
# 清空代码
code_block.clear_code()
```

```python
# 设置编程语言
code_block.set_language("python")
```

```python
# 使用 QPlainTextEdit 的方法
code_block = XCodeBlock()

# 获取代码
code = code_block.toPlainText()

# 设置代码
code_block.setPlainText("新的代码内容")

# 追加代码
code_block.appendPlainText("追加的代码")

# 清空代码
code_block.clear()

# 设置只读
code_block.setReadOnly(False)
```

## 语法高亮

支持以下语法元素的高亮：

| 语法元素 | 示例 |
|----------|--------|
| 关键字 | `def`, `class`, `if`, `for`, `while`, `return` 等 |
| 字符串 | `"hello"`, `'world'` |
| 注释 | `# 这是注释` |
| 函数名 | `function_name()` |
| 数字 | `123`, `3.14` |
| 操作符 | `=`, `+`, `-`, `*`, `/`, `==`, `!=` 等 |

## 特性

- ✅ 主题适配 - 自动适配明暗主题切换
- ✅ 语法高亮 - Python 语法高亮支持
- ✅ 只读模式 - 默认为只读，防止用户编辑
- ✅ 代码字体 - 使用等宽字体（JetBrains Mono、Fira Code 等）
- ✅ 自动换行 - 默认不自动换行
