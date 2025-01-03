import os, re, sys, ccxt, time
from telethon import TelegramClient, events

api_id = 25895085
api_hash = "4d83e959108956d7c0b05bd8f52f54b5"
bot_token = os.environ.get("BOT_TOKEN")

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    run = True
    ex = ccxt.mexc()
    while run:
        n = ex.fetch_ticker("BTC/USDT")
        await event.reply(n["last"])
        time.sleep(15)

@client.on(events.NewMessage(pattern="/stop"))
async def start(event):
    global run
    run = False
        

client.run_until_disconnected()
