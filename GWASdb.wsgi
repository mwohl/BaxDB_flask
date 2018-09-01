activate_this = '/var/www/GWASdb/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
sys.path.insert(0, '/var/www/GWASdb')
from GWASdb import app as application
