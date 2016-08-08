import yaml
import os
import json

class stackTemplates:
    def __init__(self): 
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

    def getCreateTemplate(self,clientData): 
        parameters={}
        para_list=['name', 'image', 'type', 'netname', 'key', 'instance_count'] 
        for key_name in para_list: 
            if key_name in clientData: 
                parameters[key_name]=clientData[key_name]
                print clientData[key_name]
        template=yaml.load(open(self.dir_path + '/things/template.yaml'))
        parameters = json.dumps(parameters)
        return template,parameters 

if __name__ == "__main__" : 
    
    obj=stackTemplates()
    s1=obj.getCreateTemplate({'name': 'my_int', 'key': 'pem_key', 'type' : 'instance_type'}) 
    print s1
        

 
    

