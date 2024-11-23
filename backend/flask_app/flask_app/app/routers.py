from flask import Blueprint, request, jsonify

main = Blueprint('main', __name__)

@main.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    print('账号：',username)
    print('密码：',password)

    # 这里可以添加你的认证逻辑
    if username == 'admin' and password == 'password':
        return jsonify({'success': True, 'message': '登录成功'})
    else:
        return jsonify({'success': False, 'message': '用户名或密码错误'}), 401