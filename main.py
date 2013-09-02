from controllers import home
from admin.controllers import home as admin_home
from agent.controllers import home as agent_home, account as agent_account, buy as agent_buy

import webapp2

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([
                            ('/', home.Index),
                            
                            ('/admin/', admin_home.Index),
                            
                            ('/agent/', agent_home.Index),
                            ('/agent/account/login/', agent_account.Login),
                            ('/agent/buy/', agent_buy.Index),
                            ('/agent/buy/create/', agent_buy.Create),
                            
							], debug=True, config=config)
