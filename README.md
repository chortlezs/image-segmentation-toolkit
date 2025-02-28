# 图片主体识别工具

这是一个基于SAM（Segment Anything Model）的图片主体识别工具，可以自动下载图片并生成主体遮罩。

## 功能特点

- 支持从URL批量下载图片并转换为PNG格式
- 使用SAM模型自动识别图片主体
- 生成高质量的主体遮罩（mask）图片
- 支持批量处理多张图片
- 自动下载所需的SAM模型文件

## 使用方法

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 下载SAM模型：
```bash
python download_sam_model.py
```

3. 下载并转换图片：
```bash
python url_to_png.py
```
将图片URL逐行粘贴到命令行中，输入空行结束。图片将被下载并转换为PNG格式，保存在`downloaded_images`目录中。

4. 生成主体遮罩：
```bash
python png_to_mask.py
```
程序会自动处理`downloaded_images`目录中的所有PNG图片，生成的遮罩图片将保存在`downloaded_images/masks`目录中。

## 系统要求

- Python 3.6 或更高版本
- CUDA支持（可选，用于GPU加速）
- 至少4GB可用内存
- 至少3GB可用磁盘空间（用于存储SAM模型）

## 注意事项

- SAM模型文件较大（约2.4GB），首次使用需要下载
- 建议使用GPU进行加速，CPU处理可能较慢
- 处理大量图片时，请确保有足够的磁盘空间

## 技术依赖

- segment_anything：用于图片主体识别
- torch：深度学习框架
- numpy：数值计算库
- Pillow：图像处理库
- requests：网络请求库

## 许可证

MIT License