import sys
import os
import importlib 
import asyncio
from core.plugin_manage import get_plugin_meta

async def test():
    await asyncio.sleep(10)
    print('======')

def dispatch(plugin_name, url, context=None):
    #yield from test()
    plugins_root = os.path.abspath(os.path.dirname(__file__)+'/../plugins')
    print(plugin_name + '  ' + url)
    restapis = get_plugin_meta(plugin_name)
    for api in restapis['restapi']:
        if url == api['url']:
            sys.path.append(plugins_root + '/' + plugin_name)
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