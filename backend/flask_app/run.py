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

# 配置上传文件夹
UPLOAD_FOLDER = '../../resource'
LOSS_PIC_DIR = '../../resource/loss_pic'
PLACE_PIC_DIR = '../../resource/place_pic'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(LOSS_PIC_DIR, exist_ok=True)
os.makedirs(PLACE_PIC_DIR, exist_ok=True)

config_path = "../config.json"
lock_file = "./tmp/myapp_init.lock"

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
