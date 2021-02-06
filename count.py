import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
cluster=MongoClient(os.getenv("MongoDB"))
db=cluster["Quasar"]
collection=db["counting"]

continuer = True

class counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot.user:
            return
        ctx=await self.bot.get_context(msg)
        if ctx.channel.id == 801830754559852545:
            chiffre=msg.content
            global continuer
            if continuer == True:
                historique=await ctx.channel.history(limit=10).flatten()
                del historique[0]
                for oldMsg in historique:
                    oldMsgStr=oldMsg.content
                    if oldMsgStr.isdigit():
                        dernierChiffre=oldMsgStr
                        break
            else:
                dernierChiffre=0
            if chiffre.isdigit():
                chiffre, dernierChiffre=int(chiffre), int(dernierChiffre)
                result=collection.find_one({"_id":ctx.author.id})
                if result==None:
                    user={"_id":ctx.author.id, "name":ctx.author.name, "correct":0, "incorrect":0, "guild":ctx.guild.id}
                    collection.insert_one(user)
                if continuer == False and chiffre != 1:
                    await msg.add_reaction("⚠️")
                    await ctx.send("Nombre erroné ! Le rush était déjà perdu. \nVos stats n'ont pas évolué. Veuillez recommencez à 1.")
                    return
                elif continuer == False and chiffre==1:
                    await msg.add_reaction("✅")
                    collection.update_one({"_id":msg.author.id}, {"$inc":{"correct":1}})
                    continuer=True
                    return
                elif chiffre == dernierChiffre+1 and msg.author != oldMsg.author:
                    await msg.add_reaction("✅")
                    collection.update_one({"_id":msg.author.id}, {"$inc":{"correct":1}})
                    continuer=True
                    return
                else:
                    await msg.add_reaction("❌")
                    collection.update_one({"_id":msg.author.id}, {"$inc":{"incorrect":1}})
                    embed = discord.Embed(color=0x78B81C)
                    embed.set_author(name=f"{msg.author} S'EST TROMPÉ À {dernierChiffre} ! \nRecommencez à 1. Vous ne pouvez pas compter deux fois d'affilée.")
                    await ctx.send(embed=embed)
                    continuer=False
                    return