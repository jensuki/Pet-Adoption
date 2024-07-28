from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField, URLField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional

class AddPetForm(FlaskForm):
    """Form to add pets"""

    name = StringField('Pet Name', validators=[InputRequired()])
    species = SelectField('Species', validators=[InputRequired()], choices=[("cat", "Cat"), ("dog", "Dog"), ("porcupine", "Porcupine")])
    photo_url = URLField('Photo URL', validators=[Optional(), URL()])
    age = IntegerField('Age', validators=[Optional(), NumberRange(min=0, max=30)])
    notes = TextAreaField('Notes')
    available = BooleanField('Available')

class EditPetForm(FlaskForm):
    """Form to edit a pet"""

    photo_url = URLField('Photo URL', validators=[Optional(), URL("Invalid URL format.")])
    age = IntegerField('Age', validators=[Optional(), NumberRange(min=0, max=30)])
    notes = TextAreaField('Notes')
    available = BooleanField('Available')