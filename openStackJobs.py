
import requests
import json
import logging
import sys
'''
		Interacting with Openstack controller
		for Heat orchestration
'''
class OpenStack_Jobs:

    def __init__(self):
        self.user_name = 'infinite'
	self.password = 'infics123'
	self.os_auth_url = 'http://172.27.3.66:5000/v2.0'
	self.os_username = 'admin'
	self.os_tenantname = 'admin'
	self.os_password = 'foobar'
	self.tenant_id = '3970e34381b64fd5838e5a573835a2fd'

	
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
        return resp.json()['access']
    		
    def createStack(self,template_file):
        '''
	Create stack using the Heat template 
	'''
	url = 'http://172.27.3.66:8004/v1/' \
			   + self.tenant_id + '/stacks/'
	auth_token = self.get_user_token(
		self.os_username, self.os_password, self.os_tenantname)
        
	resp = self.post_request(
		url, auth_token, nova_cacert=False, stream=False)
	return resp.json()['switches']	
		
    def deleteStack(self,stack_name):
        '''
	Delete the stack based on stack_name
	'''
	url = 'http://172.27.3.66:8004/v1/' \
			   + self.tenant_id + '/stacks/' + stack_name
        auth_token = self.get_user_token(
                self.os_username, self.os_password, self.os_tenantname)
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
			   + self.tenant_id + '/stacks/' + stack_name
	auth_token = self.get_user_token(
		self.os_username, self.os_password, self.os_tenantname)
        #headers["Content-type"] = "application/json"
        headers = {}
        if auth_token:
            token = auth_token['token']
            headers["X-Auth-Token"] = token['id']
	resp = requests.get(
		url, headers=headers)
        return resp.json()
		
    def getStackOutput(self,stack_name,stack_id,template_file):
        '''
	Get the output of the stack based on stack user
	'''
	url = 'http://172.27.3.66:8004/v1/' \
			   + self.tenant_id + '/stacks/' + stack_name + '/' + stack_id + '/outputs'
	auth_token = self.get_user_token(
                self.os_username, self.os_password, self.os_tenantname)
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

		
