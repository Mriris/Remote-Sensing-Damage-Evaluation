# This is a sample Python script.
import os.path

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from models.common import DetectMultiBackend, letterbox
from utils.general import (non_max_suppression, scale_coords, xyxy2xywh)
import numpy as np
import cv2
import torch
import time
from utils.torch_utils import select_device
import torch
import torch.nn.functional as F
from PIL import Image
from torch import nn
from nets.segformer import SegFormer
import json
colors = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (128, 64, 12), (128, 0, 128), (0, 128, 128),
                            (128, 128, 128), (64, 0, 0), (192, 0, 0), (0, 0, 255), (192, 128, 0), (64, 0, 128), (192, 0, 128),
                            (64, 128, 128), (192, 128, 128), (0, 64, 0), (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128),
                            (64, 128, 0)]
objects_name = ['plane', 'buquanfeiji', 'launchCar', 'antennaCar', 'radiaCar', 'commandCar', 'santongche',
                'powerCar','buquanche', 'tanke']
car_seg_cls = ["_background_", "jiashicang", "box", "fashebox", "leidaban", "fuel"]
plane_seg_cls = ["_background_", "jishen", "jitou", "leida", "jiyi", "chuiwei", "lunzi"]
tank_seg_cls = ["_background_", "huopao", "jiashicang", "cheshen", "lvdai"]
car_position_name = ['head', 'box', 'fashebox', 'wheel', 'fuel', 'leidaban', 'pole', 'wang']
def ini_seg(num_classes,phi,model_path):
    net = SegFormer(num_classes=num_classes, phi=phi, pretrained=False)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    net.load_state_dict(torch.load(model_path, map_location=device, weights_only=False))
    net = net.eval()
    return net

def seg_porcess(model,img,imgsize,device):
    h,w,_ = img.shape
    img = img[:,:,::-1]

    img = cv2.resize(img,imgsize,cv2.INTER_LINEAR)
    img = np.array(img,np.float32)
    img -= np.array([123.675, 116.28, 103.53], np.float32)
    img /= np.array([58.395, 57.12, 57.375], np.float32)
    img = np.expand_dims(np.transpose(np.array(img, np.float32), (2, 0, 1)), 0)
    img = torch.from_numpy(img)
    img = img
    with torch.no_grad():
        output = model(img)[0]
        output = F.softmax(output.permute(1, 2, 0), dim=-1).cpu().numpy()
    output = np.argmax(output, axis=-1)
    output = np.squeeze(output).astype(np.uint8)
    y_pre = cv2.resize(output, (w, h), interpolation=cv2.INTER_NEAREST)
    return y_pre

def det_porcess(model,img,imgsize,device):
    stride, names, pt = model.stride, model.names, model.pt
    img = letterbox(img, (imgsize, imgsize), stride=stride, auto=pt)[0]
    img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
    im = np.ascontiguousarray(img)
    im = torch.from_numpy(im).to(device)
    im = im.float()
    im /= 255  # 0 - 255 to 0.0 - 1.0
    if len(im.shape) == 3:
        im = im[None]  # expand for batch dim
    pred = model(im, augment=False, visualize=False)
    print(im.shape)
    return pred,im.shape[2:]

def init():
    device = 'cpu'
    models_list = []

    building_seg_model = ini_seg(2,"b1",r"C:\0Program\Python\VIEWS\models\RSDE\model_files\building.pth")
    damage_seg_model = ini_seg(2, "b1", r"C:\0Program\Python\VIEWS\models\RSDE\model_files\damage.pth")

    models_list.append(building_seg_model)
    models_list.append(damage_seg_model)


    return models_list


def process_images(handle=None, input_images=None, out_path=''):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    pre_image = input_images[0]
    post_image = input_images[1]
    building_seg_model = handle[0]
    damage_seg_model = handle[1]
    building_seg = seg_porcess(building_seg_model, pre_image, [512, 512], device)
    building_seg_img = np.reshape(np.array(colors, np.uint8)[np.reshape(building_seg, [-1])],
                         [building_seg.shape[0], building_seg.shape[1], -1])
    building_seg_img = pre_image + building_seg_img * 0.7
    cv2.imwrite(os.path.join(out_path, 'building_seg_img.jpg'), building_seg_img)
    # building_seg_repeat = building_seg[:, :, np.newaxis].repeat(3, axis=-1)
    # mask_building = np.where(building_seg_repeat != [1, 1, 1], np.array([0, 0, 0]), img)
    contours, _ = cv2.findContours(building_seg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # 把边缘画到原图上
    # pre_image = cv2.drawContours(pre_image, contours, -1, (0, 0, 255), 3)
    # cv2.imwrite(os.path.join(out_path, '222.jpg'), pre_image)

    nn = 0
    out_post = post_image.copy()
    out_png = np.zeros((post_image.shape[0], post_image.shape[1]), np.uint8)
    for cont in contours:
        nn += 1
        x, y, w, h = cv2.boundingRect(cont)
        if w*h<400:
            continue
        #把矩形画在pre_image上
        out_post = cv2.rectangle(out_post, (x, y), (x + w, y + h), (255, 255, 255), 10)

        crop_seg_png = building_seg[y:y + h, x:x + w]
        building_pix_num = np.sum(crop_seg_png)
        crop_post_img = post_image[y:y + h, x:x + w, :]
        damage_seg = seg_porcess(damage_seg_model, crop_post_img, [512, 512], device)
        damage_pix_num = np.sum(damage_seg)
        damage_ratio = damage_pix_num/building_pix_num
        damage_seg = damage_seg*10
        # damage = np.where(damage_seg == 1)
        out_png[y:y + h, x:x + w] = damage_seg
        if damage_ratio<0.2:
            damge_level = 'low'
            text_color = (0,255,0)
        elif damage_ratio<0.7:
            damge_level = 'mid'
            text_color = (255,255,0)
        else:
            damge_level = 'high'
            text_color = (255,0,0)
        out_text = damge_level+": {:.2f}".format(damage_ratio)
        out_post = cv2.putText(out_post,out_text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
            4,text_color, 10, cv2.LINE_AA)

    seg_img = np.reshape(np.array(colors, np.uint8)[np.reshape(out_png, [-1])],
                     [out_png.shape[0], out_png.shape[1], -1])

    out_post = out_post+seg_img*0.3
    cv2.imwrite(os.path.join(out_path, 'out.jpg'), out_post)
    return 0




    # #-------------------------------------分别存储靶标的名字、边界框xyxy、目标现有部位、部位的xyxy、靶标的分割毁伤信息-----------------------------
    # objects_pre_name = []
    # objects_pre_box = []
    # objects_pre_position_name = []
    # objects_pre_position_box = []
    # objects_imgs = []
    # #------------------------------------第一维度是靶标索引，第二维度存储部位名字、像素数量、毁伤像素数量、毁伤比率-------------------------
    # objects_pre_damage_seg = []
    # #----------------------------------------------------开始推理-------------------------------------------------------------
    # obj_det_model = handle[0]
    # car_position_det_model = handle[1]
    # car_position_seg_model = handle[2]
    # car_damage_seg_model = handle[3]
    # plane_position_seg_model = handle[4]
    # plane_damage_seg_model = handle[5]
    # tank_position_seg_model = handle[6]
    # tank_damage_seg_model = handle[7]
    # original_h,original_w,_ = input_image.shape
    # img = input_image.copy()
    # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # conf_thres, iou_thres, classes, agnostic_nms, max_det,imgsz = 0.2, 0.45, None, False, 10,640
    # pred,det_size = det_porcess(obj_det_model,img,640,device)
    # pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
    # # Process predictions
    # for i, det in enumerate(pred):  # per image
    #     if len(det):
    #         print(det_size,input_image.shape)
    #         det[:, :4] = scale_coords(det_size, det[:, :4], input_image.shape).round()
    #         idx_car = 1
    #         idx_plane = 1
    #         idx_tank = 1
    #         for *xyxy, conf, cls in reversed(det):
    #             xyxy0 = torch.tensor(xyxy).view(-1).tolist()
    #             xyxy0 = list(map(int,xyxy0))
    #             # input_image = cv2.rectangle(input_image, (int(xyxy0[0]), int(xyxy0[1])), (int(xyxy0[2]), int(xyxy0[3])), (0, 0, 255), 2)
    #             cls_name = objects_name[int(cls.item())]
    #             object_img = input_image[xyxy0[1]:xyxy0[3],xyxy0[0]:xyxy0[2],:].copy()
    #             orininal_h,orininal_w,_ = object_img.shape
    #             #----------------------------------------对车辆类靶标进行分析----------------------------------------------
    #             if cls_name in ['launchCar', 'antennaCar', 'radiaCar', 'commandCar','powerCar']:
    #                 objects_pre_name.append(cls_name)
    #                 objects_pre_box.append(xyxy0)
    #                 #-------------------对车的部位进行分割后，根据分割部位继续分割毁伤区--------------------------------
    #                 position_seg = seg_porcess(car_position_seg_model, object_img, [640,640], device)
    #                 position_seg_repeat = position_seg[:, :, np.newaxis].repeat(3, axis=-1)
    #                 #----------------------存储所有部位的像素数量、毁伤像素数量、部位索引、毁伤比率-----------------------
    #                 position_pixel_nums = []
    #                 damage_pixel_nums = []
    #                 position_names = []
    #                 damage_ratios = []
    #                 ratio = 0
    #                 for p_i in range(len(car_seg_cls)-1):
    #                     position_img = np.where(position_seg_repeat != [p_i + 1, p_i + 1, p_i + 1], np.array([0, 0, 0]), object_img).astype("uint8")
    #                     if position_img.any()!=0:
    #                         position_pixel_num =np.sum(position_seg == p_i + 1)
    #                         position_pixel_nums.append(position_pixel_num)
    #                         position_damage = seg_porcess(car_damage_seg_model, position_img, [640,640], device)
    #                         position_seg = np.where(position_damage == 1, 10, position_seg)
    #                         damage_pixel_num = np.sum(position_damage == 1)
    #                         damage_pixel_nums.append(damage_pixel_num)
    #                         position_names.append(car_seg_cls[p_i+1])
    #                         ratio = damage_pixel_num/position_pixel_num
    #                         ratio = 1 if ratio>1 else ratio
    #                         damage_ratios.append(ratio)
    #                     else:
    #                         damage_ratios.append(ratio)
    #                 objects_pre_damage_seg.append([position_names,position_pixel_nums,damage_pixel_nums,damage_ratios])
    #
    #                 # --------------------------------对车的部位进行目标检测---------------------------------------
    #                 car_position_pred, car_position_det_size = det_porcess(car_position_det_model, object_img, 640, device)
    #                 car_position_pred = non_max_suppression(car_position_pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)[0]
    #                 car_position_pred[:, :4] = scale_coords(car_position_det_size, car_position_pred[:, :4], object_img.shape).round()
    #                 #---------------存储当前车辆的部位名字和xyxy------------------------
    #                 car_p_names = []
    #                 car_p_box = []
    #                 for *car_p_xyxy, car_p_conf, car_p_cls in reversed(car_position_pred):
    #                     car_p_xyxy0 = torch.tensor(car_p_xyxy).view(-1).tolist()
    #                     car_p_xyxy0 = list(map(int, car_p_xyxy0))
    #                     car_p_name = car_position_name[int(car_p_cls.item())]
    #                     car_p_names.append(car_p_name)
    #                     car_p_box.append(car_p_xyxy0)
    #                     object_img = cv2.rectangle(object_img, (int(car_p_xyxy0[0]), int(car_p_xyxy0[1])), (int(car_p_xyxy0[2]), int(car_p_xyxy0[3])),
    #                                         (0, 0, 255), 5)
    #                 objects_pre_position_name.append(car_p_names)
    #                 objects_pre_position_box.append(car_p_box)
    #                 seg_img = np.reshape(np.array(colors, np.uint8)[np.reshape(position_seg, [-1])],
    #                                      [orininal_h, orininal_w, -1])
    #
    #                 object_img = object_img+seg_img*0.7
    #                 objects_imgs.append(object_img)
    #                 cv2.imwrite(os.path.join(out_path,cls_name+str(idx_car)+'.jpg'),object_img)
    #                 idx_car+=1
    #                 # image = Image.fromarray(np.uint8(seg_img))
    #                 # old_img = Image.fromarray(np.uint8(object_img))
    #                 # render_map = Image.blend(old_img, image, 0.7)
    #                 # render_map.save(cls_name+'.jpg')
    #             # ----------------------------------------对飞机类靶标进行分析----------------------------------------------
    #             if cls_name=="plane":
    #                 objects_pre_name.append(cls_name)
    #                 objects_pre_box.append(xyxy0)
    #                 # -------------------对飞机的部位进行分割后，根据分割部位继续分割毁伤区--------------------------------
    #                 position_seg = seg_porcess(plane_position_seg_model, object_img, [640, 640], device)
    #
    #                 position_seg_repeat = position_seg[:, :, np.newaxis].repeat(3, axis=-1)
    #
    #                 # ----------------------存储所有部位的像素数量、毁伤像素数量、部位索引、毁伤比率-----------------------
    #                 position_pixel_nums = []
    #                 damage_pixel_nums = []
    #                 position_names = []
    #                 damage_ratios = []
    #                 ratio = 0
    #                 for p_i in range(len(plane_seg_cls) - 1):
    #                     position_img = np.where(position_seg_repeat != [p_i + 1, p_i + 1, p_i + 1], np.array([0, 0, 0]),
    #                                             object_img).astype("uint8")
    #
    #                     if position_img.any() != 0:
    #                         position_pixel_num = np.sum(position_seg == p_i + 1)
    #                         position_pixel_nums.append(position_pixel_num)
    #                         position_damage = seg_porcess(plane_damage_seg_model, position_img, [640, 640], device)
    #                         position_seg = np.where(position_damage == 1, 10, position_seg)
    #                         damage_pixel_num = np.sum(position_damage == 1)
    #                         damage_pixel_nums.append(damage_pixel_num)
    #                         position_names.append(plane_seg_cls[p_i + 1])
    #                         ratio = damage_pixel_num/position_pixel_num
    #                         ratio = 1 if ratio>1 else ratio
    #                         damage_ratios.append(ratio)
    #                     else:
    #                         damage_ratios.append(0)
    #                 objects_pre_damage_seg.append(
    #                     [position_names, position_pixel_nums, damage_pixel_nums, damage_ratios])
    #                 seg_img = np.reshape(np.array(colors, np.uint8)[np.reshape(position_seg, [-1])],
    #                                      [orininal_h, orininal_w, -1])
    #                 object_img = object_img+seg_img*0.7
    #                 objects_imgs.append(object_img)
    #                 cv2.imwrite(os.path.join(out_path,cls_name+str(idx_plane)+'.jpg'),object_img)
    #                 idx_plane+=1
    #                 # image = Image.fromarray(np.uint8(seg_img))
    #                 # old_img = Image.fromarray(np.uint8(object_img))
    #                 # render_map = Image.blend(old_img, image, 0.7)
    #                 # render_map.save(cls_name + '.jpg')
    #
    #             # ----------------------------------------对坦克类靶标进行分析----------------------------------------------
    #             if cls_name == "tanke":
    #                 objects_pre_name.append(cls_name)
    #                 objects_pre_box.append(xyxy0)
    #                 # -------------------对坦克的部位进行分割后，根据分割部位继续分割毁伤区--------------------------------
    #                 position_seg = seg_porcess(tank_position_seg_model, object_img, [640, 640], device)
    #                 n3 = np.sum(np.where(position_seg==3))
    #                 n4 = np.sum(np.where(position_seg==4))
    #                 n1 = np.sum(np.where(position_seg==1))
    #                 n2 = np.sum(np.where(position_seg==2))
    #                 print(np.sum(np.where(position_seg==1)),np.sum(np.where(position_seg==2)),np.sum(np.where(position_seg==3)),np.sum(np.where(position_seg==4)))
    #                 position_seg_repeat = position_seg[:, :, np.newaxis].repeat(3, axis=-1)
    #
    #                 # ----------------------存储所有部位的像素数量、毁伤像素数量、部位索引、毁伤比率-----------------------
    #                 position_pixel_nums = []
    #                 damage_pixel_nums = []
    #                 position_names = []
    #                 damage_ratios = []
    #                 for p_i in range(len(tank_seg_cls) - 1):
    #                     # position_img = np.where(position_seg_repeat != [p_i + 1, p_i + 1, p_i + 1], np.array([0, 0, 0]),
    #                     #                         object_img).astype("uint8")
    #                     #
    #                     # if position_img.any() != 0:
    #                     #     position_pixel_num = np.sum(position_seg == p_i + 1)
    #                     #     position_pixel_nums.append(position_pixel_num)
    #                     #     position_damage = seg_porcess(tank_damage_seg_model, position_img, [640, 640], device)
    #                     #     position_seg = np.where(position_damage == 1, 10, position_seg)
    #                     #     damage_pixel_num = np.sum(position_damage == 1)
    #                     #     damage_pixel_nums.append(damage_pixel_num)
    #                     #     position_names.append(tank_seg_cls[p_i + 1])
    #                     #     ratio = damage_pixel_num / position_pixel_num
    #                     #     ratio = 1 if ratio > 1 else ratio
    #                     #     damage_ratios.append(ratio)
    #                     # else:
    #                     damage_ratios.append(0)
    #                 objects_pre_damage_seg.append(
    #                     [position_names, position_pixel_nums, damage_pixel_nums, damage_ratios])
    #                 seg_img = np.reshape(np.array(colors, np.uint8)[np.reshape(position_seg, [-1])],
    #                                      [orininal_h, orininal_w, -1])
    #                 object_img = object_img + seg_img * 0.7
    #                 objects_imgs.append(object_img)
    #                 cv2.imwrite(os.path.join(out_path, cls_name + str(idx_tank) + '.jpg'), object_img)
    #                 idx_tank += 1
    #                 # image = Image.fromarray(np.uint8(seg_img))
    #                 # old_img = Image.fromarray(np.uint8(object_img))
    #                 # render_map = Image.blend(old_img, image, 0.7)
    #                 # render_map.save(cls_name + '.jpg')
    # return objects_pre_name,objects_pre_box,objects_pre_position_name,objects_pre_position_box ,objects_pre_damage_seg,objects_imgs


# if __name__ == '__main__':
#     model = init()
    # img = cv2.imread(r"mix.jpg")
    # objects_pre_name,objects_pre_box,objects_pre_position_name,objects_pre_position_box ,objects_pre_damage_seg = process_images(model, img)
    # print("靶标名称：",objects_pre_name)
    # print("坐标：",objects_pre_box)
    # print("车辆类靶标现有部位：",objects_pre_position_name)
    # print("坐标：",objects_pre_position_box)
    # print("分割毁伤信息：部位名称",objects_pre_damage_seg[0][0])
    # print("分割毁伤信息：部位像素数",objects_pre_damage_seg[0][1])
    # print("分割毁伤信息：毁伤像素数",objects_pre_damage_seg[0][2])
    # print("分割毁伤信息：毁伤比率",objects_pre_damage_seg[0][3])



