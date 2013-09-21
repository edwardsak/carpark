from admin.controllers.base import BaseHandler
from sharelib.utils import DateTime
from datalayer.models.models import User, Register


import os
import jinja2
import json

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

        
class RegisterTransaction(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        users = User.query().fetch()
        
        
        template_values = {
                           'title': 'Detail Register List',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'users': users,
                           }
        
        template = JINJA_ENVIRONMENT.get_template('register/transaction.html')
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
            
            # create json
            data = []
            for register in registers:
                data.append({
                             'tranCode': register.tran_code,
                             'carPlate': register.car_reg_no,
                             'tranDate': DateTime.to_date_string(register.tran_date),
                             'agentCode': register.agent_code,
                             'ic': register.customer_ic,
                             'name': register.customer_name,
                             'address': register.customer_address,
                             'tel': register.customer_tel,
                             'hp': register.customer_hp,
                             'email': register.customer_email,
                             'tagNo': register.tag_code,
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        json_str = json.dumps(json_values)
        self.response.out.write(json_str)
        