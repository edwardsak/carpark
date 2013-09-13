from attendant.controllers.base import BaseHandler
from sharelib.utils import DateTime
from datalayer.models.models import Attendant
from datalayer.models.models import Charge
from datalayer.viewmodels.viewmodels import ChargeViewModel
from datalayer.appservice.attendant.charge import ChargeAppService


import os
import jinja2
import json

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

class Create(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_attendant = self.current_attendant()
        
        template_values = {
                           'title': 'Charge',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_attendant': current_attendant
                           }
        
        template = JINJA_ENVIRONMENT.get_template('charge/create.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        json_values = {}
        
        try:
            attendant_code = self.session['attendant_code']
            
            # get post data
            date = DateTime.to_date(self.request.get("date"))
            lot_no = self.request.get("lotNo")
            car_reg_no = self.request.get("carPlate")
    
            #save data to view model class
            vm = ChargeViewModel()
            vm.tran_date = date
            vm.attendant_code = attendant_code
            vm.lot_no = lot_no
            vm.car_reg_no = car_reg_no
      
            app_service = ChargeAppService()
            app_service.create(vm)
            
            json_values['returnStatus'] = True
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        json_str = json.dumps(json_values)
        self.response.out.write(json_str)
        
class Index(BaseHandler):
    def get(self):
        # validate agent is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_attendant = self.current_attendant()
        
        template_values = {
                           'title': 'Charge List',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_attendant': current_attendant
                           }
        
        template = JINJA_ENVIRONMENT.get_template('charge/index.html')
        self.response.write(template.render(template_values))

class Update(BaseHandler):
    def get(self, code):
        # validate admin is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_attendant = self.current_attendant()
        
        attendant = Attendant.query(Attendant.code==code).get()
        
        template_values = {
                           'title': 'Update Profile',
                           'current_attendant': current_attendant,
                           'attendant': attendant
                           } 
        
        template = JINJA_ENVIRONMENT.get_template('account/update.html')
        self.response.write(template.render(template_values))
        
    def post(self, code):
        json_values = {}
        
        try:
            name = self.request.get('name')
            address = self.request.get('address')
            tel = self.request.get('tel')
            hp = self.request.get('hp')
            email = self.request.get('email')
            last_modified = self.request.get('lastModified')
            
            attendant = Attendant.query(Attendant.code==code).get()
            
            vm = ChargeViewModel()
            vm.code = code
            vm.name = name
            vm.address = address
            vm.tel = tel
            vm.hp = hp
            vm.email = email
            vm.account_type = attendant.account_type
            vm.active = True
            vm.last_modified = last_modified
            
            app_service = ChargeAppService()
            app_service.update(vm)
        
            json_values['returnStatus'] = True
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
        
        json_str = json.dumps(json_values)
        self.response.out.write(json_str);
        
class Search(BaseHandler):
    def post(self):
        json_values = {}
        
        try:
            date_from = self.request.get('dateFrom')
            date_to = self.request.get("dateTo")
            lot_no = self.request.get("lotNo")
            car_reg_no = self.request.get("carPlate")
            current_attendant = self.current_attendant()
            attendant_code = current_attendant.code
            
            q = Charge.query()
            
            if date_from and len(date_from) > 0:
                date_from = DateTime.to_date(date_from)
                q = q.filter(Charge.tran_date>=date_from)
                
            if date_to and len(date_to) > 0:
                date_to = DateTime.to_date(date_to)
                q = q.filter(Charge.tran_date<=date_to)
            
            if lot_no:
                q = q.filter(Charge.lot_no==lot_no)
            
            if car_reg_no:
                q = q.filter(Charge.car_reg_no==car_reg_no)
                
            if (not date_from and date_to and lot_no and car_reg_no):    
                q = q.filter(Charge.attendant_code==attendant_code)          
                
            charges = q.fetch()
            
            # create json
            data = []
            for charge in charges:
                data.append({
                             'attendantCode': charge.attendant_code,
                             'date': DateTime.to_date_string(charge.tran_date),
                             'lotNo': charge.lot_no,
                             'carPlate': charge.car_reg_no,
                             'remark': charge.remark,
                             })

            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex) 
            
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);
