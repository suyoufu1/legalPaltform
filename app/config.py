import os

BASE_PATH = os.path.abspath(os.path.dirname(__file__))




class Config(object):
    # 无警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 设置redis默认过期时间
    EXPIRES_TIME = 60*3
# 开发环境
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:520000ww@47.106.183.183:3306/legalbook'
    # 配置redis
    REDIS_DB_URL = {
        'host': '47.106.183.183',
        'port': '9200',
        'password': '',
        'db': 1
    }
    DEBUG = True
#配置的字典
configDict = {
    'default':DevelopmentConfig,
    'development':DevelopmentConfig
}

