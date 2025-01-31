from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename, send_file
import os
import base64
from datetime import datetime
from DealFunc.savewriteInfo import SaveInfo
from DealFunc.readinfo import ReadInfo
from backend.ClipFinder import Finder
import threading
import atexit
from openai import OpenAI
import json


# 配置上传文件夹
UPLOAD_FOLDER = '../../resource'
LOSS_PIC_DIR = '../../resource/loss_pic'
PLACE_PIC_DIR = '../../resource/place_pic'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(LOSS_PIC_DIR, exist_ok=True)
os.makedirs(PLACE_PIC_DIR, exist_ok=True)

config_path = "../config.json"
lock_file = "./tmp/myapp_init.lock"

# 大模型的提示词
prompt_text="""您是一位专业且礼貌的客户服务代表。您的任务是通过收集尽可能多的丢失物品或情况的详细信息，帮助用户恢复丢失和找到的信息。为了有效地做到这一点，您应该通过提出相关问题来与用户互动，引导他们提供全面的细节。

    具体来说，您可以要求提供以下信息：
    -丢失的物品类型。
    -物品的颜色。
    -任何独特的形状、图案或特征。
    -可能有助于识别该物品的任何其他相关细节。
    同时你不要询问关于丢失场合，丢失时间等信息，只需要获取物品信息即可
    继续询问后续问题，直到您收集到足够的信息或用户表示他们无法提供进一步的详细信息。如果用户提供的信息不完整，请温和地提示他们提供更多细节。

    一旦你收集了大部分必要的信息，将数据总结成一份简洁的报告，格式为“一张 xxxx 的图片”，其中xxxx根据提供的信息描述了丢失的物品。

    每次以JSON格式返回，内容格式为：
    {
    “status”：“未完成”，
    “info”：“”
    “reply”：你的回复再加上“如果没有其余信息了也可以直接进行查找哦！”
    }


    最后，以JSON格式用中文向我提供汇总的信息，只返回JSON不要返回其他任何信息了：
    {
    “status”：“完成”，
    “info”：“一张xxxxx的图片”，
    “reply”："谢谢您提供的信息，我会帮助您进行查找！"
    }


    确保你与用户的互动在整个过程中保持礼貌和乐于助人。"""
# 大模型的api
llmapikey="sk-9ebc62478cb641e7bdcaea1d9e68f3d1"
# 大模型的url
llmurl="https://dashscope.aliyuncs.com/compatible-mode/v1"

client = OpenAI(
    api_key=llmapikey,
    base_url=llmurl,
)

# 全局变量用于存储对话历史
conversation_history = []






# 用于存储对象的全局变量和线程锁
class GlobalObjects:
    saveTool = None
    reader = None
    finder = None
    lock = threading.Lock()

def remove_lock_file():
    if os.path.exists(lock_file):
        os.remove(lock_file)

def init_objects():
    """
    初始化全局对象，只运行一次
    """
    with GlobalObjects.lock:
        if GlobalObjects.saveTool is None or GlobalObjects.reader is None or GlobalObjects.finder is None:
            print('开始初始化...')
            GlobalObjects.saveTool = SaveInfo()
            GlobalObjects.reader = ReadInfo()
            GlobalObjects.finder = Finder(config_path=config_path)
            GlobalObjects.finder.encodeImage(pic_path=LOSS_PIC_DIR)
            print("初始化完成")
            # 创建锁文件
            open(lock_file, 'a').close()

# 注册退出处理程序，删除锁文件
atexit.register(remove_lock_file)

# 初始化全局对象
init_objects()

# Flask 应用设置
app = Flask(__name__)
app.config['init_database'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/login', methods=['POST'])
def check_login():
    data = request.get_json()
    username = data.get('acc')
    password = data.get('pass')
    print('账号：', username)
    print('密码：', password)

    if username == 'admin' and password == '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8':
        return jsonify({'success': True, 'message': '登录成功'})
    else:
        return jsonify({'success': False, 'message': '用户名或密码错误'})

@app.route('/api/reg', methods=['POST'])
def check_reg():
    data = request.get_json()
    contactType = data.get('contactType')
    username = data.get('username')
    password = data.get('password')
    contactNumber = data.get('contactNumber')

    print('账号：', username)
    print('密码：', password)
    print('联系方式：', contactNumber)
    print('联系方式类型：', contactType)
    return jsonify({'success': True, 'message': '注册成功'})

@app.route('/api/writeInfo', methods=['POST'])
def write_info():
    print("已经接收到信息")
    data = request.json
    description = data.get('description')
    location = data.get('location')
    method = data.get('method')
    designated_place = data.get('designatedPlace')
    lost_images = data.get('lostImage', [])
    designated_place_images = data.get('designatedPlaceImage', [])

    print(f"描述: {description}, 位置: {location}, 方法: {method}, 放置地点: {designated_place}")
    print(f"失物图片数量: {len(lost_images)}, 放置地点图片数量: {len(designated_place_images)}")

    current_time = datetime.now()
    formatname = current_time.strftime("%Y-%m-%d-%H-%M-%S")

    saveTool = GlobalObjects.saveTool
    saveTool.haveplaceimg = 1 if len(designated_place_images) != 0 else 0
    saveTool.save(description, location, formatname.split("-"), method, "", "", designated_place, saveTool.haveplaceimg)

    # 保存失物图片
    saved_lost_images = []
    for image in lost_images:
        filename = formatname + "-0.png"
        base64_data = image.get('url')
        if base64_data:
            save_base64_image(base64_data, filename)
            saved_lost_images.append(filename)

    # 保存放置地点图片
    saved_designated_place_images = []
    for image in designated_place_images:
        filename = formatname + "-1.png"
        base64_data = image.get('url')
        if base64_data:
            save_base64_image(base64_data, filename)
            saved_designated_place_images.append(filename)

    return jsonify({
        'success': True,
        'message': '提交成功！',
        'savedLostImages': saved_lost_images,
        'savedDesignatedPlaceImages': saved_designated_place_images
    })

def save_base64_image(base64_data, filename):
    try:
        header, base64_data = base64_data.split(',', 1)
        img_data = base64.b64decode(base64_data)
        save_path = LOSS_PIC_DIR if filename.endswith('0.png') else PLACE_PIC_DIR
        with open(os.path.join(save_path, filename), 'wb') as file:
            file.write(img_data)
    except Exception as e:
        print("图片保存失败:", e)
        raise

@app.route('/api/lost_items', methods=['POST'])
def get_itemsInfo():
    jsondata = request.get_json()
    page = int(jsondata.get('page', 1))
    page_size = int(jsondata.get('pageSize', 10))
    reader = GlobalObjects.reader
    data = reader.readdata(page, page_size)
    return jsonify({'items': data})

def deal_image_name(pathlist):
    # 将图片的路径转化为可查询的格式
    res=[]
    for p in pathlist:
        plist=p[0].split('/')
        res.append(plist[-1])
    return res


def findPIC(CLIPprompt):
    finder = GlobalObjects.finder
    pathlist = finder.find(CLIPprompt)

    reader = GlobalObjects.reader

    name = deal_image_name(pathlist)

    data = reader.readGivenNameItem(name)

    print("图片路径集合为：\n", pathlist)
    return data
@app.route("/api/LLMText",methods=['POST'])
def UseLLM():
    global conversation_history
    data1 = request.get_json()
    userinput = data1.get('text', None)
    print("收到的输入为：", userinput)
    system_message = {
        'role': 'system',
        'content': prompt_text
    }

    if not conversation_history:
        conversation_history = [system_message]

    try:
        # 将用户的输入添加到对话历史中
        conversation_history.append({'role': 'user', 'content': userinput})

        # 使用完整的对话历史来获取响应
        completion = client.chat.completions.create(
            model="qwen-turbo-2024-11-01",
            messages=conversation_history,
        )

        assistant_reply = completion.choices[0].message
        conversation_history.append(assistant_reply)
        try:
            reply_dict = json.loads(assistant_reply.content)
        except json.JSONDecodeError:
            return jsonify({"isok": False,"llmtext": "json解析错误", "error": True,"items": ""}), 500

        status = reply_dict.get("status")
        info = reply_dict.get("info")
        reply = reply_dict.get("reply")

        # 根据状态返回响应
        if status == "完成":
            print("最终CLIP的提示词为：", info)
            conversation_history = []
            print("助手记忆已清空，可以开始查询下一件物品")
            searchdata=findPIC(info)
            return jsonify({"isok": True, "llmtext": info, "error": False,"items": searchdata})
        else:
            return jsonify({"isok": False, "llmtext": reply, "error": False,"items": ""})

    except Exception as e:
        print("发生错误：", str(e))
        return jsonify({"isok": False, "llmtext": "","error": str(e),"items": ""}), 500


@app.route("/api/UserText", methods=['POST'])
def getUserText():
    data1 = request.get_json()
    userinput = data1.get('text', None)
    print("收到的输入为：", userinput)

    finder = GlobalObjects.finder
    pathlist = finder.find(userinput)

    reader = GlobalObjects.reader

    name=deal_image_name(pathlist)

    data = reader.readGivenNameItem(name)

    print("图片路径集合为：\n", pathlist)
    return jsonify({"issuccess": True,
                    "items":data})

@app.route('/static/uploads/<filename>', methods=['GET'])
def get_file(filename):
    print("获取图片的代码被调用了，filename为：", filename)
    loss_pic_path = os.path.join(LOSS_PIC_DIR, filename)
    place_pic_path = os.path.join(PLACE_PIC_DIR, filename)

    if os.path.exists(loss_pic_path):
        return send_from_directory(LOSS_PIC_DIR, filename)
    elif os.path.exists(place_pic_path):
        return send_from_directory(PLACE_PIC_DIR, filename)
    else:
        print("图片未找到")
        return jsonify({"error": "图片未找到"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
