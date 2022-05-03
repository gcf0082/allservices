import os
import json
from os import path

allPlugins = {}

def load_plugins():
    _load_meta_file()

def get_plugins():
    return allPlugins

def get_plugin_meta(pluginName):
    return allPlugins[pluginName]

def _load_meta_file():
    plugin_root = path.dirname(__file__) + '/../plugins'
    for dirname in os.listdir(plugin_root):
        plugin = {}
        f = open(plugin_root + '/' + dirname + '/' + 'meta.json', 'r')
        metaJson = json.load(f)
        allPlugins[dirname] = metaJson
