"""
中文表格示例 - 自动检测中文字符
Chinese Table Example - Automatic Chinese Character Detection
"""

import pandas as pd
import sys
import os

# 添加父目录到路径以便导入dataframe2image
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dataframe2image import df_to_image, df_to_html, TableStyle

def create_chinese_company_data():
    """创建中文公司数据示例"""
    data = {
        '公司名称': [
            '阿里巴巴集团',
            '腾讯控股有限公司', 
            '百度在线网络技术',
            '京东集团股份有限公司',
            '美团点评',
            '字节跳动科技有限公司'
        ],
        '行业类别': [
            '电子商务',
            '社交媒体',
            '搜索引擎',
            '零售电商',
            '本地生活服务',
            '短视频/社交'
        ],
        '成立年份': [1999, 1998, 2000, 1998, 2010, 2012],
        '员工数量': [245000, 112771, 41000, 540000, 60000, 110000],
        '市值(亿美元)': [476.5, 583.8, 45.2, 78.9, 156.3, 220.0],
        '主要产品': [
            '淘宝/天猫/支付宝',
            '微信/QQ/腾讯云',
            '百度搜索/百度地图',
            '京东商城/京东物流',
            '美团外卖/大众点评',
            '抖音/今日头条'
        ]
    }
    return pd.DataFrame(data)

def create_chinese_financial_data():
    """创建中文财务数据示例"""
    data = {
        '季度': ['2023Q1', '2023Q2', '2023Q3', '2023Q4'],
        '营业收入(亿元)': [2580.35, 2876.42, 3122.89, 3456.78],
        '净利润(亿元)': [456.23, 523.67, 678.45, 789.12],
        '毛利率(%)': [45.6, 47.2, 48.8, 49.3],
        '同比增长率(%)': [12.5, 15.3, 18.7, 21.2],
        '市场份额(%)': [28.5, 29.8, 31.2, 32.6]
    }
    return pd.DataFrame(data)

def main():
    """运行中文表格示例"""
    print("🚀 开始生成中文表格示例...\n")
    
    # 示例1: 中国科技公司数据
    print("📊 生成中国科技公司数据表格...")
    company_df = create_chinese_company_data()
    
    # 使用不同主题生成表格
    themes = {
        'light': '浅色主题',
        'dark': '深色主题', 
        'blue': '蓝色主题',
        'green': '绿色主题'
    }
    
    for theme_key, theme_name in themes.items():
        filename = f'chinese_companies_{theme_key}.png'
        df_to_image(
            company_df, 
            filename, 
            style=theme_key, 
            width=1000
        )
        print(f"✅ {theme_name}表格已保存为 '{filename}'")
    
    print()
    
    # 示例2: 财务数据
    print("💰 生成财务数据表格...")
    financial_df = create_chinese_financial_data()
    
    df_to_image(
        financial_df,
        'chinese_financial.png',
        style='blue',
        width=800
    )
    print("✅ 财务数据表格已保存为 'chinese_financial.png'")
    
    print()
    
    # 示例3: 自定义样式的中文表格
    print("🎨 生成自定义样式的中文表格...")
    
    # 创建自定义样式
    custom_style = TableStyle(
        font_size=14,
        header_bg_color="#FF6B6B",
        header_text_color="#FFFFFF", 
        row_bg_colors=["#FFFFFF", "#FFF5F5"],
        border_color="#FF6B6B",
        cell_padding="12px 16px"
    )
    
    df_to_image(
        company_df,
        'chinese_custom_style.png',
        style=custom_style,
        width=1200
    )
    print("✅ 自定义样式表格已保存为 'chinese_custom_style.png'")
    
    print()
    
    # 示例4: 生成HTML文件
    print("🌐 生成HTML文件...")
    
    html_content = df_to_html(
        company_df,
        style='light'
    )
    
    with open('chinese_companies.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("✅ HTML文件已保存为 'chinese_companies.html'")
    
    print()
    print("🎉 所有中文表格示例生成完成!")
    print("📁 请查看当前目录中生成的图片和HTML文件")
    print()
    print("💡 提示:")
    print("  - 库会自动检测DataFrame中的中文字符")
    print("  - 当检测到中文字符时，自动使用 src/dataframe2image/font 目录中的方正兰亭圆字体")
    print("  - 支持所有主题样式和自定义样式，无需手动配置")

if __name__ == "__main__":
    main()
