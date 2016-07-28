#Heat demo
#!/usr/bin/python

from flask import Flask, request

class clientInterface:
    def __init__(self, ctrObj):
        self.app = Flask(__name__)
        self.controller = ctrObj
        self.app.add_url_rule('/setup', None, self.setup, methods=['GET', 'POST'])
        self.app.add_url_rule('/stack/<name>', None, self.stack, methods=['GET', 'POST', 'DELETE'])
        self.app.add_url_rule('/stack/<name>/output', None, self.stackOutput, methods=['GET'])

    def setup(self):
        if request.method == 'GET':
            return self.controller.getOSSetup()
        elif request.method == 'POST' and request.is_json:
            return self.controller.setOSSetup(request.json)
        else: 
            return "Error: Operation Not Supported", 405

    def stack(self, name=None):
        if request.method == 'GET':
            return self.controller.getStackStatus(name)
        elif request.method == 'POST' and request.is_json:
            return self.controller.createStack(name, request.json)
        elif request.method == 'DELETE':
            return self.controller.deleteStack(name)
        else: 
            return "Error: Operation Not Supported", 405

    def stackOutput(self, name=None):
        if request.method == 'GET':
            return self.controller.getStackOutput(name)

    def runApp(self):
        self.app.run()
    

if __name__ == "__main__":
    ci = clientInterface()
    ci.runApp()

