import os, re, sys, ccxt, time, threading, asyncio, random, logging, io, sys, traceback
from telethon import TelegramClient, events
from datetime import datetime, timedelta
from flask import Flask
from telethon.tl.types import MessageMediaDocument

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
    coinsss = """
    /render
    /near
    /sei
    /vanar
    /aptos
    /orai
    /prcl
    /w
    /flt
    /pha
    /jup
    /tai
    /naka
    /btc
    /dogs
    /not"""
    await event.reply(f"**COIN PRICE BOT**\n\n**Coins:** {coinsss}")

@client.on(events.NewMessage)
async def price(event):
    global run
    if event.text in ("/start" , "/stop", ".eval") or event.sender.bot:
        return
    if event.text.startswith("/"):
        sp = event.text.split("/") [1]
    else:
        return
    coin = f"{sp.upper()}/USDT"
    uuid = event.sender.id
    if run and uuid == db["uid"] and db["start"]:
        await event.reply("Pehle hi price dekhna chalu kia na stupid /stop kr")
        return
    k = await event.reply(f"**Showing** `{coin}` **Price...**")
    ex = ccxt.bitget()
    run = True
    db.update({"uid": event.sender.id, "start":True})
    while run:
        try:
            n = ex.fetch_ticker(coin)
            time_str = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime("**Date:** %d %B %Y \n**Time:** %H:%M:%S ")
            price = float(n['last'])
            mc = price * 19810000
            lp = f"**{coin} Price:** {price} \n**Market Cap:** {mc} \n\n**Last Update:** \n{time_str}"
            await k.edit(lp)
            await asyncio.sleep(15)
        except Exception as e:
            await k.edit(f"ERROR: {e}")
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
    reply = await event.reply("**×•× Processing.... ×•×**")
    cmd = event.text.split(" ", maxsplit=1)[1]
    if not cmd:
        await reply.edit("Provide some code to evaluate.")
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

    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = f"`{exc.strip()}`"
    elif stderr:
        evaluation = f"`{stderr.strip()}`"
    elif stdout:
        evaluation = f"`{stdout.strip()}`"
    else:
        evaluation = "**Success:**"
    outp = f"**•• Eval ••**\n`{cmd}`\n\n**•• Output ••**\n{evaluation}"

    if len(outp) > 4000:
        with io.BytesIO(str.encode(outp)) as out_file:
            out_file.name = "eval_result.txt"
            await reply.reply(file=out_file)
    else:
        await reply.edit(outp.strip())

async def aexec(code, client, event):
    exec(
        "async def __aexec(client, event): "
        + "".join(f"\n {line}" for line in code.split("\n"))
    )
    return await locals()["__aexec"](client, event)


@client.on(events.NewMessage(pattern=".open"))
async def open_file(event):
    if not event.reply_to:
        await event.reply("Please reply to a file!")
        return

    try:
        # Get the reply message containing the file
        msg = await event.get_reply_message()

        if not msg or not msg.media:
            await event.reply("No file found in the replied message.")
            return

        # Check if the media is a document (file)
        if isinstance(msg.media, MessageMediaDocument):
            # Download the document (file)
            file_path = await client.download_file(msg.media.document)

            # Open and read the file content (if it's a text file)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            # Break the content into chunks if it is too large
            chunks = [content[i:i+4096] for i in range(0, len(content), 4096)]
            for chunk in chunks:
                await event.reply(chunk)

            # Remove the downloaded file
            os.remove(file_path)
        else:
            await event.reply("The replied message does not contain a document.")
    except Exception as e:
        await event.reply(f"An error occurred: {e}")

def run_flask():
    app.run(host='0.0.0.0', port=8000)

flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

client.run_until_disconnected()
