import sys
import os
import importlib 
import asyncio
import threading
import requests
from core.plugin_manage import get_plugin_meta

def set_work_result(work_id, result):
    requests.post(url='http://127.0.0.1:3000/api/webhook/result', params={'work_id':work_id}, json=result)

def get_work_result(work_id):
    rsp = requests.get(url='http://127.0.0.1:3000/rest/work/result', params={'work_id':work_id})
    return rsp.json()['data']['result']

def runService(callit, work_id):
    content = callit()    
    print(content)
    set_work_result(work_id, content)
    print('======' + work_id)

def dispatch(plugin_name, url, work_id, context=None):
    #yield from test()
    plugins_root = os.path.abspath(os.path.dirname(__file__)+'/../plugins')
    print(plugin_name + '  ' + url)
    restapis = get_plugin_meta(plugin_name)
    result = 'ok'
    for api in restapis['restapi']:
        if url == api['url']:
            sys.path.append(plugins_root + '/' + plugin_name)
            #如果想每次都重新加载模块使用 importlib.reload
            #callit = getattr(importlib.reload(importlib.import_module(api['endpoint'])), api['function']) 
            callit = getattr(importlib.import_module(api['endpoint']), api['function']) 
            t = threading.Thread(target=runService, args=(callit,work_id,), name='run service')   
            t.start()
            t.join(2)
            #如果线程未结束暂时无法获取结果信息，只要结束了才有结果信息
            if t.is_alive():
                pass
            else:
                result = get_work_result(work_id)
    return result

def handle_python():
    pass

def handle_bash():
    pass