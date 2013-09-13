from admin.controllers.base import BaseHandler
from datalayer.models.models import User
from datalayer.viewmodels.viewmodels import UserViewModel
from datalayer.appservice.admin.account import AccountAppService

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
            self.redirect('/admin/')
            
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
            
            if code is None or len(code) < 1:
                raise Exception('You must enter an Admin ID.')
            
            if pwd is None or len(pwd) < 1:
                raise Exception('You must enter a Password.')
            
            vm = UserViewModel()
            vm.code = code
            vm.pwd = pwd
            
            app_service = AccountAppService()
            app_service.login(vm)
            
            # save to session
            self.session['user_code'] = vm.code
            
            json_values['returnStatus'] = True
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
        
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);
             
class Logout(BaseHandler):
    def post(self):
        if self.session.get('user_code'):
            del self.session['user_code']
            
        self.response.out.write("");
        
class Index(BaseHandler):
    def get(self):
        current_user = self.current_user()
        
        if current_user is not None:
            self.redirect('/admin/')
        
        user = User.query().fetch()
   
        template_values = {
                           'title': 'Update Profile',
                           #'current_user': current_user
                           'user': user
                           }
        
        template = JINJA_ENVIRONMENT.get_template('account/index.html')
        self.response.write(template.render(template_values))

class Update(BaseHandler):
    def get(self, code):
        # validate admin is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        
        user = User.query(User.code==code).get()
        
        template_values = {
                           'title': 'Update Profile',
                           'current_user': current_user,
                           'user': user
                           }
        
        template = JINJA_ENVIRONMENT.get_template('account/update.html')
        self.response.write(template.render(template_values))
        
    def post(self, code):
        json_values = {}
        
        try:
            name = self.request.get('name')

            last_modified = self.request.get('lastModified')
            
            #user = User.query(User.code==code).get()
            current_user = self.current_user()
            
            vm = UserViewModel()
            vm.code = current_user.code
            vm.name = name
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

class ResetPwd(BaseHandler):
    def get(self):       
        # validate admin is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        
        template_values = {
                           'title': 'Reset Password!',
                           'current_user': current_user,
                           } 
        
        template = JINJA_ENVIRONMENT.get_template('account/resetpwd.html')
        self.response.write(template.render(template_values))
    
    def post(self):
        json_values = {}
        
        try:
            current_user = self.current_user()
            
            admin_id = self.request.get('adminId')
            pwd = self.request.get('newPwd')
            old_pwd = self.request.get('oldPwd')
      
            vm = UserViewModel()
            vm.code = current_user.code
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
        
class ChangePwd(BaseHandler):
    def get(self):       
        # validate admin is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        
        template_values = {
                           'title': 'Change Password!',
                           'current_user': current_user,
                           } 
        
        template = JINJA_ENVIRONMENT.get_template('account/changepwd.html')
        self.response.write(template.render(template_values))
    
    def post(self):
        json_values = {}
        
        try:
            current_user = self.current_user()
            
            pwd = self.request.get('newPwd')
            old_pwd = self.request.get('oldPwd')
      
            vm = UserViewModel()
            vm.code = current_user.code
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