项目目录结构
      legalPaltform/
        |-- app/
        |   |-- algorithm/
        |   |   |-- IdealWordCloudKit
        |   |   |-- KeyInfoExtraction
        |   |   |-- sentencesimarly
        |   |-- controller
        |   |-- models
        |   |-- redis
        |   |-- static
        |   |-- templates
        |   |-- utils
        |   |-- build_database.py
        |   |-- config.py
        |   |-- extensions.py
        |-- venv
        |-- manage.py
        |-- requirements.txt
        |-- README.txt
1.templates说明：
    主页：homepage
    关键字统计:keywordStatistics
    地区统计:regionalStatistics
    文本展示：show
    无相似案件推荐:noSimilar
    案件数量分布：caseDistribution
    检索内容展示:searchShow
    检索界面：search
    法院统计:courtStatistics
    相似案件推荐文本展示:
    相似案件推荐首页:similarPage
    统计:statistics
    词云统计:worldcloudStatistics
    罪名预测界面:crimepage
    罪名预测小界面:crimeclass
 2.controller说明：
    主页：main.py
    相似度推荐：recomment.py
    检索：search.py
    统计分析:statistics.py
    罪名预测：prediction.py
  3.algorithm 算法：
    1）、sentencesimarly 句子相似度算法
    2）、KeyInfoExtraction 文本摘要抽取
   4.elasticsearch安装linux：
     1)安装jdk11以上
            1.安装命令：wget https://download.oracle.com/otn-pub/java/jdk/13.0.1+9/cec27d702aa74d5a8630c65ae61e4305/jdk-13.0.1_linux-x64_bin.tar.gz?AuthParam=1577954453_a6b4a63fb1bf26cb51d040fdef2f0229
            2.配置环境变量
                export JAVA_HOME=/opt/jdk
                export PATH=$JAVA_HOME/bin:$PATH
                export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
            3.环境变量生效
                source  /etc/profile
      2）安装es
            使用root用户
                vi /etc/sysctl.conf
            # 在最后一行添加一下内容
                vm.max_map_count=655360
            切换到es用户
                su elsearch
            下载es最新版本
                wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.5.1-linux-x86_64.tar.gz
            配置文件
            vi /opt/es/config/elasticsearch.yml
             #---设置以下内容
                cluster.name: es-bigdata-rt-s1
                node.name: 10.20.214.139
                path.data: /data02/es/data
                path.logs: /data02/es/logs
                network.host: 10.20.214.139
                http.port: 9200
                discovery.seed_hosts: ["10.20.214.139", "10.20.214.140","10.20.214.141"]
                cluster.initial_master_nodes: ["10.20.214.139", "10.20.214.140","10.20.214.141"]
                http.cors.enabled: true
                http.cors.allow-origin: "*"
                node.master: true
                node.data: true
            目录授权
            # 使用root用户
                mkdir -p /data02/es/logs
                chown elsearch:elsearch -R /data02/es
        3）安装IK分词器
            官网地址 https://github.com/medcl/elasticsearch-analysis-ik
            配置
                create plugin folder cd your-es-root/plugins/ && mkdir ik
                unzip plugin to folder your-es-root/plugins/ik
         4）启动ES服务
            每个机器上都需要启动
             /opt/es/bin/elasticsearch  -d

         5)改一下配置文件，把集群和节点信息配了一下；然后修改了一下整个目录的所有权为elasticsearch；然后切换到elasticsearch用户，启动。后台启动./elasticsearch -d
       5.python库的安装
            所有依赖的库文件都在requirements.txt,clone项目后，直接用命令安装：pip install -r requirements.txt
       6.启动文件
            manage.py：启动程序
       
