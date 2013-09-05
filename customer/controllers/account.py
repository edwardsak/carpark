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
        current_customer = self.current_customer()
        
        if current_customer is not None:
            self.redirect('/customer/')
            
        template_values = {
                           'title': 'Login',
                           'current_customer': current_customer
                           }
        
        template = JINJA_ENVIRONMENT.get_template('account/login.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        json_values = {}
        
        try:
            code = self.request.get('code')
            pwd = self.request.get('pwd')
            
            if code is None:
                raise Exception('You must enter an Customer ID.')
            
            if pwd is None:
                raise Exception('You must enter a Password.')
            
            vm = UserViewModel()
            vm.code = code
            vm.pwd = pwd
            
            app_service = UserAppService()
            app_service.login(vm)
            
            # save to session
            self.session['customer_code'] = vm.code
            
            json_values['returnStatus'] = True
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
        
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);
             
class Logout(BaseHandler):
    def get(self):
        if self.session.get('customer_code'):
            del self.session['customer_code']
        
        self.redirect("/customer/account/login")
        
class Index(BaseHandler):       
    def get(self):
        current_customer = self.current_customer()
        
        if current_customer is not None:
            self.redirect('/customer/')
        
        customer = Customer.query().fetch()
   
        template_values = {
                           'title': 'Update Profile',
                           #'current_customer': current_customer
                           'customer': customer
                           }
        
        template = JINJA_ENVIRONMENT.get_template('account/index.html')
        self.response.write(template.render(template_values))


class ChangePwd(BaseHandler):
    def get(self):       
        #customer = Customer.query(Customer.pwd==pwd).get()
        
        template_values = {
                           'title': 'Update Customer Password!',
                           #'customer': customer
                           } 
        
        template = JINJA_ENVIRONMENT.get_template('account/changepwd.html')
        self.response.write(template.render(template_values))
        