from app import db, create_app
from app.routes import app
from app.models import *

if __name__ == '__main__':
   app = create_app("development")
   app.run()


