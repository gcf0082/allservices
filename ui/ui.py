#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask,jsonify

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
              "label": "Project1",
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2000, debug=True)
