import pymysql,sys,os
from pymysql.converters import escape_string
import redis
import time,tools 
import threading,json


# FIX:Version 1.0.3.beta
# 修复多线程的情况下,sql_run 互斥性的问题
# 修复sql_run 函数在 执行插入语句时 get_insert_id 忘记解锁导致卡死的BUG
# 修复执行SQL语句前可能MYSQL服务已经开的问题

class database:
    __mysql_config = None
    __redis_config = None 
    __mysql_lock = None
    mysql_client = None
    cursor = None
    redis_client = None
    debug = False
    sql = "" 
    wheres = []
    rabbit_mq_config = {}
    node_id  = None
    node_mode = ""


    def __init__(self,mysql,redis,thread_id=0,log=True) -> None:
        self.log = log
        self.thread_id = thread_id
        self.__mysql_config = mysql 
        self.__redis_config = redis
        self.__mysql_lock = threading.Lock()
        self.__exec_lock = threading.Lock()

        self.wheres = []
   
        self.get_mysql_client(True)
        self.get_redis_client(True)

   
    def sql_lock(self):
        self.__mysql_lock.acquire()
    
    def sql_unlock(self):
        self.__mysql_lock.release()
   
    def get_mysql_client(self,success=False):
        if not self.mysql_client:
            try:
                self.mysql_client = pymysql.connect(host=self.__mysql_config["hostname"], port=self.__mysql_config["port"],user=self.__mysql_config["username"], 
                                                    passwd=self.__mysql_config["password"],  database=self.__mysql_config["database"],autocommit=True)
                if success and self.log:
                    tools.console_log("[INFO]连接MYSQL[" +  self.__mysql_config["hostname"] + ":" + str(self.__mysql_config["port"]) + "-" + str(self.__mysql_config["database"]) + "]成功",self.thread_id)
            except Exception as err:
                tools.console_log("[ERROR]连接MYSQL[" + self.__mysql_config["hostname"] + ":" + str(self.__mysql_config["port"]) + "-" + str(self.__mysql_config["database"]) + "]失败,3s后重试",self.thread_id)
                tools.console_log("[ERROR]" + str(err),self.thread_id)
                tools.console_log("[LOG]3 秒后重试连接MYSQL服务器",self.thread_id)
                time.sleep(3)
                return self.get_mysql_client(True)
        else:
            try:
                self.mysql_client.ping(reconnect=True)
            except Exception as err:
                tools.console_log("[WARNING]与MYSQL 服务器的连接异常中断,重试重新连接到MYSQL 服务器",self.thread_id)
                return self.get_mysql_client(True)
        self.cursor = self.mysql_client.cursor()
        return self.mysql_client


    def get_redis_client(self,success=False):
        if not self.redis_client:
            try:
                self.redis_client = redis.Redis(host=self.__redis_config["host"], port=self.__redis_config["port"], password=self.__redis_config["password"],  db=self.__redis_config["index"],decode_responses=True)
                self.redis_client.ping()
                if success and self.log:
                    tools.console_log("[INFO]连接REDIS[" + self.__redis_config["host"] + ":" + str(self.__redis_config["port"]) + "-" + str(self.__redis_config["index"]) + "]成功",self.thread_id)
            except Exception as err:
                tools.console_log("[ERROR]连接REDIS[" + self.__redis_config["host"] + ":" + str(self.__redis_config["port"]) + "-" + str(self.__redis_config["index"]) + "]失败,3s后重试",self.thread_id)
                tools.console_log("[ERROR]" + str(err),self.thread_id)
                sys.exit()
        else:
            return self.redis_client

        
    def _get_last_id(self):
        self.mysql_client.ping(True)
        cursor = self.mysql_client.cursor()
        sql = "SELECT last_insert_id()"
        cursor.execute(sql)
        id = cursor.fetchall()[0][0]
        cursor.close()
        self.__exec_lock.release()
        return id

    def sql_value(self,value):
        if value == None:
            return "NULL"
        if type(value) == type('str'):
            return "\"" + escape_string(value) + "\""
        if type(value) == type(1):
            return str(value)
        if type(value) == type(1.01):
            return str(value)
        # 更新对 true / false 类型的判断
        if type(value) == type(True):
            value = "true" if value else "false"
            return value
        
    def sql_like(self,value):
        value = str(value)
        return "\"%" + escape_string(value) + "%\"" 
    
   

    
    def sql_run(self,sql,args=None,retry=0):
        self.wheres = []
        self.get_mysql_client()
        if self.debug:
            tools.console_log("[SQL]" + sql,self.thread_id)
       
        cursor = self.cursor
        mode = sql.split(" ")[0].lower()
        self.sql = sql
        self.__exec_lock.acquire()
        sql_starttime = time.time() 
        try:

            self.mysql_client.ping(reconnect=True)
            if args:
                affected_rows = cursor.executemany(sql,args)
                tools.console_log("[INFO]批量插入数据成功,共插入" + str(affected_rows) + "条记录")
            else:
                affected_rows = cursor.execute(sql)
            status = True
            cursor.close()

        except Exception as err:
            tools.console_log("[ERROR]SQL ERROR:" + sql,self.thread_id)
            tools.console_log("[ERROR]" + str(err),self.thread_id)
            cursor.close()
            status = False
        sql_usingtime = int(( time.time() - sql_starttime) * 1000)
        
        tools.write_append( "sql.log","[%d ms]%s" % (sql_usingtime,sql))
    
        if status:
            if mode == "insert":
                # 请求 _get_last_id 会自动解锁
                results = self._get_last_id()
            else:
                if mode == "select":
                    results = []
                    rows = cursor.fetchall()
                    if len(rows) == 0:
                        self.__exec_lock.release()
                        return []
                    result_fields = [i[0] for i in cursor.description]
                    results = []
                    for row in rows:
                        result = {}
                        index = 0
                        for field in result_fields:
                            result[field] = row[index]
                            index = index + 1
                        results.append(result)
                if mode == "update" or mode == "delete":
                    results = affected_rows
                self.__exec_lock.release()
            return results
        else:
            self.__exec_lock.release()
            return False
        

    def sql_exist(self,table,joins=[]):
        count = self.sql_count(table,joins)
        if count == 0:
            return False
        else:
            return True
        
    def sql_count(self,table,joins=[]):
        data = self.sql_query(table,["COUNT(*)"],joins)
        return data[0]["COUNT(*)"]


    def sql_query(self,table,fields=["*"],joins=[],limit="",order=""):
        sql_fields = ""
        sql_joins = "" 
        sql_where = ""

        for field in fields:
            if sql_fields != "":
                sql_fields = sql_fields + " , "
            sql_fields = sql_fields + field
        for join in joins:
            if sql_joins != "":
                sql_joins = sql_joins + " "
            sql_joins = sql_joins + "JOIN `%s` ON %s" % (join[0],join[1])
        for where in self.wheres:
            if sql_where != "" :
                sql_where = sql_where + " " + where[3] + " "
            if '.' in where[0]:
                sql_where = sql_where + " %s %s %s" % (where[0],where[1],where[2])
            else:
                sql_where = sql_where + " `%s` %s %s" % (where[0],where[1],where[2])
        if sql_where != "":
            sql_where = "WHERE " + sql_where
        sql = "SELECT %s FROM `%s` %s %s %s %s" % (sql_fields,table,sql_joins,sql_where,order,limit)

        return self.sql_run(sql)
        
    
    def sql_where(self,field,condition,value,conn='AND'):
        where = [field,condition,value,conn]
        self.wheres.append(where)
    
    def sql_delete(self,table):
        sql_where = ""
        for where in self.wheres:
            if sql_where != "" :
                sql_where = sql_where + " " + where[3] + " "
            if '.' in where[0]:
                sql_where = sql_where + " %s %s %s" % (where[0],where[1],where[2])
            else:
                sql_where = sql_where + " `%s` %s %s" % (where[0],where[1],where[2])
        if sql_where != "":
            sql_where = "WHERE " + sql_where
        sql = "DELETE FROM `%s` %s" % (table,sql_where)
        return self.sql_run(sql)

    
    def sql_update(self,table,updates):
        sql_where = ""
        for where in self.wheres:
            if sql_where != "" :
                sql_where = sql_where + " " + where[3] + " "
            if '.' in where[0]:
                sql_where = sql_where + " %s %s %s" % (where[0],where[1],where[2])
            else:
                sql_where = sql_where + " `%s` %s %s" % (where[0],where[1],where[2])
        if sql_where != "":
            sql_where = "WHERE " + sql_where
        if "update_time" not in updates.keys():
            updates["update_time"] = int(time.time())
        sql_update = ""
        for key in updates.keys():
            if sql_update != "":
                sql_update = sql_update + " , "
            sql_update = sql_update + "`%s` = %s" % (key,self.sql_value(updates[key]))
        sql = "UPDATE `%s` SET %s %s" % (table,sql_update,sql_where)
        return self.sql_run(sql)

    def sql_insert(self,table,inserts):
        datas = []
        if type(inserts) != type([]):
            datas.append(inserts)
        else:
            datas = inserts
        # 单数据执行
        if len(datas) == 1:
            if type(inserts) == type([]):
                inserts = inserts[0]
            sql_keys = ""
            sql_values = ""
            if "create_time" not in inserts.keys():
                inserts["create_time"] = int(time.time())
            for key in inserts.keys():
                if sql_keys != "":
                    sql_keys = sql_keys + ","
                    sql_values = sql_values + ","
                sql_keys = sql_keys + "`"+  key + "`" 
                sql_values = sql_values + self.sql_value(inserts[key])
            sql =  "INSERT INTO `%s` (%s) VALUES (%s)\n" % (table,sql_keys,sql_values)
            return self.sql_run(sql)
        else:
            sql = ""
            sql_keys = ""
            sql_values = ""
            values = []
            for data in datas:
                value = []
                if "create_time" not in data.keys():
                    data["create_time"] = int(time.time())
                for key in data.keys():
                    if not sql:
                        if sql_keys != "":
                            sql_keys = sql_keys + ","
                            sql_values = sql_values + ","
                        sql_keys = sql_keys + "`"+  key + "`" 
                        sql_values = sql_values + "%s"
                    value.append(data[key])
                sql = "INSERT INTO `%s` (%s) VALUES (%s)"  % (table,sql_keys,sql_values)
                values.append(value)
            return self.sql_run(sql,values)
        
    def cache_delete(self,key):
        self.get_redis_client().delete(key)
        
    def cache_get_value(self,key):
        value = self.get_redis_client().get(key)
        if tools.is_json(value):
            return json.loads(value)
        return value
    
    def cache_set_value(self,key,value,ttl=-1):
        if tools.is_object(value):
            value = json.dumps(value,ensure_ascii=True)
        if ttl != -1:
            self.get_redis_client().set(key,value,ttl)
        else:
            self.get_redis_client().set(key,value)

    def cache_delete(self,key):
        self.get_redis_client().delete(key)
    
    def cache_has(self,key):
        enable_ignore_cache = False
        if "enable_ignore_cache" in os.environ.keys():
            if tools.is_true(os.environ["enable_ignore_cache"]):
                enable_ignore_cache = True
        if enable_ignore_cache:
            return False
        if self.get_redis_client().exists(key):
            return True
        else:
            return False
        
    def cache_ttl(self,key,ttl):
        self.get_redis_client().expire(key,ttl)
        
    def cache_keys(self,key):
        results  = self.get_redis_client().keys(key)
        return results
        

