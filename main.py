from controllers import home, init
from admin.controllers import home as admin_home, account as admin_account, user as admin_user, agent as admin_agent, attendant as admin_attendant, customer as admin_customer, closing as admin_closing
from admin.controllers.reports import dailyprofit, monthlyprofit, dailycharge, monthlycharge, dailychargebyattendant, monthlychargebyattendant, dailytopup, monthlytopup 
from admin.controllers.summaryreports import agentbuy, agentdeposit, agentregister, agenttopup
from agent.controllers import home as agent_home, account as agent_account, buy as agent_buy, deposit as agent_deposit, register as agent_register, topup as agent_topup, statement as agent_statement
from attendant.controllers import home as attendant_home, account as attendant_account, charge as attendant_charge
from customer.controllers import home as customer_home, account as customer_account, statement as customer_statement
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
                            ('/admin/account/update/([^/]+)/', admin_account.Update),
                            ('/admin/account/login/', admin_account.Login),
                            ('/admin/account/logout/', admin_account.Logout),
                            ('/admin/account/resetpwd/', admin_account.ResetPwd),
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
                            
                            ('/admin/closing/', admin_closing.Index),
                            ('/admin/closing/lock/', admin_closing.Lock),
                            ('/admin/closing/unlock/', admin_closing.Unlock),
                            ('/admin/closing/close/', admin_closing.Close),
                            ('/admin/closing/revert/', admin_closing.Revert),
                            
                            ('/admin/reports/profitbyday/', dailyprofit.DailyProfit),
                            ('/admin/reports/profitbymonth/', monthlyprofit.MonthlyProfit),
                            ('/admin/reports/chargebyday/', dailycharge.DailyCharge),
                            ('/admin/reports/chargebymonth/', monthlycharge.MonthlyCharge),
                            ('/admin/reports/chargebydayandattendant/', dailychargebyattendant.DailyAttendantCharge),
                            ('/admin/reports/chargebymonthandattendant/', monthlychargebyattendant.MonthlyAttendantCharge),
                            ('/admin/reports/topupbyday/', dailytopup.DailyTopUp),
                            ('/admin/reports/topupbymonth/', monthlytopup.MonthlyTopUp),
                            
                            ('/admin/summaryreports/buybyagent/', agentbuy.BuyByAgent),
                            ('/admin/buy/detail/([^/]+)/', agentbuy.BuyDetail),
                            ('/admin/summaryreports/depositbyagent/', agentdeposit.DepositByAgent),
                            ('/admin/deposit/detail/([^/]+)/', agentdeposit.DepositDetail),
                            ('/admin/summaryreports/registerbyagent/', agentregister.RegisterByAgent),
                            ('/admin/register/detail/([^/]+)/', agentregister.RegisterDetail),
                            ('/admin/register/car/detail/([^/]+)/', agentregister.RegisterCarDetail),
                            ('/admin/summaryreports/topupbyagent/', agenttopup.TopUpByAgent),
                            ('/admin/topup/detail/([^/]+)/', agenttopup.TopUpDetail),
                            
                            ('/agent/', agent_home.Index),
                            ('/agent/about/', agent_home.About),
                            ('/agent/account/update/([^/]+)/', agent_account.Update),
                            ('/agent/account/login/', agent_account.Login),
                            ('/agent/account/logout/', agent_account.Logout),
                            ('/agent/account/changepwd/', agent_account.ChangePwd),
                            
                            ('/agent/buy/', agent_buy.Index),
                            ('/agent/buy/create/', agent_buy.Create),
                            ('/agent/buy/search/', agent_buy.Search),
                            ('/agent/buy/receipt/([^/]+)/', agent_buy.Receipt),
                            ('/agent/deposit/', agent_deposit.Index),
                            ('/agent/deposit/create/', agent_deposit.Create),
                            ('/agent/deposit/search/', agent_deposit.Search),
                            ('/agent/deposit/receipt/([^/]+)/', agent_deposit.Receipt),
                            ('/agent/register/', agent_register.Index),
                            ('/agent/register/create/', agent_register.Create),
                            ('/agent/register/search/', agent_register.Search),
                            ('/agent/register/receipt/([^/]+)/', agent_register.Receipt),
                            ('/agent/topup/', agent_topup.Index),
                            ('/agent/topup/create/', agent_topup.Create),
                            ('/agent/topup/search/', agent_topup.Search),
                            ('/agent/topup/receipt/([^/]+)/', agent_topup.Receipt),
                            ('/agent/statement/', agent_statement.Statement),
                            
                            
                            ('/attendant/', attendant_home.Index),
                            ('/attendant/about/', attendant_home.About),
                            ('/attendant/account/update/([^/]+)/', attendant_account.Update),
                            ('/attendant/account/login/', attendant_account.Login),
                            ('/attendant/account/logout/', attendant_account.Logout),
                            ('/attendant/account/changepwd/', attendant_account.ChangePwd),
                            ('/attendant/charge/', attendant_charge.Index),
                            ('/attendant/charge/create/', attendant_charge.Create),
                            ('/attendant/charge/search/', attendant_charge.Search),
                            
                            ('/customer/', customer_home.Index),
                            ('/customer/about/', customer_home.About),
                            ('/customer/home/balance/', customer_home.Balance),
                            ('/customer/account/update/([^/]+)/', customer_account.Update),
                            ('/customer/account/login/', customer_account.Login),
                            ('/customer/account/logout/', customer_account.Logout),
                            ('/customer/account/changepwd/', customer_account.ChangePwd),
                            ('/customer/statement/([^/]+)/', customer_statement.Statement),
                            
                            ('/init/', init.Init),
                            ('/datalayer/test/([^/]+)/', datalayer_test.Test),
                            
							], debug=True, config=config)
