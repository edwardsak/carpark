from admin.controllers.base import BaseHandler
from sharelib.utils import DateTime
from datalayer.models.models import User
from datalayer.viewmodels.viewmodels import UserViewModel
from datalayer.appservice.admin.user import UserAppService

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
                           'title': 'Create User',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user
                           }
        
        template = JINJA_ENVIRONMENT.get_template('/user/create.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        json_values = {}
        
        try:
            # get post data
            name = self.request.get("name")
            code = self.request.get("code")
            pwd = self.request.get("pwd")
            level = int(self.request.get("level"))
    
            #save data to view model class
            vm = UserViewModel()
            vm.code = code
            vm.name = name
            vm.pwd = pwd
            vm.level = level
                
            app_service = UserAppService()
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
        
        users = User.query().fetch()
        
        template_values = {
                           'title': 'User List',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'users': users
                           }
        
        template = JINJA_ENVIRONMENT.get_template('user/index.html')
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
                           'title': 'Update User',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'user': user
                           }
        
        template = JINJA_ENVIRONMENT.get_template('user/update.html')
        self.response.write(template.render(template_values))
        
    def post(self, code):
        json_values = {}
        
        try:
            name = self.request.get('name')
            pwd = self.request.get("pwd")
            level = self.request.get("level")
            
            vm = UserViewModel()
            vm.code = User.query(User.code==code).get()
            vm.name = name
            vm.pwd = pwd
            vm.level = level
            
            app_service = UserAppService()
            app_service.update(vm)
        
            json_values['returnStatus'] = True
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
        
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);

class Search(BaseHandler):
    def post(self):
        name = self.request.get('name')
        code = self.request.get("code")
        
        q = User.query()
        
        if name:
            q = q.filter(User.name==name)
            
        if code:
            q = q.filter(User.code==code)
            
        users = q.fetch()
        
        # create json
        data = []
        for user in users:
            data.append({
                         'code':user.code,
                         'name': user.name,
                         })
            
        json_values = {
                       'returnStatus': True,
                       'data': data
                       }
        
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);
