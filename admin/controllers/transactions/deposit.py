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

        
class DepositTransaction(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        users = User.query().fetch()
        
        template_values = {
                           'title': 'Deposit Transaction',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'users': users,
                           }
        
        template = JINJA_ENVIRONMENT.get_template('deposit/transaction.html')
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
            
            # create json
            data = []
            for deposit in deposits:
                data.append({
                             'tranCode': deposit.tran_code,
                             'tranDate': DateTime.to_date_string(deposit.tran_date),
                             'agentCode': deposit.agent_code,
                             'amount': deposit.amt,
                             'paymentDate': DateTime.to_date_string(deposit.payment_date),
                             'refNo': deposit.payment_ref_no,
                             'paymentType': deposit.payment_type,
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        json_str = json.dumps(json_values)
        self.response.out.write(json_str)