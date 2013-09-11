from agent.controllers.base import BaseHandler
from sharelib.utils import DateTime
from datalayer.models.models import Agent
from datalayer.models.models import Register
from datalayer.viewmodels.viewmodels import RegisterViewModel
from datalayer.appservice.agent.register import RegisterAppService


import os
import jinja2
import json

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

class Create(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_agent = self.current_agent()
        
        template_values = {
                           'title': 'Register',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_agent': current_agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('register/create.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        json_values = {}
        
        try:
            agent_code = self.session['agent_code']
            
            # get post data
            date = DateTime.to_date(self.request.get("date"))
            carPlate = self.request.get("carPlate")
            name = self.request.get("name")
            ic = self.request.get("ic")
            address = self.request.get("address")
            tel = self.request.get("tel")
            hp = self.request.get("hp")
            email = self.request.get("email")
            tagNo = self.request.get("tagNo")
    
            #save data to view model class
            vm = RegisterViewModel()
            vm.tran_date = date
            vm.agent_code = agent_code
            vm.car_reg_no = carPlate
            vm.customer_name = name
            vm.customer_ic = ic
            vm.customer_address = address
            vm.customer_tel = tel
            vm.customer_hp = hp
            vm.customer_email = email
            vm.tag_code = tagNo
      
            app_service = RegisterAppService()
            app_service.create(vm)
            
            json_values['returnStatus'] = True
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        json_str = json.dumps(json_values)
        self.response.out.write(json_str)
        
class Index(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_agent = self.current_agent()
        
        template_values = {
                           'title': 'Register List',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_agent': current_agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('register/index.html')
        self.response.write(template.render(template_values))

class Update(BaseHandler):
    def get(self, code):
        # validate admin is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_agent = self.current_agent()
        
        agent = Agent.query(Agent.code==code).get()
        
        template_values = {
                           'title': 'Update Profile',
                           'current_agent': current_agent,
                           'agent': agent
                           } 
        
        template = JINJA_ENVIRONMENT.get_template('account/update.html')
        self.response.write(template.render(template_values))
        
    def post(self, code):
        json_values = {}
        
        try:
            name = self.request.get('name')
            address = self.request.get('address')
            tel = self.request.get('tel')
            hp = self.request.get('hp')
            email = self.request.get('email')
            last_modified = self.request.get('lastModified')
            
            agent = Agent.query(Agent.code==code).get()
            
            vm = RegisterViewModel()
            vm.code = code
            vm.name = name
            vm.address = address
            vm.tel = tel
            vm.hp = hp
            vm.email = email
            vm.account_type = agent.account_type
            vm.active = True
            vm.last_modified = last_modified
            
            app_service = RegisterAppService()
            app_service.update(vm)
        
            json_values['returnStatus'] = True
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
        
        json_str = json.dumps(json_values)
        self.response.out.write(json_str);
        
class Search(BaseHandler):
    def post(self):
        json_values = {}
        
        try:
            date_from = DateTime.to_date(self.request.get('dateFrom'))
            date_to = DateTime.to_date(self.request.get("dateTo"))
            carPlate = self.request.get('carPlate')
            current_agent = self.current_agent()
            code = current_agent.code
            
            q = Register.query()
            
            if date_from:
                q = q.filter(Register.tran_date>=date_from)
                
            if date_to:
                q = q.filter(Register.tran_date<=date_to)
                
            if carPlate:
                q = q.filter(Register.car_reg_no==carPlate)
                
            if code:
                q = q.filter(Register.agent_code==code)
                
            registers = q.fetch()
            
            # create json
            data = []
            for register in registers:
                data.append({
                             'agentCode': register.agent_code,
                             'date': DateTime.to_date_string(register.tran_date),
                             'carPlate': register.car_reg_no,
                             'name': register.customer_name,
                             'ic': register.customer_ic,
                             'address': register.customer_address,
                             'tel': register.customer_tel,
                             'hp': register.customer_hp,
                             'email': register.customer_email,
                             'tagNo': register.tag_code
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);
