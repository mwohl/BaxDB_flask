import os
from GWASdb import app

basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = '/var/www/GWASdb/uploads/test'
ALLOWED_EXTENSIONS = set(['txt','csv','xls','xlsx','rep'])

app.secret_key = 'nfwjhaoiwn153nlk84jslk8ns5'
CSRF_ENABLED = True

# SQLALCHEMY_DATABASE_URI = 
# SQLALCHEMY_COMMIT_ON_TEARDOWN =
# SQLALCHEMY_MIGRATE_REPO = 

