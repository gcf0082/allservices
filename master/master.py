from unicodedata import name
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, primary_key=False, index = True)

    
class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, primary_key=False, index = True)
    ip = db.Column(db.String(128))
    port = db.Column(db.Integer)

class Project_Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)  #这个主键没有实际
    project_id = db.Column(db.Integer)
    agent_id = db.Column(db.Integer)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer)
    url = db.Column(db.String(256))   
    method = db.Column(db.String(16))
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer)
    service_url = db.Column(db.String(256)) #每个agent的rest接口代表一个服务
    service_method = db.Column(db.String(16)) #http方法GET，POST，PUT等
    result_type = db.Column(db.String(128))  #结果的类型，如果任务的结果内容比较多，这里可以是结果的文件路径
    result = db.Column(db.String(1024))  #任务执行的结果

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)