import ConfigParser
import requests
import json
import logging
import sys
import string
import os 

"""
    Class to handle OpenStack Credentials
"""
class osDetails:
    def __init__(self):
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            config = ConfigParser.RawConfigParser()
            config.read(dir_path + '/things/os.cfg')
            self.auth_url = config.get('openstack', 'auth_url')
            self.password = config.get('openstack', 'password')
            self.domain_name = config.get('openstack', 'domain_name')
            self.user_id = config.get('openstack', 'user_id')
            self.project_id = config.get('openstack', 'project_id')
            
        except:
            self.auth_url = None
            self.password = None
            self.domain_name = None
            self.user_id = None
            self.project_id = None

    def set(self, auth_url, userid, password, projectid, domainname):
        try:
            config = ConfigParser.RawConfigParser()
            config.add_section('openstack')
            config.set('openstack', 'auth_url', auth_url)
            config.set('openstack', 'userid', userid)
            config.set('openstack', 'password', password)
            config.set('openstack', 'domain_name', domainname)
            config.set('openstack', 'project_id', projectid)
            dir_path = os.path.dirname(os.path.realpath(__file__))
            with open(dir_path + '/things/os.cfg', 'w') as configfile:
                config.write(configfile)
            self.auth_url = auth_url
            self.user_id = userid
            self.password = password
            self.domain_name = domainname
            self.project_id = projectid
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
class openStackJobs:

    def __init__(self):
        self.os = osDetails()
        self.heat_url = ""
        self.token = ""

    def getSetup(self):
        if self.os.auth_url == None:
            return "OpenStack Credentials not found", 404
        else:
            return json.dumps(self.os.get())

    def setSetup(self, authurl, userid, password, projectid, domainname):
        if self.os.set(authurl, userid, password, projectid, domainname) == True:
            return "OpenStack credentials updated successfully"
        else:
            return "Error while updating OpenStack credentials", 400

    def get_user_token(self):
        """
        Gets a keystone usertoken using the credentials provided by user
        """
        url =  self.os.auth_url + '/auth/tokens'
#        url  =  'http://172.27.3.191:5000/v3/auth/tokens' 
        #import pdb;pdb.set_trace() 
        creds = {
            "auth": {
                "identity": {
                "methods": [
                "password"
                    ],
                    "password": {
                    "user": {
                        "id": self.os.user_id,
                        "domain": {
                            "id": self.os.domain_name
                                  },
                        "password": self.os.password
                            }
                                }
                           },
                "scope": {
                    "project": {
                        "id": self.os.project_id
                               }
                         }
                   }
               }

        print creds
        try:
            headers = {}
            headers["Content-type"] = "application/json"
            resp=requests.post(url, data=json.dumps(creds), headers=headers)
            if resp.status_code not in [200, 201]:
                return False, ("Can't get token", resp.status_code)
            respData = resp.json()
        except:
            return False, (sys.exc_info()[1], 500)

        # to get token
        if resp and resp.headers.get('X-Subject-Token'):
            self.token = resp.headers.get('X-Subject-Token')

        # get heat_url
        print resp
        if respData.get('token').get('catalog'):
            '''
            for endPoint in resp.get('serviceCatalog'):
                if endPoint.get('type') == 'orchestration' and \
                      type(endPoint.get('endpoints')) == list and \
                      len(endPoint['endpoints']) > 0:
                    self.heat_url = endPoint['endpoints'][0].get('publicURL')
            '''
#            print respData['token']['catalog'][]
            self.heat_url = "http://172.27.3.191:8004/v1/cff654e1722248b695fb921ccd1d72aa" 
#            self.heat_url = respData['token']['catalog'][5]['endpoints']['url']

        if not self.token:
            return False, ("Can't get token", 500)
        if not self.heat_url:
            return False, ("Can't get heat public url", 503)
        return (True,)

    def createStack(self, stack_name, template, parameters):
        '''
	Create stack using the Heat template 
	'''
        ret = self.get_user_token()
        if not ret[0]:
            return ret[1]

        url = self.heat_url + '/stacks'
        headers = {}
        headers["X-Auth-Token"] = self.token

        base_par = '{"files": {}, "disable_rollback": true, "stack_name": "' + stack_name + '", '
        process_data = base_par + '"parameters": ' + str(parameters) + ', "template": ' + str(template) + ' }'

        # replaces single quote to double quote, as json expects
        process_data = string.replace(process_data, "'", '"')
        data_formed=json.dumps(process_data)
        data=json.loads(data_formed)
        resp = requests.post(
                url, headers=headers, data=data)

        print data
        print resp.status_code
        print resp.json()
        if resp.status_code == 201:
            return "Stack Creating"
        else:
            return ("Error: while Creating the stack", resp.status_code)
 
		
    def deleteStack(self, stack_name):
        '''
	Delete the stack based on stack_name
	'''
        stack_id = self.getStackId(stack_name)
        if not stack_id:
            return ("Error: Not able to fetch stack-id", 500)

        ret = self.get_user_token()
        if not ret[0]:
            return ret[1]

        url = self.heat_url + '/stacks/' + stack_name + "/" + stack_id 
        headers = {}
        headers["X-Auth-Token"] = self.token
        resp = requests.delete(
                url, headers=headers)

        print resp.status_code
        if resp.status_code == 204:
            return "Stack Deleted"
        else:
            return ("Error: while Deleting the stack", resp.status_code)


    def getStackStatus(self, stack_name):
        '''
	Get stack Status based on stack name
	'''
        ret = self.get_user_token()
        if not ret[0]:
            return ret[1]

	url = self.heat_url + '/stacks/' + stack_name
        headers = {}
        headers["X-Auth-Token"] = self.token
	resp = requests.get(
		url, headers=headers)

        if resp.status_code in [200, 302] and resp.json().get('stack'):
            return resp.json()['stack'].get('stack_status')
        else:
            return ("Error: while fetching Stack Status", resp.status_code)


    def getStackId(self, stack_name):
        '''
	Get the stack-id of the specific stack-name
	'''
        ret = self.get_user_token()
        if not ret[0]:
            return None

	url = self.heat_url + '/stacks/' + stack_name
        headers = {}
        headers["X-Auth-Token"] = self.token
        resp = requests.get(
                url, headers=headers)

        if resp.status_code in [200, 302] and resp.json().get('stack'):
            return resp.json()['stack'].get('id')
        return None
        

    def getStackOutput(self, stack_name):
        '''
	Get the output of the stack based on stack user
	'''
        stack_id = self.getStackId(stack_name)
        if not stack_id:
            return ("Error: Not able to fetch stack-id", 500)
        
        ret = self.get_user_token()
        if not ret[0]:
            return ret[1]

	url = self.heat_url + '/stacks/' + stack_name + '/' + stack_id + '/outputs'
        headers = {}
        headers["X-Auth-Token"] = self.token
        resp = requests.get(
                url, headers=headers)
        if resp.status_code == 200:
            return str(resp.json())
        else:
            return ("Error: while fetching output", resp.status_code)


if __name__== "__main__":
    obj1=openStackJobs()
    status_resp =obj1.getStackStatus('tssd')
    stack_view=obj1.getStackOutput('tssd') 
    print status_resp
    print stack_view

