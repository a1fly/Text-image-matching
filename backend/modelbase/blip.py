import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import os
import json
from backend.tools.imageTool import ImageProcessor

class BLIP:
    def __init__(self,
                 config_path="./config.json",
                 mdoel_path=None,
                 batch_size=None):
        # 加载配置文件
        with open(config_path, "r") as f:
            config = json.load(f)
        self.config=config["blip_config"]

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        if mdoel_path is None:
            self.model_path = self.config["model_path"]
        else:
            self.model_path = mdoel_path

        if batch_size is None:
            self.batch_size = self.config["batch_size"]
        else:
            self.batch_size = batch_size

        # 加载模型和处理器
        self.processor = BlipProcessor.from_pretrained(self.model_path)
        self.model = BlipForConditionalGeneration.from_pretrained(self.model_path).to(self.device)

    def generate_captions(self,image_paths):
        # 获取图片路径
        all_captions = []
        # 批量生成描述
        for i in range(0, len(image_paths), self.batch_size):
            batch_paths = image_paths[i:i + self.batch_size]
            images = [Image.open(img_path).convert("RGB") for img_path in batch_paths]
            inputs = self.processor(images=images, return_tensors="pt", padding=True).to(self.device)

            with torch.no_grad():
                output = self.model.generate(**inputs)

            captions = self.processor.batch_decode(output, skip_special_tokens=True)
            all_captions.extend(zip(batch_paths, captions))

        return all_captions


if __name__ == "__main__":
    caption_generator = BLIP(config_path="../config.json",mdoel_path="../model/blip_model")
    print(1)
    ip=ImageProcessor()
    image_paths=ip.get_all_pic_paths("../resource/loss_pic")
    captions = caption_generator.generate_captions(image_paths)
    print("captions = ",captions)
    for img_path, caption in captions:
        print(f"{img_path}: {caption}")
