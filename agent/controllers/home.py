from agent.controllers.base import BaseHandler

import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

class Index(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        #if self.authenticate() == False:
        #    return
        
        #current_agent = self.current_agent()
        
        template_values = {
                           'title': 'Agent Home',
                           #'current_agent': current_agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('home/index.html')
        self.response.write(template.render(template_values))