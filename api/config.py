import api
from flask import g


@api.app.route("/api/config/",methods=['GET'])
def http_request_config_query():
    page_num = int(g.params["page_num"]) if "page_num" in g.params.keys() else 1
    page_size = int(g.params["page_size"]) if "page_size" in g.params.keys() else 10
    g.db.sql_lock()
    datas = g.db.sql_query("sys_config",limit="LIMIT %d , %d" % ((page_num -1)*page_size,page_size),order="ORDER BY id");
    all_count = g.db.sql_count("sys_config")
    g.db.sql_unlock()
    data = {"page_num":page_num,"page_size":page_size,"total":all_count,"data":datas}
    return api.json_response({"code":0,"msg":"","data":data})

@api.app.route("/api/config/<item_name>/",methods=['GET'])
def http_request_config_detail(item_name):
    g.db.sql_lock()
    g.db.sql_where("item_name","=",g.db.sql_value(item_name))
    config = g.db.sql_query("sys_config")
    g.db.sql_unlock()
    if len(config) > 0:
        data = config[0]
        return api.json_response({"code":0,"msg":"","data":data})
    return api.json_response({"code":404,"msg":"配置项不存在!","data":{"item_name":item_name}})

@api.app.route("/api/config/",methods=['POST'])
def http_request_config_create():
    item_name = g.payload["item_name"]
    item_value = g.payload["item_value"]
    desc = g.payload["desc"] if "desc" in g.payload.keys() else ""
    g.db.sql_lock()
    g.db.sql_where("item_name","=",g.db.sql_value(item_name))
    is_exist = g.db.sql_count("sys_config")
    g.db.sql_unlock()
    if is_exist:
        return api.json_response({"code":403,"msg":"该配置项已经存在"})
    else:
        new_config = {
            "item_name":item_name,
            "item_value":item_value
        }
        g.db.sql_lock()
        id = g.db.sql_insert("sys_config",new_config)
        g.db.sql_unlock()
        return api.json_response({"code":0,"msg":"操作成功","data":{"id":id}})
        
# 批量更新配置
@api.app.route("/api/config/",methods=['PUT'])
def http_request_config_update_list():
    configs = g.payload["configs"]
    response = []
    success = 0
    for index in range(0,len(configs)):
        config = configs[index]
        status = True
        if "item_name" in config.keys():
            g.db.sql_lock()
            g.db.sql_where("item_name","=",g.db.sql_value(config["item_name"]))
            g.db.sql_where("id","!=",config['id'])
            is_exist = g.db.sql_count("sys_config")
            g.db.sql_unlock()
            if is_exist:
                response.append({"input":config,"response":{"status":"error","msg":"已经存在相同名称的配置项目"}})
                status = False
        if status:
            update = {}
            fields = ["item_name","item_value","desc"]
            for field in fields:
                if field in config.keys():
                    update[field] = config[field]
            g.db.sql_lock()
            g.db.sql_where("id","=",g.db.sql_value(config['id']))
            g.db.sql_update("sys_config",update)
            g.db.sql_unlock()
            response.append({"input":config,"response":{"status":"success","msg":"操作成功"}})
            success = success + 1
    return api.json_response({"code":0,"msg":"操作成功","data":{"total":len(configs),"success":success,"error":len(configs)-success,"detail":response}})
    


@api.app.route("/api/config/<id>",methods=['DELETE'])
def http_request_config_delete(id):
    g.db.sql_lock()
    g.db.sql_where("id","=",g.db.sql_value(id))
    g.db.sql_unlock()
    is_exist = g.db.sql_count("sys_config")
    if not is_exist:
        return api.json_response({"code":404,"msg":"配置项不存在或者已经被删除"})
    else:
        g.db.sql_lock()
        g.db.sql_where("id","=",g.db.sql_value(id))
        g.db.sql_delete("sys_config")
        g.db.sql_unlock()
        return api.json_response({"code":0,"msg":"操作成功","data":None})


@api.app.route("/api/config/<id>",methods=['POST'])
def http_request_config_update(id):
    if "item_name" in g.payload.keys():
        g.db.sql_lock()
        g.db.sql_where("item_name","=",g.db.sql_value(g.payload["item_name"]))
        g.db.sql_where("id","!=",id)
        is_exist = g.db.sql_count("sys_config")
        g.db.sql_unlock()
        if is_exist:
            return api.json_response({"code":403,"msg":"已经存在相同名称的配置项目"})
    update = {}
    fields = ["item_name","item_value","desc"]
    for field in fields:
        if field in g.payload.keys():
            update[field] = g.payload[field]
    g.db.sql_lock()
    g.db.sql_where("id","=",g.db.sql_value(id))
    g.db.sql_update("sys_config",update)
    g.db.sql_unlock()
    return api.json_response({"code":0,"msg":"","data":None})