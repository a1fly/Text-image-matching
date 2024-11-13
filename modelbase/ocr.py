import json
from transformers import AutoModel, AutoTokenizer
import torch


class OcrModel:
    def __init__(self, config_path="../config.json"):
        # 加载配置文件
        with open(config_path, "r") as f:
            config = json.load(f)

        self.config=config["ocr_config"]

        # 从配置文件中提取参数
        self.modelpath = self.config["ocr_model_path"]
        self.trust_remote_code = self.config["trust_remote_code"]
        self.low_cpu_mem_usage = self.config["low_cpu_mem_usage"]
        self.use_safetensors = self.config["use_safetensors"]

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # 加载模型和tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.modelpath, trust_remote_code=self.trust_remote_code)
        self.model = AutoModel.from_pretrained(self.modelpath,
                                               trust_remote_code=self.trust_remote_code,
                                               low_cpu_mem_usage=self.low_cpu_mem_usage,
                                               device_map=self.device,
                                               use_safetensors=self.use_safetensors,
                                               pad_token_id=self.tokenizer.eos_token_id)
        self.model = self.model.eval().to(self.device)  # 确保模型加载到正确的设备

    def extract_text(self, imagepath):
        # 使用OCR模型提取图片中的文字
        res = self.model.chat(self.tokenizer, imagepath, ocr_type='ocr')
        return res


# 示例：主程序
if __name__ == '__main__':
    image_file = "../game.jpg"
    model = OcrModel()
    text = model.extract_text(image_file)

    print("=====================================")
    print(text)
    print("=====================================")

