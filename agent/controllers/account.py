from agent.controllers.base import BaseHandler
from datalayer.models.models import Agent
from datalayer.viewmodels.viewmodels import AgentViewModel
from datalayer.appservice.agent.account import AccountAppService

import json
import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

class Login(BaseHandler):
    def get(self):
        current_agent = self.current_agent()
        
        if current_agent is not None:
            self.redirect('/agent/')
            
        template_values = {
                           'title': 'Login',
                           'current_agent': current_agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('account/login.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        json_values = {}
        
        try:
            code = self.request.get('code')
            pwd = self.request.get('pwd')
            
            if code is None or len(code) < 1:
                raise Exception('You must enter an Agent ID.')
            
            if pwd is None or len(pwd) < 1:
                raise Exception('You must enter a Password.')
            
            vm = AgentViewModel()
            vm.code = code
            vm.pwd = pwd
            
            app_service = AccountAppService()
            app_service.login(vm)
            
            # save to session
            self.session['agent_code'] = vm.code
            
            json_values['returnStatus'] = True
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
        
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);
             
class Logout(BaseHandler):
    def get(self):
        if self.session.get('agent_code'):
            del self.session['agent_code']
        
        self.redirect("/agent/account/login/")
             
class Update(BaseHandler):
    def get(self, code):
        # validate admin is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_agent = self.current_agent()
        
        agent = Agent.query(Agent.code==code).get()
        
        template_values = {
                           'title': 'Update Profile',
                           'current_agent': current_agent,
                           'agent': agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('account/update.html')
        self.response.write(template.render(template_values))
        
    def post(self, code):
        json_values = {}
        
        try:
            name = self.request.get('name')
            address = self.request.get('address')
            tel = self.request.get('tel')
            hp = self.request.get('hp')
            email = self.request.get('email')
            last_modified = self.request.get('lastModified')
            
            agent = Agent.query(Agent.code==code).get()
            current_agent = self.current_agent()
            
            vm = AgentViewModel()
            vm.code = current_agent.code
            vm.name = name
            vm.address = address
            vm.tel = tel
            vm.hp = hp
            vm.email = email
            vm.account_type = agent.account_type
            vm.active = True
            vm.last_modified = last_modified
            
            app_service = AccountAppService()
            app_service.update(vm)
        
            json_values['returnStatus'] = True
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
        
        json_str = json.dumps(json_values)
        self.response.out.write(json_str);

class ChangePwd(BaseHandler):
    def get(self):       
        # validate admin is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_agent = self.current_agent()
        
        template_values = {
                           'title': 'Change Password!',
                           'current_agent': current_agent,
                           } 
        
        template = JINJA_ENVIRONMENT.get_template('account/changepwd.html')
        self.response.write(template.render(template_values))
    
    def post(self):
        json_values = {}
        
        try:
            current_agent = self.current_agent()
            
            pwd = self.request.get('newPwd')
            old_pwd = self.request.get('oldPwd')
      
            vm = AgentViewModel()
            vm.code = current_agent.code
            vm.pwd = pwd
            vm.old_pwd = old_pwd
            
            app_service = AccountAppService()
            app_service.change_pwd(vm)
            
            json_values['returnStatus'] = True
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
        
        json_str = json.dumps(json_values)
        self.response.out.write(json_str);