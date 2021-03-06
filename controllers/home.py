import webapp2

import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

class Index(webapp2.RequestHandler):
    def get(self):
        template_values = {
                           'title': 'Home'
                           }
        
        template = JINJA_ENVIRONMENT.get_template('home/index.html')
        self.response.write(template.render(template_values))