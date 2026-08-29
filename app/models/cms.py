from datetime import datetime
from app.extensions import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('Post', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    seo_title = db.Column(db.String(150))
    seo_description = db.Column(db.String(255))
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Page {self.title}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(255))
    featured_image = db.Column(db.String(255))
    tags = db.Column(db.String(255))
    seo_title = db.Column(db.String(150))
    seo_description = db.Column(db.String(255))
    comments_enabled = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Post {self.title}>'

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String(150), nullable=False)
    organizer = db.Column(db.String(150))
    featured_image = db.Column(db.String(255))
    registration_url = db.Column(db.String(255))
    countdown_enabled = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Event {self.title}>'

class Download(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(10))
    category = db.Column(db.String(50), default='General')
    download_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Download {self.title}>'

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30))
    subject = db.Column(db.String(150), nullable=False)
    message_content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    reply_content = db.Column(db.Text)
    replied_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ContactMessage {self.subject} from {self.name}>'

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)
    photo_path = db.Column(db.String(255))
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Testimonial {self.name}>'

class HomeSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    title = db.Column(db.String(150))
    subtitle = db.Column(db.String(150))
    content = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    is_enabled = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<HomeSection {self.name}>'

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    media = db.relationship('Media', backref='album', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Album {self.title}>'

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    media_path = db.Column(db.String(255), nullable=False)
    media_type = db.Column(db.String(20), default='image')
    caption = db.Column(db.String(255))
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Media {self.media_path}>'

