from customer.controllers.base import BaseHandler
from sharelib.utils import DateTime
from datalayer.models.models import Customer, Car, Register, TopUp, Charge, Tran
from datalayer.appservice.customer.statement import Statement as customerStatement

import os
import jinja2
import json

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

        
class Statement(BaseHandler):
    def get(self, reg_no):
        # validate admin is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_customer = self.current_customer()
        
        register = Register.query(Register.car_reg_no==reg_no).get()
        
        template_values = {
                           'title': 'Statement',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_customer': current_customer,
                           'register': register
                           }
        
        template = JINJA_ENVIRONMENT.get_template('statement/index.html')
        self.response.write(template.render(template_values))
        
    def post(self, reg_no):
        json_values = {}
            
        try:
            #get
            car_reg_no = self.request.get('reg_no')  
            tran_date = DateTime.malaysia_today()
                
            customer_statement = customerStatement()
            values = customer_statement.get(car_reg_no, tran_date)
            
            data = []
            for value in values:
                data.append({
                             'tranDate': DateTime.to_date_string(value.tran_date),
                             'tranCode': value.tran_code,
                             'description': value.description,
                             'dbAmt': value.db_amt,
                             'crAmt': value.cr_amt,
                             'balAmt': value.bal_amt
                             })
                
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        json_str = json.dumps(json_values)
        self.response.out.write(json_str)

class OldStatement(BaseHandler):       
    def get(self, reg_no):
        # validate admin is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_customer = self.current_customer()
        
        register = Register.query(Register.car_reg_no==reg_no).get()
        
        template_values = {
                           'title': 'Statement',
                           'today': DateTime.to_date_string(DateTime.malaysia_today()),
                           'current_customer': current_customer,
                           'register': register
                           }
        
        template = JINJA_ENVIRONMENT.get_template('statement/index.html')
        self.response.write(template.render(template_values))
        
    def post(self, reg_no):
        json_values = {}
        
        try:
            reg_no = self.request.get('reg_no')
            cars = Car.query(Car.reg_no==reg_no).fetch()
            car = cars[0]
            today_date = DateTime.malaysia_today()
            
            trans = Tran.query(
                               Tran.car_reg_no==reg_no,
                               Tran.tran_date==today_date
                               ).order(Tran.seq).fetch()
            
            registers = Register.query(
                                       Register.car_reg_no==reg_no,
                                       Register.tran_date==today_date
                                       ).fetch()
            
            topups = TopUp.query(
                                 TopUp.car_reg_no==reg_no, 
                                 TopUp.tran_date==today_date
                                 ).fetch()
            
            charges = Charge.query(
                                   Charge.car_reg_no==car.reg_no,
                                   Charge.tran_date==today_date
                                   ).fetch()
                                   
            # group by tran_code
            register_tran_codes = {}
            for register in registers:
                register_tran_codes[register.tran_code] = register
            
            topup_tran_codes = {}  
            for topup in topups:
                topup_tran_codes[topup.tran_code] = topup 
                
            charge_tran_codes = {}
            for charge in charges:
                charge_tran_codes[charge.tran_code] = charge
            
            # create json
            data = []
            bal_amt = 0
            for tran in trans:
                if register_tran_codes.has_key(tran.tran_code):
                    register = register_tran_codes[tran.tran_code]
                    bal_amt += register.sub_total 
                    bal_amt = round(bal_amt, 2)
                    data.append({
                                 'carRegNo': car.reg_no,
                                 'date': DateTime.to_date_string(register.tran_date),
                                 'description': register.tran_code,
                                 'dbAmt': register.sub_total,
                                 'crAmt': 0,
                                 'balAmt': bal_amt
                                 })
                    
                elif topup_tran_codes.has_key(tran.tran_code):
                    topup = topup_tran_codes[tran.tran_code]
                    bal_amt += topup.sub_total 
                    bal_amt = round(bal_amt, 2)
                    data.append({
                                 'carRegNo': car.reg_no,
                                 'date': DateTime.to_date_string(topup.tran_date),
                                 'description': topup.tran_code,
                                 'dbAmt': topup.sub_total,
                                 'crAmt': 0,
                                 'balAmt': bal_amt
                                 })
                
                elif charge_tran_codes.has_key(tran.tran_code):
                    charge = charge_tran_codes[tran.tran_code]
                    bal_amt -= charge.sub_total
                    bal_amt = round(bal_amt, 2)
                    data.append({
                                 'carRegNo': car.reg_no,
                                 'date': DateTime.to_date_string(charge.tran_date),
                                 'description': charge.tran_code,
                                 'dbAmt': 0,
                                 'crAmt': charge.sub_total,
                                 'balAmt': bal_amt
                                 })
                    
            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);
