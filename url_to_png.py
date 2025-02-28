import requests
from PIL import Image
import os
from io import BytesIO

def download_and_convert(url, output_dir, index):
    try:
        # 下载图片
        response = requests.get(url)
        response.raise_for_status()
        
        # 使用PIL打开图片
        image = Image.open(BytesIO(response.content))
        
        # 转换为PNG格式并保存
        output_path = os.path.join(output_dir, f'image_{index}.png')
        image.save(output_path, 'PNG')
        
        print(f'成功下载并转换: {url} -> {output_path}')
        return True
    except Exception as e:
        print(f'处理图片时出错 {url}: {str(e)}')
        return False

def batch_download_images():
    # 创建输出目录
    output_dir = 'downloaded_images'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print('请输入图片URL（每行一个URL，输入空行结束）：')
    urls = []
    while True:
        url = input().strip()
        if not url:
            break
        urls.append(url)
    
    if not urls:
        print('没有输入URL，程序退出')
        return
    
    print(f'\n开始下载 {len(urls)} 个图片...')
    success_count = 0
    
    for i, url in enumerate(urls, 1):
        if download_and_convert(url, output_dir, i):
            success_count += 1
    
    print(f'\n下载完成！成功: {success_count}/{len(urls)}')
    print(f'图片保存在: {os.path.abspath(output_dir)}')

if __name__ == '__main__':
    print('URL图片下载器 - 支持将图片转换为PNG格式')
    print('='*50)
    batch_download_images()