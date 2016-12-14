from flask import Flask, render_template, url_for, request, redirect
# from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, SubmitField, validators
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime



app = Flask(__name__, template_folder='.')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.sqlite'
app.config['SECRET_KEY'] = 'this is a secret string'
Base = declarative_base()
engine = create_engine('sqlite:///comments.sqlite')
session = sessionmaker(bind=engine)()


class CommentsForm(Form):
	username = StringField('姓名', validators=[validators.DataRequired('姓名不能为空')])
	comments = TextAreaField('内容', validators=[validators.DataRequired('留言不能为空')])
	submit = SubmitField('提交')

class Comment(Base):
	__tablename__ = 'comments'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	body = Column(String)
	date = Column(DateTime, default=datetime.now)

@app.route('/', methods=['GET', 'POST'])
def index():
	form = CommentsForm(request.form)
	if request.method == 'POST' and form.validate():
		comment = Comment(name=form.username.data, body=form.comments.data)
		session.add(comment)
		session.commit()
		return redirect(url_for('.index'))
	comments = session.query(Comment).order_by(Comment.date.desc()).all()
	return render_template('comments.html', form=form, comments=comments)


if __name__ == '__main__':
	app.run(debug=True)