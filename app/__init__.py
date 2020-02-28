from flask import Flask
from .config import configDict
from .extensions import config_extensions
from .controller import blueprint_register
def create_app(configName):
    app = Flask(__name__)
    app.config.from_object(configDict[configName])  # 初始化Config类的配置环境
    config_extensions(app)   # 第三方扩展库初始化app
    blueprint_register(app)  # 注册蓝本 app.
    return app
