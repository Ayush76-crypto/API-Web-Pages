import discord
import os
import requests
import json
import random
from replit import db

client = discord.Client()

sad_words = ["sad", "depressed", "angry", "unhappy", "depress", "misery"]

starter_msg = ["Cheer Up!", "Hang in there!", "You are a strong person!"]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)

def update_enc(enc_msg):
    if "encouragements" in db.keys():
        encouragements = db['encouragements']
        encouragements.append(enc_msg)
        db['encouragements'] = encouragements
    else:
        db['encouragements'] = [enc_msg]

def dalete_enc(index):
    encouragements = db['encouragements']
    if len(encouragements) > index:
        del encouragements[index]
        db['encouragements'] = encouragements


@client.event
async def on_ready():
    print("We have Logged in as {0.user}".format(client))

# Message from bot itself
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    options = starter_msg
    if "encouragements" in db.keys():
        options = options + db['encouragements']

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
        enc_msg = msg.split("$new ", 1)[1]
        update_enc(enc_msg)
        await message.channel.send("New encouraging message added!")

    if msg.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("$del", 1)[1])
            dalete_enc(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

my_secret = os.environ['TOKEN']
client.run(my_secret
