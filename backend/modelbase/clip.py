import torch
from PIL import Image
import cn_clip.clip as clip
from cn_clip.clip import load_from_name
from pathlib import Path
import matplotlib.pyplot as plt
from tqdm import tqdm
from typing import List, Tuple
from backend.tools.imageTool import ImageProcessor
import json
import torch.nn.functional as F

"""
使用CLIP模型进行图文匹配得出文字和所有图片的相似度

功能介绍：

1. batch_load_images 为节省时间和内存消耗，采取批量读取图片到内存的方式
2. calculate_similarity 计算输入的句子与图片的相似程度
3. show_images 输入图片路径和分数进行展示
4. Top_n_Pic 返回最相似的前n张图片


"""



class CLIP:
    def __init__(self,
                 config_path='./config.json',
                 modelname=None,
                 modelpath=None,
                 batch_size=None):
        """
        初始化图像搜索类，加载 CLIP 模型和预处理步骤。

        参数:
        model_name (str): 模型名称，默认为 "ViT-B-16"。
        model_path (str): 模型文件存储路径。
        device (str): 使用的设备，默认为 None，自动选择 "cuda" 或 "cpu"。
        """
        with open(config_path) as f:
            self.config = json.load(f)
        self.config =self.config['clip_config']

        if modelname is None:
            self.modelname = self.config['modelname']
        else:
            self.modelname = modelname
        if modelpath is None:
            self.modelpath = self.config['model_path']
        else:
            self.modelpath = modelpath
        if batch_size is None:
            self.batch_size = self.config['batch_size']
        else:
            self.batch_size = batch_size


        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"使用设备: {self.device}")

        # 加载模型和预处理函数
        self.model, self.preprocess = load_from_name(self.modelname, device=self.device, download_root=self.modelpath)

    def batch_load_images(self, image_paths: List[str]) -> Tuple[List[str], torch.Tensor]:
        """
        按批次加载图片，并对每张图片进行预处理。

        参数:
        image_paths (List[str]): 图片路径列表。
        batch_size (int): 每个批次的大小。

        返回:
        Tuple[List[str], torch.Tensor]: 每个批次的图片路径和对应的预处理后的图片张量。
        """
        batch_images = []
        batch_paths = []
        for i, image_path in enumerate(image_paths):
            # 读取并预处理图片
            image = self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)
            batch_images.append(image)
            batch_paths.append(image_path)

            # 如果达到当前批次大小，返回当前批次并清空缓存
            if len(batch_images) == self.batch_size or i == len(image_paths) - 1:
                yield batch_paths, torch.cat(batch_images, dim=0)  # 将图片合并成一个batch
                batch_images = []
                batch_paths = []



    def calculate_similarity(self, image_paths: List[str], query_text: str) -> List[Tuple[str, float]]:
        """
        计算图片与查询文本之间的相似度。

        参数:
        image_paths (List[str]): 图片路径列表。
        query_text (str): 查询文本，作为与图片进行匹配的文本信息。

        返回:
        List[Tuple[str, float]]: 图片路径与相似度的元组列表。
        """
        # 将查询文本转化为特征向量并进行归一化
        text = clip.tokenize([query_text]).to(self.device)
        text_features = self.model.encode_text(text)
        text_features = F.normalize(text_features, p=2, dim=-1)

        similarity_scores = []

        with torch.no_grad():
            for batch_paths, batch_images in tqdm(self.batch_load_images(image_paths),
                                                  desc="计算相似度", unit="批次",
                                                  total=len(image_paths) // self.batch_size + 1,
                                                  dynamic_ncols=True, leave=False):
                # 获取批次中的图像特征并进行归一化
                batch_image_features = self.model.encode_image(batch_images)
                batch_image_features = F.normalize(batch_image_features, p=2, dim=-1)

                # 计算每张图片与文本的余弦相似度或其他距离
                for image_path, image_feature in zip(batch_paths, batch_image_features):
                    similarity_score = F.cosine_similarity(image_feature.unsqueeze(0), text_features).item()
                    similarity_scores.append((image_path, similarity_score))

        return similarity_scores

    def Boxes_encode(self, image_path: str,image, boxes: List[List[float]]) -> List[torch.Tensor]:
        """
        为图片里面的所有的框框截取的图片编码

        参数:
        image_path (str): 原始图片的路径
        boxes (List[List[float]]): 要裁剪的区域，每个区域是一个 (left, top, right, bottom) 的列表

        返回:
        List[torch.Tensor]: 每个裁剪图片的特征向量
        """
        feature_list = []

        img=image
        # 遍历每个坐标并裁剪
        for xylist in boxes:
            left, top, right, bottom = map(int, xylist)
            box_img = img.crop((left, top, right, bottom))
            preprocessed_box_img = self.preprocess(box_img).unsqueeze(0).to(self.device)
            with torch.no_grad():
                box_feature = self.model.encode_image(preprocessed_box_img)
            feature_list.append(F.normalize(box_feature, p=2, dim=-1).squeeze(0))

        return feature_list

    def encode_Text(self,input_text):
        text = clip.tokenize([input_text]).to(self.device)
        text_features = self.model.encode_text(text)
        text_features = F.normalize(text_features, p=2, dim=-1)
        return text_features

    def cos_similarity(self, text_features: torch.Tensor, image_features: List[torch.Tensor]) -> List[float]:
        """
        计算文本特征向量与多个图像特征向量的余弦相似度

        参数:
        text_features (torch.Tensor): 文本的特征向量
        image_features (List[torch.Tensor]): 图像的特征向量列表

        返回:
        List[float]: 相似度列表
        """
        similarities = []
        for img_feature in image_features:
            similarity = F.cosine_similarity(text_features, img_feature.unsqueeze(0)).item()
            similarities.append(similarity)
        return similarities



    def show_images(self, Top_image_paths: List[str], scores: List[float]):
        """
        显示多张图片并展示它们的相似度分数。

        参数:
        image_paths (List[str]): 图片路径列表。
        scores (List[float]): 对应的相似度分数。
        """
        plt.figure(figsize=(15, 5))
        for i, (image_path, score) in enumerate(zip(Top_image_paths, scores)):
            image = Image.open(image_path)
            plt.subplot(1, len(Top_image_paths), i + 1)
            plt.imshow(image)
            plt.axis('off')
            plt.title(f"相似度: {score:.6f}")
        plt.show()

    def Top_n_Pic(self,similarity_scores,n):
        """
        输出相似度最高的前n张图片的路径和分数

        参数：
        similarity_scores: List[Tuple[str, float]] 所有的相似度

        返回：
        top_n_images: List[str] 前n张图片的路径
        top_n_scores: List[float] 前n张图片的分数
        """
        while True:
            try:
                if n <= 0 or n > len(image_paths):
                    print(f"请输入一个合理的数量 (1 到 {len(image_paths)})。")
                else:
                    break
            except ValueError:
                print("请输入一个有效的数字。")

        # 提取相似度最高的 n 张图片路径和分数
        top_n_images = [item[0] for item in similarity_scores[:n]]
        top_n_scores = [item[1] for item in similarity_scores[:n]]

        print(f"\n最相似的 {n} 张图片:")
        for image_path, score in zip(top_n_images, top_n_scores):
            print(f"图片 {image_path} 相似度： {score:.6f}")
        return top_n_images,top_n_scores



if __name__ == '__main__':
    searcher = CLIP(config_path="../config.json",modelpath="../model/clip_model")
    ip=ImageProcessor()



    # 图片文件夹的路径
    picpath = "../../resource/loss_pic"
    # 获取图片路径
    image_paths = ip.get_all_pic_paths(picpath)
    print(f"找到 {len(image_paths)} 张图片。\n")

    if len(image_paths) == 0:
        print("当前目录未存储图片！！！")
        exit(0)

    while(True):
        query_text = input("请输入查询的文本：")
        # 计算图片与查询文本之间的相似度
        similarity_scores = searcher.calculate_similarity(image_paths, query_text)
        # 按照相似度值（float）排序，从大到小
        sorted_images = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # 获取前三大的图片路径
        top_3_images = [image_path for image_path, similarity in sorted_images[:3]]

        # 输出前三大的图片路径
        # print(top_3_images)
        # print("=======================================================================")
        # print("=======================================================================")
        # print(sorted_images[:3])
        for k in range(len(sorted_images)):
            print(f"{k+1}",sorted_images[k])
        print("=======================================================================")


