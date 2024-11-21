import matplotlib.pyplot as plt
import numpy as np

from PIL import Image,ImageDraw

from modelbase.clip import CLIP
from tools.imageTool import ImageProcessor
from modelbase.yolo_detection import YoloDetection
import cn_clip.clip as clip
from cn_clip.clip import load_from_name
import torch.nn.functional as F


if __name__=='__main__':
    config_path="./config.json"
    searcher = CLIP(config_path)
    ip = ImageProcessor(config_path)

    # 图片文件夹的路径
    picpath = "./resource/loss_pic"
    # 获取图片路径
    image_paths = ip.get_all_pic_paths(picpath)
    print(f"找到 {len(image_paths)} 张图片。\n")

    if len(image_paths) == 0:
        print("当前目录未存储图片！！！")
        exit(0)

    yolo = YoloDetection(config_path=config_path)
    print(2)

    results = yolo.detect_batch(image_paths)
    print(3)
    # print(results)
    # print("*********************************")
    # print(results[0])
    # print("*********************************")
    # print(type(results))

    while(True):
        text=input(">>>")
        text_feature=searcher.encode_Text(text)



        res=[]

        for i, boxes in enumerate(results):
            print("************", i,'*****************')
            # 打开图片
            img = Image.open(image_paths[i])
            draw = ImageDraw.Draw(img)

            # 如果有检测框，则绘制检测框
            if boxes.any():
                for box in boxes:
                    draw.rectangle(box, outline="red", width=3)  # 绘制红色边框

            # 保存或显示带有检测框的图片
            img.save(f'./output_{i}.jpg')  # 保存图片


            # print(f"图片 {image_paths[i]} 检测框: {boxes}")
            if not boxes.any():
                temp=Image.open(image_paths[i])
                feature=searcher.Boxes_encode(image_paths[i],temp,[[0,0,temp.size[0],temp.size[1]]])
            else:
                feature=searcher.Boxes_encode(image_paths[i],Image.open(image_paths[i]),boxes)
            sim=searcher.cos_similarity(text_feature,feature)
            res.append(max(sim))


        paired_list = list(zip(res, image_paths))

        sorted_paired_list = sorted(paired_list, key=lambda x: x[0], reverse=True)
        n=int(input("几个: "))

        score1=[x[0] for x in paired_list]

        sorted_image_paths = [path for _, path in sorted_paired_list[:n]]

        for path in sorted_image_paths:
            print(path)


        #==============================================================
        #===========================单纯使用CLIP========================
        #==============================================================
        print("=========================================================")
        print("=========================================================")
        print("=========================================================")

        similarity_scores = searcher.calculate_similarity(image_paths, text)

        score2=[x[1] for x in similarity_scores]

        sorted_data = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        top_n_paths = [path for path, _ in sorted_data[:n]]

        for path in top_n_paths:
            print(path)

        print("=========================================================")
        print("=========================================================")
        print("=========================================================")


        all_score=[]
        for i in range(len(score1)):
            all_score.append(score1[i]*0.4+score2[i]*0.6)


        paired_list = list(zip(all_score, image_paths))

        sorted_paired_list = sorted(paired_list, key=lambda x: x[0], reverse=True)



        sorted_image_paths = [path for _, path in sorted_paired_list[:n]]

        for path in sorted_image_paths:
            print(path)





















