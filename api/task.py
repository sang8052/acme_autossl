
import api
from flask import g,current_app
import tools,os,time

import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import formataddr

import OpenSSL
import OpenSSL.crypto
from OpenSSL.crypto import X509
from dateutil import parser
 
import base64,json,requests,traceback

@api.app.route("/api/task/<id>/",methods=['GET'])
def http_request_tasks_list(id):
    g.db.sql_lock()
    g.db.sql_where("uid","=",g.db.sql_value(g.session["uid"]))
    g.db.sql_where("id","=",g.db.sql_value(id))
    task = g.db.sql_query("sys_task")
    g.db.sql_unlock() 
    if len(task) == 0:
        return api.json_response({"code":404,"msg":"任务不存在或者已经被删除"})
    else:
        task = task[0]
        return api.json_response({"code":0,"msg":"操作成功","data":task})
    
# 回调测试接口   
@api.app.route("/api/task/callback/",methods=["POST"])
def http_request_tasks_callback_sigin():
    b64data = g.payload["b64data"]
    current_timestamp = g.payload["current_timestamp"]
    sign = g.payload["sign"]
    server_timestamp = int(time.time())
    if abs( server_timestamp - int(current_timestamp)) > 3:
        return api.json_response({"code":500,"msg":"签名过期!","data":{"server_timestamp":server_timestamp,"callback_timestamp":callback_timestamp}})
    else:
        # 计算签名 
        callback_sign_token = api.query_system_config("callback_sign_token")
        sign_payload = "Acme_AutoSSL:" + b64data + ":" + callback_sign_token + ":" + str(current_timestamp)
        server_sign = tools.text_md5(sign_payload)
        if server_sign != sign:
            tools.console_log("[DEBUG]Callback SignPayload:" + sign_payload)
            tools.console_log("[DEBUG]Callback Sign:" + server_sign)
            return api.json_response({"code":0,"msg":"签名效验失败!","data":{"sign":sign,"callback_timestamp":callback_timestamp,"b64data":b64data}})
        else:
            # 签名成功
            data = base64.b64decode(b64data.encode()).decode()
            tools.console_log("[INFO]签名效验成功,证书信息:" + data )
            return api.json_response({"code":0,"msg":"操作成功","data":None})
            
        


# 任务执行结束后 shell 脚本自动调用
@api.app.route("/api/task/callback/<cert_id>/",methods=['GET'])
def http_request_tasks_callback(cert_id):
     # 检查域名
    g.db.sql_lock()
    g.db.sql_where("id","=",g.db.sql_value(cert_id))
    cert = g.db.sql_query("user_cert")
    g.db.sql_unlock()
    if len(cert) == 0:
        return api.json_response({"code":404,"msg":"证书不存在"})
    cert = cert[0] 
    
    # 拿到任务信息
    g.db.sql_lock()
    g.db.sql_where("cert_id","=",g.db.sql_value(cert_id))
    task = g.db.sql_query("sys_task")[0]
    g.db.sql_unlock()
    if task["status"] == "running":
        error_log = tools.read_file(api.current_app.work_path + "/tmp/" + task["tmp_uuid"] + "/shell.log")
        ssl_private_key = tools.read_file(api.current_app.work_path + "/tmp/" + task["tmp_uuid"]  + "/private.key")
        ssl_fullchain = tools.read_file(api.current_app.work_path  + "/tmp/" + task["tmp_uuid"] + "/fullchain.pem")
        if ssl_fullchain == "":
            tools.console_log("[WARNING]读取证书文件[%s]出错了" % (api.current_app.work_path  + "/" + task["tmp_uuid"] + "/fullchain.pem"))

            update_task = {
             "status":"error"
            }

            g.db.sql_where("id","=",g.db.sql_value(task["id"]))
            g.db.sql_update("sys_task",update_task)
            if task["reg_path"]:
                os.system("rm -rf %s" % (task["reg_path"]))
            if task["tmp_uuid"]:
                os.system("rm -rf %s/tmp/%s" % (api.current_app.work_path,task["tmp_uuid"]))

        else:
            cert_content: X509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, ssl_fullchain)
            cert_issuer = cert_content.get_issuer()
            cert_subject = cert_content.get_subject()
            extension_count = cert_content.get_extension_count()
            extension_ls = []
            for i in range(extension_count):
                extension = str(cert_content.get_extension(i))
                extension_ls.append(extension)
            _cert_info = {
                "version": cert_content.get_version() + 1,
                "serial_number": hex(cert_content.get_serial_number()),
                "signature_algorithm": cert_content.get_signature_algorithm().decode("UTF-8"),
                "common_name": cert_issuer.commonName,
                "start_time": parser.parse(cert_content.get_notBefore().decode("UTF-8")).strftime('%Y%m%d%H%M%S'),
                "format_start_time": parser.parse(cert_content.get_notBefore().decode("UTF-8")).strftime('%Y-%m-%d %H:%M:%S'),
                "end_time": parser.parse(cert_content.get_notAfter().decode("UTF-8")).strftime('%Y%m%d%H%M%S'),
                "format_end_time": parser.parse(cert_content.get_notAfter().decode("UTF-8")).strftime('%Y-%m-%d %H:%M:%S'),
                "has_expired": cert_content.has_expired(),
                "pubkey": OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, cert_content.get_pubkey()).decode("utf-8"),
                "pubkey_len": cert_content.get_pubkey().bits(),
                "pubkey_type": cert_content.get_pubkey().type(),
                "extension_count": cert_content.get_extension_count(),
                "issuer_info": {},
                "subject_info": {},
                "extension_info": extension_ls,
            }
            for item in cert_issuer.get_components():
                _cert_info["issuer_info"][str(item[0].decode("utf-8"))] = str(item[1].decode("utf-8"))
            for item in cert_subject.get_components():
                _cert_info["subject_info"][str(item[0].decode("utf-8"))] = str(item[1].decode("utf-8"))


            # 更新证书信息
            update_cert = {
                "ssl_private_key":ssl_private_key,
                "ssl_public_key":_cert_info["pubkey"],
                "ssl_fullchain":ssl_fullchain,
                "signature_algorithm":_cert_info["signature_algorithm"],
                "serial_number":_cert_info["serial_number"],
                "reg_time":_cert_info["format_start_time"],
                "expire_time":_cert_info["format_end_time"],
                "common_name":_cert_info["issuer_info"]['C'] + " " + _cert_info["issuer_info"]['O'] +  " " + _cert_info["issuer_info"]['CN']
            }
            g.db.sql_where("id","=",g.db.sql_value(cert_id))
            g.db.sql_update("user_cert",update_cert)

            
            update_task = {
                "status":"success"
            }

            g.db.sql_where("id","=",g.db.sql_value(task["id"]))
            g.db.sql_update("sys_task",update_task)


            if task["reg_path"]:
                os.system("rm -rf %s" % (task["reg_path"]))
            if task["tmp_uuid"]:
                os.system("rm -rf %s/tmp/%s" % (api.current_app.work_path,task["tmp_uuid"]))

        # 发送邮件通知信息
        smtp_server_host = api.query_system_config("smtp_server_host")
        smtp_server_port = int(api.query_system_config("smtp_server_port"))
        smtp_server_ssl  = True if int(api.query_system_config("smtp_server_ssl")) == 1 else False
        smtp_user_username = api.query_system_config("smtp_user_username")
        smtp_user_password = api.query_system_config("smtp_user_password")
        smtp_user_nickname = api.query_system_config("smtp_user_nickname")
      
        mail_cert_title = api.query_system_config("mail_cert_title")
        
        g.db.sql_lock()
        g.db.sql_where("id","=",g.db.sql_value(cert["domain_id"]))
        domain = g.db.sql_query("user_dns_domain")[0]
        g.db.sql_unlock()
        
        g.db.sql_lock()
        g.db.sql_where("id","=",g.db.sql_value(cert["uid"]))
        mail_send_to = g.db.sql_query("sys_user",["mail_address"])[0]["mail_address"]
        g.db.sql_unlock()
        
        reg_domain = cert["prefix"] + "." + domain["domain"]  if cert["prefix"] != "" else domain["domain"]
        if update_task["status"] == "success":
            mail_content = api.query_system_config("mail_cert_template_success")
            data = {
                "current_time":tools.format_date(),
                "cert_create_time":tools.format_date(times=cert["create_time"]),
                "cert_reg_domain":reg_domain,
                "cert_root_domain":domain["domain"],
                "cert_serial_number":update_cert["serial_number"],
                "cert_signature_algorithm":update_cert["signature_algorithm"],
                "cert_common_name":update_cert["common_name"],
                "cert_reg_time":update_cert["reg_time"],
                "cert_expire_time":update_cert["expire_time"],
                "mail_send_to":mail_send_to,
                "current_app_version": current_app.app_version
            }
            
        if update_task["status"] == "error":
            mail_content = api.query_system_config("mail_cert_template_error")
            data = {
                "current_time":tools.format_date(),
                "cert_create_time":tools.format_date(times=cert["create_time"]),
                "cert_reg_domain":reg_domain,
                "cert_root_domain":domain["domain"],
                "mail_send_to":mail_send_to,
                "current_app_version": current_app.app_version
            }
            
        for key in data.keys():
            mail_content = mail_content.replace("{{"+key+"}}",data[key])
        
        message = MIMEMultipart()
        message['From'] = formataddr([smtp_user_nickname,smtp_user_username])
        message['To'] =  Header(mail_send_to)      
        message['Subject'] = Header(mail_cert_title)
        
        # 邮件正文
        message.attach(MIMEText(mail_content,'html','utf-8'));
        file_domain = reg_domain.replace("*","_")
        if update_task["status"] == "success":
            file = MIMEApplication(update_cert["ssl_private_key"])
            file.add_header("content-disposition","attachment",filename=file_domain + "_private.key")
            message.attach(file)
            file = MIMEApplication(update_cert["ssl_fullchain"])
            file.add_header("content-disposition","attachment",filename=file_domain + "_fullchain.pem")
            message.attach(file)
        if update_task["status"] == "error":
            file = MIMEApplication(error_log)
            file.add_header("content-disposition","attachment",filename=file_domain + "_error.log")
            message.attach(file)
        if smtp_server_ssl:
            smtp_server = smtplib.SMTP_SSL(smtp_server_host,smtp_server_port)
        else:
            smtp_server = smtplib.STMP(smtp_server_host,smtp_server_port)
        try:
            smtp_server.login(smtp_user_username, smtp_user_password)  
            smtp_server.sendmail(smtp_user_username, [mail_send_to], message.as_string())
            smtp_server.quit()
            tools.console_log("[INFO]通知邮件发送成功!")
        except Exception as err:
            mail_err = traceback.format_exc()
            tools.console_log("[WARNING]通知邮件发送失败,ERROR:" + mail_err)
            
        # 回调请求 可以通过这个参数自动部署
        if cert["callback_url"] != "":
            g.db.sql_lock()
            g.db.sql_where("id","=",g.db.sql_value(cert_id))
            cert_current = g.db.sql_query("user_cert")[0]
            cert_current["domain"] = domain["domain"]
            g.db.sql_unlock()
            b64data = base64.b64encode(json.dumps(cert_current).encode()).decode()
            callback_sign_token = api.query_system_config("callback_sign_token")
            current_timestamp = int(time.time())
            sign_payload = "Acme_AutoSSL:" + b64data + ":" + callback_sign_token + ":" + str(current_timestamp)
            callback_payload = {"data":b64data,"sign":tools.text_md5(sign_payload),"current_timestamp":current_timestamp}
            try:
                tools.console_log("[LOG]向[%s]发起回调,TaskId:%d,CertId:%d" % (int(task["id"],int(cert_id))))
                user_agent = "Acme_AutoSSL Auto Callback/CertId:" + cert_id + ",TaskId:" + str(task["id"])
                resp = requests.post(cert["callback_url"],data=json.dumps(callback_payload),headers={"User-Agent":user_agent,"content-type":"application/json"},timeout=5)
                tools.console_log("[INFO]回调[%s]成功,Response:" + resp.text)
            except Exception as err:
                callback_err = traceback.format_exc()
                tools.console_log("[WARNING]回调[%s]失败,Error:" + callback_err)
            
   
    return  api.json_response({"code":0,"msg":"操作成功","data":None})


