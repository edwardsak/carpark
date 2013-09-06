from admin.controllers.base import BaseHandler
from sharelib.utils import DateTime
from datalayer.models.models import User

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
                           'title': 'Create Customer',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user
                           }
        
        template = JINJA_ENVIRONMENT.get_template('/customer/create.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        # get post data
        name = self.request.get("name")
        code = self.request.get("code")
        pwd = self.request.get("pwd")
        level = self.request.get("level")

        
        # create new car
        user = User()
        user.name = name
        user.code = code
        user.pwd = pwd
        user.level = level
        
        user.put()
        
        # return result
        json_values = {
                       'returnStatus': True
                       }
        
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
                           'title': 'Customer List',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'users': users
                           }
        
        template = JINJA_ENVIRONMENT.get_template('/customer/index.html')
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
                           'title': 'Update Customer',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'user': user
                           }
        
        template = JINJA_ENVIRONMENT.get_template('/customer/update.html')
        self.response.write(template.render(template_values))
        
    def post(self, code):
        name = self.request.get('name')
        code = self.request.get("code")
        pwd = self.request.get("pwd")
        level = self.request.get("level")
        
        user = User.query(User.code==code).get()
        user.name = name
        user.code = code
        user.pwd = pwd
        user.level = level
        
        user.put()
        
        json_values = {
                       'returnStatus': True
                       }
        
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
