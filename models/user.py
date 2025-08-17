from db.connect_db import db
from datetime import datetime, timezone


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    facebook_name = db.Column(db.String(80), nullable=False, unique=True)
    facebook_access_token = db.Column(db.String(512))
    facebook_id = db.Column(db.String(80), nullable=False, unique=True)
    facebook_token_expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    posts = db.relationship('Post', back_populates='author', cascade="all, delete-orphan")
