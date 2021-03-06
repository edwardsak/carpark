from agent.controllers.base import BaseHandler
from sharelib.utils import DateTime
from datalayer.models.models import Agent
from datalayer.appservice.agent.statement import Statement as AgentStatement

import os
import jinja2
import json

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

class Statement(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_agent = self.current_agent()
        agents = Agent.query().fetch()
        
        template_values = {
                           'title': 'Statement',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_agent': current_agent,
                           'agents': agents
                           }
        
        template = JINJA_ENVIRONMENT.get_template('statement/index.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        json_values = {}
        
        try:
            #get
            current_agent = self.current_agent()
            
            agent_code = current_agent.code
            tran_date = DateTime.to_date(self.request.get('date'))
            
            agent_statement = AgentStatement()
            values = agent_statement.get(agent_code, tran_date)
            
            data = []
            for value in values:
                data.append({
                             'tranDate': DateTime.to_date_string(value.tran_date),
                             'tranCode': value.tran_code,
                             'description': value.description,
                             'dbAmt': value.db_amt,
                             'crAmt': value.cr_amt,
                             'balAmt': value.bal_amt
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        json_str = json.dumps(json_values)
        self.response.out.write(json_str)
