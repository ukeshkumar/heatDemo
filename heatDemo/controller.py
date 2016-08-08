from openStackJobs import openStackJobs
from stackTemplates import stackTemplates


class controller: 
    def __init__(self,):
        self.stackTempl = stackTemplates()
        self.osJobs = openStackJobs()

    def createStack(self, stackName, clientData):
        (template, parameters) = self.stackTempl.getCreateTemplate(clientData)
        return self.osJobs.createStack(stackName, template, parameters)

    def deleteStack(self, stackName): 
        return self.osJobs.deleteStack(stackName)

    def getStackStatus(self, stackName): 
        #import pdb;pdb.set_trace();
        print "in get"
        return self.osJobs.getStackStatus(stackName)

    def getStackOutput(self, stackName): 
        return self.osJobs.getStackOutput(stackName)

    def getOSSetup(self):
        return self.osJobs.getSetup()

    def setOSSetup(self, clientData):
        if 'auth_url' not in clientData or 'user_id' not in clientData or 'password' not in clientData or 'project_id' not in clientData or 'domain_name' not in clientData:
            return "Bad Request", 405
        return self.osJobs.setSetup(clientData['auth_url'], clientData['user_id'], clientData['password'], clientData['project_id'], clientData['domain_name'])

 
