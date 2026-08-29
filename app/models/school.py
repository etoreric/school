from datetime import datetime

from app.extensions import db


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    administrators = db.relationship(
        'User', backref='school', lazy=True, foreign_keys='User.school_id'
    )


class SchoolInvite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_hash = db.Column(db.String(64), unique=True, nullable=False, index=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    used_at = db.Column(db.DateTime)

    created_by = db.relationship('User', backref='school_invites')

    @property
    def is_used(self):
        return self.used_at is not None