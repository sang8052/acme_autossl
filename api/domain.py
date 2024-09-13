import api
from flask import g

@api.app.route("/api/domain/",methods=['GET'])
def http_request_domain_query():
    page_num = int(g.params["page_num"]) if "page_num" in g.params.keys() else 1
    page_size = int(g.params["page_size"]) if "page_size" in g.params.keys() else 10
    keyword =  g.params["keyword"] if "keyword" in g.params.keys() else ""
    key_id =  g.params["key_id"] if "key_id" in g.params.keys() else ""
    g.db.sql_lock()
    g.db.sql_where("user_dns_domain.uid","=",g.db.sql_value(g.session["uid"]))
    if key_id != "":
        g.db.sql_where("key_id","=",g.db.sql_value(key_id))
    if keyword != "":
        g.db.sql_where("domain","like",g.db.sql_value("%" + keyword + "%"))

    datas = g.db.sql_query("user_dns_domain",
        fields=["user_dns_domain.*","user_dns_api.key_name","user_dns_api.key_type"],
        limit="LIMIT %d , %d" % ((page_num -1)*page_size,page_size),
        joins=[["user_dns_api","user_dns_domain.key_id = user_dns_api.id "]]
    )
    
    g.db.sql_where("uid","=",g.db.sql_value(g.session["uid"]))
    if keyword != "":
        g.db.sql_where("domain","like",g.db.sql_value("%" + keyword + "%"))
    all_count = g.db.sql_count("user_dns_domain")
    g.db.sql_unlock()
    data = {"page_num":page_num,"page_size":page_size,"total":all_count,"data":datas}
    return api.json_response({"code":0,"msg":"","data":data})

@api.app.route("/api/domain/",methods=['POST'])
def http_request_domain_create():
    domain = g.payload["domain"]
    key_id = g.payload["key_id"]
    g.db.sql_lock()
    g.db.sql_where("domain","=",g.db.sql_value(domain))
    g.db.sql_where("uid","=",g.db.sql_value(g.session["uid"]))
    is_exist = g.db.sql_count("user_dns_domain")
    g.db.sql_unlock()
    if is_exist != 0:
        return api.json_response({"code":403,"msg":"已经存在这个域名了"})
    g.db.sql_lock()
    g.db.sql_where("uid","=",g.db.sql_value(g.session["uid"]))
    g.db.sql_where("id","=",g.db.sql_value(key_id))
    is_exist = g.db.sql_count("user_dns_api")
    g.db.sql_unlock()
    if is_exist == 0:
        return api.json_response({"code":404,"msg":"秘钥不存在或者已经被删除"})
    # 开始准备 新建域名
    new_domain = {
        "key_id":key_id,
        "uid":g.session["uid"],
        "domain":domain
    }
    id = g.db.sql_insert("user_dns_domain",new_domain)
    return api.json_response({"code":0,"msg":"操作成功","data":{"id":id}})

@api.app.route("/api/domain/<id>/",methods=['DELETE'])
def http_request_domain_delete(id):
    g.db.sql_lock()
    g.db.sql_where("uid","=",g.db.sql_value(g.session["uid"]))
    g.db.sql_where("id","=",g.db.sql_value(id))
    is_exist = g.db.sql_count("user_dns_domain")
    g.db.sql_unlock()
    if not is_exist:
        return api.json_response({"code":404,"msg":"域名不存在或已经被删除"})
    else:
        g.db.sql_lock()
        g.db.sql_where("id","=",g.db.sql_value(id))
        g.db.sql_delete("user_dns_domain")
        g.db.sql_unlock()
        return api.json_response({"code":0,"msg":"操作成功","data":None}) 


    
    
