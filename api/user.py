import api,tools
from flask import g
from flask_socketio import  disconnect
import time 

# 使某个用户强制下线
def unlogin_by_username(username):
    user_session_ids = g.db.cache_keys("acme_auto_ssl:user_session:*")
    for user_session_id in user_session_ids:
        user_session = g.db.cache_get_value(user_session_id)
        if user_session["username"] == username:
            g.db.cache_delete(user_session_id)
            if "websocket_sid" in user_session.keys():
                g.db.cache_delete("acme_auto_ssl:websocket_client:" + user_session["websocket_sid"])
                disconnect(user_session["websocket_sid"],namespace=api.name_space)
            tools.console_log("[INFO]Session-Id:%s 已强制下线" % (user_session["session_id"]))
    

@api.app.route("/api/user/",methods=['GET'])
def http_request_user_session():
    return api.json_response({"code":0,"msg":"操作成功","data":g.session})
    
# 修改邮箱或昵称
@api.app.route("/api/user/",methods=['POST'])
def http_request_user_update_mail():
    mail_address = g.payload["mail_address"]
    nickname = g.payload["nickname"]
    g.db.sql_lock()
    g.db.sql_where("id","=",g.db.sql_value(g.session["uid"]))
    update_user = {"mail_address":mail_address,"nickname":nickname}
    g.db.sql_update("sys_user",update_user)
    g.db.sql_unlock()
    g.session["mail_address"] = mail_address;
    g.session["nickname"] = nickname;
    g.db.cache_set_value("acme_auto_ssl:user_session:" + g.session_id,g.session)
    return api.json_response({"code":0,"msg":"操作成功","data":g.session})
    
@api.app.route("/api/user/password/",methods=['POST'])
def http_request_user_update_password():
    old_password = g.payload["old_password"]
    new_password = g.payload["new_password"]
    g.db.sql_lock()
    g.db.sql_where("id","=",g.db.sql_value(g.session["uid"]))
    g.db.sql_where("password","=",g.db.sql_value(tools.text_md5(g.session["username"] + ":" + old_password)))
    users = g.db.sql_query("sys_user")
    g.db.sql_unlock()
    if len(users) == 0:
        return api.json_response({"code":500,"msg":"原密码不正确"})
    else:
        update_user = {"password":tools.text_md5(g.session["username"] + ":" + new_password)}
        g.db.sql_lock()
        g.db.sql_where("id","=",g.db.sql_value(g.session["uid"]))
        g.db.sql_update("sys_user",update_user)
        g.db.sql_unlock()
        unlogin_by_username(g.session["username"])

    return api.json_response({"code":0,"msg":"操作成功","data":g.session})

@api.app.route("/api/user/login/",methods=['POST'])
def http_request_user_login():
    username = g.payload["username"]
    password = g.payload["password"]
    g.db.sql_lock()
    g.db.sql_where("username","=",g.db.sql_value(username))
    g.db.sql_where("password","=",g.db.sql_value(tools.text_md5(username + ":" + password)))
    tools.console_log("用户输入的密码的md5:" + tools.text_md5(username + ":" + password))
    users = g.db.sql_query("sys_user")
    g.db.sql_unlock()
    if len(users) == 0:
        return api.json_response({"code":403,"msg":"用户名或密码不正确"})
    else:
        user_session = users[0]
        user_session["uid"] = user_session["id"]
        del user_session["password"]
        del user_session["id"]
        del user_session["create_time"]
        del user_session["update_time"]
        user_session["user_agent"] = g.user_agent
        user_session["client_ip"] = g.client_ip
        user_session["login_time"] = int(time.time() * 1000)
        # 强制下线其他客户端
        unlogin_by_username(user_session["username"])
        session_id = tools.get_uuid()
        user_session["session_id"] = session_id
        g.db.cache_set_value("acme_auto_ssl:user_session:" + session_id,user_session,600)
        g.rheaders["X-Session-Id"] = session_id
        return api.json_response({"code":0,"msg":"登录成功","data":user_session})
    
@api.app.route("/api/user/reg/",methods=['POST'])
def http_request_user_reg():
    username = g.payload["username"]
    password = g.payload["password"]
    nickname = g.payload["nickname"]
    mail_address = g.payload["mail_address"]
    g.db.sql_lock()
    g.db.sql_where("username","=",g.db.sql_value(username))
    users = g.db.sql_query("sys_user")
    g.db.sql_where("mail_address","=",g.db.sql_value(mail_address))
    mails = g.db.sql_query("sys_user")
    g.db.sql_unlock()
    if len(users) != 0:
        return api.json_response({"code":500,"msg":"用户名已注册!"})
    elif len(mails) != 0:
        return api.json_response({"code":500,"msg":"邮箱地址已经被绑定!"})
    else:
        new_user = {"username":username,"password":tools.text_md5(username + ":" + password),"nickname":nickname,"mail_address":mail_address}
        g.db.sql_lock()
        uid = g.db.sql_insert("sys_user",new_user)
        g.db.sql_unlock()
        return api.json_response({"code":0,"msg":"注册成功","data":{"uid":uid}})
    


