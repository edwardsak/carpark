from admin.controllers.base import BaseHandler
from sharelib.utils import DateTime
from datalayer.models.models import User, Deposit, Agent


import os
import jinja2
import json

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

class DepositByAgent(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        users = User.query().fetch()
        
        template_values = {
                           'title': 'Deposit List By Agent',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'users': users
                           }
        
        template = JINJA_ENVIRONMENT.get_template('deposit/index.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        json_values = {}
        
        try:
            #get           
            date_from = self.request.get('dateFrom')
            date_to = self.request.get('dateTo')
            agent_code = self.request.get('agentCode')
            
            q = Deposit.query()
            
            if date_from and len(date_from) > 0:
                date_from = DateTime.to_date(date_from)
                
            if date_to and len(date_to) > 0:
                date_to = DateTime.to_date(date_to)
            
            if agent_code:
                q = q.filter(Deposit.agent_code==agent_code)
                
            if (not date_from and date_to):    
                raise Exception('You must enter a Date.')
               
            deposits = q.fetch()
            
            data = []
            for deposit in deposits:
                data.append({
                             'agentCode': deposit.agent_code,
                             'tranDate': DateTime.to_date_string(deposit.tran_date),
                             'amt': deposit.amt
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        json_str = json.dumps(json_values)
        self.response.out.write(json_str)
        
class DepositDetail(BaseHandler):
    def get(self, agent_code):
        # validate agent is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        
        deposit = Deposit.query(Deposit.agent_code==agent_code).get()
        agent = Agent.query(Agent.code==agent_code).get()
        
        template_values = {
                           'title': 'Detail Deposit List',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'deposit': deposit,
                           'agent': agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('deposit/detail.html')
        self.response.write(template.render(template_values))
        
    def post(self, agent_code):
        json_values = {}
        
        try:
            #get           
            agent_code = self.request.get('agentCode')
            
            deposits = Deposit.query(Deposit.agent_code==agent_code).fetch()
            
            # create json
            data = []
            for deposit in deposits:
                data.append({
                             'tranDate': DateTime.to_date_string(deposit.tran_date),
                             'amount': deposit.amt,
                             'paymentDate': DateTime.to_date_string(deposit.payment_date),
                             'refNo': deposit.payment_ref_no,
                             'paymentType': deposit.payment_type,
                             'tranCode': deposit.tran_code,
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        json_str = json.dumps(json_values)
        self.response.out.write(json_str)