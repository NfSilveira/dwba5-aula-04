from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '5f70306f0b891ef83ac5c56fb7e0986c'

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('Informe o seu nome:', validators=[DataRequired()])
    surname = StringField('Informe o seu sobrenome:', validators=[DataRequired()])
    school_name = StringField('Informe a sua instituição de ensino:', validators=[DataRequired()])
    course_options = [('dswa5', 'DSWA5'), ('dwba4', 'DWBA4'), ('tgp', 'Gestão de Projetos')]
    course = SelectField('Informe a sua disciplina:', choices=course_options)
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():

        remote_addr = request.remote_addr
        host = request.host
        old_name = session.get('name')
        old_surname = session.get('surname')
        old_full_name = (old_name + ' ' + old_surname) if old_name and old_surname else ''

        full_name = form.name.data + ' ' + form.surname.data
        if old_full_name != '' and old_full_name != full_name:
            flash('Parece que você mudou seu nome!')
        session['name'] = form.name.data
        session['surname'] = form.surname.data
        session['school_name'] = form.school_name.data
        session['course'] = next((course_display_name for course_code, course_display_name in form.course_options if course_code == form.course.data), None)
        session['remote_address'] = remote_addr
        session['host'] = host
        return redirect(url_for('index'))
    return render_template('index.html', form=form, current_time = datetime.utcnow(), name=session.get('name'), surname=session.get('surname'), remote_address=session.get('remote_address'), host=session.get('host'))
