from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required, Email
## when you add validors, must add import

import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

@app.route('/')
def home():
    return "Hello, world!"

class itunesForm(FlaskForm):
	artist_name = StringField("Enter an artist's name", validators=[Required()])
	number_results = IntegerField("How many results would you like", validators=[Required()])
	your_email = StringField("Enter your email", validators=[Required(), Email()])
	my_submit = SubmitField("Submit")

@app.route('/itunes-form')
def itunes_form():
    simpleForm = itunesForm()
    return render_template('itunes-form.html', form=simpleForm) # HINT : create itunes-form.html to represent the form defined in your class

@app.route('/itunes-result', methods = ['GET', 'POST'])
def itunes_result():
    my_form = itunesForm(request.form)
    if request.method == 'POST' and my_form.validate_on_submit():
        artist_name = my_form.name.data
        number_results = my_form.number_results.data
        your_email = my_form.your_email.data
        params = {}
        params['term'] = artist_name
        params['limit'] = number_results
        response = requests.get('https://itunes.apple.com/search', params = params)
        response_py = json.loads(response.text)['results']
      
    flash('All fields are required!')
    return render_template('itunes-result.html', result_html = response_py)

if __name__ == '__main__':
    app.run()
