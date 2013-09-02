from sharelib.session import SessionHandler
from datalayer.models.models import User

class BaseHandler(SessionHandler):
    def current_user(self):
        if not hasattr(self, "_current_user"):
            self._current_user = None
            code = self.session.get("user_code")
            
            if code:
                q = User.query(User.code == str(code))
                obj = q.get()
                
                self._current_user = obj
        
        return self._current_user
    
    def authenticate(self):
        code = self.session.get('user_code')
        
        if code is None or len(str(code)) <= 0:
            self.redirect('/admin/account/login/')
            return False
        
        return True