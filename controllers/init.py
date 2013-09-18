from datalayer.appservice.admin.user import UserAppService
from datalayer.appservice.admin.systemsetting import SystemSettingAppService
from datalayer.appservice.admin.closing import ClosingAppService
from datalayer.viewmodels.viewmodels import UserViewModel, SystemSettingViewModel, ClosingViewModel
from sharelib.utils import DateTime

from datetime import timedelta

import webapp2

class Init(webapp2.RequestHandler):
    def get(self):
        # initialize data
        self.__create_system_setting()
        self.__create_closing()
        
        user_vm = UserViewModel()
        user_vm.code = '1'
        user_vm.name = '1'
        user_vm.pwd = '1'
        user_vm.level = 1
        
        user_as = UserAppService()
        user_as.create(user_vm)
        
    def __create_system_setting(self):
        vm = SystemSettingViewModel()
        vm.tag_sell_price = 10
        vm.register_value = 10
        vm.reset_duration = 2
        
        app = SystemSettingAppService()
        app.create(vm)
        
    def __create_closing(self):
        vm = ClosingViewModel()
        vm.closing_date = DateTime.malaysia_today() - timedelta(days=1)
        
        app = ClosingAppService()
        app.create(vm)