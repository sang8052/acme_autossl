import os,sys,time,json
import requests
import hashlib,base64,sys,time,uuid
import threading
console_lock = threading.Lock()




def console_log(content,thread_id = 0):
    console_lock.acquire()
    if thread_id != 0:
        thread_text = "{THREAD-%d}" % (thread_id)
    else:
        thread_text = ""
    console = "%s[%s]%s" % (thread_text,format_date(), content)
    color_id = 37
    if str_include(console, '[INFO]') != -1:
        color_id = 32
    if str_include(console, '[WARNING]') != -1:
        color_id = 33
    if str_include(console, '[SQL]') != -1:
        color_id = 34
    if str_include(console, '[REQUEST]') != -1:
        color_id = 34
    if str_include(console, '[DEBUG]') != -1:
        color_id = 35
    if str_include(console, '[ERROR]') != -1:
        color_id = 31
    log = "\033[%dm%s\033[0m" % (color_id, console)
    print(log,flush=True)
    sys.stdout.flush()
    console_lock.release()


def console_print(color_id, console,pid=None):
    console_lock.acquire()
    if pid :
        log_pid = "\033[%dm%s\033[0m" % (35, "{PID:%d}" % (pid))
        log = "\033[%dm%s\033[0m" % (color_id, console)
        log = log_pid + log 
    else:
        log = "\033[%dm%s\033[0m" % (color_id, console)
    print(log,flush=True)
    sys.stdout.flush()
    console_lock.release()


def file_md5(path):
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    

def str_include(str, include):
    try:
        index = str.index(include)
        return index
    except:
        return -1

def format_date(format="%Y-%m-%d %H:%M:%S", times=None):
    if not times: times = int(time.time())
    time_local = time.localtime(times)
    return time.strftime(format, time_local)

def text_md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def text_base64(text):
    return base64.b64encode(text.encode('utf-8'))

def write_file(path,content):
    fp = open(path,"w")
    fp.write(content)
    fp.close()

def read_file(path):
    if not os.path.exists(path):
        return ""
    try:
        fp = open(path,"r",encoding='utf-8')
    except:
        fp = open(path,"r",encoding="gbk")
    content = fp.read()
    fp.close()
    return content

def get_ms_time():
    return int(time.time() * 1000)

def get_uuid():
    return str(uuid.uuid4())

   
def get_redis_client(config,success=False):
    while True:
        try:
            pool = ConnectionPool(
                host=config["host"],
                port=config["port"],
                password=config["password"],
                db=config["index"],
                health_check_interval=10,
                decode_responses=True)
            client = Redis(connection_pool=pool)
            client.ping()
            if success:
                console_log("[INFO]连接Redis[" + config["host"] + ":" + str(config["port"]) + "-" + str(config["index"]) + "]成功")
        except Exception as err:
            console_log("[WARNING]连接Redis[" + config["host"] + ":" + str(config["port"]) + "-" + str(config["index"]) + "]失败,3s后重试")
            print(err)
            time.sleep(3)
            continue
        else:
            return client

def read_json(filename):
    content = read_file(filename)
    try:
        return json.loads(content)
    except Exception as err:
        console_log("[ERROR]读取JSON文件[%s]失败" % (filename))
        return {}



def mkdir_nx(path):
    if not os.path.exists(path):
        os.mkdir(path)


def is_json(text):
    if type(text) != type("str"):
        return False
    if text == "":
        return False
    try:
        json.loads(text)
        return True
    except Exception as err:
        return False
    
def is_object(val):
    if is_list(val):
        return True
    if is_dict(val):
        return True
    return False

def is_list(val):
    return type(val) == type([])

def is_dict(val):
    return type(val) == type({})

def is_int(val):
    return type(val) == type(1)

def is_float(val):
    return type(val) == type(1.0)

def is_str(val):
    return type(val) == type("str")

def is_type(val,val_type):
    return eval("is_%s(val)" % (val_type))
    

def write_append(path,content):
    try:
        fp = open(path,"a",encoding='utf-8')
        fp.write(content + "\r\n")
        fp.close()
    except Exception as err:
        pass


def write_json(path,data):
    text = json.dumps(data,ensure_ascii=False)
    write_file(path,text)
    console_log("[LOG]向文件 %s 写入JSON数据 %d 字节" % (path,len(text)) )



