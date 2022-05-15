from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import uuid
import requests
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_pyfile("master.cfg")
socketio = SocketIO(app)
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
    id = db.Column(db.String(64), primary_key=True)
    service_id = db.Column(db.Integer)
    agent_id = db.Column(db.Integer)
    status = db.Column(db.String(64))

class Work(db.Model):    
    id = db.Column(db.String(64), primary_key=True)
    task_id = db.Column(db.Integer)
    status = db.Column(db.String(64))
    result = db.Column(db.String(1024))

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
    project_name = request.json['project_name']
    project = Project.query.filter(Project.name==project_name).first()
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

@app.route('/rest/service/<path:url>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def service(url):
    project_name = request.args.get('project_name')
    agent_names = request.args.get('agent_names').split(',')
    project = Project.query.filter(Project.name==project_name).first()
    agents = Agent.query.filter(Project.id == project.id).all()
    agents_handled = []
    task_id = str(uuid.uuid4())
    for agent in agents:
        if agent.name in agent_names:
            agents_handled.append(agent.name)
            task = Task(id=task_id, agent_id=agent.id)
            db.session.add(task)
            work = Work(id=str(uuid.uuid4()), task_id=task_id, status="created")
            db.session.add(work)
            db.session.commit()
            newHeaders = request.headers
            #newHeaders.pop('Content-Length')
            #newHeaders.pop('Host')
            newParams = request.args.copy()
            newParams.pop('project_name')
            newParams.pop('agent_names')
            newParams.add('work_id', work.id)
            print(request.data)
            print(request.headers)
            rsp = requests.request(method=request.method, 
            url='http://' + agent.ip + ':' + str(agent.port) +'/service/'+url,
            params=newParams,
            data=request.data)
            print(rsp.json())
    
    
    return jsonify({
        "status":0,
        "msg": "成功",
        "data":{
            "task_id":task_id,
            "result":rsp.json()['data']['result']
        }
    })

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("resize", namespace="/master_ui")
def resize(data):
    socketio.emit("resize", data, namespace="/master_agent")

@socketio.on("pty-input", namespace="/master_ui")
def pty_input(data):
    socketio.emit("pty-input", data, namespace="/master_agent")

@socketio.on("pty-output", namespace="/master_agent")
def pty_output(data):
    socketio.emit("pty-output", data, namespace="/master_ui")    

@socketio.on("connect", namespace="/master_ui")
def connect_ui():
    app.logger.info("new ui client connected")    


@socketio.on("connect", namespace="/master_agent")
def connect_agent():
    app.logger.info("new agent client connected")       

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=3000, debug=True)
    socketio.run(app, host='0.0.0.0', port=3000, debug=True)