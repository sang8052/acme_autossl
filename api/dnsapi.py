import api
from flask import g

@api.app.route("/api/dnsapi/system/",methods=['GET'])
def http_request_system_query():
    g.db.sql_lock()
    data = g.db.sql_query("sys_dns_api")
    g.db.sql_unlock()
    return api.json_response({"code":0,"msg":"","data":data})


@api.app.route("/api/dnsapi/",methods=['GET'])
def http_request_key_query():

    page_num = int(g.params["page_num"]) if "page_num" in g.params.keys() else 1
    page_size = int(g.params["page_size"]) if "page_size" in g.params.keys() else 10
    keyword =  g.params["keyword"] if "keyword" in g.params.keys() else ""
    key_type = g.params["key_type"] if "key_type" in g.params.keys() else ""
    g.db.sql_lock()
    g.db.sql_where("uid","=",g.db.sql_value(g.session["uid"]))
    if key_type != "":
        g.db.sql_where("key_type","=",g.db.sql_value(key_type))
    if keyword != "":
        g.db.sql_where("key_name","like",g.db.sql_value("%" + keyword + "%"))
    datas = g.db.sql_query("user_dns_api",limit="LIMIT %d , %d" % ((page_num -1)*page_size,page_size))

    g.db.sql_where("uid","=",g.db.sql_value(g.session["uid"]))
    if key_type != "":
        g.db.sql_where("key_type","=",g.db.sql_value(key_type))
    if keyword != "":
        g.db.sql_where("key_name","like",g.db.sql_value("%" + keyword + "%"))
    all_count = g.db.sql_count("user_dns_api")
    g.db.sql_unlock()
    data = {"page_num":page_num,"page_size":page_size,"total":all_count,"data":datas}
    return api.json_response({"code":0,"msg":"","data":data})

@api.app.route("/api/dnsapi/",methods=['POST'])
def http_request_key_create():
    key_name = g.payload["key_name"]
    key_type = g.payload["key_type"]
    access_id = g.payload["access_id"]
    access_key = g.payload["access_key"]
    g.db.sql_lock()
    g.db.sql_where("key_name","=",g.db.sql_value(key_name))
    g.db.sql_where("uid","=",g.db.sql_value(g.session["uid"]))
    is_exist = g.db.sql_count("user_dns_api")
    g.db.sql_unlock()
    if is_exist:
        return api.json_response({"code":403,"msg":"已经有这个名称的API密钥了"})
    else:
        new_key = {
            "uid":g.session["uid"],
            "key_name":key_name,
            "key_type":key_type,
            "access_id":access_id,
            "access_key":access_key
        }
        g.db.sql_lock()
        id = g.db.sql_insert("user_dns_api",new_key)
        g.db.sql_unlock()
        return api.json_response({"code":0,"msg":"新建API密钥信息成功","data":{"id":id}})
    

@api.app.route("/api/dnsapi/<id>/",methods=["GET"])
def http_request_key_detail(id):
    g.db.sql_lock()
    g.db.sql_where("uid","=",g.db.sql_value(g.session["uid"]))
    g.db.sql_where("id","=",g.db.sql_value(id))
    key = g.db.sql_query("user_dns_api")
    g.db.sql_unlock()
    if len(key) == 0:
        return api.json_response({"code":404,"msg":"秘钥不存在或者已经被删除"})
    else:
        return api.json_response({"code":0,"msg":"","data":key[0]})
    
@api.app.route("/api/dnsapi/<id>/",methods=["DELETE"])
def http_request_key_delete(id):
    g.db.sql_lock()
    g.db.sql_where("uid","=",g.db.sql_value(g.session["uid"]))
    g.db.sql_where("id","=",g.db.sql_value(id))
    is_exist = g.db.sql_count("user_dns_api")
    g.db.sql_unlock()
    if not is_exist:
        return api.json_response({"code":404,"msg":"秘钥不存在或者已经被删除"})
    else:
        g.db.sql_lock()
        g.db.sql_where("id","=",g.db.sql_value(id))
        g.db.sql_delete("user_dns_api")
        g.db.sql_unlock()
        return api.json_response({"code":0,"msg":"删除秘钥成功","data":None})

@api.app.route("/api/dnsapi/<id>/",methods=["POST"])
def http_request_key_update(id):
    g.db.sql_lock()
    g.db.sql_where("uid","=",g.db.sql_value(g.session["uid"]))
    g.db.sql_where("id","=",g.db.sql_value(id))
    is_exist = g.db.sql_count("user_dns_api")
    g.db.sql_unlock()
    if not is_exist:
        return api.json_response({"code":404,"msg":"秘钥不存在或者已经被删除"})
    else:
        if "key_name" in g.payload.keys():
            g.db.sql_lock()
            g.db.sql_where("uid","=",g.db.sql_value(g.session["uid"]))
            g.db.sql_where("key_name","=",g.db.sql_value(g.payload["key_name"]))
            g.db.sql_where("id","!=",id)
            is_exist = g.db.sql_count("user_dns_api")
            g.db.sql_unlock()
            if is_exist:
                return api.json_response({"code":403,"msg":"已经存在相同名称的配置项目"})
        update_key = {}
        fields = ["key_type","access_id","access_key","key_name"]
        for field in fields:
            update_key[field] = g.payload[field]
        g.db.sql_lock()
        g.db.sql_where("id","=",g.db.sql_value(id))
        g.db.sql_update("user_dns_api",update_key)
        g.db.sql_unlock()
        return api.json_response({"code":0,"msg":"操作成功","data":None})
 

 

    