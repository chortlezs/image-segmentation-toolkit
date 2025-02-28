import os
import numpy as np
import torch
from PIL import Image
from segment_anything import sam_model_registry, SamPredictor

def check_model_file(model_path):
    # 检查模型文件是否存在
    if not os.path.exists(model_path):
        print(f'错误：找不到SAM模型文件 {model_path}')
        print('请运行 download_sam_model.py 下载模型文件')
        return False
    
    # 检查文件大小（SAM模型文件应该大于2GB）
    file_size = os.path.getsize(model_path) / (1024 * 1024 * 1024)  # 转换为GB
    if file_size < 2.0:
        print(f'警告：SAM模型文件大小异常（{file_size:.1f}GB），可能已损坏')
        print('建议重新运行 download_sam_model.py 下载模型文件')
        return False
    
    return True

def initialize_sam():
    # 初始化SAM模型
    sam_checkpoint = "sam_vit_h_4b8939.pth"
    model_type = "vit_h"
    
    # 检查模型文件
    if not check_model_file(sam_checkpoint):
        return None
    
    try:
        print('正在加载SAM模型到内存...')
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        sam.to(device=device)
        print('SAM模型加载成功！')
        return SamPredictor(sam)
    except Exception as e:
        print(f'加载SAM模型时出错：{str(e)}')
        print('建议重新运行 download_sam_model.py 下载模型文件')
        return None

def generate_mask(predictor, image):
    # 生成图像主体mask
    predictor.set_image(np.array(image))
    # 使用图像中心点作为提示
    h, w = np.array(image).shape[:2]
    input_point = np.array([[w//2, h//2]])
    input_label = np.array([1])
    masks, _, _ = predictor.predict(point_coords=input_point, point_labels=input_label)
    # 返回最大的mask作为主体mask
    return masks[0]

def process_images(input_dir):
    # 初始化SAM模型
    print('正在初始化SAM模型...')
    predictor = initialize_sam()
    if predictor is None:
        return
    print('SAM模型初始化完成！')
    
    # 创建输出目录
    masks_dir = os.path.join(input_dir, 'masks')
    if not os.path.exists(masks_dir):
        os.makedirs(masks_dir)
    
    # 获取所有PNG图片
    image_files = [f for f in os.listdir(input_dir) if f.endswith('.png') and not f.endswith('_mask.png')]
    
    if not image_files:
        print('没有找到PNG图片，程序退出')
        return
    
    print(f'\n开始处理 {len(image_files)} 个PNG图片...')
    success_count = 0
    
    for image_file in image_files:
        try:
            # 读取图片
            image_path = os.path.join(input_dir, image_file)
            image = Image.open(image_path)
            
            # 生成mask并保存
            mask = generate_mask(predictor, image)
            mask_image = Image.fromarray((mask * 255).astype(np.uint8))
            mask_name = os.path.splitext(image_file)[0] + '_mask.png'
            mask_path = os.path.join(masks_dir, mask_name)
            mask_image.save(mask_path)
            
            print(f'成功处理: {image_file} -> {mask_name}')
            success_count += 1
        except Exception as e:
            print(f'处理图片时出错 {image_file}: {str(e)}')
    
    print(f'\n处理完成！成功: {success_count}/{len(image_files)}')
    print(f'Mask图片保存在: {os.path.abspath(masks_dir)}')

if __name__ == '__main__':
    print('PNG图片主体识别器 - 生成Mask图片')
    print('='*50)
    
    # 获取输入目录
    while True:
        input_dir = input('请输入包含PNG图片的目录路径（默认为 downloaded_images）：').strip()
        # 去除可能包含的引号
        input_dir = input_dir.strip('"').strip("'")
        if not input_dir:
            input_dir = 'downloaded_images'
        
        if os.path.exists(input_dir):
            break
        else:
            print('目录不存在，请重新输入')
    
    process_images(input_dir)