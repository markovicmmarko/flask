import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import *


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)


class Tank(db.Model):
    __tablename__ = "tanks"
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    make = db.Column(db.Text)

    def __init__(self,name,make):
        self.name = name
        self.make = make

    def __repr__(self):
        return f"Tank: {self.name} - Production: {self.make}"
    

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_tank", methods=['GET', 'POST'])
def add_tank():
    form = AddForm()
    if form.validate_on_submit():
        with app.app_context():
            name = form.name.data
            make = form.make.data
            new_tank = Tank(name=name, make=make)
            db.session.add(new_tank)
            db.session.commit()
        return redirect(url_for('show_tanks'))
    
    return render_template("add.html", form=form)


@app.route("/show_tanks")
def show_tanks():
    with app.app_context():
        tanks = Tank.query.all()
    return render_template("show.html", tanks=tanks)


@app.route("/delete_tank", methods=['GET','POST'])
def delete_tank():
    form = DeleteForm()
    if form.validate_on_submit():
        with app.app_context():
            tank_id = form.tank_id.data
            tank    = Tank.query.get(tank_id)
            db.session.delete(tank)
            db.session.commit()
        return redirect(url_for('show_tanks'))
    
    return render_template("delete.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)