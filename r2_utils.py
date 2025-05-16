"""
R2 存储工具模块。
负责下载、上传和管理 Cloudflare R2 存储的图片。
"""
import os
import hashlib
import requests
import boto3
from config import R2_ACCESS_KEY, R2_SECRET_KEY, R2_BUCKET, R2_ENDPOINT, IMAGE_PREFIX, VERBOSE_OUTPUT

def download_image(url, save_path):
    """
    从URL下载图片到本地临时文件
    
    参数:
        url (str): 图片URL地址
        save_path (str): 本地保存路径
        
    返回:
        bool: 下载是否成功
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(response.content)
        if VERBOSE_OUTPUT:
            print(f"下载图片成功: {url}")
        return True
    except Exception as e:
        print(f"下载图片失败: {url}，原因: {e}")
        return False

def upload_to_r2(local_path, object_name):
    """
    上传本地文件到R2存储
    
    参数:
        local_path (str): 本地文件路径
        object_name (str): R2中的对象名称
        
    返回:
        str或None: 上传成功返回R2公开URL，失败返回None
    """
    try:
        session = boto3.session.Session()
        s3 = session.client(
            service_name="s3",
            aws_access_key_id=R2_ACCESS_KEY,
            aws_secret_access_key=R2_SECRET_KEY,
            endpoint_url=R2_ENDPOINT,
        )
        s3.upload_file(local_path, R2_BUCKET, object_name)
        # R2 的公开访问链接格式
        url = f"{R2_ENDPOINT}/{R2_BUCKET}/{object_name}"
        if VERBOSE_OUTPUT:
            print(f"上传到R2成功: {url}")
        return url
    except Exception as e:
        print(f"上传到R2失败: {local_path}，原因: {e}")
        return None

def process_image(img_url):
    """
    处理图片：下载、上传到R2并返回新的URL
    
    参数:
        img_url (str): 原始图片URL
        
    返回:
        str: 处理后的图片URL（如果处理失败则返回原URL）
    """
    # 用图片链接的hash作为文件名，避免重复
    img_hash = hashlib.md5(img_url.encode("utf-8")).hexdigest()
    ext = os.path.splitext(img_url)[-1].split("?")[0] or ".jpg"  # 获取扩展名，默认为.jpg
    local_path = f"tmp_{img_hash}{ext}"
    
    try:
        # 1. 下载图片
        if download_image(img_url, local_path):
            # 2. 上传到R2
            r2_url = upload_to_r2(local_path, f"{IMAGE_PREFIX}/{img_hash}{ext}")
            # 3. 删除临时文件
            os.remove(local_path)
            # 4. 返回新URL或原URL
            return r2_url if r2_url else img_url
        return img_url
    except Exception as e:
        print(f"处理图片失败: {img_url}，原因: {e}")
        # 如果临时文件存在，尝试删除
        if os.path.exists(local_path):
            try:
                os.remove(local_path)
            except:
                pass
        return img_url 