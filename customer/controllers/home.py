from customer.controllers.base import BaseHandler
from sharelib.utils import DateTime
from datalayer.models.models import Customer
from datalayer.models.models import Car
from datalayer.models.models import Charge

import os
import jinja2
import json

JINJA_ENVIRONMENT = jinja2.Environment(
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')),
                                       extensions=['jinja2.ext.autoescape']
                                       )

class Index(BaseHandler):
    def get(self):
        # validate customer is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_customer = self.current_customer()
        
        # get car bal
        #cars = Car.query(Car.customer_ic==current_customer.ic).fetch()
        #bals = []
 
        #for car in cars:
            #bals.append({
            #'carPlate': car.reg_no,
            #'ic': car.customer_ic,
            #'bal': car.bal_amt
            #})
        
        template_values = {
                           'title': 'Balance',
                           'current_customer': current_customer,
                           'returnStatus': True,
                           #'bals': bals
                           }
        
        template = JINJA_ENVIRONMENT.get_template('home/index.html')
        self.response.write(template.render(template_values))
        
class About(BaseHandler):
    def get(self):
        # validate customer is logined or not
        # if not redirect to login page
        if self.authenticate() == False:
            return
        
        current_customer = self.current_customer()
        
        template_values = {
                           'title': 'Customer Home About',
                           'current_customer': current_customer
                           }
        
        template = JINJA_ENVIRONMENT.get_template('home/about.html')
        self.response.write(template.render(template_values))
        
class Balance(BaseHandler):
    def post(self):
        json_values = {}
        
        try:
            ic = self.request.get('ic')
            
            cars = Car.query(Car.customer_ic==ic).fetch()    
            
            # create json
            data = []
            for car in cars:
                charges = Charge.query(Charge.car_reg_no==car.reg_no).fetch()
                
                amt = 0
                for charge in charges:
                    amt += charge.sub_total
                
                data.append({
                             'carRegNo': car.reg_no,
                             'chargeAmt': amt,
                             'balAmt': car.bal_amt
                             })

            json_values['returnStatus'] = True
            json_values['data'] = data
        except Exception, ex:
            json_values['returnStatus'] = False
            json_values['returnMessage'] = str(ex)
            
        jsonStr = json.dumps(json_values)
        self.response.out.write(jsonStr);