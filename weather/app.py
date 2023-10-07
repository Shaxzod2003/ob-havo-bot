from telegram import Bot,Update
from dotenv import load_dotenv
import handlers 
import os
from telegram.ext import Dispatcher,CommandHandler,MessageHandler, Filters
from flask import Flask, request
load_dotenv()
TOKEN=os.environ.get("TOKEN")
bot=Bot(token=TOKEN)
dp=Dispatcher(bot, None, workers=0)

app=Flask(__name__)

@app.route("/webhook",method=["GET","POST"])
def main():
    if request.method=="GET":
        return "Webhook is good running"
    if request.method=="POST":
        body=request.get_json
        update=Update.de_json(body,bot)
        dp.add_handler(CommandHandler(["start", "boshlash"], handlers.start))
        dp.add_handler(MessageHandler(Filters.location, handlers.send_weather))
        dp.process_update(update)
        return {"Message": "succesfully"}
if __name__=="__main__":
    app.run(debug=True)