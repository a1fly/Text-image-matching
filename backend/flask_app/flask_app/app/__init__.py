from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # 启用 CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})


    return app