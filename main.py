from controllers import home
from admin.controllers import home as admin_home
from agent.controllers import home as agent_home, account as agent_account, buy as agent_buy
from attendant.controllers import home as attendant_home, account as attendant_account, parking as attendant_parking

import webapp2

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([
                            ('/', home.Index),
                            
                            ('/admin/', admin_home.Index),
                            
                            ('/agent/', agent_home.Index),
                            ('/agent/about/', agent_home.About),
                            ('/agent/account/', agent_account.Index),
                            ('/agent/account/login/', agent_account.Login),
                            ('/agent/account/changePwd/', agent_account.ChangePwd),
                            ('/agent/buy/statement/', agent_buy.Statement),
                            ('/agent/buy/tag/', agent_buy.Tag),
                            ('/agent/buy/tag/list/', agent_buy.TagList),
                            ('/agent/buy/create/', agent_buy.Create),
                            ('/agent/buy/create/list/', agent_buy.CreateList),
                            ('/agent/buy/deposit/', agent_buy.Deposit),
                            ('/agent/buy/deposit/list/', agent_buy.DepositList),
                            ('/agent/buy/topup/', agent_buy.Topup),
                            ('/agent/buy/topup/list/', agent_buy.TopupList),
                            
                            ('/attendant/', attendant_home.Index),
                            ('/attendant/about/', attendant_home.About),
                            ('/attendant/account/', attendant_account.Index),
                            ('/attendant/account/login/', attendant_account.Login),
                            ('/attendant/account/changePwd/', attendant_account.ChangePwd),
                            ('/attendant/parking/charge/', attendant_parking.Charge),
                            ('/attendant/parking/charge/list/', attendant_parking.ChargeList),
                            
							], debug=True, config=config)
