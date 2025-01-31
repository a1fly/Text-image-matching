import matplotlib
import matplotlib.pyplot as plt
import pylab
import numpy as np

from PIL import Image,ImageDraw

from backend.modelbase.clip import CLIP
from backend.modelbase.translater import Translator
from backend.tools.imageTool import ImageProcessor
from backend.modelbase.yolo_detection import YoloDetection
import cn_clip.clip as clip
from cn_clip.clip import load_from_name
import torch.nn.functional as F
from backend.modelbase.blip import BLIP
from backend.modelbase.similarity import SimilarTool


def normalize(scores):
    min_score = min(scores)
    max_score = max(scores)
    return [(score - min_score) / (max_score - min_score) if max_score > min_score else 0.0 for score in scores]


class Finder:
    def __init__(self, config_path=None):
        if config_path is None:
            self.config_path = "./config.json"
        else:
            self.config_path = config_path

        self.searcher = CLIP(self.config_path)
        self.ip=ImageProcessor(self.config_path)
        self.yolo = YoloDetection(config_path=self.config_path)

        self.image_features=""
        self.image_paths=""




    def encodeImage(self,pic_path):
        image_paths = self.ip.get_all_pic_paths(pic_path)
        print(f"找到 {len(image_paths)} 张图片。\n")

        if len(image_paths) == 0:
            print("当前目录未存储图片！！！")
            return

        results = self.yolo.detect_batch(image_paths)

        # 预先对所有图片进行特征编码
        image_features = []
        for i, (image_path, boxes) in enumerate(zip(image_paths, results)):
            img = Image.open(image_path)
            if not boxes.any():
                feature = self.searcher.Boxes_encode(image_path, img, [[0, 0, img.size[0], img.size[1]]])
            else:
                feature = self.searcher.Boxes_encode(image_path, img, boxes)
            image_features.append(feature)

        self.image_features=image_features
        self.image_paths=image_paths




    def find(self,text,n=3):


        text_feature = self.searcher.encode_Text(text)

        # 计算文本与每个图片特征的相似度
        res = [max(self.searcher.cos_similarity(text_feature, feature)) for feature in self.image_features]

        paired_list = list(zip(res, self.image_paths))

        score1 = [x[0] for x in paired_list]

        similarity_scores = self.searcher.calculate_similarity(self.image_paths, text)

        score2 = [x[1] for x in similarity_scores]

        # 计算加权平均
        all_score = []
        for i in range(len(score1)):
            all_score.append(score1[i] + score2[i])

        paired_list = list(zip(all_score, self.image_paths))

        sorted_paired_list = sorted(paired_list, key=lambda x: x[0], reverse=True)

        sorted_image_paths = [path for _, path in sorted_paired_list[:n]]
        sorted_sc = [sc for sc, _ in sorted_paired_list[:n]]

        pathlist=[]
        for path in list(zip(sorted_image_paths, sorted_sc)):
            pathlist.append(path)
        return pathlist


if __name__=='__main__':
    # CLIP 需要调整config.json的模型路径
    f=Finder()
    f.encodeImage(pic_path="../resource/loss_pic")
    while True:
        text = input("请输入文本：")
        if text=="exit":
            break
        pathlist=f.find(text)
        for k in range(len(pathlist)):
            print(f"{k+1}",pathlist[k])
        print("============================================")
        print("============================================")



















