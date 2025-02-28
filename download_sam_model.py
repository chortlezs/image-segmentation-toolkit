import requests
import sys
import os

def check_dependencies():
    try:
        print('正在检查Python环境...')
        import requests
        print('✓ requests 模块已安装')
        return True
    except ImportError:
        print('错误：缺少必要的Python包')
        print('请运行以下命令安装：')
        print('pip install requests')
        return False

def check_python_version():
    print(f'Python版本: {sys.version}')
    if sys.version_info < (3, 6):
        print('警告：建议使用Python 3.6或更高版本')
        return False
    return True

def main():
    print('SAM模型下载器')
    print('='*50)
    
    if not check_python_version() or not check_dependencies():
        sys.exit(1)
    
    try:
        import requests
        
        url = 'https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth'
        filename = 'sam_vit_h_4b8939.pth'
        
        if os.path.exists(filename):
            print(f'发现已存在的模型文件：{filename}')
            size_gb = os.path.getsize(filename) / (1024*1024*1024)
            if size_gb < 2.0:
                print(f'警告：现有文件大小异常（{size_gb:.1f}GB），将重新下载')
                os.remove(filename)
            else:
                print(f'文件大小正常（{size_gb:.1f}GB），无需重新下载')
                sys.exit(0)
        
        print('正在检查网络连接...')
        try:
            response = requests.get('https://www.google.com', timeout=5)
            response.raise_for_status()
            print('✓ 网络连接正常')
        except requests.RequestException as e:
            print('网络连接测试失败，请检查：')
            print('1. 是否已连接到互联网')
            print('2. 是否需要设置代理')
            print(f'错误详情：{str(e)}')
            sys.exit(1)
        
        print(f'\n开始下载SAM模型文件: {filename}')
        print('文件较大（约2.4GB），请耐心等待...')
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, stream=True, headers=headers, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024 * 1024  # 1MB
        downloaded = 0

        with open(filename, 'wb') as f:
            for data in response.iter_content(block_size):
                f.write(data)
                downloaded += len(data)
                progress = int(50 * downloaded / total_size)
                sys.stdout.write(f'\r下载进度: [{"="*progress}{" "*(50-progress)}] {downloaded/(1024*1024*1024):.1f}GB/{total_size/(1024*1024*1024):.1f}GB')
                sys.stdout.flush()
        print('\n下载完成！')
        
        if os.path.getsize(filename) != total_size:
            print('警告：下载的文件大小与预期不符，可能已损坏')
            print('建议重新运行此脚本进行下载')
            os.remove(filename)
            sys.exit(1)
        
        print('模型文件下载成功，现在可以运行 png_to_mask.py 了')
        
    except requests.Timeout:
        print('\n下载超时，请检查网络连接速度')
        if os.path.exists(filename):
            os.remove(filename)
        sys.exit(1)
    except requests.RequestException as e:
        print(f'\n网络请求错误：{str(e)}')
        print('请检查网络连接或代理设置')
        if os.path.exists(filename):
            os.remove(filename)
        sys.exit(1)
    except Exception as e:
        print(f'\n程序出错：{str(e)}')
        print('请检查网络连接后重试')
        if os.path.exists(filename):
            os.remove(filename)
        sys.exit(1)

if __name__ == '__main__':
    main()