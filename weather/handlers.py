from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
import os
import requests
from .temp import FORECAST_TAMP
from .db import DB

db = DB('db.json')

API_KEY = os.getenv("API_KEY")


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    user = update.effective_user

    keyboard_karkup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='📍 Location', request_location=True)]
        ],
        resize_keyboard=True
    )
    
    if db.is_user(user.id):
        update.message.reply_text(
            text=f"Hi {user.first_name}! Welcome back to the bot!/n/nsend your location",
            reply_markup=keyboard_karkup
        )
    else:
        db.add_user(user.id, user.first_name, user.last_name, user.username)
        update.message.reply_text(
            text=f"Hello {user.first_name}! Welcome to the bot!/n/nsend your location",
            reply_markup=keyboard_karkup
        )


def send_weather(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""

    location = update.message.location

    payload = {
        "lat" : location.latitude,
        "lon": location.longitude,
        "appid" : API_KEY
    }
    
    response = requests.get(url="https://api.openweathermap.org/data/2.5/weather", params=payload)

    data = response.json()

    if data["cod"] == 200:
        update.message.reply_text(
            text=FORECAST_TAMP.format(
                date=update.message.date.strftime("%A, %-d-%B"),
                city=data["name"],
                description=data["weather"][0]["description"],
                temp=data["main"]["temp"] - 273.15,
                feels_like=data["main"]["feels_like"] - 273.15,
                clouds=data["clouds"]["all"],
                humidity=data["main"]["humidity"],
                wind=data["wind"]["speed"]
            )
        )
    
    else:
        update.message.reply_text(
            text=f"The city {update.message.text} doesn't exist."
        )