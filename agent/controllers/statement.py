from agent.controllers.base import BaseHandler
from sharelib.utils import DateTime
from datalayer.models.models import Agent
from datalayer.viewmodels.viewmodels import AgentViewModel
from datalayer.appservice.agent.account import AccountAppService

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
        
        template = JINJA_ENVIRONMENT.get_template('buy/statement.html')
        self.response.write(template.render(template_values))

