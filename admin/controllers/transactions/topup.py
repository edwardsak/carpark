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

        
class TopUpTransaction(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        users = User.query().fetch()
        
        template_values = {
                           'title': 'Top Up Transaction',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'users': users,
                           }
        
        template = JINJA_ENVIRONMENT.get_template('topup/transaction.html')
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
                             'tranCode': topup.tran_code,
                             'carPlate': topup.car_reg_no,
                             'tranDate': DateTime.to_date_string(topup.tran_date),
                             'agentCode': topup.agent_code,
                             'subTotal': topup.sub_total,
                             'commission': topup.comm_amt,
                             'amount': topup.amt,                    
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        json_str = json.dumps(json_values)
        self.response.out.write(json_str)