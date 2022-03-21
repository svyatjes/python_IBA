import json
import os
import sqlite3

from flask import Flask, redirect, request, url_for, render_template
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from decouple import config

from oauthlib.oauth2 import WebApplicationClient
import requests
import datetime

from db import init_db_command
from user import User
from weather import Forecast
from user_agent import ParsedUserAgent


GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

try:
    init_db_command()
except sqlite3.OperationalError:
    pass  # Assume it's already been created

client = WebApplicationClient(GOOGLE_CLIENT_ID)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/index")
def endpoints():
    data = {
        "date": datetime.date.today(),
        "is_authenticated": current_user.is_authenticated,
    }
    return render_template("/index.html", data=data)


@app.route("/list/<city>")
@login_required
def wether_in_city(city):
    weather = Forecast(city)
    forecast = weather.forecast_for_several_days() if weather.city_id else None
    return render_template("/list_city.html", forecast=forecast, city=city)


@app.route("/<city>/<date>")
@login_required
def wether_in_city_on_date(city, date):
    weather = Forecast(city)
    forecast = weather.forecast_for_specific_day(date) if weather.city_id else None
    inf = {
        "city": city,
        "city_status": weather.city_id,
        "date": date,
    }
    return render_template("/city_date.html", forecast=forecast, inf=inf)


@app.route("/about")
@login_required
def about_page():
    data = {
        "name": current_user.name,
        "email": current_user.email,
        "profile_pic_source": current_user.profile_pic,
    }
    return render_template("/about.html", data=data)


@app.route("/useragent")
@login_required
def useragent():
    p = ParsedUserAgent(request.user_agent.string)
    data = {"platform": p.platform, "browser": p.browser}
    return render_template("/useragent.html", data=data)


@app.route("/")
def index():
    return redirect(url_for("endpoints"))


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    user = User(id_=unique_id, name=users_name, email=users_email, profile_pic=picture)

    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    login_user(user)

    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    # pip install pyopenssl for ssl_context
    app.run(ssl_context="adhoc", debug=True)
