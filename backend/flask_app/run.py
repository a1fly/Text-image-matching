from flask import Flask, request, jsonify,send_from_directory
from werkzeug.utils import secure_filename
import requests
import os
import base64
from datetime import datetime

app = Flask(__name__)


# 配置上传文件夹
UPLOAD_FOLDER = '../../resource'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


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
        with open(os.path.join(UPLOAD_FOLDER, filename), 'wb') as file:
            file.write(img_data)
    except Exception as e:
        print("图片保存失败:", e)
        raise



@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



