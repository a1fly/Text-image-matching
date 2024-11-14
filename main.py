import matplotlib.pyplot as plt

from PIL import Image

from modelbase.blip import BLIP
from modelbase.clip import CLIP
from tools.imageTool import ImageProcessor
from modelbase.translater import Translator
from modelbase.similarity import SimilarTool

if __name__=='__main__':
    config_path="./config.json"
    searcher = CLIP(config_path)
    ip = ImageProcessor(config_path)

    # 图片文件夹的路径
    picpath = "./resource/test_pic"
    # 获取图片路径
    image_paths = ip.get_all_pic_paths(picpath)
    print(f"找到 {len(image_paths)} 张图片。\n")

    if len(image_paths) == 0:
        print("当前目录未存储图片！！！")
        exit(0)

    query_text = input("请输入查询的文本：")

    similarity_scores = searcher.calculate_similarity(image_paths, query_text)
    print("ClIP的相似度:")
    print(similarity_scores)
    # s=[x[1] for x in similarity_scores]
    # # 获取排序后的下标（从大到小）
    # sorted_indices = sorted(range(len(s)), key=lambda i: s[i], reverse=True)
    #
    # # 根据排序后的下标输出 image_path 中的内容
    # sorted_image_paths = [image_paths[i] for i in sorted_indices]
    #
    # # 输出排序后的图像路径列表
    # print(sorted_image_paths)
    # print(sorted(s, reverse=True))
    #
    # plt.figure(figsize=(15, 5))
    # image = Image.open(sorted_image_paths[0])
    # plt.imshow(image)
    # plt.show()






















    # 第二步：使用blip
    blip_model = BLIP(config_path)
    captions = blip_model.generate_captions(image_paths)
    print("BLIP生成的文本:")
    print(captions)
    print("====================================")
    print(captions[0])
    print("====================================")


    # 第三步：翻译输入的文本到english以便计算相似度
    trans=Translator(config_path)
    query_text_en=trans.translate_zh_to_en([query_text])
    print("英文版的查询文本:")
    print(query_text_en)
    print("====================================")

    # 第四步：计算文本相似度
    sim=SimilarTool()
    caption_list=[x[1] for x in captions]
    similarity_scores_en=sim.getSimilarity(query_text_en[0],caption_list)
    print("翻译后BLIP生成的文本的相似度:")
    print(similarity_scores_en)
    print("====================================")


    # 第五步：计算分数之和排序，，输出图片路径
    # 之和
    # 假设 sum_score 是相似度分数，similarity_scores_en 是一个列表，image_path 是包含图像路径的列表
    sum_score = [x[1] for x in similarity_scores] + similarity_scores_en[0]

    # 获取排序后的下标（从大到小）
    sorted_indices = sorted(range(len(sum_score)), key=lambda i: sum_score[i], reverse=True)

    # 根据排序后的下标输出 image_path 中的内容
    sorted_image_paths = [image_paths[i] for i in sorted_indices]

    # 输出排序后的图像路径列表
    print(sorted_image_paths)
    print(sorted(sum_score, reverse=True))

    plt.figure(figsize=(15, 5))
    image = Image.open(sorted_image_paths[0])
    plt.imshow(image)
    plt.show()





















