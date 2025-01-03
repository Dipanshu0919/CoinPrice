import os, re, sys, ccxt, time, threading, asyncio
from telethon import TelegramClient, events
from flask import Flask
from datetime import datetime, timedelta

api_id = 25895085
api_hash = "4d83e959108956d7c0b05bd8f52f54b5"
bot_token = "7996280741:AAGuaV3WFDlssl5E91FyExlu9AUFimYLgJg"

client = TelegramClient('CoinPricee_Bot', api_id, api_hash).start(bot_token=bot_token)

app = Flask(__name__)

run = True

@app.route('/health', methods=['GET'])
def health_check():
    return 'Healthy', 200

@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    k = await event.reply("`Showing BTC Price...`")
    global run
    ex = ccxt.mexc()
    while run:
        n = ex.fetch_ticker("BTC/USDT")
        time = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime("**Date:** `%d %B %Y` \n**Time:** `%H:%M:%S` ")
        lp = f"**BTC Price:** `{str(n['last'])}` \n\n**Last Update:** \n{time}"
        await k.edit(lp)
        await asyncio.sleep(15)

@client.on(events.NewMessage(pattern="/stop"))
async def stop(event):
    global run
    run = False

def run_flask():
    app.run(host='0.0.0.0', port=8000)

flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

client.run_until_disconnected()
