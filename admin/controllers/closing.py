from admin.controllers.base import BaseHandler
from sharelib.utils import DateTime, Bool
from datalayer.models.models import Closing
from datalayer.appservice.admin.closing import ClosingAppService
from datalayer.viewmodels.viewmodels import ClosingViewModel

import os
import jinja2
import json

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

class Index(BaseHandler):
    def get(self):
        # validate customer is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        
        closing = Closing.query().get()
        
        template_values = {
                           'title': 'Closing',
                           'closingDate': DateTime.to_time_string(closing.closing_date),
                           'auditLock': Bool.to_string(closing.audit_lock),
                           'current_user': current_user
                           }
        
        template = JINJA_ENVIRONMENT.get_template('closing/index.html')
        self.response.write(template.render(template_values))
        
class Lock(BaseHandler): 
    def post(self):
        json_values = {}
        
        try:           
            current_user = self.current_user()
            
            vm = ClosingViewModel()
            vm.user_code = current_user.code
            
            closing = ClosingAppService()
            closing.lock(vm)

            json_values['returnStatus'] = True
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);
        
class Unlock(BaseHandler): 
    def post(self):
        json_values = {}
        
        try:           
            current_user = self.current_user()
            
            vm = ClosingViewModel()
            vm.user_code = current_user.code
            
            closing = ClosingAppService()
            closing.unlock(vm)

            json_values['returnStatus'] = True
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);

class Close(BaseHandler):     
    def post(self):
        json_values = {}
        
        try:           
            current_user = self.current_user()
            
            vm = ClosingViewModel()
            vm.user_code = current_user.code
            
            closing = ClosingAppService()
            closing.close(vm)

            json_values['returnStatus'] = True
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);
        
class Revert(BaseHandler): 
    def post(self):
        json_values = {}
        
        try:           
            current_user = self.current_user()
            
            vm = ClosingViewModel()
            vm.user_code = current_user.code
            
            closing = ClosingAppService()
            closing.revert(vm)

            json_values['returnStatus'] = True
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);