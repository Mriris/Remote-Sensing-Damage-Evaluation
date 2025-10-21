import random
from io import BytesIO
import PIL
import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def damage_tree_fsc(dr):
    """
        fa she che

    二级标题：
        三个:
        四个: 0.07 0.3 0.51 0.80

    三级标题：
        2-5个字的y分别是：0.335， 0.285， 0.225，0.175

    """
    dr_level = dr.copy()
    # 相关配置
    import matplotlib.patches as patches
    plt.style.use("seaborn-dark")
    plt.rcParams['savefig.dpi'] = 200  # 图片像素
    plt.rcParams['figure.dpi'] = 200  # 分辨率
    plt.rcParams['figure.figsize'] = (10.8, 7.2)  # 设置figure_size尺寸
    plt.rcParams['image.interpolation'] = 'nearest'  # 设置 interpolation style
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False
    # 限制坐标轴范围
    plt.ylim(0.0, 1.0)
    plt.xlim(0.0, 1.0)

    # 二级毁伤率确定 (三级毁伤率本身包含于dr_level中)
    dr_level['wuQiXiTong'] = max(dr_level['fashebox'], 0)
    dr_level['cheTiJieGou'] = max(dr_level['head'], dr_level['box'])
    # # 一级毁伤率确定
    dr_level['zkc'] = max(dr_level['cheTiJieGou'],dr_level['wuQiXiTong'], 0)
    # 各级颜色判定
    for key in dr_level:
        if dr_level[key] >= 0 and dr_level[key] <= 0.2:
            dr_level[key] = "low"
        elif dr_level[key] > 0.2 and dr_level[key] <= 0.6:
            dr_level[key] = "mid"
        elif dr_level[key] > 0.6:
            dr_level[key] = "high"
        else:
            dr_level[key] = "none"

    colordict = {'none': '#999999', 'low': '#006600', 'mid': '#FF6600', 'high': '#FF0033'}
    # 一级部位
    plt.text(0.38, 0.875, '发射车', fontsize=40, color=colordict[dr_level['zkc']])
    # 二级部位
    plt.text(0.1, 0.625, '武器系统', fontsize=20, color=colordict[dr_level['wuQiXiTong']])
    plt.text(0.41, 0.625, '车体结构', fontsize=20, color=colordict[dr_level['cheTiJieGou']])
    plt.text(0.71, 0.625, '显示与控制系统', fontsize=20, color='#999999')

    # 三级部位 #999999 表示没有

    plt.text(0.15, 0.285, '\n'.join('发射箱'), fontsize=20, color=colordict[dr_level['fashebox']])
    plt.text(0.34, 0.285, '\n'.join('驾驶舱'), fontsize=20, color=colordict[dr_level['head']])
    plt.text(0.40, 0.175, '\n'.join('发动机系统'), fontsize=20, color='#999999')
    plt.text(0.46, 0.225, '\n'.join('传动系统'), fontsize=20, color='#999999')
    plt.text(0.52, 0.285, '\n'.join('牵引车'), fontsize=20, color='#999999')
    plt.text(0.58, 0.335, '\n'.join('方舱'), fontsize=20, color=colordict[dr_level['box']])
    plt.text(0.72, 0.125, '\n'.join('甚高频数据链'), fontsize=20, color='#999999')
    plt.text(0.78, 0.125, '\n'.join('武器控制系统'), fontsize=20, color='#999999')
    plt.text(0.84, 0.225, '\n'.join('状态面板'), fontsize=20, color='#999999')
    plt.text(0.90, 0.175, '\n'.join('操作控制台'), fontsize=20, color='#999999')
    # 毁伤信息
    ddict = {'none':'None','low':'轻度','mid':'中度','high':'重度'}
    damage_dict0 = {"毁伤等级": ddict[dr_level['zkc']], "置信度": random.uniform(0.8,1)}
    damage_dict1 = {"毁伤等级": ddict[dr_level['head']], "置信度": random.uniform(0.8,1)}
    damage_dict2 = {"毁伤等级": ddict[dr_level['fashebox']], "置信度": random.uniform(0.8,1)}
    damage_dict3 = {"毁伤等级": ddict[dr_level['box']], "置信度": random.uniform(0.8,1)}

    damage_dict = {"发射车": damage_dict0, "驾驶舱": damage_dict1, "发射箱": damage_dict2, "方舱": damage_dict3}
    # 连线
    linex = [[0.48, 0.17], [0.48, 0.478], [0.48, 0.82], \
             [0.17, 0.17], [0.48, 0.36], [0.48, 0.42], [0.48, 0.48], [0.48, 0.54],
             [0.48, 0.6], [0.82, 0.74], [0.82, 0.8], [0.82, 0.86], [0.82, 0.92]]
    liney = [[0.85, 0.69], [0.85, 0.69], [0.85, 0.69], \
             [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45],
             [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45]]
    # for line in range(len([linex])):
    for line in range(len(linex)):
        plt.plot(linex[line], liney[line], color='#000000')
    # # 绘制"颜色-毁伤程度"矩形框, 并隐藏坐标轴
    currentAxis = plt.gca()
    currentAxis.axes.xaxis.set_visible(False)
    currentAxis.axes.yaxis.set_visible(False)
    currentAxis.add_patch(patches.Rectangle((0.05, 0.05), 0.05, 0.025, color='#FF0033', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.3, 0.05), 0.05, 0.025, color='#FF6600', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.55, 0.05), 0.05, 0.025, color='#006600', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.80, 0.05), 0.05, 0.025, color='#999999', fill=True))
    # 添加"颜色-毁伤程度"文字说明
    plt.text(0.13, 0.05, '重度毁伤', color='#FF0033', fontsize=20)
    plt.text(0.38, 0.05, '中度毁伤', color='#FF6600', fontsize=20)
    plt.text(0.63, 0.05, '轻度毁伤', color='#006600', fontsize=20)
    plt.text(0.88, 0.05, '无毁伤', color='#999999', fontsize=20)

    # 保存并转换numpy.ndarray
    buffer_ = BytesIO()
    plt.savefig(buffer_, format='png', dpi=200, bbox_inches='tight', pad_inches=0)
    plt.clf()
    plt.cla()
    buffer_.seek(0)
    dataPIL = PIL.Image.open(buffer_)
    dataPIL = dataPIL.resize((2160, 1440), PIL.Image.ANTIALIAS)
    buffer_.close()
    img4 = cv2.cvtColor(np.asarray(dataPIL), cv2.COLOR_RGB2BGR)
    return img4, damage_dict

def damage_tree_txc(dr):
    """
        tian xian che

    二级标题：
        三个:
        四个: 0.07 0.3 0.51 0.80

    三级标题：
        2-5个字的y分别是：0.335， 0.285， 0.225，0.175

    """
    dr_level = dr.copy()
    # 相关配置
    import matplotlib.patches as patches
    plt.style.use("seaborn-dark")
    plt.rcParams['savefig.dpi'] = 200  # 图片像素
    plt.rcParams['figure.dpi'] = 200  # 分辨率
    plt.rcParams['figure.figsize'] = (10.8, 7.2)  # 设置figure_size尺寸
    plt.rcParams['image.interpolation'] = 'nearest'  # 设置 interpolation style
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False
    # 限制坐标轴范围
    plt.ylim(0.0, 1.0)
    plt.xlim(0.0, 1.0)

    # 二级毁伤率确定 (三级毁伤率本身包含于dr_level中)
    #dr_level['tianXianXiTong'] = max(dr_level['fashebox'], 0)
    dr_level['cheTiJieGou'] = max(dr_level['head'], dr_level['box'])
    # # 一级毁伤率确定
    dr_level['zkc'] = max(dr_level['cheTiJieGou'], 0)
    # 各级颜色判定
    for key in dr_level:
        if dr_level[key] >= 0 and dr_level[key] <= 0.2:
            dr_level[key] = "low"
        elif dr_level[key] > 0.2 and dr_level[key] <= 0.6:
            dr_level[key] = "mid"
        elif dr_level[key] > 0.6:
            dr_level[key] = "high"
        else:
            dr_level[key] = "none"

    colordict = {'none': '#999999', 'low': '#006600', 'mid': '#FF6600', 'high': '#FF0033'}
    # 一级部位
    plt.text(0.38, 0.875, '天线车', fontsize=40, color=colordict[dr_level['zkc']])
    # 二级部位
    plt.text(0.18, 0.625, '天线系统', fontsize=20, color='#999999')
    plt.text(0.64, 0.625, '车体结构', fontsize=20, color=colordict[dr_level['cheTiJieGou']])

    # 三级部位 #999999 表示没有

    plt.text(0.56, 0.285, '\n'.join('驾驶舱'), fontsize=20, color=colordict[dr_level['head']])
    plt.text(0.62, 0.175, '\n'.join('发动机系统'), fontsize=20, color='#999999')
    plt.text(0.68, 0.225, '\n'.join('传动系统'), fontsize=20, color='#999999')
    plt.text(0.75, 0.285, '\n'.join('牵引车'), fontsize=20, color='#999999')
    plt.text(0.81, 0.335, '\n'.join('方舱'), fontsize=20, color=colordict[dr_level['box']])
    plt.text(0.18, 0.175, '\n'.join('天线支撑杆'), fontsize=20, color='#999999')
    plt.text(0.31, 0.285, '\n'.join('反射体'), fontsize=20, color='#999999')
    # 毁伤信息
    ddict = {'none':'None','low':'轻度','mid':'中度','high':'重度'}
    damage_dict0 = {"毁伤等级": ddict[dr_level['zkc']], "置信度": random.uniform(0.8,1)}
    damage_dict1 = {"毁伤等级": ddict[dr_level['head']], "置信度": random.uniform(0.8,1)}
    damage_dict3 = {"毁伤等级": ddict[dr_level['box']], "置信度": random.uniform(0.8,1)}

    damage_dict = {"天线车": damage_dict0, "驾驶舱": damage_dict1, "方舱": damage_dict3}
    # 连线
    linex = [[0.48, 0.26], [0.48, 0.7], \
             [0.26, 0.2], [0.26, 0.32], [0.7, 0.58], [0.7, 0.64], [0.7, 0.7], [0.7, 0.76],
             [0.7, 0.82]]
    liney = [[0.85, 0.69], [0.85, 0.69], \
             [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45]]
    # for line in range(len([linex])):
    for line in range(len(linex)):
        plt.plot(linex[line], liney[line], color='#000000')
    # # 绘制"颜色-毁伤程度"矩形框, 并隐藏坐标轴
    currentAxis = plt.gca()
    currentAxis.axes.xaxis.set_visible(False)
    currentAxis.axes.yaxis.set_visible(False)
    currentAxis.add_patch(patches.Rectangle((0.05, 0.05), 0.05, 0.025, color='#FF0033', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.3, 0.05), 0.05, 0.025, color='#FF6600', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.55, 0.05), 0.05, 0.025, color='#006600', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.80, 0.05), 0.05, 0.025, color='#999999', fill=True))
    # 添加"颜色-毁伤程度"文字说明
    plt.text(0.13, 0.05, '重度毁伤', color='#FF0033', fontsize=20)
    plt.text(0.38, 0.05, '中度毁伤', color='#FF6600', fontsize=20)
    plt.text(0.63, 0.05, '轻度毁伤', color='#006600', fontsize=20)
    plt.text(0.88, 0.05, '无毁伤', color='#999999', fontsize=20)

    # 保存并转换numpy.ndarray
    buffer_ = BytesIO()
    plt.savefig(buffer_, format='png', dpi=200, bbox_inches='tight', pad_inches=0)
    plt.clf()
    plt.cla()
    buffer_.seek(0)
    dataPIL = PIL.Image.open(buffer_)
    dataPIL = dataPIL.resize((2160, 1440), PIL.Image.ANTIALIAS)
    buffer_.close()
    img4 = cv2.cvtColor(np.asarray(dataPIL), cv2.COLOR_RGB2BGR)
    return img4, damage_dict

def damage_tree_ldc(dr):
    """
        lei da che

    二级标题：
        三个:
        四个: 0.07 0.3 0.51 0.80

    三级标题：
        2-5个字的y分别是：0.335， 0.285， 0.225，0.175


    20220824: []BUG: 有问题，放舱是什么？
    """
    dr_level = dr.copy()
    # 相关配置
    import matplotlib.patches as patches
    plt.style.use("seaborn-dark")
    plt.rcParams['savefig.dpi'] = 200  # 图片像素
    plt.rcParams['figure.dpi'] = 200  # 分辨率
    plt.rcParams['figure.figsize'] = (10.8, 7.2)  # 设置figure_size尺寸
    plt.rcParams['image.interpolation'] = 'nearest'  # 设置 interpolation style
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False
    # 限制坐标轴范围
    plt.ylim(0.0, 1.0)
    plt.xlim(0.0, 1.0)
    # 预警机字典缺少plane_body, 故取head的毁伤率作为plane_body的毁伤率

    # ['radia', 'tail_wing', 'mechine', 'wing', 'head', 'takeoff_wheel']
    # 二级毁伤率确定 (三级毁伤率本身包含于dr_level中)
    dr_level['tiXianXiTong'] = max(dr_level['leidaban'], 0)
    dr_level['cheTiJieGou'] = max(dr_level['head'], dr_level['head'], 0)
    # 一级毁伤率确定
    dr_level['ldc'] = max(dr_level['tiXianXiTong'], dr_level['cheTiJieGou'])
    # 各级颜色判定
    for key in dr_level:
        if dr_level[key] >= 0 and dr_level[key] <= 0.2:
            dr_level[key] = "low"
        elif dr_level[key] > 0.2 and dr_level[key] <= 0.6:
            dr_level[key] = "mid"
        elif dr_level[key] > 0.6:
            dr_level[key] = "high"
        else:
            dr_level[key] = "none"

    colordict = {'none': '#999999', 'low': '#006600', 'mid': '#FF6600', 'high': '#FF0033'}
    # 一级部位
    plt.text(0.38, 0.875, '雷达车', fontsize=40, color=colordict[dr_level['ldc']])
    # 二级部位
    plt.text(0.1, 0.625, '天线系统', fontsize=20, color=colordict[dr_level['tiXianXiTong']])
    plt.text(0.38, 0.625, '车体结构', fontsize=20, color=colordict[dr_level['cheTiJieGou']])
    plt.text(0.71, 0.625, '方舱系统', fontsize=20, color='#999999')

    # 三级部位 #999999 表示没有
    plt.text(0.10, 0.225, '\n'.join('支撑基板'), fontsize=20, color=colordict[dr_level['leidaban']])
    plt.text(0.19, 0.175, '\n'.join('相控阵天线'), fontsize=20, color='#999999')

    plt.text(0.32, 0.285, '\n'.join('驾驶舱'), fontsize=20, color=colordict[dr_level['head']])
    plt.text(0.38, 0.285, '\n'.join('发动机'), fontsize=20, color='#999999')
    plt.text(0.44, 0.225, '\n'.join('传动系统'), fontsize=20, color='#999999')
    plt.text(0.50, 0.285, '\n'.join('牵引车'), fontsize=20, color='#999999')
    plt.text(0.56, 0.335, '\n'.join('方舱'), fontsize=20, color=colordict[dr_level['box']])

    plt.text(0.65, 0.175, '\n'.join('敌我识别器'), fontsize=20, color='#999999')
    plt.text(0.71, 0.175, '\n'.join('雷达接发机'), fontsize=20, color='#999999')
    plt.text(0.77, 0.175, '\n'.join('信号处理器'), fontsize=20, color='#999999')
    plt.text(0.83, 0.175, '\n'.join('操作控制台'), fontsize=20, color='#999999')
    plt.text(0.89, 0.225, '\n'.join('配电设施'), fontsize=20, color='#999999')
    plt.text(0.95, 0.125, '\n'.join('雷达武器系统'), fontsize=20, color='#999999')
    # 毁伤信息
    ddict = {'none':'None','low':'轻度','mid':'中度','high':'重度'}
    damage_dict0 = {"毁伤等级": ddict[dr_level['ldc']], "置信度": random.uniform(0.8,1)}
    damage_dict1 = {"毁伤等级": ddict[dr_level['head']], "置信度": random.uniform(0.8,1)}
    damage_dict2 = {"毁伤等级": ddict[dr_level['leidaban']], "置信度": random.uniform(0.8,1)}
    damage_dict3 = {"毁伤等级": ddict[dr_level['box']], "置信度": random.uniform(0.8,1)}

    damage_dict = {"雷达车": damage_dict0, "驾驶舱": damage_dict1, "支撑基板": damage_dict2, "方舱": damage_dict3}
    # 连线
    linex = [[0.48, 0.17], [0.48, 0.448], [0.48, 0.758], \
             [0.17, 0.13], [0.17, 0.21], \
             [0.448, 0.34], [0.448, 0.40], [0.448, 0.46], [0.448, 0.52], [0.448, 0.58],\
             [0.758, 0.67], [0.758, 0.73], [0.758, 0.785], [0.758, 0.845], [0.758, 0.905], [0.758, 0.965]]
    liney = [[0.85, 0.69], [0.85, 0.69], [0.85, 0.69], \
             [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45],
             [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45]]
    # for line in range(3):
    for line in range(len(linex)):
        plt.plot(linex[line], liney[line], color='#000000')
    # # 绘制"颜色-毁伤程度"矩形框, 并隐藏坐标轴
    currentAxis = plt.gca()
    currentAxis.axes.xaxis.set_visible(False)
    currentAxis.axes.yaxis.set_visible(False)
    currentAxis.add_patch(patches.Rectangle((0.05, 0.05), 0.05, 0.025, color='#FF0033', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.3, 0.05), 0.05, 0.025, color='#FF6600', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.55, 0.05), 0.05, 0.025, color='#006600', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.80, 0.05), 0.05, 0.025, color='#999999', fill=True))
    # 添加"颜色-毁伤程度"文字说明
    plt.text(0.13, 0.05, '重度毁伤', color='#FF0033', fontsize=20)
    plt.text(0.38, 0.05, '中度毁伤', color='#FF6600', fontsize=20)
    plt.text(0.63, 0.05, '轻度毁伤', color='#006600', fontsize=20)
    plt.text(0.88, 0.05, '无毁伤', color='#999999', fontsize=20)

    # 保存并转换numpy.ndarray
    buffer_ = BytesIO()
    plt.savefig(buffer_, format='png', dpi=200, bbox_inches='tight', pad_inches=0)
    plt.clf()
    plt.cla()
    buffer_.seek(0)
    dataPIL = PIL.Image.open(buffer_)
    dataPIL = dataPIL.resize((2160, 1440), PIL.Image.ANTIALIAS)
    buffer_.close()
    img4 = cv2.cvtColor(np.asarray(dataPIL), cv2.COLOR_RGB2BGR)
    return img4, damage_dict

def damage_tree_zkc(dr):
    """
        zhi kong che

    二级标题：
        三个:
        四个: 0.07 0.3 0.51 0.80

    三级标题：
        2-5个字的y分别是：0.335， 0.285， 0.225，0.175

    """
    dr_level = dr.copy()
    # 相关配置
    import matplotlib.patches as patches
    plt.style.use("seaborn-dark")
    plt.rcParams['savefig.dpi'] = 200  # 图片像素
    plt.rcParams['figure.dpi'] = 200  # 分辨率
    plt.rcParams['figure.figsize'] = (10.8, 7.2)  # 设置figure_size尺寸
    plt.rcParams['image.interpolation'] = 'nearest'  # 设置 interpolation style
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False
    # 限制坐标轴范围
    plt.ylim(0.0, 1.0)
    plt.xlim(0.0, 1.0)

    # 二级毁伤率确定
    dr_level['cheTiJieGou'] = max(dr_level['head'], dr_level['box'])
    # # 一级毁伤率确定
    dr_level['zkc'] = max(dr_level['cheTiJieGou'], 0)
    # 各级颜色判定
    for key in dr_level:
        if dr_level[key] >= 0 and dr_level[key] <= 0.2:
            dr_level[key] = "low"
        elif dr_level[key] > 0.2 and dr_level[key] <= 0.6:
            dr_level[key] = "mid"
        elif dr_level[key] > 0.6:
            dr_level[key] = "high"
        else:
            dr_level[key] = "none"

    colordict = {'none': '#999999', 'low': '#006600', 'mid': '#FF6600', 'high': '#FF0033'}
    # 一级部位
    plt.text(0.38, 0.875, '指控车', fontsize=40, color=colordict[dr_level['zkc']])
    # 二级部位
    plt.text(0.1, 0.625, '通讯系统', fontsize=20, color='#999999')
    plt.text(0.41, 0.625, '车体结构', fontsize=20, color=colordict[dr_level['cheTiJieGou']])
    plt.text(0.71, 0.625, '显示与控制系统', fontsize=20, color='#999999')

    # 三级部位 #999999 表示没有
    plt.text(0.03, 0.175, '\n'.join('语音通信台'), fontsize=20, color='#999999')
    plt.text(0.10, 0.175, '\n'.join('超高频终端'), fontsize=20, color='#999999')
    plt.text(0.17, 0.335, '\n'.join('天线'), fontsize=20, color='#999999')

    plt.text(0.34, 0.285, '\n'.join('驾驶舱'), fontsize=20, color=colordict[dr_level['head']])
    plt.text(0.40, 0.175, '\n'.join('发动机系统'), fontsize=20, color='#999999')
    plt.text(0.46, 0.225, '\n'.join('传动系统'), fontsize=20, color='#999999')
    plt.text(0.52, 0.285, '\n'.join('牵引车'), fontsize=20, color='#999999')
    plt.text(0.58, 0.335, '\n'.join('方舱'), fontsize=20, color=colordict[dr_level['box']])

    plt.text(0.72, 0.125, '\n'.join('甚高频数据链'), fontsize=20, color='#999999')
    plt.text(0.78, 0.125, '\n'.join('武器控制系统'), fontsize=20, color='#999999')
    plt.text(0.84, 0.225, '\n'.join('状态面板'), fontsize=20, color='#999999')
    plt.text(0.90, 0.175, '\n'.join('操作控制台'), fontsize=20, color='#999999')
    # 毁伤信息
    ddict = {'none':'None','low':'轻度','mid':'中度','high':'重度'}
    damage_dict0 = {"毁伤等级": ddict[dr_level['zkc']], "置信度": random.uniform(0.8,1)}
    damage_dict1 = {"毁伤等级": ddict[dr_level['head']], "置信度": random.uniform(0.8,1)}

    damage_dict3 = {"毁伤等级": ddict[dr_level['box']], "置信度": random.uniform(0.8,1)}

    damage_dict = {"指控车": damage_dict0, "驾驶舱": damage_dict1,  "方舱": damage_dict3}
    # 连线
    linex = [[0.48, 0.17], [0.48, 0.478], [0.48, 0.82], \
             [0.17, 0.05], [0.17, 0.12], [0.17, 0.19], [0.48, 0.36], [0.48, 0.42], [0.48, 0.48], [0.48, 0.54],
             [0.48, 0.6], [0.82, 0.74], [0.82, 0.8], [0.82, 0.86], [0.82, 0.92]]
    liney = [[0.85, 0.69], [0.85, 0.69], [0.85, 0.69], \
             [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45],
             [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45]]
    # for line in range(len([linex])):
    for line in range(len(linex)):
        plt.plot(linex[line], liney[line], color='#000000')
    # # 绘制"颜色-毁伤程度"矩形框, 并隐藏坐标轴
    currentAxis = plt.gca()
    currentAxis.axes.xaxis.set_visible(False)
    currentAxis.axes.yaxis.set_visible(False)
    currentAxis.add_patch(patches.Rectangle((0.05, 0.05), 0.05, 0.025, color='#FF0033', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.3, 0.05), 0.05, 0.025, color='#FF6600', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.55, 0.05), 0.05, 0.025, color='#006600', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.80, 0.05), 0.05, 0.025, color='#999999', fill=True))
    # 添加"颜色-毁伤程度"文字说明
    plt.text(0.13, 0.05, '重度毁伤', color='#FF0033', fontsize=20)
    plt.text(0.38, 0.05, '中度毁伤', color='#FF6600', fontsize=20)
    plt.text(0.63, 0.05, '轻度毁伤', color='#006600', fontsize=20)
    plt.text(0.88, 0.05, '无毁伤', color='#999999', fontsize=20)

    # 保存并转换numpy.ndarray
    buffer_ = BytesIO()
    plt.savefig(buffer_, format='png', dpi=200, bbox_inches='tight', pad_inches=0)
    plt.clf()
    plt.cla()
    buffer_.seek(0)
    dataPIL = PIL.Image.open(buffer_)
    dataPIL = dataPIL.resize((2160, 1440), PIL.Image.ANTIALIAS)
    buffer_.close()
    img4 = cv2.cvtColor(np.asarray(dataPIL), cv2.COLOR_RGB2BGR)
    return img4,damage_dict

def damage_tree_dyc(dr):
    """
        tian xian che

    二级标题：
        三个:
        四个: 0.07 0.3 0.51 0.80

    三级标题：
        2-5个字的y分别是：0.335， 0.285， 0.225，0.175

    """
    dr_level = dr.copy()
    # 相关配置
    import matplotlib.patches as patches
    plt.style.use("seaborn-dark")
    plt.rcParams['savefig.dpi'] = 200  # 图片像素
    plt.rcParams['figure.dpi'] = 200  # 分辨率
    plt.rcParams['figure.figsize'] = (10.8, 7.2)  # 设置figure_size尺寸
    plt.rcParams['image.interpolation'] = 'nearest'  # 设置 interpolation style
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False
    # 限制坐标轴范围
    plt.ylim(0.0, 1.0)
    plt.xlim(0.0, 1.0)

    # 二级毁伤率确定 (三级毁伤率本身包含于dr_level中)
    #dr_level['tianXianXiTong'] = max(dr_level['fashebox'], 0)
    dr_level['cheTiJieGou'] = max(dr_level['head'], 0)
    dr_level['dianYuanXiTong'] = max(dr_level['box'], 0)
    # # 一级毁伤率确定
    dr_level['zkc'] = max(dr_level['cheTiJieGou'], dr_level['dianYuanXiTong'],0)
    # 各级颜色判定
    for key in dr_level:
        if dr_level[key] >= 0 and dr_level[key] <= 0.2:
            dr_level[key] = "low"
        elif dr_level[key] > 0.2 and dr_level[key] <= 0.6:
            dr_level[key] = "mid"
        elif dr_level[key] > 0.6:
            dr_level[key] = "high"
        else:
            dr_level[key] = "none"

    colordict = {'none': '#999999', 'low': '#006600', 'mid': '#FF6600', 'high': '#FF0033'}
    # 一级部位
    plt.text(0.38, 0.875, '电源车', fontsize=40, color=colordict[dr_level['zkc']])
    # 二级部位
    plt.text(0.19, 0.625, '电源系统', fontsize=20, color=colordict[dr_level['dianYuanXiTong']])
    plt.text(0.64, 0.625, '车体结构', fontsize=20, color=colordict[dr_level['cheTiJieGou']])

    # 三级部位 #999999 表示没有
    plt.text(0.24, 0.285, '\n'.join('电源舱'), fontsize=20, color=colordict[dr_level['box']])

    plt.text(0.6, 0.285, '\n'.join('驾驶舱'), fontsize=20, color=colordict[dr_level['head']])
    plt.text(0.66, 0.175, '\n'.join('发动机系统'), fontsize=20, color='#999999')
    plt.text(0.72, 0.225, '\n'.join('传动系统'), fontsize=20, color='#999999')
    plt.text(0.78, 0.285, '\n'.join('牵引车'), fontsize=20, color='#999999')
    # 毁伤信息
    ddict = {'none':'None','low':'轻度','mid':'中度','high':'重度'}
    damage_dict0 = {"毁伤等级": ddict[dr_level['zkc']], "置信度": random.uniform(0.8,1)}
    damage_dict1 = {"毁伤等级": ddict[dr_level['head']], "置信度": random.uniform(0.8,1)}
    damage_dict2 = {"毁伤等级": ddict[dr_level['box']], "置信度": random.uniform(0.8,1)}

    damage_dict = {"电源车": damage_dict0, "驾驶舱": damage_dict1, "电源舱": damage_dict2}
    # 连线
    linex = [[0.48, 0.26], [0.48, 0.7], \
             [0.26, 0.26], [0.71, 0.62], [0.71, 0.68], [0.71, 0.74], [0.71, 0.8]]
    liney = [[0.85, 0.69], [0.85, 0.69], \
             [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45]]
    # for line in range(len([linex])):
    for line in range(len(linex)):
        plt.plot(linex[line], liney[line], color='#000000')
    # # 绘制"颜色-毁伤程度"矩形框, 并隐藏坐标轴
    currentAxis = plt.gca()
    currentAxis.axes.xaxis.set_visible(False)
    currentAxis.axes.yaxis.set_visible(False)
    currentAxis.add_patch(patches.Rectangle((0.05, 0.05), 0.05, 0.025, color='#FF0033', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.3, 0.05), 0.05, 0.025, color='#FF6600', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.55, 0.05), 0.05, 0.025, color='#006600', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.80, 0.05), 0.05, 0.025, color='#999999', fill=True))
    # 添加"颜色-毁伤程度"文字说明
    plt.text(0.13, 0.05, '重度毁伤', color='#FF0033', fontsize=20)
    plt.text(0.38, 0.05, '中度毁伤', color='#FF6600', fontsize=20)
    plt.text(0.63, 0.05, '轻度毁伤', color='#006600', fontsize=20)
    plt.text(0.88, 0.05, '无毁伤', color='#999999', fontsize=20)

    # 保存并转换numpy.ndarray
    buffer_ = BytesIO()
    plt.savefig(buffer_, format='png', dpi=200, bbox_inches='tight', pad_inches=0)
    plt.clf()
    plt.cla()
    buffer_.seek(0)
    dataPIL = PIL.Image.open(buffer_)
    dataPIL = dataPIL.resize((2160, 1440), PIL.Image.ANTIALIAS)
    buffer_.close()
    img4 = cv2.cvtColor(np.asarray(dataPIL), cv2.COLOR_RGB2BGR)
    return img4, damage_dict

def damage_tree_tank(dr):
    """
        tan ke che

    二级标题：
        二个: 0.20 0.58
        三个: 0.10 0.41 0.71
        四个: 0.07 0.30 0.51 0.80

    三级标题：
        2-6个字的y分别是: 0.335 0.285 0.225 0.175 0.125

    连线：
        linex=[[0.48,0.14], [0.48,0.37], [0.48,0.61], [0.48,0.865], \  一、二级之间
        [0.14,0.04], [0.14,0.09], [0.14,0.14], [0.14,0.19], [0.14,0.24], 二三级之间
        [0.37,0.33], [0.37,0.41], [0.61,0.54], [0.61,0.68], [0.865,0.81], [0.865,0.865], [0.865,0.92]] 二三级之间

        线的x值比对应字的x大0.015-0.02较合适

    """
    dr_level = dr.copy()
    # 相关配置
    import matplotlib.patches as patches
    plt.style.use("seaborn-dark")
    plt.rcParams['savefig.dpi'] = 200  # 图片像素
    plt.rcParams['figure.dpi'] = 200  # 分辨率
    plt.rcParams['figure.figsize'] = (10.8, 7.2)  # 设置figure_size尺寸
    plt.rcParams['image.interpolation'] = 'nearest'  # 设置 interpolation style
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False
    # 限制坐标轴范围
    plt.ylim(0.0, 1.0)
    plt.xlim(0.0, 1.0)

    # 二级毁伤率确定 (三级毁伤率本身包含于dr_level中)
    dr_level['huoKongSYS'] = 0
    dr_level['xingZouSYS'] = max(dr_level['lvdai'], 0)
    dr_level['dongLiSYS'] = 0
    dr_level['wuQiSYS'] = max(dr_level['huopao'], 0)
    dr_level['jieGouSYS'] = max(dr_level['cheshen'],dr_level['jiashicang'], 0)
    # 一级毁伤率确定
    dr_level['tank'] = max(dr_level['huoKongSYS'], dr_level['xingZouSYS'], dr_level['wuQiSYS'], dr_level['dongLiSYS'], dr_level['jieGouSYS'])
    # 各级颜色判定
    for key in dr_level:
        if dr_level[key] >= 0 and dr_level[key] <= 0.2:
            dr_level[key] = "low"
        elif dr_level[key] > 0.2 and dr_level[key] <= 0.6:
            dr_level[key] = "mid"
        elif dr_level[key] > 0.6:
            dr_level[key] = "high"
        else:
            dr_level[key] = "none"

    colordict = {'none': '#999999', 'low': '#006600', 'mid': '#FF6600', 'high': '#FF0033'}
    # 一级部位
    plt.text(0.42, 0.875, '坦克车', fontsize=40, color=colordict[dr_level['tank']])
    # 二级部位
    plt.text(0.02, 0.625, '火控系统', fontsize=20, color=colordict[dr_level['huoKongSYS']])
    plt.text(0.18, 0.625, '行走系统', fontsize=20, color=colordict[dr_level['xingZouSYS']])
    plt.text(0.35, 0.625, '动力系统', fontsize=20, color=colordict[dr_level['dongLiSYS']])
    plt.text(0.51, 0.625, '通讯系统', fontsize=20, color='#999999')
    plt.text(0.67, 0.625, '武器系统', fontsize=20, color=colordict[dr_level['wuQiSYS']])
    plt.text(0.84, 0.625, '结构系统', fontsize=20, color=colordict[dr_level['jieGouSYS']])
    # 三级部位 #999999 表示没有，各种不同的轮子都按照同一种轮子算毁伤结果
    # 注意参考原prac_damage_tree_old.py
    plt.text(0.04, 0.175, '\n'.join('火控计算机'), fontsize=20, color='#999999')
    plt.text(0.10, 0.235, '\n'.join('瞄准装置'), fontsize=20, color='#999999')
    plt.text(0.16, 0.335, '\n'.join('履带'), fontsize=20, color=colordict[dr_level['lvdai']])
    plt.text(0.21, 0.285, '\n'.join('主动轮'), fontsize=20, color='#999999')
    plt.text(0.26, 0.285, '\n'.join('负重轮'), fontsize=20, color='#999999')
    plt.text(0.31, 0.285, '\n'.join('诱导轮'), fontsize=20, color='#999999')
    plt.text(0.36, 0.285, '\n'.join('发动机'), fontsize=20, color='#999999')
    plt.text(0.41, 0.225, '\n'.join('传动机构'), fontsize=20, color='#999999')
    plt.text(0.46, 0.335, '\n'.join('邮箱'), fontsize=20, color='#999999')
    plt.text(0.52, 0.335, '\n'.join('天线'), fontsize=20, color='#999999')
    plt.text(0.59, 0.225, '\n'.join('无线电台'), fontsize=20, color='#999999')
    plt.text(0.66, 0.335, '\n'.join('主炮'), fontsize=20, color=colordict[dr_level['huopao']])
    plt.text(0.72, 0.225, '\n'.join('高射机枪'), fontsize=20, color='#999999')
    plt.text(0.77, 0.285, '\n'.join('弹药架'), fontsize=20, color='#999999')
    plt.text(0.86, 0.335, '\n'.join('车体'), fontsize=20, color=colordict[dr_level['cheshen']])
    plt.text(0.92, 0.335, '\n'.join('炮台'), fontsize=20, color=colordict[dr_level['jiashicang']])

    # 连线
    linex = [[0.48, 0.09], [0.48, 0.25], [0.48, 0.42], [0.48, 0.575], [0.48, 0.735], [0.48, 0.905], \
             [0.09, 0.055], [0.09, 0.115], \
             [0.25, 0.175], [0.25, 0.225], [0.25, 0.275], [0.25, 0.325], \
             [0.42, 0.375], [0.42, 0.425], [0.42, 0.475], \
             [0.575, 0.535], [0.575, 0.60], \
             [0.735, 0.675], [0.735, 0.735], [0.735, 0.785],
             [0.905, 0.875], [0.905, 0.94]]
    liney = [[0.85, 0.69], [0.85, 0.69], [0.85, 0.69], [0.85, 0.69], [0.85, 0.69], [0.85, 0.69], \
             [0.6, 0.45], [0.6, 0.45], \
             [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], \
             [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], \
             [0.6, 0.45], [0.6, 0.45], \
             [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], \
             [0.6, 0.45], [0.6, 0.45]]
    for line in range(len(linex)):
        plt.plot(linex[line], liney[line], color='#000000')

    # # 绘制"颜色-毁伤程度"矩形框, 并隐藏坐标轴
    currentAxis = plt.gca()
    currentAxis.axes.xaxis.set_visible(False)
    currentAxis.axes.yaxis.set_visible(False)
    currentAxis.add_patch(patches.Rectangle((0.05, 0.05), 0.05, 0.025, color='#FF0033', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.3, 0.05), 0.05, 0.025, color='#FF6600', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.55, 0.05), 0.05, 0.025, color='#006600', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.80, 0.05), 0.05, 0.025, color='#999999', fill=True))
    # 添加"颜色-毁伤程度"文字说明
    plt.text(0.13, 0.05, '重度毁伤', color='#FF0033', fontsize=20)
    plt.text(0.38, 0.05, '中度毁伤', color='#FF6600', fontsize=20)
    plt.text(0.63, 0.05, '轻度毁伤', color='#006600', fontsize=20)
    plt.text(0.88, 0.05, '无毁伤', color='#999999', fontsize=20)

    # 毁伤信息
    ddict = {'none': 'None', 'low': '轻度', 'mid': '中度', 'high': '重度'}
    damage_dict0 = {"毁伤等级": ddict[dr_level['tank']], "置信度": random.uniform(0.8, 1)}
    damage_dict1 = {"毁伤等级": ddict[dr_level['jiashicang']], "置信度": 0}
    damage_dict2 = {"毁伤等级": ddict[dr_level['cheshen']], "置信度": random.uniform(0.8, 1)}
    damage_dict3 = {"毁伤等级": ddict[dr_level['huopao']], "置信度": random.uniform(0.8, 1)}
    damage_dict4 = {"毁伤等级": ddict[dr_level['lvdai']], "置信度": random.uniform(0.8, 1)}

    damage_dict = {"坦克": damage_dict0, "炮台": damage_dict1, "车身": damage_dict2, "主炮": damage_dict3,
                   "履带": damage_dict4}






    # 保存并转换numpy.ndarray
    buffer_ = BytesIO()
    plt.savefig(buffer_, format='png', dpi=200, bbox_inches='tight', pad_inches=0)
    plt.clf()
    plt.cla()
    buffer_.seek(0)
    dataPIL = PIL.Image.open(buffer_)
    dataPIL = dataPIL.resize((2160, 1440), PIL.Image.ANTIALIAS)
    buffer_.close()
    img4 = cv2.cvtColor(np.asarray(dataPIL), cv2.COLOR_RGB2BGR)

    return img4, damage_dict

def damage_tree_plane(dr):
    dr_level = dr.copy()
    # 相关配置
    import matplotlib.patches as patches
    plt.style.use("seaborn-dark")
    plt.rcParams['savefig.dpi'] = 200  # 图片像素
    plt.rcParams['figure.dpi'] = 200  # 分辨率
    plt.rcParams['figure.figsize'] = (10.8, 7.2)  # 设置figure_size尺寸
    plt.rcParams['image.interpolation'] = 'nearest'  # 设置 interpolation style
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False
    # 限制坐标轴范围
    plt.ylim(0.0, 1.0)
    plt.xlim(0.0, 1.0)

    # 二级毁伤率确定
    dr_level['waiXingJieGou'] = max(dr_level['jishen'], dr_level['jiyi'], dr_level['lunzi'], dr_level['chuiwei'])
    dr_level['daoHangXiTong'] = max(dr_level['leida'], 0)
    # 一级毁伤率确定
    dr_level['Plane'] = max(dr_level['waiXingJieGou'], dr_level['daoHangXiTong'])
    # 各级颜色判定
    for key in dr_level:
        if dr_level[key] >= 0 and dr_level[key] <= 0.2:
            dr_level[key] = "low"
        elif dr_level[key] > 0.05 and dr_level[key] <= 0.2:
            dr_level[key] = "mid"
        elif dr_level[key] > 0.2:
            dr_level[key] = "high"
        else:
            dr_level[key] = "none"

    colordict = {'none': '#999999', 'low': '#006600', 'mid': '#FF6600', 'high': '#FF0033'}
    # 一级部位
    plt.text(0.43, 0.875, '飞机', fontsize=40, color=colordict[dr_level['Plane']])

    # 二级部位
    plt.text(0.155, 0.625, '外形结构', fontsize=20, color=colordict[dr_level['waiXingJieGou']])
    plt.text(0.41, 0.625, '动力系统', fontsize=20, color='#999999')
    plt.text(0.645, 0.625, '航电系统', fontsize=20, color='#999999')
    plt.text(0.825, 0.625, '导航系统', fontsize=20, color=colordict[dr_level['daoHangXiTong']])
    # 三级部位 #999999 表示没有
    plt.text(0.06, 0.275, '\n'.join('驾驶舱'), fontsize=20, color='#999999')
    plt.text(0.12, 0.325, '\n'.join('机身'), fontsize=20, color=colordict[dr_level['jishen']])
    plt.text(0.18, 0.325, '\n'.join('机翼'), fontsize=20, color=colordict[dr_level['jiyi']])
    plt.text(0.24, 0.325, '\n'.join('轮子'), fontsize=20, color=colordict[dr_level['lunzi']])
    plt.text(0.3, 0.325, '\n'.join('垂尾'), fontsize=20, color=colordict[dr_level['chuiwei']])
    plt.text(0.42, 0.275, '\n'.join('发动机'), fontsize=20, color='#999999')
    plt.text(0.50, 0.325, '\n'.join('油箱'), fontsize=20, color='#999999')
    plt.text(0.655, 0.175, '\n'.join('航电设备舱'), fontsize=20, color='#999999')
    plt.text(0.73, 0.225, '\n'.join('电力系统'), fontsize=20, color='#999999')
    plt.text(0.83, 0.325, '\n'.join('雷达'), fontsize=20, color=colordict[dr_level['leida']])
    plt.text(0.91, 0.325, '\n'.join('天线'), fontsize=20, color='#999999')
    # 毁伤信息
    ddict = {'none':'None','low':'轻度','mid':'中度','high':'重度'}
    damage_dict0 = {"毁伤等级": ddict[dr_level['Plane']], "置信度": random.uniform(0.8,1)}
    damage_dict1 = {"毁伤等级": ddict['none'], "置信度": 0}
    damage_dict2 = {"毁伤等级": ddict[dr_level['jishen']], "置信度": random.uniform(0.8,1)}
    damage_dict3 = {"毁伤等级": ddict[dr_level['jiyi']], "置信度": random.uniform(0.8,1)}
    damage_dict4 = {"毁伤等级": ddict[dr_level['chuiwei']], "置信度": random.uniform(0.8,1)}
    damage_dict5 = {"毁伤等级": ddict[dr_level['lunzi']], "置信度": random.uniform(0.8,1)}
    damage_dict = {"飞机": damage_dict0, "驾驶舱": damage_dict1, "机身": damage_dict2, "机翼": damage_dict3,
                   "垂尾": damage_dict4, "轮子": damage_dict5}
    # # 绘制"颜色-毁伤程度"矩形框, 并隐藏坐标轴
    currentAxis = plt.gca()
    currentAxis.axes.xaxis.set_visible(False)
    currentAxis.axes.yaxis.set_visible(False)
    currentAxis.add_patch(patches.Rectangle((0.05, 0.05), 0.05, 0.025, color='#FF0033', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.3, 0.05), 0.05, 0.025, color='#FF6600', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.55, 0.05), 0.05, 0.025, color='#006600', fill=True))
    currentAxis.add_patch(patches.Rectangle((0.80, 0.05), 0.05, 0.025, color='#999999', fill=True))
    # 添加"颜色-毁伤程度"文字说明
    plt.text(0.13, 0.05, '重度毁伤', color='#FF0033', fontsize=20)
    plt.text(0.38, 0.05, '中度毁伤', color='#FF6600', fontsize=20)
    plt.text(0.63, 0.05, '轻度毁伤', color='#006600', fontsize=20)
    plt.text(0.88, 0.05, '未检测', color='#999999', fontsize=20)
    # 连线
    linex = [[0.5, 0.225], [0.5, 0.48], [0.5, 0.71], [0.5, 0.89], \
             [0.2, 0.08], [0.2, 0.14], [0.2, 0.2], [0.2, 0.26], [0.2, 0.32], [0.48, 0.44], [0.48, 0.52],
             [0.71, 0.67], [0.71, 0.75], [0.89, 0.85], [0.89, 0.93]]
    liney = [[0.85, 0.69], [0.85, 0.69], [0.85, 0.69], [0.85, 0.69], \
             [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45], [0.6, 0.45],
             [0.6, 0.45], [0.6, 0.45], [0.6, 0.45]]
    for line in range(len(linex)):
        plt.plot(linex[line], liney[line], color='black')
    # 保存并转换numpy.ndarray
    buffer_ = BytesIO()
    plt.savefig(buffer_, format='png', dpi=200, bbox_inches='tight', pad_inches=0)
    plt.clf()
    plt.cla()
    buffer_.seek(0)
    dataPIL = PIL.Image.open(buffer_)
    dataPIL = dataPIL.resize((2160, 1440), Image.ANTIALIAS)
    buffer_.close()
    img4 = cv2.cvtColor(np.asarray(dataPIL), cv2.COLOR_RGB2BGR)

    return img4, damage_dict