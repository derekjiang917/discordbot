# bot.py
import os
import random
import discord
import pymongo
from discord.ext import commands
from pymongo import MongoClient
from dotenv import load_dotenv
import urllib.parse
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MONGOURL = os.getenv('URL')
bot = commands.Bot(command_prefix='!')

#mongodb
cluster = MongoClient(MONGOURL)
db = cluster["userdata"]
collection = db["userdata"]

with open("swears.txt") as file:
    swears = set([word.strip() for word in file.readlines()])

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def timer(ctx, time = ''):
    if(time.isnumeric()):
        sleep_time = int(time)
        time += " seconds"
    else:
        try:
            h, m, s = time.split(':')
            sleep_time = int(h) * 3600 + int(m) * 60 + int(s)
        except:
            await ctx.send("Usage: !timer <seconds> or !timer <HH:MM:SS>")
            return
    await ctx.send("ok sir set a timer for " + time)
    await asyncio.sleep(sleep_time)
    await ctx.send("@x cr trees are done <:loggers:875457790339067964>")


@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
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
            notifications = [
                f'you swore {score} times :angry:', f'uhhmm youve been a bigot {score} times settle down',
                f'uhhhhh we got a level {score} bigot alert <:fishHMMM:832321878210248774>', f'cringe nazi <:mordy:839593308866740243>',
                f'YIKES <:teeth:700532868547477574>'
                ]
            await ctx.channel.send(random.choice(notifications))
    await bot.process_commands(ctx)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise discord.DiscordException


bot.run(TOKEN)
