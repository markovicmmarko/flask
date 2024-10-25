from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField

class AddForm(FlaskForm):
    name   = StringField("Enter the type and model of the tank: ")
    make   = StringField("Enter the country where this tank is being produced: ")
    submit = SubmitField("Submit")


class DeleteForm(FlaskForm):
    tank_id = IntegerField("Enter the ID num of the tank you want to remove: ")
    submit  = SubmitField("Submit")