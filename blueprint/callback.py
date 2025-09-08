from flask import Blueprint
from flask import request, jsonify, render_template
import requests
from dotenv import load_dotenv
import os
from utils import *
from models.user import User, db
from datetime import datetime, timezone

load_dotenv()

# Config
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

callback_bp = Blueprint('callback', __name__)


@callback_bp.get('/callback')
def callback():
    try:
        code = request.args.get("code")
        telegram_id = request.args.get("state")  # we passed this in "state"

        if not code or not telegram_id:
            return "Missing code or state", 400

        # Exchange code for access token
        token_url = "https://graph.facebook.com/v19.0/oauth/access_token"
        params = {
            "client_id": APP_ID,
            "redirect_uri": REDIRECT_URI,
            "client_secret": APP_SECRET,
            "code": code,
        }
        token_res = requests.get(token_url, params=params)
        data = token_res.json()
        
        if "access_token" not in data:
            return jsonify(data), 400
        
        access_token = data["access_token"]
        
        #  Get user info from Facebook Graph API
        user_info_url = "https://graph.facebook.com/me"
        user_params = {
            "fields": "id,name,email",
            "access_token": access_token
        }
        user_res = requests.get(user_info_url, params=user_params)
        user_data = user_res.json()
        
        # Default: no Instagram ID yet
        instagram_id = None

        # Step 1: Get pages managed by the user
        pages_url = "https://graph.facebook.com/me/accounts"
        pages_res = requests.get(pages_url, params={"access_token": access_token})
        pages_data = pages_res.json()

        if "data" in pages_data and len(pages_data["data"]) > 0:
            for page in pages_data["data"]:
                page_id = page.get("id")

                # Step 2: Check if page has an Instagram business account
                page_url = f"https://graph.facebook.com/{page_id}"
                page_res = requests.get(
                    page_url,
                    params={
                        "fields": "instagram_business_account",
                        "access_token": access_token,
                    },
                )
                page_info = page_res.json()

                if "instagram_business_account" in page_info:
                    instagram_id = page_info["instagram_business_account"]["id"]
                    break  # take the first connected IG account
        
        # Save user to database
        user = User.query.filter_by(facebook_name=user_data.get("name")).first()
        
        if not user:
            new_user = User(
                facebook_name=user_data.get("name"),
                telegram_id=telegram_id,
                facebook_id=instagram_id,
                facebook_access_token=access_token,
                facebook_token_expires_at=calculate_expiry(data["expires_in"]),
                created_at=datetime.now(timezone.utc)
            )
            db.session.add(new_user)
            db.session.commit()
        else:
            # Update access token if user exists
            user.facebook_access_token = access_token
            user.facebook_id = instagram_id
            db.session.commit()

        # Notify the Telegram user
        notify_telegram_user(telegram_id)

        return render_template("return_to_telegram.html")
    except Exception as e:
        db.session.rollback()  # rollback in case DB transaction failed
        return render_template("server_error.html"), 500
