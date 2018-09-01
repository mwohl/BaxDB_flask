# Import necessary classes from Flask-WTF extension
from GWASdb import app
from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField, SubmitField, PasswordField, SelectField, FormField, FileField
from wtforms.validators import InputRequired, Email, ValidationError
from wtforms.fields.html5 import EmailField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask.ext.sqlalchemy import get_debug_queries
from models import db, User, Population, Growout
import logging

# Contact Form class - inherits from base Form class from Flask-WTF
class ContactForm(Form):
	name = TextField("Name", validators=[InputRequired("Please enter your name.")])
	email = EmailField("Email", validators=[InputRequired("Please enter your email address."), Email("Please enter a valid email address.")])
	subject = TextField("Subject", validators=[InputRequired("Please enter a subject.")])
	message = TextAreaField("Message", validators=[InputRequired("Please enter a message.")])
	submit = SubmitField("Send")

class SignupForm(Form):
	firstname = TextField("First name", validators=[InputRequired("Please enter your first name.")])
	lastname = TextField("Last name", validators=[InputRequired("Please enter your last name.")])
	email = EmailField("Email", validators=[InputRequired("Please enter your email address."), Email("Please enter a valid email address.")])
	password = PasswordField("Password", validators=[InputRequired("Please enter a password.")])
	submit = SubmitField("Create account")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user:
			self.email.errors.append("That email is already taken")
			return False
		else:
			return True

class SigninForm(Form):
	email = EmailField("Email", validators=[InputRequired("Please enter your email address."), Email("Please enter a valid email address.")])
	password = PasswordField("Password", validators=[InputRequired("Please enter your password.")])
	submit = SubmitField("Sign In")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user and user.check_password(self.password.data):
			return True
		else:
			self.email.errors.append("You have entered an invalid email or password")
			return False

class AddPopulationForm(Form):
	organism = TextField("Organism", validators=[InputRequired("Please enter an organism.")])
	population = TextField("Population", validators=[InputRequired("Please enter the population.")])
	description = TextAreaField("Description")
	submit = SubmitField("Add Population")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

class SelectExistingPopulationForm(Form):
	def getOrganisms():
		return Population.query
	
	def getPopulations():
		#return Population.query.filter_by(organism='Soybean').all()
		return Population.query.filter_by().all()

	#def string selectedOrganism
	#def getPopulations():
	#	return Population.query.filter_by(organism=selectedOrganism).all()

	# all you do here is write another function that USES getPopulations() and narrows down the results according to organism
	# then this new function is the query_factory for the population field


	#organism = QuerySelectField(query_factory = getOrganisms, get_label='organism', allow_blank=True, validators=[InputRequired("Please select an organism.")])
	#population = QuerySelectField(query_factory = getPopulations, get_label='population', allow_blank=True, validators=[InputRequired("Please select a population.")])
	organism = SelectField()
	population = SelectField()
	submit = SubmitField("Select Population")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

class genomeVersionForm(Form):
	genomeVersion = TextField("genome version", validators=[InputRequired("Please enter the genome version used in the current GWAS.")])			
	submit = SubmitField("Continue")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		myChoices = [(org, org) for org in db.session.query(Population.organism.distinct())]
		for i in range(len(myChoices)):
			for j in range(len(myChoices[i])):
				for k in range(len(myChoices[i][j])):
					app.logger.info(myChoices[i][j][k])

	def validate(self):
		if not Form.validate(self):
			return False

class phenotypeFileForm(Form):
	phenotypeFile = FileField("Upload Phenotype File")
	submit = SubmitField("Continue")

# WORKS- Form with nested addpop and selectpop forms
#class PopulationForm(Form):
#	AddPopulation = FormField(AddPopulationForm, "Add a New Population")
#	SelectExistingPopulation = FormField(SelectExistingPopulationForm, "Select an Existing Population")

# query_factory=fill_population_select, allow_blank=True	
#	selectPopulationOrganism = QuerySelectField(get_label='organism')
#	def getExistingPopulations():
#		existingPopulations = [(p.organism, p.population) for p in Population.query]
#		return existingPopulations

#	population = SelectField(u'Select an Existing Population')
#
#	def get_populations(request):
#		population = Population.query.order_by(Population.population)
#		form.population.choices = [(Population.organism, Population.population) for p in Population.query.order_by('organism')]
#
#	def fill_populations():
#		return Model.query
#
#	myPopulations = QuerySelectField(query_factory=fill_populations)

#class AddGWASForm(Form):
#	organism = TextField("Organism", validators=[InputRequired("Please enter an organism.")])
#	description = TextField("Description")
#	growout_location = TextField("Growout Location", validators=[InputRequired("Please enter the location of the growout sampled.")])
#	growout_year = TextField("Growout Year", validators=[InputRequired("Please enter the year in which samples were grown.")])
#	tissue = TextField("Tissue", validators=[InputRequired("Please enter the type of tissue sampled")])
#	treatment = TextField("Treatment", validators=[InputRequired("Please enter the type of treatment used or 'none' if no treatment.")])
#	gwas_program = TextField("GWAS Program Used", validators=[InputRequired("Please enter the GWAS Program used.")])
#	gwas_model = TextField("GWAS Model Used", validators=[InputRequired("Please enter the GWAS Model used.")])
#	genome_version = TextField("Genome Version Used", validators=[InputRequired("Please enter the genome version used.")])
#	marker_set = TextField("Marker Set Used", validators=[InputRequired("Please enter the marker set used.")])
#	submit = SubmitField("Add GWAS Experiment")
#
#	def __init__(self, *args, **kwargs):
#		Form.__init__(self, *args, **kwargs)
#
#	def validate(self):
#		if not Form.validate(self):
#			return False
