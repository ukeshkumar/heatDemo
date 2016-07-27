import ConfigParser
import json

class osDetails:
    def __init__(self):
        try:
            config = ConfigParser.RawConfigParser()
            config.read('os.cfg')
            self.authUrl = config.get('openstack', 'OS_AUTH_URL')
            self.username = config.get('openstack', 'OS_USERNAME')
            self.password = config.get('openstack', 'OS_PASSWORD')
            self.tenantId = config.get('openstack', 'OS_TENANT_ID')
        except:
            self.authUrl = None
            self.username = None
            self.password = None
            self.tenantId = None

    def set(self, authUrl, username, password, tenantId):
        try:
            config = ConfigParser.RawConfigParser()
            config.add_section('openstack')
            config.set('openstack', 'OS_AUTH_URL', authUrl)
            config.set('openstack', 'OS_USERNAME', username) 
            config.set('openstack', 'OS_PASSWORD', password)
            config.set('openstack', 'OS_TENANT_ID', tenantId)
            with open('os.cfg', 'w') as configfile:
                config.write(configfile)
            self.authUrl = authUrl
            self.username = username
            self.password = password
            self.tenantId = tenantId
            return True
        except Exception as e:
            print e
            return False
    
    def get(self):
        return self.__dict__

class openStackJobs:
    def __init__(self):
        self.os = osDetails()
    
    def getSetup(self):
        if self.os.authUrl == None:
            return "OpenStack Credentials not found", 404
        else:
            return json.dumps(self.os.get())

    def setSetup(self, authUrl, username, password, tenantId):
        if self.os.set(authUrl, username, password, tenantId) == True:
            return "OpenStack credentials updated successfully"
        else:
            return "Error while updating OpenStack credentials", 400



if __name__ == '__main__':
    os = osDetails()
    print os.get()
    print os.set(os.authUrl, "new-user", os.password, os.tenantId)
    print os.get()
    
