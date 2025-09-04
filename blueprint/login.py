from flask import Blueprint, render_template
from flask import redirect, request
from dotenv import load_dotenv
import os

load_dotenv()

# Config
APP_ID = os.getenv("APP_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")

login_bp = Blueprint('login', __name__)


@login_bp.get("/login")
def login():
    try:
        telegram_id = request.args.get("telegram_id")
        if not telegram_id:
            return "Missing telegram_id", 400

        fb_oauth_url = (
            f"https://www.facebook.com/v19.0/dialog/oauth"
            f"?client_id={APP_ID}"
            f"&redirect_uri={REDIRECT_URI}"
            f"&scope=pages_show_list,instagram_basic,pages_read_engagement,pages_manage_posts"
            f"&state={telegram_id}"
        )

        return redirect(fb_oauth_url)
    except Exception as e:
        return render_template("server_error.html"), 500