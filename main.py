import os

from app import db, create_app
from app.routes import app
from app.models import *

'''
   Se exponen dos métodos de ejecución: como aplicación standalone de python
   y para uso con algún WSGI como waitress o gunicorn.
'''
if __name__ == '__main__':
   app = create_app(os.getenv("APP_ENVIRONMENT"))
   app.run()
else:
   app = create_app(os.getenv("APP_ENVIRONMENT"))


