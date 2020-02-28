from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from flask_uploads import UploadSet,IMAGES,configure_uploads,patch_request_class
from flask_debugtoolbar import DebugToolbarExtension
from flask_ckeditor import CKEditor
from flask_cache import Cache
# 创建对象
db = SQLAlchemy()
migrate = Migrate(db=db)
moment = Moment()


# 初始化
def config_extensions(app):
    db.init_app(app)
    migrate.init_app(app)
    moment.init_app(app)
    # cache.init_app(app,config={'CACHE_TYPE':'redis'})
