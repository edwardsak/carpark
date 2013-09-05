from sharelib.session import SessionHandler
from datalayer.models.models import Customer

class BaseHandler(SessionHandler):
    def current_customer(self):
        if not hasattr(self, "_current_customer"):
            self.current_customer = None
            code = self.session.get("customer_code")
            
            if code:
                q = Customer.query(Customer.code == str(code))
                obj = q.get()
                
                self._current_customer = obj
        
        return self.current_customer
    
    def authenticate(self):
        code = self.session.get('customer_code')
        
        if code is None or len(str(code)) <= 0:
            self.redirect('/customer/account/login/')
            return False
        
        return True