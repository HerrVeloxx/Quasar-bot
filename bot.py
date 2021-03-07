import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

conn = sqlite3.connect('quasar.db')
cur = conn.cursor()

async def get_prefix(bot,msg):
    return cur.execute("SELECT prefix FROM config WHERE guildid = ?", msg.guild.id).fetchone()






intents = discord.Intents.default()
intents.members = True
intents.typing = True
intents.presences = True
intents.reactions = True


bot = commands.Bot(intents=intents,command_prefix = str(get_prefix), description = "Bot multifonctions")




@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    activity = discord.Game(name=">help | Développé par Veloxx#4705 et eupone#9975", type=3)
    await bot.change_presence(status = discord.Status.online, activity = activity)
    print(f"Successfully logged in and booted...!\n")
    for fold in os.listdir("cogs"):
        print(fold + "\n")
        for files in os.listdir(fold):
            print(files)
            bot.load_extension(files)
    print("Extension load !\n\n")


@bot.event
async def on_command_error(event,ctx):   #error handler
    await ctx.send(event)


@bot.event
async def on_guild_join(guild):
    cur.execute("SELECT * FROM config WHERE guildid = ?",(int(guild.id),) )
    exist = cur.fetchone()
    if not exist:
        cur.execute('''INSERT INTO config(guildid,prefix) VALUES (?,'>')''', ( int(guild.id), ) )
        conn.commit()
        print("new guild !")
    for memb in guild.members :
        if memb.id != bot.user.id:
            cur.execute("SELECT * FROM user WHERE userid = ?",(int(memb.id),) )
            exist = cur.fetchone()
            if not exist and not memb.bot:
                cur.execute('''INSERT INTO user(userid,guildid) VALUES (?,?)''',( int(memb.id),int(guild.id) ) )
                conn.commit()


"""
@bot.command(name="prefix")
@commands.guild_only()
async def setprefix(ctx, *, prefixes=""):
    server = collection.find_one({"guild":ctx.guild.id})
    
    collection.update_one({"guild":ctx.guild.id}, {"$set":{"prefixe":prefixes}})
    result=collection.find_one({"guild":ctx.guild.id})
    newPrefix=result.get("prefixe")
    await ctx.send(f"Le nouveau préfixe est {newPrefix}")
"""




bot.run(os.getenv("TOKEN"))