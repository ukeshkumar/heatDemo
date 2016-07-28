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
        return self.osJobs.geetStackStatus(stackName)

    def getStackOutput(self, stackName): 
        return self.osJobs.getStackOutput(stackName)

    def getOSSetup(self):
        return self.osJobs.getSetup()

    def setOSSetup(self, clientData):
        if 'authUrl' not in clientData or 'username' not in clientData or 'password' not in clientData or 'tenantId' not in clientData or 'tenantName' not in clientData:
            return "Bad Request", 405
        return self.osJobs.setSetup(clientData['authUrl'], clientData['username'], clientData['password'], clientData['tenantName'], clientData['tenantId'])

 
