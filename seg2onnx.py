from segformer import SegFormer_Segmentation
simplify=False

phi = "b1"
onnx_save_path = "model_files/tank_position_seg.onnx"
segformer = SegFormer_Segmentation(model_path ="model_files/tank_position_seg.pth",num_classes = 5,phi = "b1",input_shape=[640,640] )
segformer.convert_to_onnx(simplify, onnx_save_path)