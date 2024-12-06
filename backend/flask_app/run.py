from flask import Flask, request, jsonify,send_from_directory
from werkzeug.utils import secure_filename,send_file
import requests
import os
import base64
from datetime import datetime
from DealFunc.savewriteInfo import SaveInfo
from DealFunc.readinfo import ReadInfo
from backend.ClipFinder import Finder
import atexit






# 配置上传文件夹
UPLOAD_FOLDER = '../../resource'
LOSS_PIC_DIR='../../resource/loss_pic'
PLACE_PIC_DIR='../../resource/place_pic'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
config_path="../config.json"



lock_file = "./tmp/myapp_init.lock"

# 用于存储对象的全局变量
saveTool = None
reader = None
finder = None

def remove_lock_file():
    if os.path.exists(lock_file):
        os.remove(lock_file)


def init_database():
    # 执行初始化逻辑
    global saveTool, reader, finder
    if not os.path.exists(lock_file):
        print('开始初始化...')
        saveTool = SaveInfo()
        reader = ReadInfo()
        finder = Finder(config_path=config_path)
        finder.encodeImage(pic_path=LOSS_PIC_DIR)
        print("初始化完成")

        # 创建锁文件以防止重复初始化
        open(lock_file, 'a').close()
    # 注册退出处理程序，在应用结束时删除锁文件
    atexit.register(remove_lock_file)



init_database()






app = Flask(__name__)
app.config['init_database'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# 登录验证
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

# 注册验证
@app.route('/api/reg', methods=['POST'])
def check_reg():
    data = request.get_json()
    contactType=data.get('contactType')
    username=data.get('username')
    password=data.get('password')
    contactNumber=data.get('contactNumber')

    print('账号：',username)
    print('密码：',password)
    print('联系方式：',contactNumber)
    print('联系方式类型：',contactType)
    # 注册验证逻辑
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

    """
    命名规则：
    失物图片：年-月-日-时-分-秒-0
    地点照片：年-月-日-时-分-秒-1
    """


    current_time = datetime.now()
    formatname = current_time.strftime("%Y-%m-%d-%H-%M-%S")


    if len(designated_place_images)!=0:
        saveTool.haveplaceimg=1
    else:
        saveTool.haveplaceimg=0

    saveTool.save(description,
                  location,
                  formatname.split("-"),
                  method,
                  "",
                  "",
                  designated_place,
                  saveTool.haveplaceimg
    )

    # 保存失物图片
    saved_lost_images = []
    for image in lost_images:
        filename = formatname+"-0.png"
        base64_data = image.get('url')
        if base64_data:
            save_base64_image(base64_data, filename)
            saved_lost_images.append(filename)

    # 保存放置地点图片
    saved_designated_place_images = []
    for image in designated_place_images:
        filename = formatname+"-1.png"
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

        # 0结尾表示为失物图片，放进失物文件夹
        if filename.endswith('0.png'):
            with open(os.path.join(UPLOAD_FOLDER, "loss_pic/"+filename), 'wb') as file:
                file.write(img_data)
        else:
            # 1结尾表示为地点图片，放进指定地点文件夹
            with open(os.path.join(UPLOAD_FOLDER, "place_pic/"+filename), 'wb') as file:
                file.write(img_data)

    except Exception as e:
        print("图片保存失败:", e)
        raise


@app.route('/api/lost_items',methods=['POST'])
def get_itemsInfo():
    jsondata = request.get_json()  # 获取请求体中的 JSON 数据
    page = int(jsondata.get('page', 1))  # 从 JSON 数据中获取 page 参数，默认值为 1
    page_size = int(jsondata.get('pageSize', 10))  # 从 JSON 数据中获取 pageSize 参数，默认值为 10

    data=reader.readdata(page,page_size)
    return jsonify({
        'items': data,
    })


@app.route("/api/UserText",methods=['POST'])
def getUserText():
    global finder
    data=request.get_json()
    userinput=data.get('text',None)
    print("收到的输入为：",userinput)



    if(finder is None):
        print("重新初始化finder")
        finder=Finder(config_path=config_path)
        finder.encodeImage(pic_path=LOSS_PIC_DIR)
    pathlist = finder.find(userinput)

    print("图片路径集合为：\n",pathlist)
    return jsonify({
        "issuccess": True,
    })








@app.route('/static/uploads/<filename>', methods=['GET'])
def get_file(filename):


    # kind 为0或者1，表示要传递失物图片还是地点图片

    print("==================================================")
    print("获取图片的代码被调用了，filename为：", filename)
    print("==================================================")
    loss_pic_path = os.path.join(LOSS_PIC_DIR, filename)
    place_pic_path = os.path.join(PLACE_PIC_DIR, filename)

    if os.path.exists(loss_pic_path):
        return send_from_directory(LOSS_PIC_DIR, filename)
    elif os.path.exists(place_pic_path):
        return send_from_directory(PLACE_PIC_DIR, filename)
    else:
        print("NO PIC FOUNDED")








if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)



