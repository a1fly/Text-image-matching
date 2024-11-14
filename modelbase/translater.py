import json
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer


class Translator:
    def __init__(self, config_path="./config.json"):
        # 加载配置文件
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        self.config = config["translate_config"]

        # 初始化配置
        self.model_path = self.config["model_path"]
        self.max_text_size = self.config["max_text_size"]
        self.num_beams = self.config["num_beams"]
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # 加载模型和分词器
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_path)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_path)

        # 将模型转移到指定的设备（GPU/CPU）
        self.model.to(self.device)

    def translate_en_to_zh(self, texts):
        """
        将英语文本翻译成中文
        :param texts: list of str，包含要翻译的多条英语文本
        :return: list of str，包含翻译后的中文文本
        """
        translations = []

        # 构建输入格式，每个文本前加上 "translate English to Chinese: "
        input_texts = [f"translate to zh  {text}" for text in texts]

        # 使用批量tokenizer进行编码
        inputs = self.tokenizer(input_texts, return_tensors="pt", padding=True, truncation=True,
                                max_length=self.max_text_size)
        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        # 使用生成模型生成翻译
        output_ids = self.model.generate(inputs["input_ids"], max_length=self.max_text_size, num_beams=self.num_beams,
                                         early_stopping=True)

        # 解码生成的翻译文本
        translations = [self.tokenizer.decode(ids, skip_special_tokens=True) for ids in output_ids]

        return translations

    def translate_zh_to_en(self, texts):
        """
        将中文文本翻译成英语
        :param texts: list of str，包含要翻译的多条中文文本
        :return: list of str，包含翻译后的英文文本
        """
        translations = []

        # 构建输入格式，每个文本前加上 "translate Chinese to English: "
        input_texts = [f"translate to en  {text}" for text in texts]

        # 使用批量tokenizer进行编码
        inputs = self.tokenizer(input_texts, return_tensors="pt", padding=True, truncation=True,
                                max_length=self.max_text_size)
        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        # 使用生成模型生成翻译
        output_ids = self.model.generate(inputs["input_ids"], max_length=self.max_text_size, num_beams=self.num_beams,
                                         early_stopping=True)

        # 解码生成的翻译文本
        translations = [self.tokenizer.decode(ids, skip_special_tokens=True) for ids in output_ids]

        return translations


# 示例用法
if __name__ == "__main__":
    # 创建 Translator 类的实例
    translator = Translator(config_path="../config.json")

    # 测试多条文本的并行翻译
    # texts = [
    #     "Hello, how are you?",
    #     "The weather is nice today.",
    #     "Transformers library makes NLP tasks easy!",
    #     "There is a man that is standing on a skateboard in the street"
    # ]

    texts = [
        "你好啊，你怎么样？",
        "我的衣服去哪里了",
        "这个作业太简单了",
        "挖土的男人"
    ]


    # translated_texts = translator.translate_en_to_zh(texts)
    translated_texts = translator.translate_zh_to_en(texts)

    # 输出翻译结果
    for i, translation in enumerate(translated_texts):
        print(f"Original: {texts[i]}")
        print(f"Translated: {translation}")
        print("-" * 50)
