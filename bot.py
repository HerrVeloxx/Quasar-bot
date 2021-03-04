import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient

load_dotenv()
cluster=MongoClient(os.getenv("MongoDB"))
db=cluster["Quasar"]
collection=db["prefix"]

default_prefixes = ['>']



ext=["owner", "autres"]




async def get_prefix(bot, msg):
    guild = collection.find_one({"guild":msg.guild.id})
    if guild == None:
        return default_prefixes
    else:
        Prefix=guild.get("prefixe")
        return Prefix




load_dotenv()
bot = commands.Bot(command_prefix = get_prefix, description = "Bot multifonctions")





@bot.command(name="prefix")
@commands.guild_only()
async def setprefix(ctx, *, prefixes=""):
    server = collection.find_one({"guild":ctx.guild.id})
    if server == None:
        newGuild={"guild":ctx.guild.id, "prefixe":""}
        collection.insert_one(newGuild)
    collection.update_one({"guild":ctx.guild.id}, {"$set":{"prefixe":prefixes}})
    result=collection.find_one({"guild":ctx.guild.id})
    newPrefix=result.get("prefixe")
    await ctx.send(f"Le nouveau préfixe est {newPrefix}")

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    activity = discord.Game(name=">help | Développé par Veloxx#4705", type=3)
    await bot.change_presence(status = discord.Status.online, activity = activity)
    print(f"Successfully logged in and booted...!\n")
    for k in ext:
        bot.load_extension(k)
    print("Extension load !\n\n")

bot.run(os.getenv("TOKEN"))