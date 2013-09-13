from customer.controllers.base import BaseHandler
from datalayer.models.models import Customer
from datalayer.viewmodels.viewmodels import CustomerViewModel
from datalayer.appservice.customer.account import AccountAppService

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
            ic = self.request.get('ic')
            pwd = self.request.get('pwd')
            
            if ic is None or len(ic) < 1:
                raise Exception('You must enter an IC/PP No.')
            
            if pwd is None or len(pwd) < 1:
                raise Exception('You must enter a Password.')
            
            vm = CustomerViewModel()
            vm.ic = ic
            vm.pwd = pwd
            
            app_service = AccountAppService()
            app_service.login(vm)
            
            # save to session
            self.session['customer_ic'] = vm.ic
            
            json_values['returnStatus'] = True
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
        
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);
             
class Logout(BaseHandler):
    def get(self):
        if self.session.get('customer_ic'):
            del self.session['customer_ic']
            
        self.redirect("/customer/account/login/")
            
class Index(BaseHandler):       
    def get(self):
        current_customer = self.current_customer()
        
        if current_customer is not None:
            self.redirect('/customer/')
        
        customer = Customer.query().fetch()
   
        template_values = {
                           'title': 'Customer Home',
                           'current_customer': current_customer,
                           'customer': customer
                           }
        
        template = JINJA_ENVIRONMENT.get_template('account/index.html')
        self.response.write(template.render(template_values))

class Update(BaseHandler):
    def get(self, ic):
        # validate admin is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_customer = self.current_customer()
        
        customer = Customer.query(Customer.ic==current_customer.ic).get()
        
        template_values = {
                           'title': 'Update Profile',
                           'current_customer': current_customer,
                           'customer': customer
                           } 
        
        template = JINJA_ENVIRONMENT.get_template('account/update.html')
        self.response.write(template.render(template_values))
        
    def post(self, ic):
        json_values = {}
        
        try:
            address = self.request.get('address')
            tel = self.request.get('tel')
            hp = self.request.get('hp')
            email = self.request.get('email')
            last_modified = self.request.get('lastModified')
            
            #customer = Customer.query(Customer.ic==ic).get()

            current_customer = self.current_customer()
            
            vm = CustomerViewModel()
            vm.name = current_customer.name
            vm.ic = current_customer.ic
            vm.code = vm.ic
            vm.address = address
            vm.tel = tel
            vm.hp = hp
            vm.email = email
            vm.active = True
            vm.comm_per = 5
            vm.last_modified = last_modified
            vm.user_code = current_customer.ic
            
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
        
        current_customer = self.current_customer()
        
        template_values = {
                           'title': 'Change Password!',
                           'current_customer': current_customer,
                           } 
        
        template = JINJA_ENVIRONMENT.get_template('account/changepwd.html')
        self.response.write(template.render(template_values))
    
    def post(self):
        json_values = {}
        
        try:
            current_customer = self.current_customer()
            
            pwd = self.request.get('newPwd')
            old_pwd = self.request.get('oldPwd')
      
            vm = CustomerViewModel()
            vm.ic = current_customer.ic
            vm.code = vm.ic
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
        