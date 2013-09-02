from controllers import home

import webapp2

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([
                            ('/', home.Index),
							], debug=True, config=config)
