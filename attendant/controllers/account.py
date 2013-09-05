from base import BaseHandler
from datalayer.models.models import Attendant
from datalayer.viewmodels.viewmodels import AttendantViewModel
from datalayer.appservice.attendant.account import AttendantAppService

import json
import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

class Login(BaseHandler):
    def get(self):
        current_attendant = self.current_attendant()
        
        if current_attendant is not None:
            self.redirect('/attendant/')
            
        template_values = {
                           'title': 'Login',
                           'current_attendant': current_attendant
                           }
        
        template = JINJA_ENVIRONMENT.get_template('account/login.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        json_values = {}
        
        try:
            code = self.request.get('code')
            pwd = self.request.get('pwd')
            
            if code is None:
                raise Exception('You must enter an Attendant ID.')
            
            if pwd is None:
                raise Exception('You must enter a Password.')
            
            vm = AttendantViewModel()
            vm.code = code
            vm.pwd = pwd
            
            app_service = AttendantAppService()
            app_service.login(vm)
            
            # save to session
            self.session['attendant_code'] = vm.code
            
            json_values['returnStatus'] = True
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
        
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);
             
class Logout(BaseHandler):
    def get(self):
        if self.session.get('attendant_code'):
            del self.session['attendant_code']
        
        self.redirect("/attendant/account/login")
        
class Index(BaseHandler):
    def get(self):
        current_attendant = self.current_attendant()
        
        if current_attendant is not None:
            self.redirect('/attendant/')
        
        attendant = Attendant.query().fetch()
   
        template_values = {
                           'title': 'Update Profile',
                           #'current_attendant': current_attendant
                           'attendant': attendant
                           }
        
        template = JINJA_ENVIRONMENT.get_template('account/index.html')
        self.response.write(template.render(template_values))

class ChangePwd(BaseHandler):
    def get(self):       
        #attendant = Attendant.query(Attendantt.pwd==pwd).get()
        
        template_values = {
                           'title': 'Change Password!',
                           #'attendant': attendant
                           } 
        
        template = JINJA_ENVIRONMENT.get_template('account/changepwd.html')
        self.response.write(template.render(template_values))
