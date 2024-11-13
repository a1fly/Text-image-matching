from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

# 加载模型和分词器
model_path = "../model/translate_model"  # 模型名称或本地路径
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

# 将模型转移到GPU（如果可用）
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)


def translate_en_to_zh(texts, text_size=512):
    """
    将英语文本翻译成中文
    :param texts: list of str，包含要翻译的多条英语文本
    :param text_size: int，每条文本的最大长度，默认值为512
    :return: list of str，包含翻译后的中文文本
    """
    translations = []

    # 构建输入格式，每个文本前加上 "translate English to Chinese: "
    input_texts = [f"translate to zh  {text}" for text in texts]

    # 使用批量tokenizer进行编码
    inputs = tokenizer(input_texts, return_tensors="pt", padding=True, truncation=True, max_length=text_size)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    # 使用生成模型生成翻译
    output_ids = model.generate(inputs["input_ids"], max_length=text_size, num_beams=4, early_stopping=True)

    # 解码生成的翻译文本
    translations = [tokenizer.decode(ids, skip_special_tokens=True) for ids in output_ids]

    return translations


# 测试多条文本的并行翻译
texts = [
    "Hello, how are you?",
    "The weather is nice today.",
    "Transformers library makes NLP tasks easy!",
    "there is a man that is standing on a skateboard in the street"
]
translated_texts = translate_en_to_zh(texts, text_size=128)

# 输出翻译结果
for i, translation in enumerate(translated_texts):
    print(f"Original: {texts[i]}")
    print(f"Translated: {translation}")
    print("-" * 50)
