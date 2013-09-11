from admin.controllers.base import BaseHandler
from sharelib.utils import DateTime
from datalayer.models.models import Attendant
from datalayer.viewmodels.viewmodels import AttendantViewModel
from datalayer.appservice.admin.attendant import AttendantAppService

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
                           'title': 'Create Attendant',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user
                           }
        
        template = JINJA_ENVIRONMENT.get_template('/attendant/create.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        json_values = {}
        
        try:
            # get post data
            name = self.request.get("name")
            attendant_code = self.request.get("code")
            pwd = self.request.get("pwd")            
            current_user = self.current_user()
            user_code = current_user.code
            
            #save data to view model class
            vm = AttendantViewModel()
            vm.name = name
            vm.code = attendant_code
            vm.pwd = pwd
            vm.active = True
            vm.user_code = user_code
            vm.comm_per = 5  
            
            app_service = AttendantAppService()
            app_service.create(vm)
            
            # return status
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
        
        attendants = Attendant.query().fetch()
        
        template_values = {
                           'title': 'Attendant List',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'attendants': attendants
                           }
        
        template = JINJA_ENVIRONMENT.get_template('attendant/index.html')
        self.response.write(template.render(template_values))
        
class Update(BaseHandler):
    def get(self, code):
        # validate admin is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        
        attendant = Attendant.query(Attendant.code==code).get()
        
        template_values = {
                           'title': 'Update Attendant',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'attendant': attendant
                           }
        
        template = JINJA_ENVIRONMENT.get_template('attendant/update.html')
        self.response.write(template.render(template_values))
        
    def post(self, code):
        json_values = {}
        
        try:
            name = self.request.get('name')
            last_modified = self.request.get('lastModified')
            
            current_user = self.current_user()
            
            vm = AttendantViewModel()
            vm.name = name
            vm.code = code
            vm.active = True
            vm.last_modified = last_modified
            vm.user_code = current_user.code
            vm.comm_per = 5
            
            app_service = AttendantAppService()
            app_service.update(vm)
        
            json_values['returnStatus'] = True
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
        
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);

class Search(BaseHandler):
    def post(self):
        json_values = {}
        
        try:
            name = self.request.get('name')
            attendant_code = self.request.get("code")
            
            q = Attendant.query()
            
            if name:
                q = q.filter(Attendant.name==name)
                
            if attendant_code:
                q = q.filter(Attendant.code==attendant_code)
                
            attendants = q.fetch()
            
            # create json
            data = []
            for attendant in attendants:
                data.append({
                             'code':attendant.code,
                             'name': attendant.name,
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
        
        json_str = json.dumps(json_values)
        self.response.out.write(json_str);