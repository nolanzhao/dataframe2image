# dataframe2image

Convert pandas DataFrame to beautiful table images.

## Features

- Convert pandas DataFrame to high-quality table images
- Beautiful, customizable styling with CSS
- Support for various image formats (PNG, JPEG, WebP)
- Responsive table design
- Easy to use API

## Installation

```bash
pip install dataframe2image
```

After installation, you need to install Playwright browsers:

```bash
playwright install chromium
```

## Quick Start

```python
import pandas as pd
from dataframe2image import df_to_image

# Create a sample DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'Age': [25, 30, 35, 28],
    'City': ['New York', 'London', 'Tokyo', 'Paris'],
    'Salary': [50000, 60000, 70000, 55000]
})

# Convert to image
df_to_image(df, output_path='table.png')
```

## Advanced Usage

```python
from dataframe2image import df_to_image, TableStyle

# Custom styling
style = TableStyle(
    theme='dark',
    font_family='Arial',
    font_size=14,
    border_color='#333',
    header_bg_color='#4CAF50',
    row_bg_colors=['#f9f9f9', '#ffffff']
)

df_to_image(
    df, 
    output_path='styled_table.png',
    style=style,
    width=800,
    height=600
)

# Enable thousand separators for numbers
df_to_image(
    df,
    output_path='table_with_separators.png',
    thousand_separator=True,  # Add thousand separators (e.g., 1,000,000)
    width=800
)

# Thousand separators in custom style
style_with_separators = TableStyle(
    theme='blue',
    font_size=14,
    thousand_separator=True  # Enable in style
)

df_to_image(
    df,
    output_path='blue_table_with_separators.png',
    style=style_with_separators
)
```

### Thousand Separators Feature

The `thousand_separator` option intelligently adds comma separators to numbers:

- **Automatic detection**: Only applies to numeric values ≥ 1,000
- **Year detection**: Automatically excludes years (1000-2100) from formatting
- **Column awareness**: Skips columns with year-related names (年, year, 年份, etc.)
- **Type handling**: Supports category data conversion and missing values
- **Smart formatting**: Preserves decimal places and handles edge cases

**Examples of formatting:**
- `1234567` → `1,234,567`
- `1999` (year) → `1999` (unchanged)
- `123.45` → `123.45` (too small, unchanged)  
- `12345.67` → `12,345.67`
- Missing values remain empty

## API Reference

### `df_to_image(df, output_path, style=None, width=None, height=None, format='png', thousand_separator=None)`

Convert a pandas DataFrame to an image.

**Parameters:**
- `df` (pandas.DataFrame): The DataFrame to convert
- `output_path` (str): Path where the image will be saved
- `style` (TableStyle, optional): Custom styling options
- `width` (int, optional): Image width in pixels
- `height` (int, optional): Image height in pixels (auto if not specified)
- `format` (str): Image format ('png', 'jpeg', 'webp')
- `thousand_separator` (bool, optional): Add thousand separators to numbers. If None, uses style setting

### `TableStyle`

Customization options for table appearance.

**Parameters:**
- `theme` (str): Theme name ('light', 'dark', 'minimal')
- `font_family` (str): Font family name
- `font_size` (int): Font size in pixels
- `border_color` (str): Border color (CSS color)
- `header_bg_color` (str): Header background color
- `row_bg_colors` (list): Alternating row background colors
- `thousand_separator` (bool): Add thousand separators to numbers (default: False)

## License

MIT License
