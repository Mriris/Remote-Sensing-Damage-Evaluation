# RSDE - 遥感建筑物损伤检测

基于深度学习的建筑物损伤检测，使用 SegFormer 语义分割模型对灾前灾后遥感图像进行对比分析。

## 功能简介

1. 检测遥感图像中的建筑物位置
2. 分析灾后图像中建筑物的损伤程度
3. 计算损伤比率并分级（低/中/高）
4. 生成可视化结果图像

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境
uv venv --python 3.12
uv pip install torch torchvision # --index-url https://download.pytorch.org/whl/cu128 #Linux可选指定CUDA版本（默认CUDA12.8），但Windows必须指定CUDA版本
uv sync # -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 准备模型文件

确保 `model_files` 目录下包含以下模型文件：
- `building.pth` - 建筑物分割模型
- `damage.pth` - 损伤检测模型

### 3. 运行检测

**基本用法：**

```bash
python main.py
```

默认会处理 `test` 目录下的示例图片（`pre.jpg` 和 `post.jpg`），结果保存在 `test/output` 目录。

**自定义输入：**

```bash
python main.py --input_former 灾前图片.jpg --input_latter 灾后图片.jpg --output_path 输出目录
```

### 4. 查看结果

运行完成后，在输出目录会生成：
- `building_seg_img.jpg` - 建筑物分割可视化结果
- `out.jpg` - 损伤检测标注结果（包含损伤等级和比率）

## 损伤等级说明

系统会根据损伤比率自动分级：

| 损伤比率 | 等级 | 颜色标注 |
|---------|------|---------|
| < 20%   | low  | 绿色 🟢 |
| 20%-70% | mid  | 黄色 🟡 |
| > 70%   | high | 红色 🔴 |

## 项目结构

```
RSDE/
├── main.py               # 主程序入口
├── inference.py          # 推理核心逻辑
├── model_files/          # 模型权重文件
│   ├── building.pth
│   ├── damage.pth
├── nets/                 # 网络模型定义
│   ├── segformer.py
│   ├── backbone.py
│   └── segformer_training.py
├── test/                 # 测试数据
│   ├── pre.jpg           # 灾前图像
│   ├── post.jpg          # 灾后图像
│   └── output/           # 输出结果
└── pyproject.toml        # 项目配置
```

## 技术原理

1. **建筑物检测**：使用 SegFormer-B1 模型对灾前图像进行语义分割，提取建筑物轮廓
2. **损伤评估**：对每个建筑物区域，使用损伤检测模型分析灾后图像
3. **损伤量化**：计算损伤像素占建筑物总像素的比例
4. **结果可视化**：在图像上标注损伤等级和比率

## 参数说明

| 参数 | 说明 | 默认值 |
|-----|------|--------|
| `--input_former` | 灾前图像路径 | `test\pre.jpg` |
| `--input_latter` | 灾后图像路径 | `test\post.jpg` |
| `--output_path` | 输出目录 | `test\output` |

