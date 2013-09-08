from controllers import home, init
from admin.controllers import home as admin_home, account as admin_account, user as admin_user, agent as admin_agent, attendant as admin_attendant, customer as admin_customer
from agent.controllers import home as agent_home, account as agent_account, buy as agent_buy, deposit as agent_deposit, register as agent_register, topup as agent_topup, statement as agent_statement
from attendant.controllers import home as attendant_home, account as attendant_account, parking as attendant_parking
from customer.controllers import home as customer_home, account as customer_account
from datalayer import test as datalayer_test


import webapp2

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([
                            ('/', home.Index),
                            
                            ('/admin/', admin_home.Index),
                            ('/admin/about/', admin_home.About),
                            ('/admin/account/', admin_account.Index),
                            ('/admin/account/login/', admin_account.Login),
                            ('/admin/account/logout/', admin_account.Logout),
                            ('/admin/account/changepwd/', admin_account.ChangePwd),
                            
                            ('/admin/user/', admin_user.Index),
                            ('/admin/user/create/', admin_user.Create),
                            ('/admin/user/update/([^/]+)/', admin_user.Update),
                            ('/admin/user/search/', admin_user.Search),
                            
                            ('/admin/agent/', admin_agent.Index),
                            ('/admin/agent/create/', admin_agent.Create),
                            ('/admin/agent/update/([^/]+)/', admin_agent.Update),
                            ('/admin/agent/search/', admin_agent.Search),
                            
                            ('/admin/attendant/', admin_attendant.Index),
                            ('/admin/attendant/create/', admin_attendant.Create),
                            ('/admin/attendant/update/([^/]+)/', admin_attendant.Update),
                            ('/admin/attendant/search/', admin_attendant.Search),
                            
                            ('/admin/customer/', admin_customer.Index),
                            ('/admin/customer/create/', admin_customer.Create),
                            ('/admin/customer/update/([^/]+)/', admin_customer.Update),
                            ('/admin/customer/search/', admin_customer.Search),
                            
                            ('/agent/', agent_home.Index),
                            ('/agent/about/', agent_home.About),
                            ('/agent/account/update/([^/]+)/', agent_account.Update),
                            ('/agent/account/login/', agent_account.Login),
                            ('/agent/account/changepwd/', agent_account.ChangePwd),
                            
                            ('/agent/buy/', agent_buy.Index),
                            ('/agent/buy/create/', agent_buy.Create),
                            ('/agent/buy/search/', agent_buy.Search),
                            ('/agent/deposit/', agent_deposit.Index),
                            ('/agent/deposit/create/', agent_deposit.Create),
                            ('/agent/deposit/search/', agent_deposit.Search),
                            ('/agent/register/', agent_register.Index),
                            ('/agent/register/create/', agent_register.Create),
                            ('/agent/register/search/', agent_register.Search),
                            ('/agent/topup/', agent_topup.Index),
                            ('/agent/topup/create/', agent_topup.Create),
                            ('/agent/topup/search/', agent_topup.Search),
                            
                            ('/attendant/', attendant_home.Index),
                            ('/attendant/about/', attendant_home.About),
                            ('/attendant/account/', attendant_account.Index),
                            ('/attendant/account/login/', attendant_account.Login),
                            ('/attendant/account/changepwd/', attendant_account.ChangePwd),
                            ('/attendant/parking/charge/', attendant_parking.Charge),
                            ('/attendant/parking/charge/list/', attendant_parking.ChargeList),
                            
                            ('/customer/', customer_home.Index),
                            ('/customer/about/', customer_home.About),
                            ('/customer/account/', customer_account.Index),
                            ('/customer/account/login/', customer_account.Login),
                            ('/customer/account/changepwd/', customer_account.ChangePwd),
                            
                            ('/init/', init.Init),
                            ('/datalayer/test/([^/]+)/', datalayer_test.Test),
                            
							], debug=True, config=config)
