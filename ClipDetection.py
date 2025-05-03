import cn_clip.clip as clip
from cn_clip.clip import load_from_name
import torch
from PIL import Image
from tool import load_images_from_folder

class ClipDet:
    def __init__(self, modelname='ViT-B-16', modelpath='./model'):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"使用设备: {self.device}")
        self.modelname = modelname
        self.modelpath = modelpath
        self.model, self.preprocess = load_from_name(self.modelname, device=self.device, download_root=self.modelpath)

    def get_text_features(self, query_texts):
        """
        获取批量文本特征
        :param query_texts: list of str, 批量文本
        :return: Tensor, 形状为 (batch_size, feature_dim)
        """
        texts = clip.tokenize(query_texts).to(self.device)  # 批量 tokenize
        text_features = self.model.encode_text(texts)  # 批量编码
        return text_features

    def get_image_features(self, images):
        """
        获取批量图像特征
        :param images: list of PIL.Image, 批量图像
        :return: Tensor, 形状为 (batch_size, feature_dim)
        """
        images_preprocessed = torch.stack([self.preprocess(image) for image in images]).to(self.device)  # 批量预处理
        image_features = self.model.encode_image(images_preprocessed)  # 批量编码
        return image_features

    def get_similarity(self, text_features, image_features):
        """
        计算文本和图像之间的余弦相似度
        :param text_features: Tensor, 形状为 (text_batch_size, feature_dim)
        :param image_features: Tensor, 形状为 (image_batch_size, feature_dim)
        :return: Tensor, 形状为 (text_batch_size, image_batch_size)
        """
        # 归一化特征
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)

        # 计算余弦相似度矩阵
        similarity = torch.nn.functional.cosine_similarity(
            text_features.unsqueeze(1),  # (text_batch_size, 1, feature_dim)
            image_features.unsqueeze(0),  # (1, image_batch_size, feature_dim)
            dim=-1  # 在最后一个维度上计算余弦相似度
        )
        return similarity

if __name__ == '__main__':
    clipdet = ClipDet()
    querty_texts = ["电工书","白色的耳机"]

    folder_path = "./pic"
    images = load_images_from_folder(folder_path)

    if not images:
        print("未找到任何图片！")
    else:
        # 批量提取图像特征
        image_features = clipdet.get_image_features(images)
        print(f"成功提取 {len(images)} 张图片的特征，特征形状为 {image_features.shape}")











