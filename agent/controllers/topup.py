from agent.controllers.base import BaseHandler
from sharelib.utils import DateTime
from datalayer.models.models import Agent
from datalayer.models.models import TopUp
from datalayer.viewmodels.viewmodels import TopUpViewModel
from datalayer.appservice.agent.topup import TopUpAppService


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
                           'title': 'Top Up',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_agent': current_agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('topup/create.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        json_values = {}
        
        try:
            agent_code = self.session['agent_code']
            
            # get post data
            date = DateTime.to_date(self.request.get("date"))
            carPlate = self.request.get("carPlate")
            amount = float(self.request.get("amount"))

    
            #save data to view model class
            vm = TopUpViewModel()
            vm.tran_date = date
            vm.agent_code = agent_code
            vm.car_reg_no = carPlate
            vm.sub_total = amount
            vm.comm_per = 5

      
            app_service = TopUpAppService()
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
                           'title': 'Top Up List',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_agent': current_agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('topup/index.html')
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
            
            vm = TopUpViewModel()
            vm.code = code
            vm.name = name
            vm.address = address
            vm.tel = tel
            vm.hp = hp
            vm.email = email
            vm.account_type = agent.account_type
            vm.active = True
            vm.last_modified = last_modified
            
            app_service = TopUpAppService()
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
            date_from = self.request.get('dateFrom')
            date_to = self.request.get("dateTo")
            carPlate = self.request.get('carPlate')
            current_agent = self.current_agent()
            agent_code = current_agent.code
                        
            q = TopUp.query()
            
            if date_from and len(date_from) > 0:
                date_from = DateTime.to_date(date_from)
                q = q.filter(TopUp.tran_date>=date_from)
                
            if date_to and len(date_to) > 0:
                date_to = DateTime.to_date(date_to)
                q = q.filter(TopUp.tran_date<=date_to)
            
            if carPlate:
                q = q.filter(TopUp.car_reg_no==carPlate)
                
            if (not date_from and date_to and carPlate):  
                q = q.filter(TopUp.agent_code==agent_code)
                
            topUps = q.fetch()
            
            # create json
            data = []
            for topUp in topUps:
                data.append({
                             'agentCode': topUp.agent_code,
                             'carPlate': topUp.car_reg_no,
                             'date': DateTime.to_date_string(topUp.tran_date),
                             'subTotal': topUp.sub_total,
                             'commission': topUp.comm_amt,
                             'amount': topUp.amt,
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
        
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);
