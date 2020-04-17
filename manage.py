from flask import Flask
from flask_migrate import MigrateCommand
from flask_script import Manager, Server
from app import create_app #导入app
app = create_app('development') #加载配置，默认开发环境
manager = Manager(app)
manager.add_command('db',MigrateCommand)
manager.add_command("runserver", Server(
    host = '127.0.0.1',port=8084)
)
# app = Flask(__name__)
# app.register_blueprint(main,url_prefix="/")
if __name__ == '__main__':
    manager.run()
