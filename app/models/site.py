from app.extensions import db

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.Text)

    def __repr__(self):
        return f'<Setting {self.key}>'
