from pathlib import Path

from PIL import Image
from datetime import datetime
import os
from typing import List
import hashlib

"""
主要用于图片的处理

功能包括：

1. 读取directory目录下的所有图片  get_all_pic_paths
2. 存储图片到指定路径下并且返回路径列表  save_images_to_directory

"""
class ImageProcessor():
    def __init__(self):
        pass

    # 获取到某文件夹下的所有文件的路径
    def get_all_pic_paths(self,directory: str)->List[str]:
        # 可用的后缀名
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
        pic_paths = [
            str(file) for file in Path(directory).rglob('*')
            if file.is_file() and file.suffix.lower() in image_extensions
        ]
        return pic_paths


    def save_images_to_directory(self,
                                 image_files: List[Image.Image],
                                 mainRoot: str = "./") -> List[str]:
        """
        将图片文件保存到特定的时间目录并返回路径列表。

        参数:
        image_files (List[Image]): 图片文件对象的列表。
        mainRoot (str): 所有图片保存的总目录

        返回:
        List[str]: 存储后的图片路径列表。
        """
        # 获取当前时间并格式化为年、月、日
        current_time = datetime.now().strftime("%Y-%m-%d").split("-")
        year, month, day = current_time[0], current_time[1], current_time[2]

        # 构建目标目录路径
        target_dir = os.path.join(mainRoot, year, month, day)

        # 如果目录不存在，则创建
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # 存储后的图片路径列表
        saved_image_paths = []

        for idx, image in enumerate(image_files):
            # 使用当前时间作为图片名
            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            # 为避免文件名冲突，可以在文件名后面加上索引
            image_name = f"{timestamp}-{idx}.jpg"
            image_path = os.path.join(target_dir, image_name)

            # 保存图片
            image.save(image_path)
            saved_image_paths.append(image_path)

        # 返回存储后的路径列表
        return saved_image_paths







if __name__=='__main__':
    ip=ImageProcessor()
    # 假设你有一个 Image 对象列表
    image_files = [Image.open("../game.jpg")]
    print(type(image_files))
    print(type(image_files[0]))


    # 调用函数保存图片
    saved_paths = ip.save_images_to_directory(image_files, mainRoot="../resource/images")

    # 打印保存的图片路径
    print(saved_paths)








