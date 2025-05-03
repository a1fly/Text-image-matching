from tool import load_images_from_folder
import torch
from PIL import Image, ImageDraw
from ClipDetection import ClipDet
from ultralytics import YOLO

import os
import time
import uuid

class YoloDet:
    def __init__(self,clipmodel, modelpath='./model/yolo12x.pt', batch_size=8, confidences=0.5):
        """
        初始化 YOLOv5 和 CLIP 编码器。

        :param modelpath: str, YOLOv5 模型路径
        :param batch_size: int, 批次大小
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.modelpath = modelpath
        self.batch_size = batch_size

        # 加载 YOLOv5 模型
        self.model = YOLO(self.modelpath)
        self.model.to(self.device)
        self.model.eval()
        self.confidences = confidences

        # 初始化 CLIP 编码器
        self.encoder = clipmodel

    def batch_load_images(self, folder_path):
        """
        按批次加载图片。

        :param folder_path: str, 图片文件夹路径
        :yield: List[PIL.Image], 当前批次的图片列表
        """
        images = load_images_from_folder(folder_path)
        if not images:
            print("未找到任何图片！")
            return

        for i in range(0, len(images), self.batch_size):
            yield images[i:i + self.batch_size]

    def detect_and_encode(self, folder_path, visualization=False):
        """
        对文件夹中的所有图片进行目标检测，并对每个检测框截取的内容进行编码。
        """
        all_encoded_vectors = []

        # 按批次加载图片
        for batch_images in self.batch_load_images(folder_path):
            print(f"处理批次，包含 {len(batch_images)} 张图片...")

            # 目标检测（注意：batch_images 是 PIL.Image 列表）
            results = self.model.predict(
                source=[img.convert("RGB") for img in batch_images],  # 确保是 RGB 图像
                conf=self.confidences,
                device=self.device
            )

            # 遍历每张图片的检测结果
            for i, result in enumerate(results):
                boxes = result.boxes.xyxy.cpu().numpy()  # ✅ 新方式获取框坐标
                confidences = result.boxes.conf.cpu().numpy()  # ✅ 获取置信度

                # 过滤低置信度的框
                filtered_boxes = boxes[confidences > self.confidences]

                # 可视化检测结果
                if visualization:
                    self.visualize_detections(batch_images[i], filtered_boxes)

                # 截取检测框区域并编码
                encoded_vectors = []
                for box in filtered_boxes:
                    x1, y1, x2, y2 = map(int, box)
                    cropped_image = batch_images[i].crop((x1, y1, x2, y2))
                    image_features = self.encoder.get_image_features([cropped_image])
                    encoded_vectors.append(image_features.squeeze(0))  # 移除 batch 维度

                # 将当前图片的编码结果添加到总列表
                all_encoded_vectors.append(encoded_vectors)

        return all_encoded_vectors

    def detect_and_crop(self, images):
        """返回每张图片的裁剪区域列表[[crop1, crop2,...], ...]"""
        all_crops = []
        for i in range(0, len(images), self.batch_size):
            batch = images[i:i + self.batch_size]

            results = self.model.predict(
                source=[img.convert("RGB") for img in batch],
                conf=self.confidences,
                device=self.device
            )

            for j, result in enumerate(results):
                boxes = result.boxes.xyxy.cpu().numpy()
                crops = [batch[j].crop(tuple(map(int, box))) for box in boxes]
                all_crops.append(crops)
        return all_crops

    def visualize_detections(self, image, boxes, output_folder="./output"):
        """
        可视化检测结果，在图片上绘制边界框并保存。

        :param image: PIL.Image, 输入图片
        :param boxes: np.ndarray, 边界框坐标 (N, 4)
        :param output_folder: str, 输出文件夹路径
        """
        # 如果没有检测到任何边界框，直接返回
        if len(boxes) == 0:
            print("未检测到任何目标，跳过保存。")
            return

        # 绘制边界框
        draw = ImageDraw.Draw(image)
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

        # 生成唯一文件名
        unique_name = f"result_{str(uuid.uuid4())[:8]}.jpg"
        output_path = os.path.join(output_folder, unique_name)

        # 确保输出文件夹存在
        os.makedirs(output_folder, exist_ok=True)

        # 保存可视化结果
        image.save(output_path)
        print(f"可视化结果已保存到: {output_path}")


if __name__ == '__main__':
    clipdet = ClipDet()
    yolodet = YoloDet(clipdet,batch_size=2, confidences=0.4)  # 设置批次大小为 4

    # 指定图片文件夹路径
    folder_path = "./pic"

    # 检测并编码
    encoded_results = yolodet.detect_and_encode(folder_path)

    # 打印结果
    for i, encoded_vectors in enumerate(encoded_results):
        print(f"图片 {i + 1} 中检测到的对象编码向量数量: {len(encoded_vectors)}")