from prac_damage_tree import *
import argparse
from inference import *
import cv2
from utilss import resize_
from weight_manager import check_and_download_weights
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_former',type=str,default=r'test\pre.jpg')
    parser.add_argument('--input_latter',type=str,default=r"test\post.jpg")
    parser.add_argument('--output_path',type=str,default=r'test\output')
    return parser.parse_args()

if __name__=="__main__":
    args = parse_args()
    input_former = args.input_former
    input_latter = args.input_latter
    output_path = args.output_path
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    try:
        check_and_download_weights()
    except Exception as e:
        print(f"\n错误: 权重文件检查失败")
        print(f"详细信息: {e}")
        print("\n请检查网络连接或手动下载权重文件")
        exit(1)
    
    print('开始加载模型...')
    model = init()
    print('----------------模型初始化完成----------------')
    
    print(f'读取前期图像: {input_former}')
    input_former_img = cv2.imread(input_former)
    print(f'读取后期图像: {input_latter}')
    input_latter_img = cv2.imread(input_latter)
    images = [input_former_img,input_latter_img]
    
    print('开始处理图像并生成结果...')
    process_images(model, images, out_path=output_path)
    print(f'处理完成！结果已保存到: {output_path}')
    # print("靶标名称：", objects_pre_name)
    # print("坐标：", objects_pre_box)
    # print("车辆类靶标现有部位：", objects_pre_position_name)
    # print("坐标：", objects_pre_position_box)
    # print("分割毁伤信息：部位名称", objects_pre_damage_seg[0][0])
    # print("分割毁伤信息：部位像素数", objects_pre_damage_seg[0][1])
    # print("分割毁伤信息：毁伤像素数", objects_pre_damage_seg[0][2])
    # print("分割毁伤信息：毁伤比率", objects_pre_damage_seg[0][3])
    out_damage_dict = {}

   