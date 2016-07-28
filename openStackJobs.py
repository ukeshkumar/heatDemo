
import ConfigParser
import requests
import json
import logging
import sys

"""
    Class to handle OpenStack Credentials
"""
class osDetails:
    def __init__(self):
        try:
            config = ConfigParser.RawConfigParser()
            config.read('os.cfg')
            self.auth_url = config.get('openstack', 'OS_AUTH_URL')
            self.username = config.get('openstack', 'OS_USERNAME')
            self.password = config.get('openstack', 'OS_PASSWORD')
            self.tenantname = config.get('openstack', 'OS_TENANT_NAME')
            self.tenantid = config.get('openstack', 'OS_TENANT_ID')
        except:
            self.auth_url = None
            self.username = None
            self.password = None
            self.tenantname = None
            self.tenantid = None

    def set(self, auth_url, username, password, tenantname, tenantid):
        try:
            config = ConfigParser.RawConfigParser()
            config.add_section('openstack')
            config.set('openstack', 'OS_AUTH_URL', auth_url)
            config.set('openstack', 'OS_USERNAME', username)
            config.set('openstack', 'OS_PASSWORD', password)
            config.set('openstack', 'OS_TENANT_NAME', tenantname)
            config.set('openstack', 'OS_TENANT_ID', tenantid)
            with open('os.cfg', 'w') as configfile:
                config.write(configfile)
            self.auth_url = auth_url
            self.username = username
            self.password = password
            self.tenantname = tenantname
            self.tenantid = tenantid
            return True
        except Exception as e:
            print e
            return False

    def get(self):
        return self.__dict__


'''
		Interacting with Openstack controller
		for Heat orchestration
'''
class OpenStack_Jobs:

    def __init__(self):
        self.os = osDetails()
        self.user_name = 'infinite'
	self.password = 'infics123'
#	self.os_auth_url = 'http://172.27.3.66:5000/v2.0'
#	self.os_username = 'admin'
#	self.os_tenantname = 'admin'
#	self.os_password = 'foobar'
#	self.tenant_id = '3970e34381b64fd5838e5a573835a2fd'

    def getSetup(self):
        if self.os.authUrl == None:
            return "OpenStack Credentials not found", 404
        else:
            return json.dumps(self.os.get())

    def setSetup(self, authUrl, username, password, tenantName, tenantId):
        if self.os.set(authUrl, username, password, tenantName, tenantId) == True:
            return "OpenStack credentials updated successfully"
        else:
            return "Error while updating OpenStack credentials", 400

    def get_user_token(self,user_name, password, tenant_name):
        """
        Gets a keystone usertoken using the credentials provided by user
        """
        url =  'http://172.27.3.66:5000/v2.0' + '/tokens'
        creds = {
            'auth': {
	        'passwordCredentials': {
	        'username': user_name,
	        'password': password
	        },
	        'tenantName': tenant_name
	    }
        }
        
        headers = {}
        headers["Content-type"] = "application/json"
        resp=requests.post(url, data=json.dumps(creds), headers=headers)
        import pdb;pdb.set_trace()
        return resp.json()['access']
    		
    def createStack(self,template_file):
        '''
	Create stack using the Heat template 
	'''
	url = 'http://172.27.3.66:8004/v1/' \
			   + self.os.tenantid + '/stacks/'
	auth_token = self.get_user_token(
		self.os.username, self.os.password, self.os.tenantname)
        if auth_token:
            token = auth_token['token']
            headers["X-Auth-Token"] = token['id']
        base_par = '{"files": {}, "disable_rollback": true,'
        process_data = base_par + str(parameters) + str(template) + '}'
        data_formed=json.dumps(str3)
        data=json.loads(data)
        resp = requests.post(
                url, headers=headers, data=data)
        return resp.json()
 
		
    def deleteStack(self,stack_name):
        '''
	Delete the stack based on stack_name
	'''
	url = 'http://172.27.3.66:8004/v1/' \
			   + self.os.tenantid + '/stacks/' + stack_name
        auth_token = self.get_user_token(
                self.os.username, self.os.password, self.os.tenantname)
        headers = {}
        #headers["Content-type"] = "application/json"
        if auth_token:
            token = auth_token['token']
            headers["X-Auth-Token"] = token['id']
        resp = requests.delete(
                url, headers=headers)
        return resp.json()

		
    def getStackStatus(self,stack_name):
        '''
	Get stack Status based on stack name
	'''
	url = 'http://172.27.3.66:8004/v1/' \
			   + self.os.tenantid + '/stacks/' + stack_name
	auth_token = self.get_user_token(
		self.os.username, self.os.password, self.os.tenantname)
        #headers["Content-type"] = "application/json"
        headers = {}
        if auth_token:
            token = auth_token['token']
            headers["X-Auth-Token"] = token['id']
        import pdb;pdb.set_trace()
	resp = requests.get(
		url, headers=headers)
        return resp.json()['stack']['stack_status']
		
    def getStackOutput(self,stack_name,stack_id,template_file):
        '''
	Get the output of the stack based on stack user
	'''
	url = 'http://172.27.3.66:8004/v1/' \
			   + self.os.tenantid + '/stacks/' + stack_name + '/' + stack_id + '/outputs'
	auth_token = self.get_user_token(
                self.os.username, self.os.password, self.os.tenantname)
        headers = {}
        if auth_token:
            token = auth_token['token']
            headers["X-Auth-Token"] = token['id']
        resp = requests.get(
                url, headers=headers)
        return resp.json()

if __name__== "__main__":
    obj1=OpenStack_Jobs()
    status_resp =obj1.getStackStatus('heat-stack')
    stack_view=obj1.getStackOutput('heat-stack','fdd9a7b6-95e1-453a-bd6d-9ad9e0a18b7c',"abc.yaml") 
    print status_resp
    print stack_view

