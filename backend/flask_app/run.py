from flask import Flask, request, jsonify,send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 配置上传文件夹
UPLOAD_FOLDER = '../../resource/loss_pic'
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



@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
