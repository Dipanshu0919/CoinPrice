from telethon import TelegramClient, events

# Use your own values from my.telegram.org
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_BOT_TOKEN'

# Create the client and connect
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Define a handler for new messages
@client.on(events.NewMessage)
async def handle_new_message(event):
    # Print the message to the console
    print(event.message.message)

    # Reply to the message
    await event.reply('Hello! This is a Telethon bot.')

# Start the client
client.run_until_disconnected()
