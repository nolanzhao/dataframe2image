"""
简单测试：验证千分位分隔符的各种场景
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dataframe2image.core import (
    should_add_thousand_separator,
    format_number_with_thousand_separator,
    is_year_like,
    preprocess_dataframe_for_formatting
)

def test_individual_functions():
    """测试各个辅助函数"""
    print("=== 测试辅助函数 ===")
    
    # 测试年份判断
    print("\n1. 年份判断测试:")
    test_values = [1999, 2023, 123, 5000, 1500, 2100, 999, 2101]
    for val in test_values:
        result = is_year_like(val)
        print(f"  {val} -> 是年份: {result}")
    
    # 测试是否应该添加千分位
    print("\n2. 千分位判断测试:")
    test_cases = [
        (1234, "价格"),
        (1999, "年份"),
        (123, "数量"),
        (50000, "营收"),
        (2020, "year"),
        (15000, "年收入"),
        (12345.67, "金额")
    ]
    
    for value, column in test_cases:
        result = should_add_thousand_separator(value, column)
        print(f"  {value} (列名: {column}) -> 添加千分位: {result}")
    
    # 测试格式化函数
    print("\n3. 格式化测试:")
    for value, column in test_cases:
        formatted = format_number_with_thousand_separator(value, column)
        print(f"  {value} -> {formatted}")

def test_dataframe_processing():
    """测试DataFrame预处理"""
    print("\n=== 测试DataFrame预处理 ===")
    
    # 创建测试数据
    data = {
        '产品名称': ['产品A', '产品B', '产品C'],
        '年份': [2020, 2021, 2022],
        '销售额': [1234567, 987654, 2345678],
        '年sales': [1500000, 2000000, 1800000],  # 包含年字的列
        '小额费用': [123, 456, 789],  # 小于1000的数值
        'category_data': pd.Categorical([1500, 2500, 3500]),  # category类型
        '缺失数据': [1000000, np.nan, 2000000]
    }
    
    df = pd.DataFrame(data)
    print("\n原始DataFrame:")
    print(df)
    print(f"\n数据类型:")
    print(df.dtypes)
    
    # 应用千分位处理
    df_formatted = preprocess_dataframe_for_formatting(df, add_thousand_separator=True)
    print("\n格式化后的DataFrame:")
    print(df_formatted)

if __name__ == "__main__":
    test_individual_functions()
    test_dataframe_processing()
