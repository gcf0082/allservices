from unicodedata import name
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("master.cfg")
db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(128), nullable=False, primary_key=False, index = True)

    
class Agent(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(128), nullable=False, primary_key=False, index = True)
    project_id = db.Column(db.Integer)
    ip = db.Column(db.String(128))
    port = db.Column(db.Integer)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256))   
    method = db.Column(db.String(16))
    result_type = db.Column(db.String(128))   

class Agent_Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer)
    service_id = db.Column(db.Integer)
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer)
    agent_id = db.Column(db.Integer)
    status = db.Column(db.String(64))
    result = db.Column(db.String(1024))  #任务执行的结果

@app.cli.command('init')
@app.route('/rest/initdb', methods= ['POST'])
def init():
    db.drop_all()
    db.create_all()
    return jsonify({
        "status":0,
        "msg": "初始化数据库成功",
        "data":{
        }
    })    

@app.route('/rest/agent/register', methods= ['POST'])
def create_agent():
    name = request.json['name']
    ip = request.json['ip']
    port = request.json['port']
    project = Project.query.filter(Project.name=='test_project2').first()
    agent = Agent(name=name, project_id=project.id, ip=ip, port=port)
    db.session.add(agent)
    db.session.commit()    
    return jsonify({
        "status":0,
        "msg": "注册成功",
        "data":{
            "id":agent.id
        }
    })


@app.route('/rest/project',methods = ['POST'])
def create_project():    
    project = Project(name=request.json['name'])
    db.session.add(project)
    db.session.commit()
    return jsonify({
        "status":0,
        "msg": "创建成功",
        "data":{
            "id":project.id
        }
    })

@app.route('/rest/svc/<path:url>')
def service(url):
    service_name = url.split('/')[0]
    pos = url.find('/')
    interal_url = url[pos:]
    return jsonify({
        "status":0,
        "msg": "成功",
        "data":{
        }
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)