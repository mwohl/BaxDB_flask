# Import app
from GWASdb import app
from flask import Flask, render_template, request, flash, session, redirect, url_for, jsonify
from flask.ext.mail import Message, Mail
from models import db, User, Population, Growout
from forms import ContactForm, SignupForm, SigninForm, AddPopulationForm, SelectExistingPopulationForm, genomeVersionForm, phenotypeFileForm
import logging
from logging.handlers import RotatingFileHandler
import os.path
from werkzeug import secure_filename

#from flask.ext.storage import get_default_storage_class
#from flask.ext.uploads import delete, init, save, Upload

# NOTE TO SELF: Log by saying app.logger.info("logthis!")

#mail = Mail()
#mail.init_app(app)

def allowed_file(filename):
	return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Maps function that renders home.html to the index URL
@app.route('/')
def index():
    return render_template('home.html')

# Maps function that renders about.html to about URL
@app.route('/about')
def about():
	return render_template('about.html')

# Maps function for rendering contact form to contact URL
@app.route('/contact', methods=['GET', 'POST'])
def contact():
	form = ContactForm()
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('contact.html', form=form)
		else:
			msg = Message(form.subject.data, sender='molly.wohl@gmail.com', recipients=['molly.wohl@gmail.com'])
			msg.body = """
			From: %s <%s>
			%s
			""" % (form.name.data, form.email.data, form.message.data)
			mail.send(msg)

			return render_template('contact.html', success=True)

	elif request.method == 'GET':
		return render_template('contact.html', form=form)

# Maps function for rendering signup form for registering new users
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()

	if 'email' in session:
		return redirect(url_for('profile'))

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:
			# Adds a new user to the User table in the database
			newuser = User(form.firstname.data, form.lastname.data ,form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()

			# Signs a new user in
			session['email'] = newuser.email
			return redirect(url_for('profile'))

	elif request.method == 'GET':
		return render_template('signup.html', form=form)

# URL Mapping for user signing in
@app.route('/signin', methods=['GET', 'POST'])
def signin():
	form = SigninForm()

	if 'email' in session:
		return redirect(url_for('profile'))

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signin.html', form=form)
		else:
			session['email'] = form.email.data
			return redirect(url_for('profile'))
	elif request.method == 'GET':
		return render_template('signin.html', form=form)

# URL Mapping for signing out a user
@app.route('/signout')
def signout():
	if 'email' not in session:
		return redirect(url_for('signin'))

	session.pop('email', None)
	return redirect(url_for('index'))


@app.route('/profile')
def profile():
	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		return redirect(url_for('signup'))
	else:
		return render_template('profile.html')

#@app.route('/gwasresult')
#def gwasresult():
#	return render_template('gwasresult.html')

### BELOW: attempt to make a single route for /addpopulation that handles cases of selecting existing population and of adding a new pop
@app.route('/addPopulation', methods=['GET', 'POST'])
def addPopulation():
	formA = SelectExistingPopulationForm()
	formA.organism.choices = [(org[0], org[0]) for org in db.session.query(Population.organism.distinct())]
	formA.population.choices = [(result.population, result.population) for result in Population.query.all()]
	formB = AddPopulationForm()
	if request.method == 'POST':
		if formA.validate() == False:
			return render_template('addPopulation.html', formA=formA, formB = formB)
		else:
			session['myOrg'] = str(formA.organism.data)
			session['myPop'] = str(formA.population.data)
			return redirect(url_for('addGenotype'))
	elif request.method == 'GET':
		return render_template('addPopulation.html', formA=formA, formB = formB) #, population=session.get('population'))
###

@app.route('/addGenotype', methods=['GET', 'POST'])
def addGenotype():
	#return render_template('addGenotype.html')
	form = genomeVersionForm()
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('addGenotype.htlm', form=form)
		else:
			session['myGenVers'] = str(form.genomeVersion.data)
			return redirect(url_for('addPhenotype'))
	elif request.method == 'GET':
		return render_template('addGenotype.html', form=form)

@app.route('/addPhenotype', methods=['GET', 'POST'])
def addPhenotype():
	form = phenotypeFileForm()
	if request.method == "POST":
		f = request.files['phenotypeFile']
		if f and allowed_file(f.filename):
			filename = secure_filename(f.filename)
			f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('addDataProcessing'))
	elif request.method == 'GET':
		return render_template('addPhenotype.html', form=form)

@app.route('/addDataProcessing')
def addDataProcessing():
       return render_template('addDataProcessing.html')

@app.route('/addGWAS')
def addGWAS():
       return render_template('addGWAS.html')

@app.route('/addResult')
def addResult():
       return render_template('addResult.html')

@app.route('/testAJAX', methods=['POST'])
def testAJAX():
    app.logger.info("BEFORE")
    app.logger.info(request)
    app.logger.info(request.get_json())
    app.logger.info("AFTER")
    organism = request.get_json()
    # put code here to render the selectExistingPopulation form WITH the organism passed into getPopulation()???!?
    organismsPopulations = Population.query.filter_by(organism=organism).all()
    app.logger.info("organism: " + organism)
    app.logger.info(organismsPopulations)

    popList = []
    for orgPopulation in organismsPopulations:
    	popList.append(orgPopulation.population)
    #for thingy in organismsPopulations:
    #	app.logger.info("thingy: " + thingy.population)
    return jsonify(popList = popList);
    #return render_template('404.html'), 404
    # return jsonify()

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500


##########################################
#@app.route('/addpopulation', methods=['GET', 'POST'])
#def addpopulation():
#	form = AddPopulationForm()
#
#	existingPopulations = [(p.organism, p.population) for p in Population.query]
#
#	app.logger.info(existingPopulations)
#
#	return render_template('addpopulation.html', form=form, existingPopulations=existingPopulations)
#
#	if request.method == 'POST':
#		if form.validate() == False:
#			return render_template('addpopulation.html', form=form)
#		else:
#			newPopulation = Population(form.organism.data, form.population.data, form.description.data)
#			db.session.add(newPopulation)
#			db.session.commit()
#			return redirect(url_for('gwasresult'))
#
#	elif request.method == 'GET':
#		return render_template('addpopulation.html', form=form)
#
#@app.route('/addpopulation', methods=['GET', 'POST'])		
#def getExistingPopulations():
#	existingPopulations = [(p.organism, p.population) for p in Population.query.all()]
#	return existingPopulations
#
#@app.route('/addpopulation', methods=['GET', 'POST'])	
#def selectpopulation():
#	form = SelectExistingPopulationForm(existingPopulations)
#	form.option.choices = existingPopulations
#	
#	if request.method == 'GET':
#			return render_template('addpopulation.html', form = form, existingPopulations = form.option.choices)
#
######################################################################################################

	


#			
# Maps function for rendering a form for adding a new GWAS
#@app.route('/addgwas', methods=['GET', 'POST'])
#def addgwas():
#	form = AddGWASForm()
#
#	if request.method == 'POST':
#		if form.validate() == False:
#			return render_template('addgwas.html', form=form)
#		else:
#			newGWAS = GWAStudy(form.organism.data, form.description.data, form.growout_location.data, form.growout_year.data, form.tissue.data, form.treatment.data, form.gwas_program.data, form.gwas_model.data, form.genome_version.data, form.marker_set.data)
#			db.session.add(newGWAS)
#			db.session.commit()
#			return redirect(url_for('gwasresult'))
#
#	elif request.method == 'GET':
#		return render_template('addgwas.html', form=form)

# Maps function that greets user to URL 'usr/<name>'
#@app.route('/user/<name>')
#def user(name):
#    return '<h1>Hello, %s!</h1>' % name
#
#@app.route('/testdb')
#def testdb():
#	if db.session.query("1").from_statement("SELECT 1").all():
#		return 'It works.'
#	else:
#		return 'Something is broken.'
