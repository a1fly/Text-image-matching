from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/login', methods=['POST'])
def check_login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    print('账号：', username)
    print('密码：', password)

    if username == 'admin' and password == 'password':
        return jsonify({'success': True, 'message': '登录成功'})
    else:
        return jsonify({'success': False, 'message': '用户名或密码错误'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
