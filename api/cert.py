import threading,json

import api
from flask import g
import os,tools,subprocess




def run_async_shell(command,log_path,session_id,db,task_id):

    def find_sid_by_session_id(session_id):
        if db.cache_has("acme_auto_ssl:user_session:" + session_id):
            websocket_client = db.cache_get_value("acme_auto_ssl:user_session:" + session_id)
            if "websocket_sid" in websocket_client:
                return websocket_client["websocket_sid"]
            else:
                return None
        return None

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # 更新线程的pid
    db.sql_lock()
    db.sql_where("id", "=", db.sql_value(task_id))
    update_task = {"pid":process.pid}
    db.sql_update("sys_task",update_task)
    db.sql_unlock()
    line_id = 1
    for line in process.stdout:
        line = line[:-1].decode("utf-8")
        if os.path.exists(log_path):
            tools.write_append(log_path,line + "\n")
        websocket_sid = find_sid_by_session_id(session_id)
        if websocket_sid:
            try:
                api.socketio.emit("terminal",json.dumps({"line_id":line_id,"content":line,"task_id":task_id}),to=websocket_sid,namespace=api.name_space)
            except Exception as err:
                print(err)
        line_id = line_id + 1
    process.wait()

    db.sql_lock()
    db.sql_where("id", "=", db.sql_value(task_id))
    task = db.sql_query("sys_task")[0]
    db.sql_unlock()

    db.sql_lock()
    db.sql_where("id", "=", db.sql_value(task["cert_id"]))
    cert = db.sql_query("user_cert")[0]
    db.sql_unlock()

    api.socketio.emit("terminal", json.dumps({"line_id": -1, "content": {"task":task,"cert":cert}, "task_id": task_id}),to=websocket_sid, namespace=api.name_space)
    if process.returncode != 0:
        tools.console_log("[WARNING]执行异步指令[%s]出错,code:%s" % (command, str(process.returncode)))
    else:
        tools.console_log("[INFO]执行异步指令[%s]成功!" % (command))


@api.app.route("/api/cert/",methods=['GET'])
def http_request_cert_query():
    page_num = int(g.params["page_num"]) if "page_num" in g.params.keys() else 1
    page_size = int(g.params["page_size"]) if "page_size" in g.params.keys() else 10
    domain_id = g.params["domain_id"] if "domain_id" in g.params.keys() else ""
    keyword =  g.params["keyword"] if "keyword" in g.params.keys() else ""
    g.db.sql_lock()
    g.db.sql_where("user_cert.uid","=",g.db.sql_value(g.session["uid"]))
    if keyword != "":
        g.db.sql_where("prefix","like",g.db.sql_value("%" + keyword + "%"))
    if domain_id != "":
        g.db.sql_where("domain_id","=",g.db.sql_value(domain_id))
    datas = g.db.sql_query("user_cert",
        fields=["user_cert.id","user_cert.expire_time","user_cert.reg_time","user_cert.domain_id","user_cert.prefix","user_cert.serial_number","user_cert.common_name","user_cert.signature_algorithm","user_dns_domain.domain"],
        limit="LIMIT %d , %d" % ((page_num -1)*page_size,page_size),
        joins=[["user_dns_domain","user_dns_domain.id = user_cert.domain_id"]],
        order="ORDER BY id desc"
    )
    
    g.db.sql_where("uid","=",g.db.sql_value(g.session["uid"]))
    if keyword != "":
        g.db.sql_where("prefix","like",g.db.sql_value("%" + keyword + "%"))
    if domain_id != "":
        g.db.sql_where("domain_id","=",g.db.sql_value(domain_id))
    all_count = g.db.sql_count("user_cert")
    g.db.sql_unlock()
    data = {"page_num":page_num,"page_size":page_size,"total":all_count,"data":datas}
    return api.json_response({"code":0,"msg":"","data":data})

@api.app.route("/api/cert/<id>/",methods=['GET'])
def http_request_cert_detail(id):
    g.db.sql_lock()
    g.db.sql_where("user_cert.uid","=",g.db.sql_value(g.session["uid"]))
    g.db.sql_where("user_cert.id","=",g.db.sql_value(id))
    cert = g.db.sql_query("user_cert",joins=[["user_dns_domain","user_dns_domain.id = user_cert.domain_id"]],fields=["user_cert.*","user_dns_domain.domain"])
    g.db.sql_unlock()
    if len(cert) == 0:
        return api.json_response({"code":404,"msg":"证书不存在或者已经被删除"})
    else:
        return api.json_response({"code":0,"msg":"","data":cert[0]})
    


@api.app.route("/api/cert/<id>/",methods=['DELETE'])
def http_request_cert_detele(id):
    g.db.sql_lock()
    g.db.sql_where("uid","=",g.db.sql_value(g.session["uid"]))
    g.db.sql_where("id","=",g.db.sql_value(id))
    is_exist = g.db.sql_count("user_cert")
    g.db.sql_unlock()
    if not is_exist:
        return api.json_response({"code":404,"msg":"证书不存在或者已经被删除"})
    else:
        g.db.sql_lock()
        g.db.sql_where("id","=",g.db.sql_value(id))
        g.db.sql_delete("user_cert")
        g.db.sql_unlock()
        return api.json_response({"code":0,"msg":"删除证书成功","data":None})


@api.app.route("/api/cert/",methods=["POST"])
def http_request_cert_create():
    prefix = g.payload["prefix"]
    domain_id = g.payload["domain_id"]
    acme_server = g.payload["acme_server"]
    callback_url = g.payload["callback_url"] if "callback_url" in g.payload.keys() else ""

    # 检查域名
    g.db.sql_lock()
    g.db.sql_where("uid","=",g.db.sql_value(g.session["uid"]))
    g.db.sql_where("id","=",g.db.sql_value(domain_id))
    domains = g.db.sql_query("user_dns_domain")
    g.db.sql_unlock()
    if len(domains) == 0:
        return api.json_response({"code":404,"msg":"域名不存在或已经被删除"})
    api_domain = domains[0]
    key_id = api_domain["key_id"]
    # 检查API 密钥
    g.db.sql_lock()
    g.db.sql_where("uid","=",g.db.sql_value(g.session["uid"]))
    g.db.sql_where("id","=",g.db.sql_value(key_id))
    keys = g.db.sql_query("user_dns_api")
    g.db.sql_unlock()
    if len(keys) == 0:
        return api.json_response({"code":404,"msg":"秘钥不存在或者已经被删除"})
    api_key = keys[0]
    

    # 新增记录
    new_cert = {
        "uid":g.session["uid"],
        "prefix":prefix,
        "domain_id":domain_id,
        "callback_url":callback_url
        
    }
    cert_id = g.db.sql_insert("user_cert",new_cert)

    root_domain = api_domain["domain"]
    if prefix == "_":
        prefix = ""
    child_domain = prefix
    reg_domains = []
    if len(child_domain) == 0:
        reg_domains = [root_domain,"www."+root_domain]
    else:
        if child_domain == "*":
            reg_domains = [root_domain,"*."+root_domain]
        else:
            if child_domain[0] == "*":
                sub_domain = child_domain[2:]
                reg_domains = [sub_domain + "." + root_domain , "*." + sub_domain + "." + root_domain]
            else:
                reg_domains = [child_domain +  "." + root_domain ]
    shell_name = ""
    for name in reg_domains:
        shell_name = shell_name + " -d " + name 
    
    g.db.sql_lock()
    g.db.sql_where("api_keyword","=",g.db.sql_value(api_key["key_type"]))
    dns_api = g.db.sql_query("sys_dns_api")[0]
    g.db.sql_unlock()
    
    acme_key_length = int(api.query_system_config("acme_key_length"))
    acme_root_path = api.query_system_config("acme_root_path")
    
    tmp_uuid = tools.get_uuid()
    tmp_dir = api.current_app.work_path + "/tmp/" + tmp_uuid 
    tools.mkdir_nx(tmp_dir)
    reg_shell = "bash %s/acme.sh --issue  --dns %s %s --keylength %d  --cert-home %s --server %s --force " % (acme_root_path,api_key["key_type"],shell_name,acme_key_length,tmp_dir,acme_server)
    reg_name = reg_domains[0]
    reg_name_path = tmp_dir + "/" + reg_name.replace(".","_") 
    if not os.path.exists(reg_name_path):
        os.mkdir(reg_name_path)
    install_shell = "bash %s/acme.sh --install-cert -d %s --cert-home %s --key-file %s/private.key --fullchain-file %s/fullchain.pem " % (acme_root_path,reg_name,tmp_dir,tmp_dir,tmp_dir)

    new_shell = """ # ACME_AutoSSL 自动签发脚本
# 注入环境变量 access_id
export %s=%s
# 注入环境变量 access_key
export %s=%s
# 签发证书
%s 
# COPY 证书
%s 

curl http://127.0.0.1:%d/api/task/callback/%s
    """ % (dns_api["api_id_field"],api_key["access_id"],dns_api["api_key_field"],api_key["access_key"],reg_shell,install_shell,api.current_app.http_port,cert_id)
    
    tmp_file = tmp_dir + "/shell.sh"
    log_file = tmp_dir + "/shell.log"

    tools.write_file(tmp_file,new_shell)

    #os_shell = "nohup bash %s > %s 2>&1 & echo $! > %s"  % (tmp_file,log_file,pid_file)
    #os.system(os_shell)
    #time.sleep(0.1)

    new_task = {
        "uid":g.session["uid"],
        "cert_id":cert_id,
        "status":"running",
        "tmp_uuid":tmp_uuid,
        "reg_path":reg_name_path
    }
    g.db.sql_lock()
    task_id = g.db.sql_insert("sys_task",new_task)
    g.db.sql_unlock()

    tools.console_log("[LOG]SHELL: bash " + tmp_file )
    th = threading.Thread(target=run_async_shell,args=("bash " + tmp_file,log_file, g.session_id, g.db, task_id,))
    th.start()
    tools.console_log("[INFO]Async Shell Start!")
    update = {"task_id":task_id}
    g.db.sql_lock()
    g.db.sql_where("id","=",g.db.sql_value(cert_id))
    g.db.sql_update("user_cert",update)
    g.db.sql_unlock()
    
    return api.json_response({"code":0,"msg":"操作成功","data":{"task_id":task_id,"cert_id":cert_id}})

    


    