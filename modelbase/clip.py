import torch
from PIL import Image
import cn_clip.clip as clip
from cn_clip.clip import load_from_name
from pathlib import Path
import matplotlib.pyplot as plt
from tqdm import tqdm


# 获取到某文件夹下的所有文件的路径
def get_all_pic_paths(directory):
    return [str(file) for file in Path(directory).rglob('*') if file.is_file()]


# 显示多张图片的函数
def show_images(image_paths, scores):
    plt.figure(figsize=(15, 5))
    for i, (image_path, score) in enumerate(zip(image_paths, scores)):
        image = Image.open(image_path)
        plt.subplot(1, len(image_paths), i + 1)
        plt.imshow(image)
        plt.axis('off')
    plt.show()


if __name__ == '__main__':
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"使用设备: {device}")

    # 模型路径
    modelpath = "../model/clip_model"

    # 加载模型
    model, preprocess = load_from_name("ViT-B-16", device=device, download_root=modelpath)

    single_text = input("输入查找的图片：")
    texts = [single_text]
    text = clip.tokenize(texts).to(device)
    text_features = model.encode_text(text)

    # 图片文件夹的路径
    picpath = "./test/resource/pic/test"
    # 获取图片的路径
    image_paths = get_all_pic_paths(picpath)
    print(f"找到{len(image_paths)}张图片。\n")

    if len(image_paths)==0:
        print("当前目录未存储图片！！！")
        exit(0)


    similarity_scores = []

    batch_size = 32  # 每批次处理的图片数量，可以根据显存或内存大小调整


    # 按批次加载图片
    def batch_load_images(image_paths, batch_size):
        batch_images = []
        batch_paths = []
        for i, image_path in enumerate(image_paths):
            # 读取并预处理图片
            image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
            batch_images.append(image)
            batch_paths.append(image_path)

            # 如果达到当前批次大小，返回当前批次并清空缓存
            if len(batch_images) == batch_size or i == len(image_paths) - 1:
                yield batch_paths, torch.cat(batch_images, dim=0)  # 将图片合并成一个batch
                batch_images = []
                batch_paths = []


    # 计算相似度
    with torch.no_grad():
        for batch_paths, batch_images in tqdm(batch_load_images(image_paths, batch_size),
                                              desc="计算相似度", unit="批次",
                                              total=len(image_paths) // batch_size + 1,
                                              dynamic_ncols=True, leave=False):
            # 获取批次中的图像特征
            batch_image_features = model.encode_image(batch_images)

            # 计算每张图片与文本的相似度
            for image_path, image_feature in zip(batch_paths, batch_image_features):
                similarity_score = torch.nn.functional.cosine_similarity(image_feature.unsqueeze(0),
                                                                         text_features).item()
                similarity_scores.append((image_path, similarity_score))

    # 按照相似度进行排序
    similarity_scores.sort(key=lambda x: x[1], reverse=True)

    while True:
        try:
            n = int(input(f"输入展示的图片数量 (最大 {len(image_paths)} 张): "))
            if n <= 0 or n > len(image_paths):
                print(f"请输入一个合理的数量 (1 到 {len(image_paths)})。")
            else:
                break
        except ValueError:
            print("请输入一个有效的数字。")

    # 提取最高的n个图片路径和相似度分数
    top_n_images = [item[0] for item in similarity_scores[:n]]
    top_n_scores = [item[1] for item in similarity_scores[:n]]

    print(f"\n  最相似{n}张图片:")
    for image_path, score in zip(top_n_images, top_n_scores):
        print(f"图片{image_path} 相似度： {score:.6f}")

    show_images(top_n_images, top_n_scores)











