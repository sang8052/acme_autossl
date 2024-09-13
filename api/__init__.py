import json,traceback
import os.path

import tools,time
from flask import Flask,request,current_app,g,make_response,send_file,redirect
from flask_socketio import SocketIO,disconnect,emit
from werkzeug.middleware.proxy_fix import ProxyFix

static_url_path = "/web"
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


# 不需要登录访问的路由
white_paths = [
    static_url_path,
    "/api/user/login",
    "/api/user/reg",
    "/api/config/mail",
    "/api/task/callback"
]

def checkup_need_login():
    for white_path in white_paths:
        if request.path.startswith(white_path) :
            return False
    if request.path == "/":
        return False
    return True

@app.route("/",methods=['GET'])
def http_request_default_index():
    return redirect(static_url_path)

@app.before_request
def app_before_request():
    g.request_id = tools.get_uuid()
    g.request_time = tools.get_ms_time()
    g.db = current_app.db 
    g.session_id = ""
    g.rheaders={}
    __http_request_header()
    __http_request_payload()

    # 检查是否需要登录后访问
    if checkup_need_login() and g.session_id == "":
        return json_response({"code":-403,"msg":"请先登录到系统!","data":{"path":request.path}})
    if g.session_id != "":
        g.db.cache_ttl("acme_auto_ssl:user_session:" + g.session_id,600)
        g.session = g.db.cache_get_value("acme_auto_ssl:user_session:" + g.session_id)


@app.after_request
def app_after_response(response):
    response.headers["X-Request-Id"] = g.request_id
    response.headers["X-Use-Time"] = str (tools.get_ms_time() - g.request_time ) + " ms"
    if request.method == "OPTIONS":
        response.status_code = 200 
    response.headers["X-Session-Id"] = g.session_id
    for key in g.rheaders.keys():
        response.headers[key] = g.rheaders[key]
    return response

@app.errorhandler(404)
def http_response_nofound(err):

    # vue history 模式路由 重定向文件到 /www/index.html
    if request.path.startswith(static_url_path):
        start_pos = len(static_url_path)
        file_path = current_app.work_path + "/www" + request.path[start_pos:]
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return send_file(file_path)
        else:
            file_path = current_app.work_path + "/www/index.html"
            if os.path.exists(file_path):
                return send_file(file_path)

    return json_response({"code":-404,"msg":"request page not found","data":{"path":request.path}},404)

@app.errorhandler(Exception)
def http_response_error(err):
    print(err)
    error_msg = str(err)
    error_response = {"code":-500,"msg":"unknow error","data":{"error":error_msg,"debug":traceback.format_exc(),"payload":g.payload,"url":request.url}}
    console_log = """[WARNING]发生未知异常,ERROR:
请求URL: %s
请求载荷: %s
错误信息: %s
错误详情: %s
""" %   (error_response["data"]["url"],json.dumps(error_response["data"]["payload"]), error_response["data"]["error"], error_response["data"]["debug"])
    tools.console_log(console_log)
    return json_response(error_response,500)

    


# 初始化 HTTP 请求的 HEADER 
def __http_request_header():
    g.request_headers = {}
    g.content_type = ""
    g.user_agent = ""
    session_id = ""
    authorization = ""
    g.client_ip = request.remote_addr
    g.request_headers = get_client_headers()
    if "x-session-id" in g.request_headers.keys():
        session_id = g.request_headers["x-session-id"]
    if "authorization" in g.request_headers.keys():
        authorization = g.request_headers["authorization"]
    if "user-agent" in g.request_headers.keys():
        g.user_agent = g.request_headers["user-agent"]
    if "content-type" in g.request_headers.keys():
        g.content_type = g.request_headers["content-type"]
    
    if g.db.cache_has("acme_auto_ssl:user_session:" + session_id):
        g.session_id = session_id
    if g.db.cache_has("acme_auto_ssl:user_session:" + authorization):
        g.session_id = authorization
        
  


# 初始化 HTTP 请求的 PAYLOAD
def __http_request_payload():
    g.params = request.args.to_dict()
    g.payload = {}
    if "application/form-data" in g.content_type or "application/x-www-form-urlencode" in g.content_type:
        try:
            g.payload = request.form.to_dict()
        except:
            g.payaload = {}
    if "application/json" in g.content_type:
        try:
            g.payload = json.loads(request.get_data(as_text=True))
        except:
            g.payload = {}


def get_client_headers():
    request_headers = {}
    for key in dict(request.headers).keys():
        request_headers[key.lower()] = dict(request.headers)[key]
    return request_headers



def proxy_client_address():
    proxy_headers = ['X-REAL-IP','X-FORWARDED-FOR','REMOTE-HOST']
    client_headers = get_client_headers()
    for proxy_header in proxy_headers:
        if proxy_header.lower() in client_headers.keys():
            return client_headers[proxy_header.lower()]
    return None



def query_system_config(item_name):
    g.db.sql_lock()
    g.db.sql_where("item_name","=",g.db.sql_value(item_name))
    g.db.sql_unlock()
    config = g.db.sql_query("sys_config");
    if len(config) >= 0:
        return config[0]["item_value"]
    else:
        return None 
                
def json_response(payload,code=200):
    response = make_response(json.dumps(payload,ensure_ascii=False),code)
    response.headers["Content-Type"] = "application/json"
    return response

from engineio.async_drivers import gevent


"""
WebSocket 会话逻辑
"""
socketio = SocketIO(async_mode='gevent')
name_space = "/socket_io"
@socketio.on('connect', namespace=name_space)
def connected_msg():
    tools.console_log("[LOG]有新的客户端建立连接,sid:" + request.sid)
    session_id = ""
    for key in dict(request.headers).keys():
        if key.lower() == "x-session-id" and session_id == "":
            session_id = dict(request.headers)[key]
    if not current_app.db.cache_has("acme_auto_ssl:user_session:" + session_id):
        tools.console_log("[WARNING]客户端session 不存在,踢出客户端!")
        disconnect(request.sid)
    else:
        client_headers = get_client_headers()
        socket_client = {
            "sid":request.sid,
            "client_ip":proxy_client_address(),
            "session_id":session_id,
            "last_heart":int(time.time()),
            "user_agent":client_headers["user-agent"] if "user-agent" in client_headers.keys() else None,
            "sec_ch_ua": client_headers["sec-ch-ua"] if "sec-ch-ua" in client_headers.keys() else None,
            "sec_ch_ua_platform": client_headers["sec-ch-ua-platform"] if "sec-ch-ua-platform" in client_headers.keys() else None,
            "origin": client_headers["origin"] if "origin" in client_headers.keys() else None,
        }
        current_app.db.cache_set_value("acme_auto_ssl:websocket_client:" + request.sid,socket_client)
        tools.console_log("[INFO]客户端会话初始化成功,sid:" + request.sid)

        # 更新web session
        web_session = current_app.db.cache_get_value("acme_auto_ssl:user_session:" + session_id)
        web_session["websocket_sid"] = request.sid
        web_session["websocket_heart"] = socket_client["last_heart"]
        current_app.db.cache_set_value("acme_auto_ssl:user_session:" + session_id, web_session, 600)

        emit("auth success",json.dumps(socket_client))



@socketio.on('disconnect', namespace=name_space)
def disconnect_msg():
    tools.console_log("[WARNING]客户端关闭了连接,sid:" + request.sid)
    current_app.db.cache_delete("acme_auto_ssl:websocket_client:" + request.sid)


@socketio.on('heart', namespace=name_space)
def mtest_message(message):
    client = find_client_by_sid(request.sid)
    if not client:
        disconnect(request.sid)
    else:
        tools.console_log("[LOG]收到客户端的心跳,sid:" + request.sid)
        # 更新websocket_client
        client["last_heart"] = int(time.time())
        client["client_ip"] = proxy_client_address()
        current_app.db.cache_set_value("acme_auto_ssl:websocket_client:" + request.sid, client)

        # 更新web session
        web_session = current_app.db.cache_get_value("acme_auto_ssl:user_session:" + client["session_id"])
        web_session["websocket_sid"]   = request.sid
        web_session["websocket_heart"] = client["last_heart"]
        current_app.db.cache_set_value("acme_auto_ssl:user_session:" + client["session_id"], web_session,600)




def find_client_by_sid(sid):
    if current_app.db.cache_has("acme_auto_ssl:websocket_client:" + sid):
        return current_app.db.cache_get_value("acme_auto_ssl:websocket_client:" + sid)
    return None

from . import user
from . import task 
from . import dnsapi 
from . import config
from . import task
from . import cert 
from . import domain
