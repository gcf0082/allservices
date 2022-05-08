import sys
import os
from core.plugin_manage import get_plugin_meta

def dispatch(serviceName, url, context=None):
    plugins_root = os.path.abspath(os.path.dirname(__file__)+'/../plugins')
    print(serviceName + '  ' + url)
    restapis = get_plugin_meta(serviceName)
    for api in restapis['restapi']:
        if url == api['url']:
            sys.path.append(plugins_root + '/' + serviceName)
            callit = getattr(__import__(api['endpoint']), api['function'])
            content = callit()
            print(content)
    return content

def handle_python():
    pass

def handle_bash():
    pass