import pytest

from core import plugin_manage

class TestPluginManage:    
    def test_01_loadPlugins(self):
        plugin_manage.load_plugins()
        print(plugin_manage.get_plugins())
        print('test ok')

