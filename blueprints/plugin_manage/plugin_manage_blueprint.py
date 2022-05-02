import os
import sys
import json
from flask import Blueprint,jsonify
from core import disptch_url



plugin_manage_blueprint = Blueprint('plugin_manage_blueprint', __name__)

@plugin_manage_blueprint.route('/service/<path:url>')
def service(url):
    service_name = url.split('/')[0]
    pos = url.find('/')
    interal_url = url[pos:]
    result = disptch_url.dispatch(service_name, interal_url)
    return result