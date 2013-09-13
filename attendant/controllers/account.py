from base import BaseHandler
from datalayer.models.models import Attendant
from datalayer.viewmodels.viewmodels import AttendantViewModel
from datalayer.appservice.attendant.account import AccountAppService

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
            
            if code is None or len(code) < 1:
                raise Exception('You must enter an Attendant ID.')
            
            if pwd is None or len(pwd) < 1:
                raise Exception('You must enter a Password.')
            
            vm = AttendantViewModel()
            vm.code = code
            vm.pwd = pwd
            
            app_service = AccountAppService()
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
        
        self.redirect("/attendant/account/login/")
        
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

class Update(BaseHandler):
    def get(self, code):
        # validate admin is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_attendant = self.current_attendant()
        
        attendant = Attendant.query(Attendant.code==code).get()
        
        template_values = {
                           'title': 'Update Profile',
                           'current_attendant': current_attendant,
                           'attendant': attendant
                           } 
        
        template = JINJA_ENVIRONMENT.get_template('account/update.html')
        self.response.write(template.render(template_values))
        
    def post(self, code):
        json_values = {}
        
        try:
            name = self.request.get('name')
            last_modified = self.request.get('lastModified')
            
            attendant = Attendant.query(Attendant.code==code).get()
            current_attendant = self.current_attendant()
            
            vm = AttendantViewModel()
            vm.code = current_attendant.code
            vm.name = name
            vm.active = True
            vm.comm_per = 5
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
        
        current_attendant = self.current_attendant()
        
        template_values = {
                           'title': 'Change Password!',
                           'current_attendant': current_attendant,
                           } 
        
        template = JINJA_ENVIRONMENT.get_template('account/changepwd.html')
        self.response.write(template.render(template_values))
    
    def post(self):
        json_values = {}
        
        try:
            current_attendant = self.current_attendant()
            
            pwd = self.request.get('newPwd')
            old_pwd = self.request.get('oldPwd')
      
            vm = AttendantViewModel()
            vm.code = current_attendant.code
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
        