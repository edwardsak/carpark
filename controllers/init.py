from datalayer.appservice.admin.user import UserAppService
from datalayer.viewmodels.viewmodels import UserViewModel

import webapp2

class Init(webapp2.RequestHandler):
    def get(self):
        # initialize data
        user_vm = UserViewModel()
        user_vm.code = '1'
        user_vm.name = '1'
        user_vm.pwd = '1'
        user_vm.level = 1
        
        user_as = UserAppService()
        user_as.create(user_vm)