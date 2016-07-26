from openStackJobs import openStackJobs
from stackTemplates import stackTemplates
 


class controller: 
    def __init__(self,):
        self.stackTempl = stackTemplates()
        self.osJobs = openStackJobs()

    def createStack(self, stackName, **kwargs):
        (template, parameters) = self.stackTempl.getCreateTemplate(kwargs)
        return self.osJobs.createStack(stackName, template, parameters)

    def deleteStack(self, stackName): 
        return self.osJobs.deleteStack(stackName)

    def getStackStatus(self, stackName): 
        return self.osJobs.geetStackStatus(stackName)

    def getStackOutput(self, stackName): 
        return self.osJobs.getStackOutput(stackName)

    def getOSSetup(self):
        return self.osJobs.getSetup()

    def setOSSetup(self, **kwArgs):
        return self.osJobs.setSetup(kwArgs)

 
