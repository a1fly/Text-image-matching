from PIL import Image
import os
# 读取 ./pic 文件夹中的所有图片
def load_images_from_folder(folder_path):
    """
    从指定文件夹加载所有图片
    :param folder_path: str, 图片文件夹路径
    :return: list of PIL.Image, 图片列表
    """
    supported_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')  # 支持的图片格式
    images = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(supported_extensions):  # 检查文件扩展名
            file_path = os.path.join(folder_path, filename)
            try:
                img = Image.open(file_path).convert("RGB")  # 确保图片是 RGB 格式
                images.append(img)
            except Exception as e:
                print(f"无法加载图片 {file_path}: {e}")
    return images