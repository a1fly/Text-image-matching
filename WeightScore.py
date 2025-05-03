import os
from PIL import Image
import torch
from ClipDetection import ClipDet
from YoloDecv12 import YoloDet


class ImageScorer:
    def __init__(self, yolo_batch_size=32):
        """
        初始化图片评分器

        :param lambda_weight: float, 全局相似度权重
        :param yolo_batch_size: int, YOLO 检测的批量大小（根据显存调整）
        """
        # 初始化 CLIP 和 YOLO 模型
        self.clip_detector = ClipDet()
        self.yolo_detector = YoloDet(batch_size=yolo_batch_size,clipmodel=self.clip_detector)


    def calculate_scores(self, query_texts, folder_path, batch_size=32,lambda_weight=0.5):
        text_features = self.clip_detector.get_text_features(query_texts)

        # 固定图片加载顺序
        image_paths = sorted(
            [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)
             if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        )

        final_scores = []
        for i in range(0, len(image_paths), batch_size):
            batch_paths = image_paths[i:i + batch_size]
            batch_images = []
            valid_paths = []

            # 加载当前批次的图片
            for img_path in batch_paths:
                try:
                    image = Image.open(img_path).convert("RGB")
                    batch_images.append(image)
                    valid_paths.append(img_path)
                except Exception as e:
                    print(f"无法加载图片 {img_path}: {e}")

            if not batch_images:
                continue

            with torch.no_grad():
                global_features = self.clip_detector.get_image_features(batch_images)
                global_sim = self.clip_detector.get_similarity(text_features, global_features)

                cropped_regions_list = self.yolo_detector.detect_and_crop(batch_images)

                local_sims = []
                for j, cropped_regions in enumerate(cropped_regions_list):
                    if cropped_regions:
                        region_features = self.clip_detector.get_image_features(cropped_regions)
                        region_sim = self.clip_detector.get_similarity(text_features, region_features)
                        local_sims.append(region_sim.max().item() if region_sim.numel() > 0 else 0.0)
                    else:
                        local_sims.append(0.0)

                for k, img_path in enumerate(valid_paths):
                    sim1 = global_sim[0][k].item()
                    sim2 = local_sims[k]
                    final_score = lambda_weight * sim1 + (1 - lambda_weight) * sim2
                    final_scores.append((img_path.split('/')[-1], final_score))

        final_scores.sort(key=lambda x: x[1], reverse=True)
        return final_scores


if __name__ == "__main__":
    # 初始化图片文件夹路径
    folder_path = "path/to/your/image/folder"

    # 创建 ImageScorer 实例
    scorer = ImageScorer()

    # 定义查询文本
    query_texts = ["a cat sitting on a couch", "a dog playing in the park"]

    # 计算图片分数
    scores = scorer.calculate_scores(query_texts=query_texts, folder_path=folder_path,lambda_weight=0.5)

    # 打印结果
    for img_name, score in scores:
        print(f"图片: {img_name}, 分数: {score:.4f}")


