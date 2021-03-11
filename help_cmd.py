import discord
import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
cluster=MongoClient(os.getenv("MongoDB"))
db=cluster["Quasar"]
collection=db["prefix"]

async def help_cmd(bot, ctx, cmd):
    guild = collection.find_one({"guild":ctx.guild.id})
    if guild == None:
        prefix = ">"
    else:
        Prefix=guild.get("prefixe")
        prefix = Prefix
    
    if cmd=="ball":
        cmd_name="8ball"
        cmd_desc="Répond à toutes vos questions."
        cmd_util="8ball [question]"
        cmd_ex="8ball Ce bot est-il le meilleur ?"
        cmd_alias=f"{prefix}8b"
    elif cmd=="coinflip":
        cmd_name="Coinflip"
        cmd_desc="Simule un lancer de pièce entre vous et un autre joueur."
        cmd_util="coinflip [joueur à affronter]"
        cmd_ex=f"coinflip {bot.user.mention}"
        cmd_alias=f"{prefix}coin \n{prefix}cf"
        
    embed = discord.Embed(title=f"Commande : {cmd_name}", inline=False)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    embed.add_field(name="Description", value=f"{cmd_desc} \n\n**Rappel** : Les crochets tel que [] ne sont pas à utiliser lors de l'éxecution des commandes.", inline=False)
    embed.add_field(name="Utilisation", value=prefix + cmd_util, inline=False)
    embed.add_field(name="Exemple", value=prefix + cmd_ex, inline=False)
    embed.add_field(name="Aliases", value=cmd_alias, inline=False)
    embed.set_footer(text=f"{bot.user.name} • Développé par Veloxx#4705 et eupone#9975", icon_url=bot.user.avatar_url)
    await ctx.send(embed=embed)