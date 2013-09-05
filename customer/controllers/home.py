from customer.controllers.base import BaseHandler
from datalayer.models.models import Customer

import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

class Index(BaseHandler):
    def get(self):
        # validate customer is logined or not
        # if not redirect to login page
        #if self.authenticate() == False:
        #    return
        
        #current_customer = self.current_customer()
        customers = Customer.query().fetch()
        
        template_values = {
                           'title': 'Customer Home',
                           #'current_customer': current_customer
                           'customers': customers
                           }
        
        template = JINJA_ENVIRONMENT.get_template('home/index.html')
        self.response.write(template.render(template_values))
        
class About(BaseHandler):
    def get(self):
        # validate customer is logined or not
        # if not redirect to login page
        #if self.authenticate() == False:
        #    return
        
        #current_customer = self.current_customer()
        
        template_values = {
                           'title': 'Attendant Home About',
                           #'current_customer': current_customer
                           }
        
        template = JINJA_ENVIRONMENT.get_template('home/about.html')
        self.response.write(template.render(template_values))