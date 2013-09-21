from admin.controllers.base import BaseHandler
from sharelib.utils import DateTime
from datalayer.models.models import User, Buy, Agent


import os
import jinja2
import json

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )


class BuyTransaction(BaseHandler):       
    def get(self):
        # validate admin is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        users = User.query().fetch()
        
        template_values = {
                           'title': 'Buy Transaction',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'users': users,
                           }
        
        template = JINJA_ENVIRONMENT.get_template('buy/transaction.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        json_values = {}
        
        try:
            #get           
            date_from = self.request.get('dateFrom')
            date_to = self.request.get('dateTo')
            agent_code = self.request.get('agentCode')
            
            q = Buy.query()
            
            if date_from and len(date_from) > 0:
                date_from = DateTime.to_date(date_from)
                q = q.filter(Buy.tran_date>=date_from)
                
            if date_to and len(date_to) > 0:
                date_to = DateTime.to_date(date_to)
                q = q.filter(Buy.tran_date<=date_to)
            
            if agent_code:
                q = q.filter(Buy.agent_code==agent_code)
    
            if (not date_from and date_to and agent_code):    
                raise Exception('You must enter a Date or Agent Code.')

            buys = q.fetch()
            
            # create json
            data = []
            for buy in buys:
                data.append({
                             'tranCode': buy.tran_code,
                             'date': DateTime.to_date_string(buy.tran_date),
                             'agentCode': buy.agent_code,
                             'qty': buy.qty,
                             'unitPrice': buy.unit_price,
                             'subTotal': buy.sub_total,
                             'commission': buy.comm_amt,
                             'amount': buy.amt,
                             'paymentDate': DateTime.to_date_string(buy.payment_date),
                             'refNo': buy.payment_ref_no,
                             'paymentType': buy.payment_type,
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        json_str = json.dumps(json_values)
        self.response.out.write(json_str)
