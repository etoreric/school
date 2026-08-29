from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_super_administrator(self):
        return self.is_admin

    def can(self, perm):
        return self.is_admin

    @property
    def role(self):
        class RoleObj:
            id = 1 if self.is_admin else 2
            name = "Super Administrator" if self.is_admin else "Staff Member"
        return RoleObj()

    @property
    def role_id(self):
        return 1 if self.is_admin else 2

    def __repr__(self):
        return f'<User {self.username}>'

