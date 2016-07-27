#Heat demo
#!/usr/bin/python

from flask import Flask, request

class clientInterface:
    def __init__(self, ctrObj):
        self.app = Flask(__name__)
        self.controller = ctrObj
        self.app.add_url_rule('/setup', None, self.setup, methods=['GET', 'POST'])
        self.app.add_url_rule('/stack/<name>', None, self.stack, methods=['GET', 'POST', 'DELETE'])

    def setup(self):
        if request.method == 'GET':
            return "GET setup details : ", 302
        elif request.method == 'POST':
            return "setup details updated : " + request.data

    def stack(self, name=None):
        if request.method == 'GET':
            ret = self.controller.createStack(name)
            return "GET Stack details : " + name
        elif request.method == 'POST' and request.is_json:
            clientData=request.json
            clientData.setdefault('name', name)
            print clientData
            return request.data
            #return "stack created : " + name
        elif request.method == 'DELETE':
            return "stack deleted : " + name
        else: 
            return "Error: operation not supported check ur arguments "

    def runApp(self):
        self.app.run()
    

if __name__ == "__main__":
    ci = clientInterface()
    ci.runApp()

