from gevent import pywsgi
from datetime import datetime
import sys 
# 新增 获取proxy_client_address的方法
def proxy_client_address(self):
    proxy_headers = ['HTTP_X_REAL_IP','HTTP_X_FORWARDED_FOR','HTTP_REMOTE_HOST']
    for proxy_header in proxy_headers:
        if proxy_header in self.environ.keys():
            return self.environ[proxy_header]
    return None
    
pywsgi.WSGIHandler.proxy_client_address = proxy_client_address

# 重写 /gevent/pywsgi.py WSGIHandler/format_request
# version:24.2.1 code: 1018
def format_request(self):
    now = datetime.now().replace(microsecond=0)
    length = self.response_length or '-'
    if self.time_finish:
        delta = '%.6f' % (self.time_finish - self.time_start)
    else:
        delta = '-'
    client_address = self.client_address[0] if isinstance(self.client_address, tuple) else self.client_address
    proxy_client_address = self.proxy_client_address()
    if proxy_client_address:
        client_address = proxy_client_address
    request_log =  '%s - - [%s] "%s" %s %s %s' % (
        client_address or '-',
        now,
        self.requestline or '',
        (self._orig_status or self.status or '000').split()[0],
        length,
        delta)
    print(request_log,flush=True)
    sys.stdout.flush()
    return request_log
pywsgi.WSGIHandler.format_request = format_request

