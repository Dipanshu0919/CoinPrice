import os, re, sys, ccxt, time, threading, asyncio
from telethon import TelegramClient, events
import ccxt, time, threading, asyncio, random, logging, io, sys, traceback
from telethon import TelegramClient, events
from datetime import datetime, timedelta
from flask import Flask

api_id = 25895085
api_hash = "4d83e959108956d7c0b05bd8f52f54b5"
bot_token = os.environ.get("BOT_TOKEN")
OWNERS = 6106882014, 5644071668, 6519277757
db = {}

client = TelegramClient('CoinPricee_Bot', api_id, api_hash).start(bot_token=bot_token)

run = False

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return 'Healthy', 200

@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    print(f"{event}\n\n\n")
    print(f"{dir(event)}\n\n\n")
    print(f"{event.sender}\n\n")
    print(event.sender.id)
    print(event.sender.first_name)

@client.on(events.NewMessage)
async def price(event):
    global run
    if event.text in ("/start" , "/stop"):
        return
    
    sp = event.text.split("/") [1]
    coin = f"{sp.upper()}/USDT"
    uuid = event.sender.id
    if run and uuid==db["uid"] and db["start"]:
        await event.reply("Pehle hi price dekhna chalu kia na stupid /stop kr")
        return
    k = await event.reply(f"**Showing** {coin} **Price...**")
    ex = ccxt.bitget()
    run = True
    db.update({"uid": event.sender.id, "start":True})
    while run:
        try:
            n = ex.fetch_ticker(coin)
            print(f"{coin} price fetched!")
            time_str = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime("**Date:** %d %B %Y \n**Time:** %H:%M:%S ")
            price = float(n['last'])
            mc = price * 19810000
        
            lp = f"**{coin} Price:** {price} \n**Market Cap:** {mc} \n\n**Last Update:** \n{time_str}"
            await k.edit(lp)
            print(f"Updated {coin} with price: {price} and market cap: {mc} at: {time_str} by user: {event.sender.first_name} - {event.sender.id}")

            await asyncio.sleep(15)
        except Exception as e:
            await k.edit("ERROR: {e}")
            run = False
            db.update({"uid": event.sender.id, "start":False})


@client.on(events.NewMessage(pattern="/stop"))
async def stop(event):
    global run
    run = False
    db.update({"uid": event.sender.id, "start":False})
    await event.reply("ruk gya")


@client.on(events.NewMessage(pattern=".eval"))
async def eval(event):
    if not event.sender.id in OWNERS:
        return
    reply = await event.reply("**Processing....**")
    cmd = event.text.split(" ", maxsplit=1)[1]
    if not cmd:
        await reply.edit("Give a eval code first!")
        return
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, event)
    except Exception:
        exc = traceback.format_exc()
    
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    out = f"**Eval\n** `{cmd}`\n**Output**\n`{evaluation.strip()}`\n"
    if len(out) > 4000:
        await reply.reply(out)
    else:
        await reply.edit(out)

async def aexec(code, client, message):
    exec("async def __aexec(client, message): " + "".join(f"\n {l_}" for l_ in code.split("\n")))
    return await locals()["__aexec"](client, message)

def run_flask():
    app.run(host='0.0.0.0', port=8000)

flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

client.run_until_disconnected()
