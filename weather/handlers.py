from telegram import Update
from telegram.ext import CallbackContext
import os
import requests
from .temp import FORECAST_TAMP
from .db import DB

db = DB("db.json")

API_KEY = os.getenv("API_KEY")


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    ans = db.add_user(user.id, user.first_name, user.last_name, user.username)
    
    print(ans)
    if ans:
        update.message.reply_text(
            text=f"Hello {user.first_name}! Welcome to the bot!"
        )
    else:
        update.message.reply_text(
            text=f"Hi {user.first_name}! Welcome back to the bot!"
        )

def send_weather(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""

    payload = {
        "q" : update.message.text,
        "appid" : API_KEY
    }
    
    response = requests.get(url="https://api.openweathermap.org/data/2.5/weather", params=payload)

    data = response.json()

    if data["cod"] == 200:
        weekdays = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }
        monthes = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
            }
        update.message.reply_text(
            text=FORECAST_TAMP.format(
                weekday=weekdays.get(update.message.date.weekday()),
                day=update.message.date.day,
                month=monthes.get(update.message.date.month),
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