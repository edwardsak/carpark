from attendant.controllers.base import BaseHandler

import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

class Index(BaseHandler):
    def get(self):
        # validate attendant is logined or not
        # if not redirect to login page
        #if self.authenticate() == False:
        #    return
        
        #current_attendant = self.current_attendant()
        
        template_values = {
                           'title': 'Attendant Home',
                           #'current_attendant': current_attendant
                           }
        
        template = JINJA_ENVIRONMENT.get_template('home/index.html')
        self.response.write(template.render(template_values))
        
class About(BaseHandler):
    def get(self):
        # validate attendant is logined or not
        # if not redirect to login page
        #if self.authenticate() == False:
        #    return
        
        #current_attendant = self.current_attendant()
        
        template_values = {
                           'title': 'Attendant Home About',
                           #'current_attendant': current_attendant
                           }
        
        template = JINJA_ENVIRONMENT.get_template('home/about.html')
        self.response.write(template.render(template_values))