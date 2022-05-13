#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask, request, jsonify
import requests

app = Flask(__name__,
            static_url_path='',
            static_folder='static')
            
@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/getdata')
def getdata():
    return jsonify({
        "status":0,
        "msg":"成功",
         "data": {
          "options": [
            {
              "label": "Project1222",
              "value": 1,
              "children": [
                {
                  "label": "agent1",
                  "value": 2
                },
                {
                  "label": "agent5",
                  "value": 3
                }
              ]
            },
            {
              "label": "Project2",
              "value": 4,
              "children": [
                {
                  "label": "agent2",
                  "value": 5
                }
              ]
            }
          ]
        }

    })

@app.route('/ui/<path:url>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def test(url):
    newParams = request.args.copy()
    rsp = requests.request(method=request.method, 
    url='http://127.0.0.1:3000/rest/service/'+url,
    params=newParams,
    data=request.data)
    print(rsp.json())    
    return jsonify({
        "status":0,
        "msg": "成功",
        "data":{
            "task_id":"task_id",
            "result":rsp.json()['data']['result']
        }
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2000, debug=True)
