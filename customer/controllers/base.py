from sharelib.session import SessionHandler
from datalayer.models.models import Customer

class BaseHandler(SessionHandler):
    def current_customer(self):
        if not hasattr(self, "_current_customer"):
            self._current_customer = None
            ic = self.session.get("customer_ic")
            
            if ic:
                q = Customer.query(Customer.ic == str(ic))
                obj = q.get()
                
                self._current_customer = obj
        
        return self._current_customer
    
    def authenticate(self):
        code = self.session.get('customer_ic')
        
        if code is None or len(str(code)) <= 0:
            self.redirect('/customer/account/login/')
            return False
        
        return True