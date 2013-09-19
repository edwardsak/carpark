from admin.controllers.base import BaseHandler
from sharelib.utils import DateTime
from datalayer.models.models import User, Register, Agent, Car, Customer


import os
import jinja2
import json

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

class RegisterByAgent(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        users = User.query().fetch()
        
        template_values = {
                           'title': 'Register List By Agent',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'users': users
                           }
        
        template = JINJA_ENVIRONMENT.get_template('register/index.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        json_values = {}
        
        try:
            #get           
            date_from = self.request.get('dateFrom')
            date_to = self.request.get('dateTo')
            agent_code = self.request.get('agentCode')
            
            q = Register.query()
            
            if date_from and len(date_from) > 0:
                date_from = DateTime.to_date(date_from)
                
            if date_to and len(date_to) > 0:
                date_to = DateTime.to_date(date_to)
                
            if agent_code:
                q = q.filter(Register.agent_code==agent_code)
                
            if (not date_from and date_to):    
                raise Exception('You must enter a Date.')
                
            registers = q.fetch()
            
            data = []
            for register in registers:
                data.append({
                             'agentCode': register.agent_code,
                             'tranDate': DateTime.to_date_string(register.tran_date),
                             'carPlate': register.car_reg_no,
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        json_str = json.dumps(json_values)
        self.response.out.write(json_str)
        
class RegisterDetail(BaseHandler):
    def get(self, agent_code):
        # validate agent is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        
        register = Register.query(Register.agent_code==agent_code).get()
        agent = Agent.query(Agent.code==agent_code).get()
        
        template_values = {
                           'title': 'Detail Register List',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'register': register,
                           'agent': agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('register/detail.html')
        self.response.write(template.render(template_values))
        
    def post(self, agent_code):
        json_values = {}
        
        try:
            #get           
            agent_code = self.request.get('agentCode')
            
            registers = Register.query(Register.agent_code==agent_code).fetch()
            
            # create json
            data = []
            for register in registers:
                data.append({
                             'carPlate': register.car_reg_no,
                             'tranDate': DateTime.to_date_string(register.tran_date),
                             'ic': register.customer_ic,
                             'name': register.customer_name,
                             'address': register.customer_address,
                             'tel': register.customer_tel,
                             'hp': register.customer_hp,
                             'email': register.customer_email,
                             'tagNo': register.tag_code,
                             'tranCode': register.tran_code,
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        json_str = json.dumps(json_values)
        self.response.out.write(json_str)
        
class RegisterCarDetail(BaseHandler):
    def get(self, reg_no):
        # validate agent is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        
        car = Car.query(Car.reg_no==reg_no).get()
        customer = Customer.query(Customer.ic==car.customer_ic).get()
        
        template_values = {
                           'title': 'Detail of Register Car',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'car': car,
                           'customer': customer
                           }
        
        template = JINJA_ENVIRONMENT.get_template('register/cardetail.html')
        self.response.write(template.render(template_values))
        
    def post(self, reg_no):
        json_values = {}
        
        try:
            #get           
            reg_no = self.request.get('reg_no')
            ic = self.request.get('ic')
            
            customer = Customer.query(Customer.ic==ic).get()
            cars = Car.query(Car.reg_no==reg_no).fetch()
            
            # create json
            data = []
            for car in cars:
                data.append({
                             'ic': car.customer_ic,
                             'balAmt': car.bal_amt,
                             'name': customer.name,
                             'tel': customer.tel,
                             'hp': customer.hp,
                             'email': customer.email,
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        json_str = json.dumps(json_values)
        self.response.out.write(json_str)