from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()   # creates tables if they don’t exist
    print("Database connected successfully")