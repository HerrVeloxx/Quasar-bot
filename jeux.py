import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
import random

load_dotenv()
cluster=MongoClient(os.getenv("MongoDB"))
db=cluster["Quasar"]
collection=db["prefix"]

def setup(bot):
    bot.add_cog(Jeux(bot))

class Jeux(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.answer=["assurément !", "c'est sûr !", "essaye encore.", "bien évidemment !", "peut-être...", "pas du tout.", "totalement !", "tu peux y aller !"]
        
    @commands.command(name="8ball")
    async def ball_choice(self, ctx, *, question=None):
        if not question:
            help_cmd(ctx, "ball")
            return
        choice=random.choice(self.answer)
        await ctx.send(f":8ball: **{ctx.author.name}**, {choice}")
        
    @commands.command(name="coinflip")
    async def coinflip(self, ctx, adv: discord.User=None):
        if not adv:
            help_cmd(ctx, "coinflip")
            return
        embed = discord.Embed()
        embed.set_author(name=f"{ctx.author.name} contre {adv.name}")
        embed.add_field(name=None, value=f"**{ctx.author.mention}, Veuillez choisir pile ou face.**")
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
        embed.add_field(name=None, value=f"**{ctx.author.mention} a choisi le côté {author_choice}.**", inline=False)
        embed.add_field(name=None, value=f"**{adv.mention}, Veuillez confirmez que vous prenez donc le côté {user_choice}.**")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        
        def checkEmoji(reaction, user):
            return adv == user and msg.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")
  
        reaction, user = await self.bot.wait_for("reaction_add", timeout = None, check = checkEmoji)
        if reaction.emoji == "✅":
            gagnant=random.choice([ctx.author, adv])
            embed = discord.Embed()
            embed.add_field(name=None, value=f"**Et le gagnant de ce lancer de pièce est ... {gagnant.mention} ! Félicitations 🎉**")
            await ctx.send(embed=embed)
        elif reaction.emoji == "❌":
            embed = discord.Embed()
            embed.add_field(name="Le lancer est annulé. Dommage...", value=None)
            await ctx.send(embed=embed)
     
    async def help_cmd(ctx, cmd):
        guild = collection.find_one({"guild":ctx.guild.id})
        if guild == None:
            prefix = ">"
        else:
            Prefix=guild.get("prefixe")
            prefix = Prefix
        
        if cmd=="ball":
            cmd_name="8ball"
            cmd_desc="Répond à toutes vos questions."
            cmd_util=f"{prefix}8ball [question]"
            cmd_ex=f"{prefix}8ball Ce bot est-il le meilleur ?"
            cmd_alias="Aucun"
        elif cmd=="coinflip":
            cmd_name="Coinflip"
            cmd_desc="Simule un lancer de pièce entre vous et un autre joueur."
            cmd_util=f"{prefix}coinflip [joueur à affronter]"
            cmd_ex=f"{prefix}coinflip {self.bot.mention}"
            cmd_alias="Aucun"
        embed = discord.Embed(title=f"Commande : {cmd_name}")
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Description", value=cmd_desc)
        embed.add_field(name=None, value="**Rappel** : Les crochets tel que [] ne sont pas à utiliser lors de l'éxecution des commandes.")
        embed.add_field(name="Utilisation", value=prefix + cmd_util)
        embed.add_field(name="Exemple", value=prefix + cmd_ex)
        embed.add_field(name="Aliases", value=cmd_alias)
        await ctx.send(embed=embed)
