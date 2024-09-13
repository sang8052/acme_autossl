import threading

from gevent import pywsgi
from gevent import monkey
# 引入 pywsgi 的代理修复模块
import pywsgi_proxy
monkey.patch_all()

import os
import tools,api,dataconn
from flask_cors import CORS

app_version = "1.3.3"

if __name__ == "__main__":

    print("ACME_AutoSSL 自动签发工具")
    print("Author:mail@szhcloud.cn")
    print("Github:https://github.com/sang8052/acme_autossl")
    print("Version:" + app_version)
    

    config = tools.read_json("./config.json")
    db = dataconn.database(config["mysql"],config["redis"])

    api.app.db = db 
    api.app.work_path = os.path.abspath("./")
    api.app.http_port = config["app"]["http_port"]
    api.app.app_version = app_version

    tools.mkdir_nx(api.app.work_path + "/tmp")
    tools.mkdir_nx(api.app.work_path + "/www")
    tools.console_log("[INFO]加载API配置文件成功")
    
  

    # 是否开启 CORS 跨越访问支持
    if config["app"]["enable_cors"]:
        CORS(api.app,supports_credentials=True)
        api.socketio.init_app(api.app, cors_allowed_origins='*')
    else:
        api.socketio.init_app(api.app)

    tools.console_log("[INFO]WSGIServer Listen 0.0.0.0:" + str(api.app.http_port))
    api.socketio.run(api.app, host='0.0.0.0', port=api.app.http_port,log_output=True)

    #server = pywsgi.WSGIServer(("0.0.0.0",api.app.http_port),api.app)
    #server.multithread = True
    #server.serve_forever()




