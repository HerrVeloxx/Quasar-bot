import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
cluster=MongoClient(os.getenv("MongoDB"))
db=cluster["Quasar"]
collection=db["helpStats"]

payloadPython = None
payloadJS = None
payloadCcpp = None
payloadDjs = None
payloadDpy = None

def setup(bot):
    bot.add_cog(helpStats(bot))

class helpStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setup-helpStats")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setupHelpStats(self, ctx):
        
        async def checkRole(message):
            return message.channel == msg.channel and message.author == ctx.message.author
        
        msg = await ctx.send("Veuillez mentionner le rôle dédié à la modération de l'xp en fonction de l'aide apportée.")
        modXP = await self.bot.wait_for("message", timeout = None, check = checkRole)
        await ctx.send(modXP.content)
        
        async def checkEmoji(reaction):
            msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            return message.id == msg.id and msg.author == ctx.author
        
        await ctx.send("Veuillez réagir aux messages ci-dessous avec l'émoji que vous voulez utiliser pour l'aide à ce langage (un seul émoji par message).")
        await ctx.send("---------------------------------")
        
        message = await ctx.send("Python")
        global payloadPython
        payloadPython = await self.bot.wait_for("raw_reaction_add", timeout = None, check = checkEmoji)
        
        message = await ctx.send("JavaScript")
        global payloadJS
        payloadJS = await self.bot.wait_for("raw_reaction_add", timeout = None, check = checkEmoji)
        
        message = await ctx.send("C et C++")
        global payloadCcpp
        payloadCcpp = await self.bot.wait_for("raw_reaction_add", timeout = None, check = checkEmoji)
        
        message = await ctx.send("Discord.js")
        global payloadDjs
        payloadDjs = await self.bot.wait_for("raw_reaction_add", timeout = None, check = checkEmoji)
        
        message = await ctx.send("Discord.py")
        global payloadDpy
        payloadDpy = await self.bot.wait_for("raw_reaction_add", timeout = None, check = checkEmoji)
        
        await ctx.send("Configuration terminée.")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if msg.author.id==self.bot.user.id:
            return
        if payload.guild_id == 789670704911613992 or payload.guild_id == 796807012947591188:
            result=collection.find_one({"_id":msg.author.id})
            emote=payload.emoji
            if result==None:
                newUser={"_id":msg.author.id, "pythonHelp":0, "ccppHelp":0, "jsHelp":0, "djsHelp":0, "dpyHelp":0}
                collection.insert_one(newUser)
            if int(emote.id)==int(payloadPython.emoji.id):
                await msg.channel.send("Python")
                collection.update_one({"_id":msg.author.id}, {"$inc":{"pythonHelp":1}})
                return
            elif emote==jsEmoji:
                await msg.channel.send("JS")
                collection.update_one({"_id":msg.author.id}, {"$inc":{"jsHelp":1}})
                return
            elif emote==ccppEmoji:
                await msg.channel.send("C/C++")
                collection.update_one({"_id":msg.author.id}, {"$inc":{"ccppHelp":1}})
                return
            elif emote==djsEmoji:
                await msg.channel.send("Discord.js")
                collection.update_one({"_id":msg.author.id}, {"$inc":{"djsHelp":1}})
                return
            elif emote==dpyEmoji:
                await msg.channel.send("Discord.py")
                collection.update_one({"_id":msg.author.id}, {"$inc":{"dpyHelp":1}})
                return