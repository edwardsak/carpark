from base import BaseHandler
from datalayer.models.models import Customer
from datalayer.viewmodels.viewmodels import UserViewModel
from datalayer.appservice.user import UserAppService

import json
import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

class Login(BaseHandler):
    def get(self):
        current_user = self.current_user()
        
        if current_user is not None:
            self.redirect('/agent/')
            
        template_values = {
                           'title': 'Login',
                           'current_user': current_user
                           }
        
        template = JINJA_ENVIRONMENT.get_template('account/login.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        json_values = {}
        
        try:
            code = self.request.get('code')
            pwd = self.request.get('pwd')
            
            if code is None:
                raise Exception('You must enter an Agent ID.')
            
            if pwd is None:
                raise Exception('You must enter a Password.')
            
            vm = UserViewModel()
            vm.code = code
            vm.pwd = pwd
            
            app_service = UserAppService()
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
        if self.session.get('user_code'):
            del self.session['user_code']
        
        self.redirect("/customer/account/login")
        
class Index(BaseHandler):
    def get(self):
        current_user = self.current_user()
        
        if current_user is not None:
            self.redirect('/agent/')
        
        customer = Customer.query().fetch()
   
        template_values = {
                           'title': 'Update Profile',
                           #'current_agent': current_agent
                           'customer': customer
                           }
        
        template = JINJA_ENVIRONMENT.get_template('account/index.html')
        self.response.write(template.render(template_values))

class ChangePwd(BaseHandler):
    def get(self):       
        #agent = Agent.query(Agent.pwd==pwd).get()
        
        template_values = {
                           'title': 'Update Agent Password!',
                           #'agent': agent
                           } 
        
        template = JINJA_ENVIRONMENT.get_template('account/changePwd.html')
        self.response.write(template.render(template_values))
        
class History(BaseHandler):
    def get(self):       
        #agent = Agent.query(Agent.pwd==pwd).get()
        
        template_values = {
                           'title': 'Agent Purchasing Info!',
                           #'agent': agent
                           } 
        
        template = JINJA_ENVIRONMENT.get_template('account/purchase.html')
        self.response.write(template.render(template_values))