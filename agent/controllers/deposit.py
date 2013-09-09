from agent.controllers.base import BaseHandler
from sharelib.utils import DateTime
from datalayer.models.models import Agent
from datalayer.models.models import Deposit
from datalayer.viewmodels.viewmodels import DepositViewModel
from datalayer.appservice.agent.deposit import DepositAppService


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
                           'title': 'Deposit',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_agent': current_agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('deposit/create.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        json_values = {}
        
        try:
            agent_code = self.session['agent_code']
            
            # get post data
            date = DateTime.to_date(self.request.get("date"))
            amt = float(self.request.get("amount"))
            payment_date = DateTime.to_date(self.request.get("paymentDate"))
            ref_no = self.request.get("refNo")
    
            #save data to view model class
            vm = DepositViewModel()
            vm.tran_date = date
            vm.amt = amt
            vm.agent_code = agent_code
            vm.payment_date = payment_date
            vm.payment_ref_no = ref_no
            vm.payment_type = 1
      
            app_service = DepositAppService()
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
                           'title': 'Deposit List',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_agent': current_agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('deposit/index.html')
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
            
            vm = DepositViewModel()
            vm.code = code
            vm.name = name
            vm.address = address
            vm.tel = tel
            vm.hp = hp
            vm.email = email
            vm.account_type = agent.account_type
            vm.active = True
            vm.last_modified = last_modified
            
            app_service = DepositAppService()
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
            current_agent = self.current_agent()
            agent_code = current_agent.code
            
            q = Deposit.query()
            
            if date_from:
                q = q.filter(Deposit.tran_date>=date_from)
                
            if date_to:
                q = q.filter(Deposit.tran_date<=date_to)
                
            if agent_code:
                q = q.filter(Deposit.agent_code==agent_code)
                
            deposits = q.fetch()
            
            # create json
            data = []
            for deposit in deposits:
                data.append({
                             'agentCode': deposit.agent_code,
                             'date': DateTime.to_date_string(deposit.tran_date),
                             'amount': deposit.amt,
                             'paymentDate': DateTime.to_date_string(deposit.payment_date),
                             'refNo': deposit.payment_ref_no,
                             'paymentType': deposit.payment_type
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex) 
        
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);
