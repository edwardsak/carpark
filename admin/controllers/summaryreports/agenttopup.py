from admin.controllers.base import BaseHandler
from sharelib.utils import DateTime
from datalayer.models.models import User, TopUp, Agent


import os
import jinja2
import json

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

class TopUpByAgent(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        users = User.query().fetch()
        
        template_values = {
                           'title': 'Top Up List By Agent',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'users': users
                           }
        
        template = JINJA_ENVIRONMENT.get_template('topup/index.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        json_values = {}
        
        try:
            #get           
            date_from = self.request.get('dateFrom')
            date_to = self.request.get('dateTo')
            agent_code = self.request.get('agentCode')
            
            q = TopUp.query()
            
            if date_from and len(date_from) > 0:
                date_from = DateTime.to_date(date_from)
                
            if date_to and len(date_to) > 0:
                date_to = DateTime.to_date(date_to)
                
            if agent_code:
                q = q.filter(TopUp.agent_code==agent_code)
                
            if (not date_from and date_to):    
                raise Exception('You must enter a Date.')
                
            topups = q.fetch()
            
            data = []
            for topup in topups:
                data.append({
                             'agentCode': topup.agent_code,
                             'tranDate': DateTime.to_date_string(topup.tran_date),
                             'subTotal': topup.sub_total
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        json_str = json.dumps(json_values)
        self.response.out.write(json_str)
        
class TopUpDetail(BaseHandler):
    def get(self, agent_code):
        # validate agent is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        
        topup = TopUp.query(TopUp.agent_code==agent_code).get()
        agent = Agent.query(Agent.code==agent_code).get()
        
        template_values = {
                           'title': 'Detail Top Up List',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'topup': topup,
                           'agent': agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('topup/detail.html')
        self.response.write(template.render(template_values))
        
    def post(self, agent_code):
        json_values = {}
        
        try:
            #get           
            agent_code = self.request.get('agentCode')
            
            topups = TopUp.query(TopUp.agent_code==agent_code).fetch()
            
            data = []
            for topup in topups:
                data.append({
                             'carPlate': topup.car_reg_no,
                             'tranDate': DateTime.to_date_string(topup.tran_date),
                             'subTotal': topup.sub_total,
                             'commission': topup.comm_amt,
                             'amount': topup.amt,
                             'tranCode': topup.tran_code,
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        json_str = json.dumps(json_values)
        self.response.out.write(json_str)