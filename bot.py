import os, re, sys, ccxt, time, threading, asyncio
from telethon import TelegramClient, events
from flask import Flask
from datetime import datetime, timedelta

api_id = 25895085
api_hash = "4d83e959108956d7c0b05bd8f52f54b5"
bot_token = os.environ.get("BOT_TOKEN")

client = TelegramClient('CoinPricee_Bot', api_id, api_hash).start(bot_token=bot_token)

app = Flask(__name__)

run = True

@app.route('/health', methods=['GET'])
def health_check():
    return 'Healthy', 200

@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    global run
    print(ccxt.exchanges)
    if run:
        await event.reply("Pehle hi price dekhna chalu kia na stupid")
        return
    
    run = True
    k = await event.reply("`Showing BTC Price...`")
    ex = ccxt.bybit()

    while run:
        try:
            n = ex.fetch_ticker("BTC/USDT")
            print(n)
        
            time_str = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime("**Date:** `%d %B %Y` \n**Time:** `%H:%M:%S` ")
            price = float(n['last'])
            mc = price * 19810000
        
            lp = f"**BTC Price:** `{price}` \n**Market Cap:** `{mc}` \n\n**Last Update:** \n{time_str}"
            await k.edit(lp)
            print(f"Updated message with price: {price} and market cap: {mc}")

            await asyncio.sleep(15)
        except ccxt.NetworkError as ne:
            print(f"Network error: {ne}")
            await k.edit("Network error occurred while fetching data.")
            break
        except ccxt.ExchangeError as ee:
            print(f"Exchange error: {ee}")
            await k.edit("Exchange error occurred while fetching data.")
            break
        except Exception as e:
            print(f"General error: {e}")
            await k.edit("Error occurred while fetching data.")
            break

@client.on(events.NewMessage(pattern="/stop"))
async def stop(event):
    global run
    run = False
    await event.reply("Price monitoring stopped.")

def run_flask():
    app.run(host='0.0.0.0', port=8000)
    
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

client.run_until_disconnected()
