import json
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer


class Translator:
    def __init__(self,
                 config_path="./config.json",
                 model_path= None,
                 num_beams=None,
                 batch_size=None):


        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        self.config = config["translate_config"]

        self.model_path = self.config["model_path"] if model_path is None else model_path
        self.num_beams = self.config["num_beams"] if num_beams is None else num_beams# 影响生成质量，越高越好但是越慢
        self.batch_size= self.config["batch_size"] if batch_size is None else batch_size
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.tokenizer = T5Tokenizer.from_pretrained(self.model_path)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_path)

        self.model.to(self.device)

    def translate(self, texts, direction="zh_to_en", batch_size=None):
        """
        批量翻译文本
        :param texts: list of str，包含要翻译的多条文本
        :param direction: str, "zh_to_en" 或 "en_to_zh"，决定翻译方向
        :param batch_size: int, 每个批次的文本数量
        :return: list of str，包含翻译后的文本
        """
        batch_size=batch_size if batch_size is not None else self.batch_size

        if direction == "en_to_zh":
            input_texts = [f"translate to zh: {text}" for text in texts]
        elif direction == "zh_to_en":
            input_texts = [f"translate to en: {text}" for text in texts]
        else:
            raise ValueError("请输入参数 'en_to_zh' 或者 'zh_to_en'")

        all_translated_texts = []

        for i in range(0, len(input_texts), batch_size):
            batch_texts = input_texts[i:i + batch_size]

            inputs = self.tokenizer(batch_texts, return_tensors="pt", padding=True, truncation=True)
            inputs = {key: value.to(self.device) for key, value in inputs.items()}

            output_ids = self.model.generate(inputs["input_ids"],num_beams=self.num_beams, early_stopping=True)
            translated_texts = [self.tokenizer.decode(ids, skip_special_tokens=True) for ids in output_ids]
            all_translated_texts.extend(translated_texts)

        return all_translated_texts


# 示例用法
if __name__ == "__main__":
    translator = Translator(config_path="../config.json",model_path="../model/translate_model")

    texts = [
        "你好啊，你怎么样？",
        "我的衣服去哪里了",
        "这个作业太简单了",
        "挖土的男人",
        "我丢了一个卡通背包，上面有小狗的图片，并且肩带是黄色的"
    ]

    translated_texts = translator.translate(texts, direction="zh_to_en", batch_size=2)

    for i, translation in enumerate(translated_texts):
        print(f"Original: {texts[i]}")
        print(f"Translated: {translation}")
        print("-" * 50)
