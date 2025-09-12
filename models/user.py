from db.connect_db import db
from datetime import datetime, timezone


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.BigInteger, unique=True, nullable=False)
    facebook_name = db.Column(db.String(80), nullable=False, unique=True)
    facebook_access_token = db.Column(db.String(512))
    instagram_id = db.Column(db.String(80), nullable=True, unique=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    posts = db.relationship('Post', back_populates='author', cascade="all, delete-orphan")
