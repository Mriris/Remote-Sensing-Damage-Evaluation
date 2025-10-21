from prac_damage_tree import *
import argparse
from inference import *
import cv2
from utilss import resize_
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_former',type=str,default=r'C:\0Program\Python\VIEWS\models\RSDE\test\pre.jpg')
    parser.add_argument('--input_latter',type=str,default=r"C:\0Program\Python\VIEWS\models\RSDE\test\post.jpg")
    parser.add_argument('--output_path',type=str,default=r'C:\0Program\Python\VIEWS\models\RSDE\test\output')
    return parser.parse_args()

if __name__=="__main__":
    args = parse_args()
    input_former = args.input_former
    input_latter = args.input_latter
    output_path = args.output_path
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    model = init()
    print('----------------模型初始化完成----------------')
    input_former_img = cv2.imread(input_former)
    input_latter_img = cv2.imread(input_latter)
    images = [input_former_img,input_latter_img]
    process_images(model, images, out_path=output_path)
    # print("靶标名称：", objects_pre_name)
    # print("坐标：", objects_pre_box)
    # print("车辆类靶标现有部位：", objects_pre_position_name)
    # print("坐标：", objects_pre_position_box)
    # print("分割毁伤信息：部位名称", objects_pre_damage_seg[0][0])
    # print("分割毁伤信息：部位像素数", objects_pre_damage_seg[0][1])
    # print("分割毁伤信息：毁伤像素数", objects_pre_damage_seg[0][2])
    # print("分割毁伤信息：毁伤比率", objects_pre_damage_seg[0][3])
    out_damage_dict = {}

   