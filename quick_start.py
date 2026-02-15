#!/usr/bin/env python3
"""
快速下载指定公司的年报
使用方法: python3 quick_start.py <股票代码>
例如: python3 quick_start.py 688777
"""

import os
import sys

from spider import Download, sseAnnual, szseAnnual, saving_path


def download_annual_report(stock_code):
    """下载指定股票的年报"""

    print(f"\n{'=' * 60}")
    print(f"开始下载 {stock_code} 的年度报告")
    print(f"{'=' * 60}\n")

    # 尝试沪市
    print("1. 查询沪市（SSE）...")
    announcements_sse = sseAnnual(1, stock_code)

    # 尝试深市
    print("2. 查询深市（SZSE）...")
    announcements_szse = szseAnnual(1, stock_code)

    all_announcements = []
    if announcements_sse:
        all_announcements.extend(announcements_sse)
        print(f"   ✓ 找到 {len(announcements_sse)} 条沪市公告")
    if announcements_szse:
        all_announcements.extend(announcements_szse)
        print(f"   ✓ 找到 {len(announcements_szse)} 条深市公告")

    if not all_announcements:
        print(f"\n✗ 未找到 {stock_code} 的任何公告")
        print("  请确认股票代码是否正确")
        return False

    print(f"\n总共找到 {len(all_announcements)} 条公告")
    print(f"\n{'=' * 60}")
    print("开始下载PDF文件...")
    print(f"{'=' * 60}\n")

    # 下载PDF
    Download(all_announcements)

    print(f"\n{'=' * 60}")
    print("✓ 下载完成！")
    print(f"{'=' * 60}")
    print(f"\nPDF文件保存在: {saving_path}")
    print("\n下一步:")
    print("  1. 转换PDF为文本: python3 pdf2txt.py")
    print("  2. 统计关键词: python3 main.py")

    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python3 quick_start.py <股票代码>")
        print("\n示例:")
        print("  python3 quick_start.py 000888  # 峨眉山旅游")
        sys.exit(1)

    stock_code = sys.argv[1]

    # 创建必要的目录（使用脚本所在目录）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(script_dir, "pdf"), exist_ok=True)
    os.makedirs(os.path.join(script_dir, "txt"), exist_ok=True)
    os.makedirs(os.path.join(script_dir, "xls"), exist_ok=True)

    download_annual_report(stock_code)
