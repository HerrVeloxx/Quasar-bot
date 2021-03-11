import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
import random
import help_cmd

load_dotenv()
cluster=MongoClient(os.getenv("MongoDB"))
db=cluster["Quasar"]
collection=db["prefix"]

def setup(bot):
    bot.add_cog(Jeux(bot))

class Jeux(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.answer=["assurément !", "c'est sûr !", "essaye encore.", "bien évidemment !", "peut-être...", "pas du tout.", "totalement !", 
                     "tu peux y aller !", "essaye plus tard.", "pas d'avis.", "c'est ton destin.", "d'après moi oui.", "tu peux compter dessus.", 
                     "peu probable...", "faut pas rêver !", "n'y compte pas.", "impossible.", "alea jecta est.", "une chance sur deux.", 
                     "repose ta question.", "sans aucun doute.", "c'est bien parti.", "très probable..."]
        
    @commands.command(aliases=["8ball", "8b"])
    async def ball_choice(self, ctx, *, question=None):
        if not question:
            await help_cmd.help_cmd(self.bot, ctx, "ball")
            return
        choice=random.choice(self.answer)
        await ctx.send(f":8ball: **{ctx.author.name}**, {choice}")
        
    @commands.command(aliases=["coin", "cf"])
    async def coinflip(self, ctx, adv: discord.User=None):
        if not adv:
            await help_cmd.help_cmd(self.bot, ctx, "coinflip")
            return
        embed = discord.Embed(title=f":coin: {ctx.author.name} contre {adv.name}")
        embed.add_field(value=f"**{ctx.author.mention}, Veuillez choisir pile ou face.**", name="\u200b")
        embed.set_footer(text="Pile ou face ?", icon_url="https://www.de-en-ligne.fr/img/pile-ou-face/pile.png")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("\U0001f17f\uFE0F")
        await msg.add_reaction("🇫")
    
        def checkCote(reaction, user):
            return ctx.author == user and msg.id == reaction.message.id and (str(reaction.emoji) == "\U0001f17f\uFE0F" or str(reaction.emoji) == "🇫")

        reaction, user = await self.bot.wait_for("reaction_add", timeout = None, check = checkCote)
        if reaction.emoji == "\U0001f17f\uFE0F":
            author_choice="pile"
            user_choice="face"
        else:
            author_choice="face"
            user_choice="pile"
        embed = discord.Embed()
        embed.add_field(value=f"**{ctx.author.mention} a choisi le côté {author_choice}. \n{adv.mention}, Veuillez confirmez que vous prenez donc le côté {user_choice}.**", 
                        name="\u200b", inline=False)
        embed.set_footer(text="Pile ou face ?", icon_url="https://www.de-en-ligne.fr/img/pile-ou-face/pile.png")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        
        def checkEmoji(reaction, user):
            return adv == user and msg.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")
  
        reaction, user = await self.bot.wait_for("reaction_add", timeout = None, check = checkEmoji)
        if reaction.emoji == "✅":
            gagnant=random.choice([ctx.author, adv])
            if gagnant == ctx.author:
                perdant=adv
            else:
                perdant=ctx.author
            embed = discord.Embed()
            embed.add_field(name=f"Et le gagnant de ce lancer de pièce est ...", 
                            value=f"**{gagnant.mention} ! Félicitations 🎉 \n\nDésolé {perdant.mention}, retente ta chance**", inline=False)
            embed.set_footer(text="Pile ou face ?", icon_url="https://www.de-en-ligne.fr/img/pile-ou-face/pile.png")
            await ctx.send(embed=embed)
        elif reaction.emoji == "❌":
            embed = discord.Embed()
            embed.add_field(value="**Le lancer est annulé. Dommage...**", name="\u200b")
            await ctx.send(embed=embed)