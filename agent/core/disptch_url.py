import sys
import os
import importlib 
from core.plugin_manage import get_plugin_meta

def dispatch(serviceName, url, context=None):
    plugins_root = os.path.abspath(os.path.dirname(__file__)+'/../plugins')
    print(serviceName + '  ' + url)
    restapis = get_plugin_meta(serviceName)
    for api in restapis['restapi']:
        if url == api['url']:
            sys.path.append(plugins_root + '/' + serviceName)
            #如果想每次都重新加载模块使用 importlib.reload
            #callit = getattr(importlib.reload(importlib.import_module(api['endpoint'])), api['function']) 
            callit = getattr(importlib.import_module(api['endpoint']), api['function'])            
            content = callit()
            print(content)
    return content

def handle_python():
    pass

def handle_bash():
    pass