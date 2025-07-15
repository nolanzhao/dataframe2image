# dataframe2image API Reference

## Core Functions

### `df_to_image()`

Convert a pandas DataFrame to a table image.

```python
def df_to_image(
    df: pd.DataFrame,
    output_path: Union[str, Path],
    style: Optional[Union[str, TableStyle]] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    format: str = "png",
    show_index: bool = True
) -> None
```

**Parameters:**

- `df` (pandas.DataFrame): The DataFrame to convert
- `output_path` (str | Path): Path where the image will be saved
- `style` (str | TableStyle, optional): Either a theme name or TableStyle object
- `width` (int, optional): Image width in pixels
- `height` (int, optional): Image height in pixels (auto-calculated if not specified)
- `format` (str): Image format - 'png', 'jpeg', or 'webp' (default: 'png')
- `show_index` (bool): Whether to show the DataFrame index (default: True)

**Raises:**

- `ValueError`: If DataFrame is empty or format is unsupported
- `RuntimeError`: If screenshot capture fails

**Example:**

```python
import pandas as pd
from df2img import df_to_image

df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df_to_image(df, 'table.png')
```

### `df_to_html()`

Convert a pandas DataFrame to styled HTML.

```python
def df_to_html(
    df: pd.DataFrame,
    style: Optional[Union[str, TableStyle]] = None,
    show_index: bool = True
) -> str
```

**Parameters:**

- `df` (pandas.DataFrame): The DataFrame to convert
- `style` (str | TableStyle, optional): Either a theme name or TableStyle object
- `show_index` (bool): Whether to show the DataFrame index (default: True)

**Returns:**

- `str`: HTML string of the styled table

**Example:**

```python
from df2img import df_to_html

html = df_to_html(df, style='dark')
with open('table.html', 'w') as f:
    f.write(html)
```

## TableStyle Class

Configure the appearance of your tables.

```python
@dataclass
class TableStyle:
    theme: str = "light"
    font_family: str = "Arial, sans-serif"
    font_size: int = 12
    border_color: str = "#ddd"
    header_bg_color: str = "#f8f9fa"
    header_text_color: str = "#212529"
    row_bg_colors: Optional[List[str]] = None
    row_text_color: str = "#212529"
    border_width: int = 1
    cell_padding: str = "8px 12px"
    table_border_radius: str = "6px"
    box_shadow: str = "0 2px 8px rgba(0,0,0,0.1)"
```

**Parameters:**

- `theme` (str): Predefined theme name ('light', 'dark', 'minimal', 'blue', 'green')
- `font_family` (str): CSS font family
- `font_size` (int): Font size in pixels
- `border_color` (str): Border color (CSS color)
- `header_bg_color` (str): Header background color
- `header_text_color` (str): Header text color
- `row_bg_colors` (List[str], optional): Alternating row background colors
- `row_text_color` (str): Row text color
- `border_width` (int): Border width in pixels
- `cell_padding` (str): Cell padding (CSS padding)
- `table_border_radius` (str): Table border radius
- `box_shadow` (str): Table box shadow

**Example:**

```python
from df2img import TableStyle, df_to_image

style = TableStyle(
    theme='custom',
    font_size=16,
    header_bg_color='#FF6B6B',
    row_bg_colors=['#FFE0E0', '#FFF0F0']
)

df_to_image(df, 'custom_table.png', style=style)
```

## Predefined Themes

### Light Theme (default)
- Clean, professional appearance
- Light background with subtle borders
- Good for reports and documentation

### Dark Theme
- Dark background with light text
- Good for presentations or dark mode interfaces

### Minimal Theme
- Very clean, borderless design
- Minimal styling for modern look

### Blue Theme
- Blue header with light blue accents
- Professional corporate look

### Green Theme
- Green header with light green accents
- Good for financial or growth data

## Usage Examples

### Basic Usage

```python
import pandas as pd
from df2img import df_to_image

# Simple DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob'],
    'Age': [25, 30],
    'City': ['NYC', 'LA']
})

# Generate image
df_to_image(df, 'basic.png')
```

### Custom Styling

```python
from df2img import df_to_image, TableStyle

# Custom style
style = TableStyle(
    font_family='Georgia, serif',
    font_size=14,
    header_bg_color='#2E86AB',
    header_text_color='white',
    row_bg_colors=['#F8F9FA', '#E9ECEF']
)

df_to_image(df, 'styled.png', style=style, width=800)
```

### Different Formats

```python
# PNG (default)
df_to_image(df, 'table.png')

# JPEG
df_to_image(df, 'table.jpg', format='jpeg')

# WebP
df_to_image(df, 'table.webp', format='webp')
```

### Without Index

```python
df_to_image(df, 'no_index.png', show_index=False)
```

## Error Handling

The library provides clear error messages for common issues:

```python
try:
    df_to_image(empty_df, 'output.png')
except ValueError as e:
    print(f"Error: {e}")  # "DataFrame is empty"

try:
    df_to_image(df, 'output.xyz', format='xyz')
except ValueError as e:
    print(f"Error: {e}")  # "Unsupported format: xyz"
```

## Performance Tips

1. **Image Size**: Larger images take more time to generate
2. **Format Choice**: PNG provides best quality, JPEG smallest size
3. **Browser Resources**: The library uses Chromium, which requires adequate memory
4. **Large DataFrames**: Consider pagination for very large datasets

## Browser Requirements

The library uses Playwright with Chromium. After installing the package:

```bash
playwright install chromium
```

This downloads the required browser binaries (~100MB).
