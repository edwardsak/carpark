from sharelib.session import SessionHandler
from datalayer.models.models import Attendant

class BaseHandler(SessionHandler):
    def current_attendant(self):
        if not hasattr(self, "_current_attendant"):
            self._current_attendant = None
            code = self.session.get("attendant_code")
            
            if code:
                q = Attendant.query(Attendant.code == str(code))
                obj = q.get()
                
                self._current_attendant = obj
        
        return self._current_attendant
    
    def authenticate(self):
        code = self.session.get('attendant_code')
        
        if code is None or len(str(code)) <= 0:
            self.redirect('/attendant/account/login/')
            return False
        
        return True