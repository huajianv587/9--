#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Capital IQ数据质量检查脚本
用于验证亚太市场分析师盈利惊喜预测数据的可行性
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# 设置中文字体（如果需要）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

def main():
    # 检查文件是否存在
    data_file = 'data/pilot/pilot_sample_50.csv'

    if not os.path.exists(data_file):
        print(f"❌ 错误：找不到数据文件 {data_file}")
        print(f"   请先从Capital IQ导出数据并保存到该路径")
        sys.exit(1)

    # 读取数据
    try:
        df = pd.read_csv(data_file)
    except Exception as e:
        print(f"❌ 读取数据失败: {e}")
        sys.exit(1)

    print("=" * 60)
    print("数据质量检查报告")
    print("=" * 60)

    # 检查1：基本信息
    print("\n【1. 基本信息】")
    print(f"总行数: {len(df)}")
    print(f"公司数: {df['Company ID'].nunique()}")

    if 'Report Date' in df.columns:
        print(f"时间范围: {df['Report Date'].min()} 到 {df['Report Date'].max()}")

    avg_quarters = len(df) / df['Company ID'].nunique()
    print(f"平均每家公司的季度数: {avg_quarters:.1f}")

    # 检查2：缺失率
    print("\n【2. 关键字段缺失率】")
    critical_fields = ['EPS Actual', 'EPS Mean Estimate', 'Number of Analysts']

    for field in critical_fields:
        if field in df.columns:
            missing_rate = df[field].isnull().sum() / len(df) * 100
            status = "✅" if missing_rate < 15 else "🔴"
            print(f"{status} {field}: {missing_rate:.1f}% 缺失")
        else:
            print(f"⚠️  {field}: 字段不存在")

    # 检查3：分析师覆盖度
    print("\n【3. 分析师覆盖度】")
    if 'Number of Analysts' in df.columns:
        analyst_stats = df['Number of Analysts'].describe()
        print(f"最小值: {analyst_stats['min']:.0f}")
        print(f"25%分位: {analyst_stats['25%']:.0f}")
        print(f"中位数: {analyst_stats['50%']:.0f}")
        print(f"75%分位: {analyst_stats['75%']:.0f}")
        print(f"最大值: {analyst_stats['max']:.0f}")

        # 判断
        if analyst_stats['50%'] >= 2:
            print("✅ 中位数 ≥ 2，覆盖度合格")
        else:
            print("🔴 中位数 < 2，覆盖度不足")
    else:
        print("⚠️  找不到 'Number of Analysts' 字段")

    # 检查4：Surprise分布
    print("\n【4. Earnings Surprise分布】")
    if 'EPS Actual' in df.columns and 'EPS Mean Estimate' in df.columns:
        # 计算surprise
        df['surprise'] = df['EPS Actual'] - df['EPS Mean Estimate']
        df['surprise_direction'] = np.sign(df['surprise'])

        # 统计
        surprise_counts = df['surprise_direction'].value_counts()
        total = len(df[df['surprise_direction'].notna()])

        pos_count = surprise_counts.get(1.0, 0)
        neg_count = surprise_counts.get(-1.0, 0)
        zero_count = surprise_counts.get(0.0, 0)

        print(f"正惊喜（实际>预测）: {pos_count} ({pos_count/total*100:.1f}%)")
        print(f"负惊喜（实际<预测）: {neg_count} ({neg_count/total*100:.1f}%)")
        print(f"无惊喜（实际=预测）: {zero_count} ({zero_count/total*100:.1f}%)")

        # 判断样本平衡性
        positive_ratio = pos_count / total if total > 0 else 0
        if 0.4 <= positive_ratio <= 0.6:
            print("✅ 正负样本相对均衡")
        else:
            print("⚠️  样本不平衡，可能需要处理")
    else:
        print("⚠️  找不到EPS字段，无法计算surprise")

    # 检查5：跨市场分布
    print("\n【5. 市场分布】")
    if 'Country' in df.columns:
        market_counts = df.groupby('Country')['Company ID'].nunique()
        print(market_counts)

        # 判断
        if len(market_counts) >= 3:
            print("✅ 覆盖3个市场")
        else:
            print("⚠️  市场覆盖不足")
    else:
        print("⚠️  找不到 'Country' 字段")

    # 检查6：异常值
    print("\n【6. 异常值检查】")
    if 'surprise' in df.columns and 'EPS Mean Estimate' in df.columns:
        # 计算相对surprise
        df['surprise_pct'] = df['surprise'] / df['EPS Mean Estimate'].abs() * 100

        # 找极端值
        extreme = df[df['surprise_pct'].abs() > 200]
        print(f"极端异常值（surprise > 200%）: {len(extreme)} 条")

        if len(extreme) > len(df) * 0.05:
            print("⚠️  异常值较多，需要检查数据质量")
        else:
            print("✅ 异常值在合理范围")

    # 生成可视化
    print("\n【7. 生成可视化】")
    try:
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        # 图1：分析师覆盖度分布
        if 'Number of Analysts' in df.columns:
            axes[0, 0].hist(df['Number of Analysts'].dropna(), bins=20, edgecolor='black')
            axes[0, 0].set_title('Analyst Coverage Distribution')
            axes[0, 0].set_xlabel('Number of Analysts')
            axes[0, 0].set_ylabel('Frequency')

        # 图2：Surprise方向分布
        if 'surprise_direction' in df.columns:
            surprise_counts.plot(kind='bar', ax=axes[0, 1], color=['red', 'gray', 'green'])
            axes[0, 1].set_title('Surprise Direction Distribution')
            axes[0, 1].set_xlabel('Direction (-1: Negative, 0: Zero, 1: Positive)')
            axes[0, 1].set_ylabel('Count')
            axes[0, 1].tick_params(axis='x', rotation=0)

        # 图3：市场分布
        if 'Country' in df.columns:
            market_counts.plot(kind='bar', ax=axes[1, 0], color='steelblue')
            axes[1, 0].set_title('Company Distribution by Market')
            axes[1, 0].set_xlabel('Market')
            axes[1, 0].set_ylabel('Number of Companies')
            axes[1, 0].tick_params(axis='x', rotation=45)

        # 图4：Surprise幅度分布
        if 'surprise_pct' in df.columns:
            # 去除极端值后绘图
            surprise_clean = df['surprise_pct'].dropna()
            surprise_clean = surprise_clean[(surprise_clean > -100) & (surprise_clean < 100)]
            axes[1, 1].hist(surprise_clean, bins=30, edgecolor='black')
            axes[1, 1].set_title('Surprise Magnitude Distribution')
            axes[1, 1].set_xlabel('Surprise (%)')
            axes[1, 1].set_ylabel('Frequency')

        plt.tight_layout()

        # 创建输出目录
        os.makedirs('data/pilot', exist_ok=True)
        plt.savefig('data/pilot/data_quality_report.png', dpi=300)
        print("✅ 可视化已保存到: data/pilot/data_quality_report.png")
    except Exception as e:
        print(f"⚠️  生成可视化失败: {e}")

    # 最终判断
    print("\n" + "=" * 60)
    print("【最终判断】")
    print("=" * 60)

    # 计算通过的检查项
    checks_passed = 0
    total_checks = 5

    # 检查1：样本量
    if df['Company ID'].nunique() >= 40:  # 50家公司的80%
        checks_passed += 1
        print("✅ 检查1：样本量充足")
    else:
        print("🔴 检查1：样本量不足")

    # 检查2：缺失率
    if 'EPS Actual' in df.columns:
        missing_rate = df['EPS Actual'].isnull().sum() / len(df)
        if missing_rate < 0.15:
            checks_passed += 1
            print("✅ 检查2：EPS数据缺失率合格")
        else:
            print("🔴 检查2：EPS数据缺失率过高")
    else:
        print("🔴 检查2：找不到EPS Actual字段")

    # 检查3：分析师覆盖
    if 'Number of Analysts' in df.columns:
        if df['Number of Analysts'].median() >= 2:
            checks_passed += 1
            print("✅ 检查3：分析师覆盖度合格")
        else:
            print("🔴 检查3：分析师覆盖度不足")
    else:
        print("🔴 检查3：找不到Number of Analysts字段")

    # 检查4：时间跨度
    avg_quarters = len(df) / df['Company ID'].nunique()
    if avg_quarters >= 12:
        checks_passed += 1
        print("✅ 检查4：时间跨度充足")
    else:
        print("🔴 检查4：时间跨度不足")

    # 检查5：市场覆盖
    if 'Country' in df.columns:
        if df['Country'].nunique() >= 3:
            checks_passed += 1
            print("✅ 检查5：市场覆盖充足")
        else:
            print("🔴 检查5：市场覆盖不足")
    else:
        print("🔴 检查5：找不到Country字段")

    print(f"\n通过检查项: {checks_passed}/{total_checks}")

    if checks_passed >= 4:
        print("\n🎉 结论：数据质量良好，可以继续方向一")
        print("   下一步：扩大样本到全量（250+公司）")
    elif checks_passed >= 3:
        print("\n⚠️  结论：数据质量一般，需要调整筛选条件")
        print("   建议：降低市值要求或扩大地域范围")
    else:
        print("\n🔴 结论：数据质量不足，建议切换到方向四（破产预测）")
        print("   原因：亚太市场的分析师覆盖度可能不如预期")

    print("\n" + "=" * 60)
    print("检查完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
