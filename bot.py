# bot.py
import os
import random
import discord
import pymongo
from discord.ext import commands
from pymongo import MongoClient
from dotenv import load_dotenv
import urllib.parse

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

#mongodb
cluster = MongoClient("mongodb+srv://derekjiang917:Ehsw^Yb3q&hUR2@tutorialcluster.atalb.mongodb.net/test")
db = cluster["userdata"]
collection = db["userdata"]

with open("swears.txt") as file:
    swears = set([word.strip() for word in file.readlines()])

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')



@client.event
async def on_message(ctx):
    if ctx.author == client.user:
        return
    myquery = { "_id": ctx.author.id }
    #if msg has any swears
    if not swears.isdisjoint(set(str(ctx.content.lower()).split())):
        #if not in db
        if (collection.count_documents(myquery) == 0):
            post = {"_id": ctx.author.id, "score": 1}
            collection.insert_one(post)
            await ctx.channel.send('ok you swear first time let you off with warning')
        else:
            query = {"_id": ctx.author.id}
            user = collection.find(query)
            for result in user:
                score = result["score"]
            score = score + 1
            collection.update_one({"_id":ctx.author.id}, {"$set":{"score":score}})
            notifications = [f'you swore {score} times :angry:', f'uhhmm youve been a bigot {score} times settle down', f'uhhhhh we got a level {score} bigot alert :fishHMMM:']
            await ctx.channel.send(random.choice(notifications))

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise discord.DiscordException


client.run(TOKEN)
