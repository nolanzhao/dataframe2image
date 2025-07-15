"""
示例：展示千分位分隔符功能的用法
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dataframe2image import df_to_image, TableStyle

def create_sample_data():
    """创建测试数据，包含各种数值类型和场景"""
    data = {
        '公司名称': ['阿里巴巴', '腾讯控股', '华为技术', '字节跳动', '美团点评'],
        '年份': [2019, 2020, 2021, 2022, 2023],  # 年份格式，不应该添加千分位
        '营收(万元)': [377289, 481277, 562119, 745215, 808500],  # 大数值，应该添加千分位
        '员工数': [12500, 8600, 19500, 11000, 6800],  # 中等数值，应该添加千分位
        '成立年份': [1999, 1998, 1987, 2012, 2010],  # 年份相关，不应该添加千分位
        '市值(亿美元)': [458.7, 635.2, 0, 140.0, 128.5],  # 包含小数和0值
        '小数值': [123, 456, 789, 234, 567],  # 小于1000的数值，不应该添加千分位
        '文本数据': ['A级', 'B级', 'A+级', 'B+级', 'A级'],  # 非数值数据
        '缺失数据': [1250000, np.nan, 3450000, np.nan, 5670000],  # 包含缺失值
    }
    
    df = pd.DataFrame(data)
    
    # 添加category类型的列进行测试
    df['评级数值'] = pd.Categorical([1, 2, 3, 2, 1])
    df['评级金额'] = pd.Categorical([15000, 25000, 35000, 20000, 18000])
    
    return df

def main():
    # 创建测试数据
    df = create_sample_data()
    
    print("原始数据:")
    print(df)
    print(f"\n数据类型:")
    print(df.dtypes)
    
    # 不使用千分位分隔符
    print("\n生成不带千分位分隔符的图片...")
    df_to_image(
        df,
        output_path='no_separator.png',
        thousand_separator=False,
        width=1000
    )
    
    # 使用千分位分隔符
    print("生成带千分位分隔符的图片...")
    df_to_image(
        df,
        output_path='with_separator.png',
        thousand_separator=True,
        width=1000
    )
    
    # 使用自定义样式和千分位分隔符
    print("生成带自定义样式和千分位分隔符的图片...")
    custom_style = TableStyle(
        theme='blue',
        font_size=14,
        thousand_separator=True  # 在样式中设置
    )
    
    df_to_image(
        df,
        output_path='custom_style_with_separator.png',
        style=custom_style,
        width=1000
    )
    
    print("完成！生成的图片文件:")
    print("- no_separator.png (不带千分位)")
    print("- with_separator.png (带千分位)")
    print("- custom_style_with_separator.png (自定义样式+千分位)")

if __name__ == "__main__":
    main()
