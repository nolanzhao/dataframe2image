"""
Example usage of dataframe2image package
"""

import pandas as pd
from dataframe2image import df_to_image, df_to_html, TableStyle

# Create sample data
def create_sample_data():
    """Create a sample DataFrame."""
    data = {
        'Product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'],
        'Brand': ['Apple', 'Logitech', 'Corsair', 'Dell', 'Sony'],
        'Price': [1299.99, 29.99, 129.99, 299.99, 199.99],
        'Rating': [4.8, 4.5, 4.7, 4.6, 4.4],
        'In Stock': [True, True, False, True, True]
    }
    return pd.DataFrame(data)

def create_chinese_sample_data():
    """Create a sample DataFrame with Chinese content."""
    data = {
        '产品名称': ['苹果MacBook Pro', '罗技鼠标', '海盗船键盘', '戴尔显示器', '索尼耳机'],
        '品牌': ['苹果', '罗技', '海盗船', '戴尔', '索尼'],
        '价格(元)': [12999.00, 299.00, 899.00, 2999.00, 1599.00],
        '评分': [4.8, 4.5, 4.7, 4.6, 4.4],
        '库存状态': ['有货', '有货', '缺货', '有货', '有货'],
        '销售地区': ['全国', '华东', '华北', '华南', '西部']
    }
    return pd.DataFrame(data)

def example_basic_usage():
    """Basic usage example."""
    print("🔄 Creating basic table image...")
    
    df = create_sample_data()
    df_to_image(df, 'basic_table.png')
    print("✅ Basic table saved as 'basic_table.png'")

def example_styled_tables():
    """Create tables with different styles."""
    print("🔄 Creating styled tables...")
    
    df = create_sample_data()
    
    # Light theme (default)
    df_to_image(df, 'table_light.png', style='light')
    print("✅ Light theme table saved as 'table_light.png'")
    
    # Dark theme
    df_to_image(df, 'table_dark.png', style='dark')
    print("✅ Dark theme table saved as 'table_dark.png'")
    
    # Minimal theme
    df_to_image(df, 'table_minimal.png', style='minimal')
    print("✅ Minimal theme table saved as 'table_minimal.png'")
    
    # Blue theme
    df_to_image(df, 'table_blue.png', style='blue')
    print("✅ Blue theme table saved as 'table_blue.png'")
    
    # Green theme
    df_to_image(df, 'table_green.png', style='green')
    print("✅ Green theme table saved as 'table_green.png'")

def example_custom_style():
    """Create table with custom styling."""
    print("🔄 Creating custom styled table...")
    
    df = create_sample_data()
    
    # Custom style
    custom_style = TableStyle(
        font_family='Georgia, serif',
        font_size=14,
        header_bg_color='#8B5CF6',
        header_text_color='#FFFFFF',
        row_bg_colors=['#F8FAFC', '#F1F5F9'],
        border_color='#8B5CF6',
        cell_padding='12px 16px',
        table_border_radius='12px',
        box_shadow='0 4px 12px rgba(139, 92, 246, 0.3)'
    )
    
    df_to_image(
        df, 
        'table_custom.png', 
        style=custom_style,
        width=900
    )
    print("✅ Custom styled table saved as 'table_custom.png'")

def example_different_formats():
    """Create tables in different image formats."""
    print("🔄 Creating tables in different formats...")
    
    df = create_sample_data()
    
    # PNG format
    df_to_image(df, 'table.png', format='png')
    print("✅ PNG format table saved as 'table.png'")
    
    # JPEG format
    df_to_image(df, 'table.jpeg', format='jpeg')
    print("✅ JPEG format table saved as 'table.jpeg'")
    
    # WebP format
    df_to_image(df, 'table.webp', format='webp')
    print("✅ WebP format table saved as 'table.webp'")

def example_html_output():
    """Generate HTML output."""
    print("🔄 Creating HTML output...")
    
    df = create_sample_data()
    
    # Generate HTML
    html_content = df_to_html(df, style='blue')
    
    # Save to file
    with open('table.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ HTML table saved as 'table.html'")

def example_large_dataset():
    """Example with larger dataset."""
    print("🔄 Creating table from larger dataset...")
    
    # Create larger dataset
    import numpy as np
    
    np.random.seed(42)
    large_data = {
        'ID': range(1, 21),
        'Name': [f'User_{i}' for i in range(1, 21)],
        'Age': np.random.randint(18, 65, 20),
        'Salary': np.random.randint(30000, 120000, 20),
        'Department': np.random.choice(['Engineering', 'Sales', 'Marketing', 'HR'], 20),
        'Score': np.round(np.random.uniform(3.0, 5.0, 20), 2)
    }
    
    large_df = pd.DataFrame(large_data)
    
    # Create table with custom dimensions
    df_to_image(
        large_df, 
        'large_table.png',
        style='minimal',
        width=1000,
        show_index=False
    )
    print("✅ Large table saved as 'large_table.png'")

def example_financial_data():
    """Example with financial data formatting."""
    print("🔄 Creating financial data table...")
    
    # Financial data
    financial_data = {
        'Stock': ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'],
        'Price': [150.25, 2750.80, 310.45, 3200.15, 850.90],
        'Change': [+2.15, -15.30, +5.25, +25.75, -12.50],
        'Change %': ['+1.45%', '-0.55%', '+1.72%', '+0.81%', '-1.45%'],
        'Volume': ['52.3M', '1.2M', '28.7M', '3.1M', '25.8M'],
        'Market Cap': ['2.45T', '1.65T', '2.30T', '1.55T', '850B']
    }
    
    financial_df = pd.DataFrame(financial_data)
    
    # Green theme for financial data
    financial_style = TableStyle(
        font_family='Monaco, monospace',
        font_size=13,
        header_bg_color='#059669',
        header_text_color='#FFFFFF',
        row_bg_colors=['#F0FDF4', '#ECFDF5'],
        border_color='#059669'
    )
    
    df_to_image(
        financial_df,
        'financial_table.png',
        style=financial_style,
        width=800,
        show_index=False
    )
    print("✅ Financial table saved as 'financial_table.png'")

def example_chinese_support():
    """Example with automatic Chinese character detection."""
    print("🔄 Creating Chinese table with automatic font detection...")
    
    df = create_chinese_sample_data()
    
    # 自动检测中文字符并生成表格图片
    df_to_image(df, 'table_chinese.png')
    print("✅ Chinese table saved as 'table_chinese.png'")
    
    # 创建不同主题的中文表格
    themes = ['light', 'dark', 'blue', 'green']
    for theme in themes:
        filename = f'table_chinese_{theme}.png'
        df_to_image(df, filename, style=theme)
        print(f"✅ Chinese {theme} theme table saved as '{filename}'")
    
    # 生成HTML文件用于预览
    html_content = df_to_html(df)
    with open('table_chinese.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("✅ Chinese HTML table saved as 'table_chinese.html'")

def main():
    """Run all examples."""
    print("🚀 Running dataframe2image examples...\n")
    
    try:
        example_basic_usage()
        print()
        
        example_styled_tables()
        print()
        
        example_custom_style()
        print()
        
        example_different_formats()
        print()
        
        example_html_output()
        print()
        
        example_large_dataset()
        print()
        
        example_financial_data()
        print()
        
        example_chinese_support()
        print()
        
        print("🎉 All examples completed successfully!")
        print("📁 Check the current directory for generated images and HTML files.")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")

if __name__ == "__main__":
    main()
