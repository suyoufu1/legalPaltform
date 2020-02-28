from .main import main # 首页蓝本
from .search import search
from .recomment import recomment
from .predicti import prediction
from  .statistics import statistic
from .predicti import predicti
# 配置蓝本列表
blueprint_config = [
    (main,''),
    (search,'/searchs'),
    (recomment,'/recomments'),
    (statistic,'/statistics'),
    (predicti,"/predictions")
]
# 注册蓝本
def blueprint_register(app):
    for blue,prefix in blueprint_config:
        print(blue,prefix)
        app.register_blueprint(blue,url_prefix=prefix)