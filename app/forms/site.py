from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, SelectField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange

class SettingsForm(FlaskForm):
    # School Info
    school_name = StringField('School Name', validators=[DataRequired(), Length(1, 100)])
    custom_domain = StringField('Custom Domain Name (e.g. www.sunnyhigh.edu or sunnyhigh.edu)', validators=[Optional(), Length(0, 255)], filters=[lambda x: x.strip() if x else x])
    logo = FileField('School Logo', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only!')
    ])
    favicon = FileField('Favicon (ICO/PNG)', validators=[
        FileAllowed(['ico', 'png'], 'ICO or PNG images only!')
    ])
    hero_image = FileField('Hero Background Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only!')
    ])
    welcome_image = FileField('Welcome Section Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only!')
    ])
    principal_image = FileField('Principal/Proprietor Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only!')
    ])
    
    # Theme Styling Colors
    primary_color = StringField('Primary Theme Color (HEX)', validators=[DataRequired(), Length(7, 7)], filters=[lambda x: x.strip() if x else x])
    secondary_color = StringField('Secondary Theme Color (HEX)', validators=[DataRequired(), Length(7, 7)])
    footer_bg_color = StringField('Footer Background Color (HEX)', validators=[Optional(), Length(7, 7)])
    
    # Contact Info
    contact_email = StringField('Contact Email', validators=[DataRequired(), Email(), Length(1, 120)], filters=[lambda x: x.strip() if x else x])
    contact_phone = StringField('Contact Phone', validators=[DataRequired(), Length(1, 20)], filters=[lambda x: x.strip() if x else x])
    contact_address = TextAreaField('Contact Address', validators=[DataRequired()], filters=[lambda x: x.strip() if x else x])
    google_maps_url = TextAreaField('Google Maps Embed URL', validators=[Optional()], filters=[lambda x: x.strip() if x else x])
    
    # Social Media Links
    social_facebook = StringField('Facebook Link', validators=[Optional(), Length(0, 255)])
    social_twitter = StringField('Twitter/X Link', validators=[Optional(), Length(0, 255)])
    social_instagram = StringField('Instagram Link', validators=[Optional(), Length(0, 255)])
    social_youtube = StringField('YouTube Link', validators=[Optional(), Length(0, 255)])
    social_whatsapp = StringField('WhatsApp Contact Link', validators=[Optional(), Length(0, 255)])
    
    # SEO & Analytics
    seo_meta_description = TextAreaField('Website SEO Meta Description', validators=[Optional(), Length(0, 250)])
    analytics_code = TextAreaField('Google Analytics Code (or other tracking script)', validators=[Optional()])
    
    # Footer
    footer_text = StringField('Footer Copyright text', validators=[DataRequired(), Length(1, 255)])
    
    submit = SubmitField('Update Settings')

class TestimonialForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 100)])
    role = StringField('Role (e.g. Alumnus, Parent, Grade 12 Student)', validators=[DataRequired(), Length(1, 50)])
    content = TextAreaField('Testimonial Content', validators=[DataRequired()])
    rating = SelectField('Rating (Stars)', coerce=int, choices=[(5, '5 Stars'), (4, '4 Stars'), (3, '3 Stars'), (2, '2 Stars'), (1, '1 Star')])
    photo = FileField('Profile Photo', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only!')
    ])
    is_published = BooleanField('Published', default=True)
    submit = SubmitField('Save Testimonial')

class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(1, 100)], filters=[lambda x: x.strip() if x else x])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(1, 120)], filters=[lambda x: x.strip() if x else x])
    phone = StringField('Phone Number', validators=[Optional(), Length(0, 20)], filters=[lambda x: x.strip() if x else x])
    subject = StringField('Subject', validators=[DataRequired(), Length(1, 150)], filters=[lambda x: x.strip() if x else x])
    message_content = TextAreaField('Your Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

