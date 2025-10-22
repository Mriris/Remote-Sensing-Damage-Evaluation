import os.path
import numpy as np
import cv2
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
def ini_seg(num_classes,phi,model_path):
    net = SegFormer(num_classes=num_classes, phi=phi, pretrained=False)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    net.load_state_dict(torch.load(model_path, map_location=device, weights_only=False))
    net = net.eval()
    return net

def seg_process(model, img, imgsize, device):
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

def init():
    device = 'cpu'
    models_list = []

    building_seg_model = ini_seg(2,"b1",os.path.join("model_files", "building.pth"))
    damage_seg_model = ini_seg(2, "b1", os.path.join("model_files", "damage.pth"))

    models_list.append(building_seg_model)
    models_list.append(damage_seg_model)


    return models_list


def process_images(handle=None, input_images=None, out_path=''):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    pre_image = input_images[0]
    post_image = input_images[1]
    building_seg_model = handle[0]
    damage_seg_model = handle[1]
    building_seg = seg_process(building_seg_model, pre_image, [512, 512], device)
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
        damage_seg = seg_process(damage_seg_model, crop_post_img, [512, 512], device)
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
