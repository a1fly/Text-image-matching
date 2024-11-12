from transformers import AutoModel, AutoTokenizer

# 用于提取图片中的文字信息，用于更好的匹配

class OcrModel:
    def __init__(self,modelpath,trust_remote_code=True, low_cpu_mem_usage=True, device_map='cuda', use_safetensors=True):
        self.path=modelpath
        self.tokenizer = AutoTokenizer.from_pretrained(self.path, 
                                                  trust_remote_code=trust_remote_code)
        
        self.model = AutoModel.from_pretrained(self.path, 
                                          trust_remote_code=trust_remote_code, 
                                          low_cpu_mem_usage=low_cpu_mem_usage, 
                                          device_map=device_map,
                                          use_safetensors=use_safetensors, 
                                          pad_token_id=self.tokenizer.eos_token_id)
        self.model = self.model.eval().cuda()

    
    def extract_text(self,imagepath):
        res = self.model.chat(self.tokenizer, imagepath, ocr_type='ocr')
        return res

 



if __name__ == '__main__':
    
    image_file = "../game.jpg"
    model=OcrModel("../model/ocr_model")
    text=model.extract_text(image_file)

    print("=====================================")
    print(text)
    print("=====================================")
    
    

