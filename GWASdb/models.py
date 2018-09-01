# Import SQLAlchemy class from Flask-SQLAlchemy
#from GWASdb import app
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

# Create a variable, db, which holds a usable instance of the SQLAlchemy class
db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120), unique=True)
	pwdhash = db.Column(db.String(54))

	def __init__(self, firstname, lastname, email, password):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.set_password(password)

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

	def __str__(self):
		return self.__name__

class Population(db.Model):
	__tablename__ = 'population'
	population_id = db.Column(db.Integer(), primary_key = True)
	organism = db.Column(db.String(100))
	population = db.Column(db.String(100))
	description = db.Column(db.String(250))
	growouts = db.relationship('Growout', backref='population', lazy='dynamic')

	def __init__(self, organism, population, description):
		self.organism = organism
		self.population = population
		self.description = description

	def __str__(self):
		return self.__name__

class Growout(db.Model):
	#__tablename__ = 'growout'
	growout_id = db.Column(db.Integer(), primary_key = True)
	location = db.Column(db.String(100))
	year = db.Column(db.String(4))
	tissue = db.Column(db.String(100))
	treatment = db.Column(db.String(250))
	population_id = db.Column(db.Integer, db.ForeignKey('population.population_id'))

	def __init__(self, location, year, tissue, treatment):
		self.location = location
		self.year = year
		self.tissue = tissue
		self.treatment = treatment

	def __str__(self):
		return self.__name__

#class GWAStudy(db.Model):
#	__tablename__ = 'gwas_metadata'
#	gwas_id = db.Column(db.Integer(), primary_key = True)
#	growout_location = db.Column(db.String(100))
#	growout_year = db.Column(db.Integer())
#	tissue = db.Column(db.String(100))
#	treatment = db.Column(db.String(100))
#	gwas_program = db.Column(db.String(100))
#	gwas_model = db.Column(db.String(100))
#	genome_version = db.Column(db.String(100))
#	marker_set = db.Column(db.Integer())
#
#	def __init__(self, organism, description, growout_location, growout_year, tissue, treatment, gwas_program, gwas_model, genome_version, marker_set):
#		self.growout_location = growout_location
#		self.growout_year = growout_year
#		self.tissue = tissue
#		self.treatment = treatment
#		self.gwas_model = gwas_model
#		self.genome_version = genome_version
#		self.marker_set = marker_set
#
#	def __repr__(self):
#		return '<GWAStudy %r>' % self.organism
