from models.models import User

import webapp2

class Index(webapp2.RequestHandler):
    def get(self):
        users = User.query().fetch()
        
        self.response.write("Hello world!")