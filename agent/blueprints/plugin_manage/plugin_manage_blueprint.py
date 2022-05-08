import json
import os
import sys

from core import disptch_url
from flask import Blueprint, jsonify, request

plugin_manage_blueprint = Blueprint('plugin_manage_blueprint', __name__)

@plugin_manage_blueprint.route('/service/<path:url>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def service(url):
    service_name = url.split('/')[0]
    pos = url.find('/')
    interal_url = url[pos:]
    print(request.data)
    print(request.headers)
    result = disptch_url.dispatch(service_name, interal_url)
    return jsonify({
        "status":0,
        "msg": "成功",
        "data":{
            'result':result
        }
    })    

