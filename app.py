from flask import Flask
from blueprints.plugin_manage.plugin_manage_blueprint import plugin_manage_blueprint
from core import plugin_manage

app = Flask(__name__)
app.register_blueprint(plugin_manage_blueprint)

if __name__ == "__main__":
    plugin_manage.load_plugins()
    app.run(host='0.0.0.0', port=5000, debug=True)