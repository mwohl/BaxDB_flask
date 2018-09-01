from flask import Flask, render_template

# Instantiate Flask application
app = Flask(__name__)

# Load configuration from separate file
app.config.from_pyfile('../config.py')

# Import models and sqlalchemy
from models import *

# Bind db object from models to app so database is accessible through db
db.init_app(app)

from flask.ext.bootstrap import Bootstrap
Bootstrap(app)

from routes import *

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
#    file_handler = RotatingFileHandler('var/log/GWASdb/GWASdbApplication.log', maxBytes=10000, backupCount=3)
    file_handler = RotatingFileHandler('var/www/logs/GWASdbApplication.log', maxBytes=10000, backupCount=3)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

# Runs the flask application with logging enabled
if __name__ == '__main__':
    app.run()
    app.logger.warning('A warning occurred')
    app.logger.error('An error occurred')
    app.logger.info('Info')
