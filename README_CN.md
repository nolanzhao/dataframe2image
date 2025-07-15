# 中文字体支持说明

## 功能介绍

dataframe2image 现在支持自动检测和处理中文字符，无需手动配置即可生成包含中文字符的表格图片，确保中文字符能够正确显示。

## 使用方法

### 基本用法

```python
import pandas as pd
from dataframe2image import df_to_image

# 创建包含中文的DataFrame
data = {
    '产品名称': ['苹果MacBook Pro', '罗技鼠标', '海盗船键盘'],
    '品牌': ['苹果', '罗技', '海盗船'],
    '价格(元)': [12999.00, 299.00, 899.00]
}
df = pd.DataFrame(data)

# 自动检测中文字符并生成图片
df_to_image(df, 'chinese_table.png')
```

### 支持的中文字体

项目在 `src/dataframe2image/font/` 目录中包含了以下中文字体：
- 方正兰亭圆简体_准.TTF
- 方正兰亭圆简体_纤.TTF

### 完整示例

```python
from dataframe2image import df_to_image, df_to_html, TableStyle

# 使用不同主题（自动检测中文字符）
df_to_image(df, 'chinese_light.png', style='light')
df_to_image(df, 'chinese_dark.png', style='dark')

# 使用自定义样式
custom_style = TableStyle(
    font_size=14,
    header_bg_color="#FF6B6B",
    header_text_color="#FFFFFF"
)
df_to_image(df, 'chinese_custom.png', style=custom_style)

# 生成HTML（自动检测中文字符）
html_content = df_to_html(df)
```

## 示例文件

运行 `examples/chinese_example.py` 可以查看完整的中文表格示例：

```bash
cd examples
python chinese_example.py
```

这将生成多个包含中文内容的表格图片，展示不同主题和样式的效果。

## 技术实现

- 自动检测DataFrame中的中文字符（包括列名、索引和数据值）
- 当检测到中文字符时，自动使用 `@font-face` CSS 规则加载本地字体文件
- 自动配置字体族回退机制，确保中文字符正确显示
- 支持所有现有的主题和自定义样式
- 保持与英文表格相同的功能和性能
- 无需手动配置，完全自动化处理
