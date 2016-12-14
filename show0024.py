from flask import Flask, redirect, url_for, request, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from datetime import datetime



app = Flask(__name__, template_folder='.')
app.config['SECRET_KEY'] = 'This is a secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = True
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

class TodoList(db.Model):
	id = db.Column(db.Integer, primary_key=True, index=True)
	body = db.Column(db.String(256), index=True)
	is_done = db.Column(db.Boolean, default=False)
	date = db.Column(db.DateTime, default=datetime.now)

class TodoListForm(FlaskForm):
	thing = StringField('写下你想要做的事', validators=[DataRequired(), Length(1, 256)])
	submit = SubmitField('确认')


@app.route('/', methods=['GET', 'POST'])	
def index():
	form = TodoListForm()
	if form.validate_on_submit():
		thing = TodoList(body=form.thing.data)
		db.session.add(thing)
		db.session.commit()
		flash('创建任务成功')
		return redirect(url_for('index'))
	page = request.args.get('page', 1, type=int)
	pagination = TodoList.query.order_by(TodoList.date.desc()).paginate(page=page,
		per_page=5)
	# things = TodoList.query.order_by(TodoList.date.desc()).all()
	return render_template('index.html', form=form, pagination=pagination)


@app.route('/delete')
def delete():
	id = request.args.get('id', -1, type=int)
	thing = TodoList.query.get_or_404(id)
	db.session.delete(thing)
	db.session.commit()
	return redirect(url_for('index'))
@app.route('/change-state')
def change_state():
	id = request.args.get('id', -1, type=int)
	thing = TodoList.query.get_or_404(id)
	thing.is_done = thing.is_done ^ True
	db.session.add(thing)
	db.session.commit()
	return jsonify({'code': 0, 'msg': 'successfully'})


if __name__ == '__main__':
	app.run()