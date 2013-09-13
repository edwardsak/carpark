from admin.controllers.base import BaseHandler
from sharelib.utils import DateTime
from datalayer.models.models import Customer
from datalayer.viewmodels.viewmodels import CustomerViewModel
from datalayer.appservice.admin.customer import CustomerAppService

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
        json_values = {}
        
        try:
            # get post data
            ic = self.request.get("customerIc")
            name = self.request.get("name")
            pwd = self.request.get("pwd")
            address = self.request.get("address")
            tel = self.request.get("tel")
            hp = self.request.get("hp")
            email = self.request.get("email")
    
            #save data to view model class
            vm = CustomerViewModel()
            vm.ic = ic
            vm.name = name
            vm.pwd = pwd
            vm.address = address
            vm.tel = tel
            vm.hp = hp
            vm.email = email
            vm.active = True
            
            app_service = CustomerAppService()
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
        
        customers = Customer.query().fetch()
        
        template_values = {
                           'title': 'Customer List',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'customers': customers
                           }
        
        template = JINJA_ENVIRONMENT.get_template('customer/index.html')
        self.response.write(template.render(template_values))
        
class Update(BaseHandler):
    def get(self, ic):
        # validate admin is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        
        customer = Customer.query(Customer.ic==ic).get()
        
        template_values = {
                           'title': 'Update Customer',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'customer': customer
                           }
        
        template = JINJA_ENVIRONMENT.get_template('customer/update.html')
        self.response.write(template.render(template_values))
        
    def post(self, ic):
        json_values = {}
        
        try:
            ic = self.request.get('ic')
            name = self.request.get('name')
            address = self.request.get("address")
            tel = self.request.get("tel")
            hp = self.request.get("hp")
            email = self.request.get("email")
            last_modified = self.request.get('lastModified')
            
            current_user = self.current_user()
            
            vm = CustomerViewModel()
            vm.name = name
            vm.ic = ic
            vm.code = vm.ic
            vm.address = address
            vm.tel = tel
            vm.hp = hp
            vm.email = email
            vm.active = True
            vm.comm_per = 5
            vm.last_modified = last_modified
            vm.user_code = current_user.code
            
            app_service = CustomerAppService()
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
            customer_ic = self.request.get("ic")
            
            q = Customer.query()
            
            if name:
                q = q.filter(Customer.name==name)
                
            if customer_ic:
                q = q.filter(Customer.ic==customer_ic)
                
            customers = q.fetch()
            
            # create json
            data = []
            for customer in customers:
                data.append({
                             'ic':customer.ic,
                             'name': customer.name,
                             'address': customer.address,
                             'tel': customer.tel,
                             'hp': customer.hp,
                             'email': customer.email,
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
        
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);
