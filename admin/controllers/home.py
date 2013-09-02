from admin.controllers.base import BaseHandler

class Index(BaseHandler):
    def get(self):
        self.response.write("Hello Admin!")