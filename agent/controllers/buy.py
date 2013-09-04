from agent.controllers.base import BaseHandler
from sharelib.utils import DateTime

import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

class Statement(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        #if self.authenticate() == False:
        #    return
        
        #current_agent = self.current_agent()
        
        template_values = {
                           'title': 'Statement',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           #'current_agent': current_agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('buy/statement.html')
        self.response.write(template.render(template_values))

class Tag(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        #if self.authenticate() == False:
        #    return
        
        #current_agent = self.current_agent()
        
        template_values = {
                           'title': 'Buy Tag',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           #'current_agent': current_agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('buy/tag.html')
        self.response.write(template.render(template_values))
        
class TagList(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        #if self.authenticate() == False:
        #    return
        
        #current_agent = self.current_agent()
        
        template_values = {
                           'title': 'Buy Tag List',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           #'current_agent': current_agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('buy/tagList.html')
        self.response.write(template.render(template_values))
   
class Deposit(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        #if self.authenticate() == False:
        #    return
        
        #current_agent = self.current_agent()
        
        template_values = {
                           'title': 'Deposit',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           #'current_agent': current_agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('buy/deposit.html')
        self.response.write(template.render(template_values))
        
class DepositList(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        #if self.authenticate() == False:
        #    return
        
        #current_agent = self.current_agent()
        
        template_values = {
                           'title': 'Deposit List',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           #'current_agent': current_agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('buy/depositList.html')
        self.response.write(template.render(template_values))
        
class Create(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        #if self.authenticate() == False:
        #    return
        
        #current_agent = self.current_agent()
        
        template_values = {
                           'title': 'Customer Register',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           #'current_agent': current_agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('buy/create.html')
        self.response.write(template.render(template_values))
        
class CreateList(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        #if self.authenticate() == False:
        #    return
        
        #current_agent = self.current_agent()
        
        template_values = {
                           'title': 'Customer Register List',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           #'current_agent': current_agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('buy/createList.html')
        self.response.write(template.render(template_values))

class Topup(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        #if self.authenticate() == False:
        #    return
        
        #current_agent = self.current_agent()
        
        template_values = {
                           'title': 'Customer Top Up',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           #'current_agent': current_agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('buy/topup.html')
        self.response.write(template.render(template_values))
        
class TopupList(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        #if self.authenticate() == False:
        #    return
        
        #current_agent = self.current_agent()
        
        template_values = {
                           'title': 'Customer Top Up List',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           #'current_agent': current_agent
                           }
        
        template = JINJA_ENVIRONMENT.get_template('buy/topupList.html')
        self.response.write(template.render(template_values))