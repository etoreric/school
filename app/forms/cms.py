from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, DateTimeField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(1, 100)])
    slug = StringField('URL Slug', validators=[
        DataRequired(), 
        Length(1, 100),
        Regexp(r'^[a-z0-9-]+$', message="Slug must contain only lowercase letters, numbers, and dashes.")
    ])
    description = TextAreaField('Description', validators=[Optional(), Length(0, 255)])
    submit = SubmitField('Save Category')

class PageForm(FlaskForm):
    title = StringField('Page Title', validators=[DataRequired(), Length(1, 100)])
    slug = StringField('URL Slug', validators=[
        DataRequired(), 
        Length(1, 100),
        Regexp(r'^[a-z0-9-]+$', message="Slug must contain only lowercase letters, numbers, and dashes.")
    ])
    content = TextAreaField('Page Content', validators=[DataRequired()])
    seo_title = StringField('SEO Title', validators=[Optional(), Length(0, 150)])
    seo_description = TextAreaField('SEO Description', validators=[Optional(), Length(0, 255)])
    is_published = BooleanField('Publish Immediately', default=True)
    submit = SubmitField('Save Page')

class PostForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired(), Length(1, 150)])
    slug = StringField('URL Slug', validators=[
        DataRequired(), 
        Length(1, 150),
        Regexp(r'^[a-z0-9-]+$', message="Slug must contain only lowercase letters, numbers, and dashes.")
    ])
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    tags = StringField('Tags', validators=[Optional(), Length(0, 255)])
    excerpt = StringField('Excerpt', validators=[Optional(), Length(0, 255)])
    content = TextAreaField('Post Content', validators=[DataRequired()])
    featured_image = FileField('Featured Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'gif'], 'Images only!')
    ])
    seo_title = StringField('SEO Title', validators=[Optional(), Length(0, 150)])
    seo_description = TextAreaField('SEO Description', validators=[Optional(), Length(0, 255)])
    comments_enabled = BooleanField('Allow Comments', default=False)
    is_published = BooleanField('Publish Immediately', default=True)
    submit = SubmitField('Save Post')

class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired(), Length(1, 150)])
    slug = StringField('URL Slug', validators=[
        DataRequired(), 
        Length(1, 150),
        Regexp(r'^[a-z0-9-]+$', message="Slug must contain only lowercase letters, numbers, and dashes.")
    ])
    start_time = DateTimeField('Start Time', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    end_time = DateTimeField('End Time', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    venue = StringField('Venue', validators=[DataRequired(), Length(1, 150)])
    organizer = StringField('Organizer', validators=[Optional(), Length(0, 150)])
    description = TextAreaField('Description', validators=[DataRequired()])
    featured_image = FileField('Featured Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'gif'], 'Images only!')
    ])
    registration_url = StringField('Registration URL', validators=[Optional(), Length(0, 255)])
    countdown_enabled = BooleanField('Show Countdown', default=False)
    is_published = BooleanField('Publish Immediately', default=True)
    submit = SubmitField('Save Event')

class DownloadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 150)])
    category = SelectField('File Category', choices=[
        ('General', 'General Resources'),
        ('Academic', 'Academic Materials & Syllabus'),
        ('Admissions', 'Admissions & Application Forms'),
        ('Policies', 'School Rules & Policies'),
        ('Newsletters', 'Newsletters & Magazines')
    ], default='General')
    file = FileField('Upload File', validators=[
        FileAllowed(['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'jpg', 'png'], 'Allowed file types')
    ])
    submit = SubmitField('Upload Document')



