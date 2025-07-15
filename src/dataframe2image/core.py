"""
Core functionality for converting DataFrames to images
"""

import asyncio
import re
import tempfile
from pathlib import Path
from typing import Optional, Union, Dict
import numpy as np

import pandas as pd
from playwright.async_api import async_playwright

from .styles import TableStyle, THEMES
from .template import render_dataframe_html


def get_chinese_fonts() -> Dict[str, str]:
    """Get available Chinese fonts from the font directory."""
    font_dir = Path(__file__).parent / "font"
    fonts = {}
    
    if font_dir.exists():
        for font_file in font_dir.glob("*.TTF"):
            # 使用字体文件名作为字体族名称
            font_name = font_file.stem.replace("_", " ")
            fonts[font_name] = str(font_file.absolute())
    
    return fonts


def contains_chinese_characters(df: pd.DataFrame) -> bool:
    """
    Check if the DataFrame contains Chinese characters.
    
    Args:
        df: The pandas DataFrame to check
        
    Returns:
        bool: True if Chinese characters are found, False otherwise
    """
    # Chinese character unicode ranges
    chinese_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\u20000-\u2a6df\u2a700-\u2b73f\u2b740-\u2b81f\u2b820-\u2ceaf]')
    
    # Check column names
    for col in df.columns:
        if isinstance(col, str) and chinese_pattern.search(col):
            return True
    
    # Check index values
    for idx in df.index:
        if isinstance(idx, str) and chinese_pattern.search(idx):
            return True
    
    # Check cell values
    for col in df.columns:
        for value in df[col]:
            if isinstance(value, str) and chinese_pattern.search(value):
                return True
    
    return False


def is_year_like(value) -> bool:
    """
    判断数值是否像年份。
    年份通常在1000-2100之间的整数。
    """
    try:
        if pd.isna(value):
            return False
        num = float(value)
        return (isinstance(value, (int, np.integer)) or num.is_integer()) and 1000 <= num <= 2100
    except (ValueError, TypeError, AttributeError):
        return False


def should_add_thousand_separator(value, column_name: str = "") -> bool:
    """
    判断是否应该为数值添加千分位分隔符。
    
    规则：
    1. 必须是数值类型
    2. 不能是缺失值
    3. 不能是年份格式的数字
    4. 绝对值大于等于1000
    5. 列名不包含"年"、"year"等年份相关词汇
    """
    try:
        if pd.isna(value):
            return False
            
        # 转换为数值
        if isinstance(value, str):
            # 尝试转换字符串为数值
            try:
                num_value = float(value.replace(',', ''))
            except ValueError:
                return False
        else:
            num_value = float(value)
        
        # 检查是否为年份
        if is_year_like(value):
            return False
            
        # 检查列名是否包含年份相关词汇
        year_keywords = ['年', 'year', 'Year', 'YEAR', '年份', '年度']
        for keyword in year_keywords:
            if keyword.lower() in column_name.lower():
                return False
        
        # 只有绝对值大于等于1000的数字才添加千分位
        return abs(num_value) >= 1000
        
    except (ValueError, TypeError, AttributeError):
        return False


def format_number_with_thousand_separator(value, column_name: str = "") -> str:
    """
    为数值添加千分位分隔符。
    
    Args:
        value: 要格式化的值
        column_name: 列名，用于判断是否为年份列
    
    Returns:
        格式化后的字符串
    """
    try:
        if pd.isna(value):
            return ""
        
        # 如果是字符串，尝试转换为数值
        if isinstance(value, str):
            try:
                # 移除已有的逗号分隔符
                clean_str = value.replace(',', '')
                num_value = float(clean_str)
                
                # 如果原字符串不能转换为数值，返回原字符串
                if not clean_str.replace('.', '').replace('-', '').isdigit():
                    return str(value)
            except ValueError:
                return str(value)
        else:
            num_value = float(value)
        
        # 检查是否应该添加千分位分隔符
        if not should_add_thousand_separator(value, column_name):
            # 对于年份或小数值，保持原有格式
            if isinstance(value, float) and not np.isnan(value):
                return f"{value:.2f}" if value != int(value) else str(int(value))
            else:
                return str(value)
        
        # 添加千分位分隔符
        if isinstance(value, float) or (isinstance(value, str) and '.' in value):
            # 保留小数位
            if num_value == int(num_value):
                return f"{int(num_value):,}"
            else:
                return f"{num_value:,.2f}"
        else:
            # 整数
            return f"{int(num_value):,}"
            
    except (ValueError, TypeError, AttributeError):
        return str(value) if value is not None else ""


def preprocess_dataframe_for_formatting(df: pd.DataFrame, add_thousand_separator: bool = False) -> pd.DataFrame:
    """
    预处理DataFrame，处理数值格式化。
    
    Args:
        df: 原始DataFrame
        add_thousand_separator: 是否添加千分位分隔符
    
    Returns:
        处理后的DataFrame
    """
    if not add_thousand_separator:
        return df.copy()
    
    df_formatted = df.copy()
    
    for column in df_formatted.columns:
        # 检查列的数据类型
        col_data = df_formatted[column]
        
        # 处理category类型的数据
        if pd.api.types.is_categorical_dtype(col_data):
            # 尝试将category转换为数值
            try:
                # 先转换为字符串，再尝试转换为数值
                numeric_data = pd.to_numeric(col_data.astype(str), errors='coerce')
                if not numeric_data.isna().all():  # 如果至少有一些值能转换为数值
                    col_data = numeric_data
            except (ValueError, TypeError):
                continue
        
        # 应用千分位格式化
        if pd.api.types.is_numeric_dtype(col_data) or col_data.dtype == 'object':
            df_formatted[column] = col_data.apply(
                lambda x: format_number_with_thousand_separator(x, column)
            )
    
    return df_formatted


async def _capture_table_screenshot(
    html_content: str,
    output_path: Union[str, Path],
    width: Optional[int] = None,
    height: Optional[int] = None,
    format: str = "png"
) -> None:
    """Capture screenshot of HTML table using Playwright."""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Set a larger default viewport to ensure all content is visible
        if width:
            viewport_height = height or 1200  # 增大默认高度
            await page.set_viewport_size({"width": width, "height": viewport_height})
        else:
            # 如果没有指定宽度，设置一个较大的默认视窗
            await page.set_viewport_size({"width": 1200, "height": 1200})
        
        # Load HTML content
        await page.set_content(html_content)
        
        # Wait for content to load and ensure all elements are rendered
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(1000)  # 额外等待确保渲染完成
        
        # Find the table container element
        table_element = await page.query_selector('.table-container')
        
        if table_element:
            # Screenshot just the table
            screenshot_options = {"path": str(output_path)}
            if format in ["png", "jpeg"]:
                screenshot_options["type"] = format
            await table_element.screenshot(**screenshot_options)
        else:
            # Fallback: screenshot the entire page
            screenshot_options = {"path": str(output_path), "full_page": True}
            if format in ["png", "jpeg"]:
                screenshot_options["type"] = format
            await page.screenshot(**screenshot_options)
        
        await browser.close()


def df_to_image(
    df: pd.DataFrame,
    output_path: Union[str, Path],
    style: Optional[Union[str, TableStyle]] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    format: str = "png",
    show_index: bool = True,
    thousand_separator: Optional[bool] = None
) -> None:
    """
    Convert a pandas DataFrame to a table image.
    
    Args:
        df: The pandas DataFrame to convert
        output_path: Path where the image will be saved
        style: Either a TableStyle object or theme name string
        width: Image width in pixels (optional)
        height: Image height in pixels (optional)
        format: Image format ('png', 'jpeg', 'webp')
        show_index: Whether to show the DataFrame index
        thousand_separator: Whether to add thousand separators to numbers.
                          If None, will use the style's thousand_separator setting.
    
    Raises:
        ValueError: If the DataFrame is empty or invalid format specified
        RuntimeError: If screenshot capture fails
    """
    
    if df.empty:
        raise ValueError("DataFrame is empty")
    
    if format.lower() not in ["png", "jpeg", "webp"]:
        raise ValueError(f"Unsupported format: {format}")
    
    # Note: Playwright only supports png and jpeg for element screenshots
    # WebP format will be saved as PNG with webp extension for compatibility
    actual_format = format.lower() if format.lower() in ["png", "jpeg"] else "png"
    
    # Handle style parameter
    if isinstance(style, str):
        if style in THEMES:
            style = THEMES[style]
        else:
            raise ValueError(f"Unknown theme: {style}")
    elif style is None:
        style = TableStyle()
    
    # 处理千分位分隔符设置
    if thousand_separator is not None:
        style.thousand_separator = thousand_separator
    
    # 预处理DataFrame以应用格式化
    df_processed = preprocess_dataframe_for_formatting(df, style.thousand_separator)
    
    # 自动检测中文字符并设置字体
    font_files = None
    if contains_chinese_characters(df_processed):
        font_files = get_chinese_fonts()
        if font_files:
            # 使用方正兰亭圆字体作为主要字体
            chinese_font_names = list(font_files.keys())
            style.font_family = f"'{chinese_font_names[0]}', 'Microsoft YaHei', 'SimHei', sans-serif"
    
    # Render HTML
    try:
        html_content = render_dataframe_html(df_processed, style, show_index, font_files)
    except Exception as e:
        raise RuntimeError(f"Failed to render HTML: {e}")
    
    # Convert to image
    try:
        asyncio.run(_capture_table_screenshot(
            html_content, output_path, width, height, actual_format
        ))
    except Exception as e:
        raise RuntimeError(f"Failed to capture screenshot: {e}")


def df_to_html(
    df: pd.DataFrame,
    style: Optional[Union[str, TableStyle]] = None,
    show_index: bool = True,
    thousand_separator: Optional[bool] = None
) -> str:
    """
    Convert a pandas DataFrame to styled HTML.
    
    Args:
        df: The pandas DataFrame to convert
        style: Either a TableStyle object or theme name string
        show_index: Whether to show the DataFrame index
        thousand_separator: Whether to add thousand separators to numbers.
                          If None, will use the style's thousand_separator setting.
    
    Returns:
        HTML string of the styled table
    """
    
    if df.empty:
        raise ValueError("DataFrame is empty")
    
    # Handle style parameter
    if isinstance(style, str):
        if style in THEMES:
            style = THEMES[style]
        else:
            raise ValueError(f"Unknown theme: {style}")
    elif style is None:
        style = TableStyle()
    
    # 处理千分位分隔符设置
    if thousand_separator is not None:
        style.thousand_separator = thousand_separator
    
    # 预处理DataFrame以应用格式化
    df_processed = preprocess_dataframe_for_formatting(df, style.thousand_separator)
    
    # 自动检测中文字符并设置字体
    font_files = None
    if contains_chinese_characters(df_processed):
        font_files = get_chinese_fonts()
        if font_files:
            # 使用方正兰亭圆字体作为主要字体
            chinese_font_names = list(font_files.keys())
            style.font_family = f"'{chinese_font_names[0]}', 'Microsoft YaHei', 'SimHei', sans-serif"
    
    return render_dataframe_html(df_processed, style, show_index, font_files)


def save_temp_html(html_content: str) -> str:
    """Save HTML content to a temporary file and return the path."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        return f.name
