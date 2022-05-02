from core.plugin_manage import get_plugin_meta

def dispatch(serviceName, url, context=None):
    print(serviceName + '  ' + url)
    print(get_plugin_meta(serviceName))
    return 'ok'

def handle_python():
    pass

def handle_bash():
    pass