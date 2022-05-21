import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
import requests

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

@app.route('/rest/agent', methods= ['GET'])
def get_all_agents():
    project_name = request.args.get('project_name')
    project = Project.query.filter(Project.name==project_name).first()
    agents = Agent.query.filter(Project.id==project.id).all()  
    tmplist = []
    for agent in agents:
        tmplist.append({"name":agent.name, "ip":agent.ip, "port":agent.port, "project_id":agent.project_id})

    return jsonify({
        "status":0,
        "msg": "获取所有agent成功",
        "data":{
            "agents": tmplist
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
    result = []
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
            result.append({"work_id":rsp.json()["data"]["work_id"], "result":rsp.json()["data"]["result"]})
    
    
    return jsonify({
        "status":0,
        "msg": "成功",
        "data":{
            "task_id":task_id,
            "result":result
        }
    })

@app.route('/api/webhook/result', methods=['POST'])
def webhook_set_work_result():
    print('requests.data:')
    print(request.json)
    work_id = request.args.get('work_id')
    Work.query.filter(Work.id == work_id).update({'result':json.dumps(request.json)})
    db.session.commit() 
    return 'ok'    

@app.route('/rest/task/status', methods=['GET'])
def get_task_status():
    return jsonify({
        "status":0,
        "msg": "成功",
        "data":{
            "task_id":'task_id',
            "status":[
                {
                    "work_id":"work_id1",
                    "status":"ok"
                },
                    {
                    "work_id":"work_id2",
                    "status":"failed"
                }
            ]
        }
    })

@app.route('/rest/task/result', methods=['GET'])
def get_task_result():
    return jsonify({
        "status":0,
        "msg": "成功",
        "data":{
            "task_id":'task_id',
            "result":[
                {
                    "work_id":"work_id1",
                    "result":"xxxx",
                    "status":"ok"
                },
                    {
                    "work_id":"work_id2",
                    "result":"yyyyy",
                    "status":"failed"
                }
            ]
        }
    })

@app.route('/rest/work/result', methods=['GET'])
def get_work_result():
    work_id = request.args.get('work_id')
    work = Work.query.filter(Work.id == work_id).first()
    print(work.result)
    return jsonify({
        "status":0,
        "msg": "成功",
        "data":{
            "task_id":'task_id',
            "work_id":'work_id',
            "result":json.loads(work.result)
        }
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)