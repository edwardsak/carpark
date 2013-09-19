from admin.controllers.base import BaseHandler
from sharelib.utils import DateTime
from datalayer.models.models import User
from datalayer.appservice.admin.reports.topupsummary import TopUpSummaryByMonthAndAgent



import os
import jinja2
import json

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

class MonthlyAgentTopUp(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_user = self.current_user()
        users = User.query().fetch()
        
        template_values = {
                           'title': 'Monthly Top Up',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_user': current_user,
                           'users': users
                           }
        
        template = JINJA_ENVIRONMENT.get_template('reports/topupbymonth.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        json_values = {}
        
        try:
            #get
            date_from = DateTime.to_date(self.request.get('dateFrom'))
            date_to = DateTime.to_date(self.request.get('dateTo'))
            agent_code = self.request.get('agentCode')
            
            topup_by_month = TopUpSummaryByMonthAndAgent()
            values = topup_by_month.get(date_from, date_to, agent_code)
            topup_by_month.get()
            
            data = []
            for value in values:
                data.append({
                             'tranDate': DateTime.to_date_string(value.tran_date),
                             'agentCode': value.agent_code,
                             'topupAmt': value.sub_total,
                             'topupComm': value.comm_amt,
                             'total': value.amt
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        json_str = json.dumps(json_values)
        self.response.out.write(json_str)