import sae
from www import wsgi

application = sae.create_wsgi_app(wsgi.application)
