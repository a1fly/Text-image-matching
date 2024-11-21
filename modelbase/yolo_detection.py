import torch
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from typing import List, Tuple
from torchvision.ops import nms
import json

"""
检测图片的物体
输出形式：（x1,y1,x2,y2）表示框框的左上角和右下角的坐标
"""


class YoloDetection:
    def __init__(self,
                 config_path='./config.json',
                 model_path=None,
                 conf=0.01,
                 batch_size=None,
                 iou_threshold=None):
        """
        参数：
        config_path-----config文件地址模型
        model_path-----模型地址
        conf-----保留置信度高于该值的框
        batch_size-----批次读取的张数
        iou_threshold-----减少重复框
        """

        with open(config_path) as f:
            self.config = json.load(f)
        if model_path is None:
            self.model_path = self.config['detection_cofig']['model_path']
        else:
            self.model_path = model_path
        if conf is None:
            self.conf = self.config['detection_cofig']['conf']
        else:
            self.conf = conf
        if batch_size is None:
            self.batch_size = self.config['detection_cofig']['batch_size']
        else:
            self.batch_size = batch_size
        if iou_threshold is None:
            self.iou_threshold = self.config['detection_cofig']['iou_threshold']
        else:
            self.iou_threshold = iou_threshold

        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=self.model_path)
        # self.model.eval()
        # self.model = torch.load(self.model_path)
        self.model.eval()

    def batch_load_images(self, image_paths: List[str]) -> Tuple[List[str], List[Image.Image]]:
         """
         按批次加载图片。

         参数:
         image_paths (List[str]): 图片路径列表。

         返回:
         Tuple[List[str], List[Image.Image]]: 当前批次的图片路径和对应的 PIL 图片对象。
         """
         batch_paths = []
         batch_images = []
         for i, image_path in enumerate(image_paths):
             image = Image.open(image_path)
             batch_paths.append(image_path)
             batch_images.append(image)

             if len(batch_paths) == self.batch_size or i == len(image_paths) - 1:
                 yield batch_paths, batch_images
                 batch_paths, batch_images = [], []

    def detect_batch(self, image_paths: List[str],is_nms=False) -> List[List[Tuple[int, int, int, int]]]:
        """
        批量检测图像中的目标，并返回每张图片中检测到的对象方框坐标。

        参数:
        image_paths: List[str] 图片路径列表

        返回:
        List[List[Tuple[int, int, int, int]]] 每张图片检测到的方框坐标
        """

        all_boxes = []

        for batch_paths, batch_images in self.batch_load_images(image_paths):
            results = self.model(batch_images)

            batch_boxes = []
            for i, result in enumerate(results.xyxy):
                boxes = result[:, :4].cpu().numpy()  # 提取框坐标
                confidences = result[:, 4].cpu().numpy()  # 提取置信度

                if is_nms:
                    # 减少重复框
                    keep = nms(
                        torch.tensor(boxes, dtype=torch.float32),
                        torch.tensor(confidences, dtype=torch.float32),
                        self.iou_threshold
                    )

                    filtered_boxes = boxes[keep.numpy().astype(int)]
                    batch_boxes.append(filtered_boxes)
                else:
                    batch_boxes.append(boxes)


            all_boxes.extend(batch_boxes)


        return all_boxes

    def save_boxes(self):
        """
        用于保存切割的坐标到数据库
        """
        pass

def plot_detections(image_path, boxes):
    """
    在图片上绘制检测框并显示。

    参数:
    - image_path: 图片路径
    - boxes: 检测框的坐标列表 [(x1, y1, x2, y2), ...]
    """

    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    for box in boxes:
        draw.rectangle(box, outline="red", width=3)

    plt.figure(figsize=(8, 8))
    plt.imshow(image)
    plt.axis("off")
    plt.show()



if __name__ == '__main__':
    image_paths = [
        '../resource/loss_pic/1.jpg',
        '../resource/loss_pic/微信图片_20241115142227.jpg',
        '../resource/loss_pic/微信图片_20241115141230.jpg'
    ]
    print(1)

    yolo = YoloDetection(config_path="../config.json",model_path="../model/yolo_model/yolov5x6.pt")
    print(2)

    results = yolo.detect_batch(image_paths)
    print(3)

    for i, boxes in enumerate(results):
        print("====", i)
        print(f"图片 {image_paths[i]} 检测框: {boxes}")

