from flask import Flask
from blueprint import *
from db.connect_db import connect_db
import os
from models import *

app = Flask(__name__)

# config
# if os.getenv("FLASK_ENV") == "development":
#     # Local database (dev)
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("LOCAL_DATABASE_URL")
# else:
#     # Production (Render) - Render provides DATABASE_URL automatically
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids warning

# Connect the database to the existing app
connect_db(app)

# Register the blueprint
app.register_blueprint(callback_bp)
app.register_blueprint(login_bp)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
