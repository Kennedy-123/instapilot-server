from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def connect_db(app):
    db.init_app(app)
    migrate.init_app(app, db)
    print("Database connected successfully")