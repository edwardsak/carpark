from sharelib.session import SessionHandler
from datalayer.models.models import Agent

class BaseHandler(SessionHandler):
    def current_agent(self):
        if not hasattr(self, "_current_agent"):
            self._current_agent = None
            code = self.session.get("agent_code")
            
            if code:
                q = Agent.query(Agent.code == str(code))
                obj = q.get()
                
                self._current_agent = obj
        
        return self._current_agent
    
    def authenticate(self):
        code = self.session.get('agent_code')
        
        if code is None or len(str(code)) <= 0:
            self.redirect('/agent/account/login/')
            return False
        
        return True