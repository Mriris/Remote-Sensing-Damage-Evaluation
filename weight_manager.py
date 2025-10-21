import os
import hashlib
import requests
from tqdm import tqdm

WEIGHTS_CONFIG = {
    "building.pth": {
        "url": "https://github.com/Mriris/Remote-Sensing-Damage-Evaluation/releases/download/weights/building.pth",
        "sha256": "f40377c66025cdec89b7e231ec33be204643786cbf9f6886e58ae9a60b118260",
        "size": 54782977
    },
    "damage.pth": {
        "url": "https://github.com/Mriris/Remote-Sensing-Damage-Evaluation/releases/download/weights/damage.pth",
        "sha256": "baef876a09acda26958fcd7040066c0782e24dc9d70b858c3942789ed55aa33a",
        "size": 54782977
    }
}

MODEL_DIR = "model_files"


def calculate_sha256(file_path):
    """计算文件的 SHA256 哈希值"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def verify_file(file_path, expected_sha256):
    """验证文件的 SHA256 哈希值是否匹配"""
    if not os.path.exists(file_path):
        return False
    
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    print(f"正在校验文件: {os.path.basename(file_path)} ({file_size_mb:.1f} MB)...")
    print(f"  (校验大文件需要一些时间，请稍候...)")
    
    try:
        actual_sha256 = calculate_sha256(file_path)
    except Exception as e:
        print(f"✗ 校验过程出错: {e}")
        return False
    
    if actual_sha256 == expected_sha256:
        print(f"✓ 校验通过")
        return True
    else:
        print(f"✗ 校验失败")
        print(f"  期望: {expected_sha256}")
        print(f"  实际: {actual_sha256}")
        return False


def download_file(url, dest_path, expected_size):
    """下载文件并显示进度条"""
    print(f"正在下载: {os.path.basename(dest_path)}...")
    
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"网络请求失败: {e}")
    
    total_size = int(response.headers.get('content-length', expected_size))
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    try:
        with open(dest_path, 'wb') as f:
            with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024, desc=os.path.basename(dest_path)) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
    except Exception as e:
        if os.path.exists(dest_path):
            os.remove(dest_path)
        raise RuntimeError(f"文件写入失败: {e}")
    
    print(f"✓ 下载完成")


def check_and_download_weights():
    """检查权重文件，如果缺失或损坏则下载"""
    print("=" * 60)
    print("检查模型权重文件...")
    print("=" * 60)
    
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
        print(f"创建目录: {MODEL_DIR}")
    
    total_files = len(WEIGHTS_CONFIG)
    current_file = 0
    
    for filename, config in WEIGHTS_CONFIG.items():
        current_file += 1
        file_path = os.path.join(MODEL_DIR, filename)
        url = config["url"]
        expected_sha256 = config["sha256"]
        expected_size = config["size"]
        
        print(f"\n[{current_file}/{total_files}] 处理权重文件: {filename}")
        
        needs_download = False
        
        if os.path.exists(file_path):
            if verify_file(file_path, expected_sha256):
                print(f"文件已存在且校验通过，跳过下载")
                continue
            else:
                print(f"文件已损坏，将重新下载")
                os.remove(file_path)
                needs_download = True
        else:
            print(f"文件不存在，需要下载")
            needs_download = True
        
        if needs_download:
            try:
                download_file(url, file_path, expected_size)
                downloaded_size = os.path.getsize(file_path)
                print(f"文件已下载，大小: {downloaded_size / (1024*1024):.2f} MB")
                
                if verify_file(file_path, expected_sha256):
                    print(f"✓ 文件下载并校验成功")
                else:
                    os.remove(file_path)
                    error_msg = f"下载的文件校验失败: {filename}"
                    print(f"✗ {error_msg}")
                    raise ValueError(error_msg)
            except Exception as e:
                error_msg = f"处理文件 {filename} 时出错: {str(e)}"
                print(f"✗ {error_msg}")
                raise RuntimeError(error_msg) from e
    
    print("\n" + "=" * 60)
    print("所有权重文件检查完成")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    check_and_download_weights()

