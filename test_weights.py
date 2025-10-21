"""
测试权重下载和校验功能
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from weight_manager import check_and_download_weights

if __name__ == "__main__":
    print("开始测试权重下载功能...\n")
    
    try:
        check_and_download_weights()
        print("\n" + "="*60)
        print("✓ 测试成功！所有权重文件准备就绪")
        print("="*60)
    except Exception as e:
        print("\n" + "="*60)
        print("✗ 测试失败！")
        print(f"错误信息: {e}")
        print("="*60)
        sys.exit(1)

