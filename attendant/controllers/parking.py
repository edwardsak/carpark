from attendant.controllers.base import BaseHandler
from sharelib.utils import DateTime

import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

class Charge(BaseHandler):
    def get(self):
        # validate attendant is logined or not
        # if not redirect to login page
        #if self.authenticate() == False:
        #    return
        
        #current_attendant = self.current_attendant()
        
        template_values = {
                           'title': 'Charge',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           #'current_attendant': current_attendant
                           }
        
        template = JINJA_ENVIRONMENT.get_template('parking/charge.html')
        self.response.write(template.render(template_values))
        
class ChargeList(BaseHandler):
    def get(self):
        # validate attendant is logined or not
        # if not redirect to login page
        #if self.authenticate() == False:
        #    return
        
        #current_attendant = self.current_attendant()
        
        template_values = {
                           'title': 'Charge List',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           #'current_attendant': current_attendant
                           }
        
        template = JINJA_ENVIRONMENT.get_template('parking/chargeList.html')
        self.response.write(template.render(template_values))