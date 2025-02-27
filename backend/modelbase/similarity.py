from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

class SimilarTool:
    def __init__(self,
                 config_path="./config.json",
                 model_path=None,):
        with open(config_path) as f:
            self.config = json.load(f)
        self.config =self.config['similar_config']
        if model_path is None:
            self.modelpath=self.config['model_path']
        else:
            self.modelpath=model_path

        self.model = SentenceTransformer(self.modelpath)

    # 获取目标句子与所有句子的相似程度
    def getSimilarity(self, target_sentence, all_sentences):
        # 获取目标句子的嵌入
        target_embedding = self.model.encode([target_sentence])

        # 获取多个句子的嵌入
        embeddings = self.model.encode(all_sentences)

        cosine_similarities = cosine_similarity(target_embedding, embeddings)

        return cosine_similarities


if __name__ == '__main__':
    target_sentence = "Man driving"
    all_sentences = [
        "arafed man in a suit sitting in a car with his hands on the steering wheel",
        "arafed man pointing at something with his finger on a white background",
        "woman in a car holding a cup of coffee and drinking coffee",
        "arafed man in white shirt pointing at something with his finger",
        "arafed woman in red dress holding up a sign with an arrow",
        "arafed man kneeling down in the dirt with a piece of wood",
        "arafed man in pink shirt pointing at something with his finger",
        "painting of a woman holding a green umbrella and a boy sitting on a hill"
    ]

    model = SimilarTool(config_path="../config.json",model_path="../model/similar_model")
    print(model.getSimilarity(target_sentence, all_sentences))

