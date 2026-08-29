from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class SchoolOnboardingForm(FlaskForm):
    school_name = StringField('School Name', validators=[DataRequired(), Length(2, 150)])
    username = StringField('Administrator Username', validators=[DataRequired(), Length(3, 64)])
    email = StringField('Administrator Email', validators=[DataRequired(), Email(), Length(1, 120)])
    password = PasswordField('Administrator Password', validators=[DataRequired(), Length(6, 128)])
    submit = SubmitField('Create School')