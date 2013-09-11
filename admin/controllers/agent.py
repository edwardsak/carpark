from admin.controllers.base import BaseHandler
from sharelib.utils import DateTime
from datalayer.models.models import Agent
from datalayer.viewmodels.viewmodels import AgentViewModel
from datalayer.appservice.admin.agent import AgentAppService

import os
import jinja2
import json

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

class Create(BaseHandler):
    def get(self):
        # validate admin is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        
        template_values = {
                           'title': 'Create Agent',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user
                           }
        
        template = JINJA_ENVIRONMENT.get_template('/agent/create.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        json_values = {}
        
        try:
            # get post data
            name = self.request.get("name")
            code = self.request.get("code")
            pwd = self.request.get("pwd")
            address = self.request.get("address")
            tel = self.request.get("tel")
            hp = self.request.get("hp")
            email = self.request.get("email")
            bal_amt = self.request.get("balAmt")
    
            #save data to view model class
            vm = AgentViewModel()
            vm.code = code
            vm.name = name
            vm.pwd = pwd
            vm.address = address
            vm.tel = tel
            vm.hp = hp
            vm.email = email
            vm.bal_amt = bal_amt
            vm.active = True
                
            app_service = AgentAppService()
            app_service.create(vm)
            
            json_values['returnStatus'] = True
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        json_str = json.dumps(json_values)
        self.response.out.write(json_str)

class Index(BaseHandler):
    def get(self):
        # validate admin is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        
        agents = Agent.query().fetch()
        
        template_values = {
                           'title': 'Agent List',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'agents': agents
                           }
        
        template = JINJA_ENVIRONMENT.get_template('agent/index.html')
        self.response.write(template.render(template_values))
        
class Update(BaseHandler):
    def get(self, code):
        # validate admin is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        
        agent = Agent.query(Agent.code==code).get()
        
        template_values = {
                           'title': 'Update Agent',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'agent': agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('agent/update.html')
        self.response.write(template.render(template_values))
        
    def post(self, code):
        json_values = {}
        
        try:
            name = self.request.get('name')
            address = self.request.get("address")
            tel = self.request.get("tel")
            hp = self.request.get("hp")
            email = self.request.get("email")
            last_modified = self.request.get('lastModified')
            
            current_user = self.current_user()
            
            vm = AgentViewModel()
            vm.code = code
            vm.name = name
            vm.address = address
            vm.tel = tel
            vm.hp = hp
            vm.email = email
            vm.active = True
            vm.last_modified = last_modified
            vm.user_code = current_user.code
            
            app_service = AgentAppService()
            app_service.update(vm)
        
            json_values['returnStatus'] = True
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
        
        json_str = json.dumps(json_values)
        self.response.out.write(json_str);

class Search(BaseHandler):
    def post(self):
        json_values = {}
        
        try:
            name = self.request.get('name')
            code = self.request.get("code")
            
            q = Agent.query()
            
            if name:
                q = q.filter(Agent.name==name)
                
            if code:
                q = q.filter(Agent.code==code)
                
            agents = q.fetch()
            
            # create json
            data = []
            for agent in agents:
                data.append({
                             'code':agent.code,
                             'name': agent.name,
                             'address': agent.address,
                             'tel': agent.tel,
                             'hp': agent.hp,
                             'email': agent.email,
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
        
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);
