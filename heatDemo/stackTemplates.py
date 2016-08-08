import yaml
import os

class stackTemplates:
    def __init__(self): 
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

    def getCreateTemplate(self,clientData): 
        parameters={}
        para_list=['name', 'image', 'type', 'netname', 'key'] 
        for key_name in para_list: 
            if key_name in clientData: 
                parameters[key_name]=clientData[key_name]
        template=yaml.load(open(self.dir_path + '/things/template.yaml'))
        return template,parameters 

if __name__ == "__main__" : 
    
    obj=stackTemplates()
    s1=obj.getCreateTemplate({'name': 'my_int', 'key': 'pem_key', 'type' : 'instance_type'}) 
    print s1
        

 
    

