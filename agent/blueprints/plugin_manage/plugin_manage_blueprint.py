import json
import os
import sys

from core import disptch_url
from flask import Blueprint, jsonify, request

plugin_manage_blueprint = Blueprint('plugin_manage_blueprint', __name__)

@plugin_manage_blueprint.route('/service/<path:url>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def service(url):
    plugin_name = url.split('/')[0]
    pos = url.find('/')
    interal_url = url[pos:]
    print(request.data)
    print(request.args)
    #todo  内部分发的时候识别需要同步执行还是异步执行，这样外层的master就可以都按同步来操作了
    result = disptch_url.dispatch(plugin_name, interal_url) 
    return jsonify({
        "status":0,
        "msg": "成功",
        "data":{
            'result':result
        }
    })    

