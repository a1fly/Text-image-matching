import matplotlib
import matplotlib.pyplot as plt
import pylab
import numpy as np

from PIL import Image,ImageDraw

from modelbase.clip import CLIP
from modelbase.translater import Translator
from tools.imageTool import ImageProcessor
from modelbase.yolo_detection import YoloDetection
import cn_clip.clip as clip
from cn_clip.clip import load_from_name
import torch.nn.functional as F
from modelbase.blip import BLIP
from modelbase.similarity import SimilarTool


def normalize(scores):
    min_score = min(scores)
    max_score = max(scores)
    return [(score - min_score) / (max_score - min_score) if max_score > min_score else 0.0 for score in scores]





if __name__=='__main__':
    config_path= "./config.json"
    searcher = CLIP(config_path)
    ip = ImageProcessor(config_path)

    # 图片文件夹的路径
    picpath = "../resource/loss_pic"
    # 获取图片路径
    image_paths = ip.get_all_pic_paths(picpath)
    print(f"找到 {len(image_paths)} 张图片。\n")

    if len(image_paths) == 0:
        print("当前目录未存储图片！！！")
        exit(0)

    yolo = YoloDetection(config_path=config_path)


    results = yolo.detect_batch(image_paths)

        # 保存
    # for i, boxes in enumerate(results):
    #     print("************", i,'*****************')
    #     # 打开图片
    #     img = Image.open(image_paths[i])
    #     draw = ImageDraw.Draw(img)
    #
    #     # 如果有检测框，则绘制检测框
    #     if boxes.any():
    #         for box in boxes:
    #             draw.rectangle(box, outline="red", width=3)  # 绘制红色边框
    #
    #     img_rgb = img.convert('RGB')
    #
    #     # 保存图像
    #     img_rgb.save(f'./output_{i}.jpg')

    # 预先对所有图片进行特征编码
    image_features = []
    for i, (image_path, boxes) in enumerate(zip(image_paths, results)):
        img = Image.open(image_path)
        if not boxes.any():
            feature = searcher.Boxes_encode(image_path, img, [[0, 0, img.size[0], img.size[1]]])
        else:
            feature = searcher.Boxes_encode(image_path, img, boxes)
        image_features.append(feature)


    while(True):


        text=input(">>>")
        text_feature=searcher.encode_Text(text)





        # # 第三步：翻译输入的文本到english以便计算相似度
        # trans=Translator(config_path)
        # query_text_en=trans.translate([text])
        # print("英文版的查询文本:")
        # print(query_text_en)
        # print("====================================")
        #
        # # 第四步：计算文本相似度
        # sim=SimilarTool()
        # caption_list=[x[1] for x in captions]
        # similarity_scores_en=sim.getSimilarity(query_text_en[0],caption_list)
        # print("翻译后BLIP生成的文本的相似度:")
        # print(similarity_scores_en)
        # print("====================================")





        res=[]

        # for i, boxes in enumerate(results):
        #     # print("************", i,'*****************')
        #     # # 打开图片
        #     # img = Image.open(image_paths[i])
        #     # draw = ImageDraw.Draw(img)
        #     #
        #     # # 如果有检测框，则绘制检测框
        #     # if boxes.any():
        #     #     for box in boxes:
        #     #         draw.rectangle(box, outline="red", width=3)  # 绘制红色边框
        #     #
        #     # img_rgb = img.convert('RGB')
        #     #
        #     # # 保存图像
        #     # img_rgb.save(f'./output_{i}.jpg')
        #
        #
        #
        #     # print(f"图片 {image_paths[i]} 检测框: {boxes}")
        #     if not boxes.any():
        #         temp=Image.open(image_paths[i])
        #         feature=searcher.Boxes_encode(image_paths[i],temp,[[0,0,temp.size[0],temp.size[1]]])
        #     else:
        #         feature=searcher.Boxes_encode(image_paths[i],Image.open(image_paths[i]),boxes)
        #     sim=searcher.cos_similarity(text_feature,feature)
        #     res.append(max(sim))

         # 计算文本与每个图片特征的相似度
        res = [max(searcher.cos_similarity(text_feature, feature)) for feature in image_features]

        paired_list = list(zip(res, image_paths))

        sorted_paired_list = sorted(paired_list, key=lambda x: x[0], reverse=True)
        # n=int(input("几个: "))
        n=3

        score1=[x[0] for x in paired_list]

        sorted_image_paths = [path for _, path in sorted_paired_list[:n]]

        # for path in sorted_image_paths:
        #     print(path)


        #==============================================================
        #===========================单纯使用CLIP========================
        #==============================================================
        # print("=========================================================")
        # print("=========================================================")
        # print("=========================================================")

        similarity_scores = searcher.calculate_similarity(image_paths, text)

        score2=[x[1] for x in similarity_scores]

        sorted_data = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        top_n_paths = [path for path, _ in sorted_data[:n]]

        # for path in top_n_paths:
        #     print(path)
        #
        # print("=========================================================")
        # print("=========================================================")
        # print("=========================================================")

        # 归一化处理
        # norm_score1 = normalize(score1)
        # norm_score2 = normalize(score2)
        # norm_score3=normalize(similarity_scores_en)

        # 计算加权平均
        all_score = []
        for i in range(len(score1)):
            all_score.append(score1[i]+ score2[i] )


        paired_list = list(zip(all_score, image_paths))

        sorted_paired_list = sorted(paired_list, key=lambda x: x[0], reverse=True)



        sorted_image_paths = [path for _, path in sorted_paired_list[:n]]
        sorted_sc = [sc for sc, _ in sorted_paired_list[:n]]

        for path in list(zip(sorted_image_paths,sorted_sc)):
            print(path)






















