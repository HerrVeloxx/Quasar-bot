import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
import owner

load_dotenv()
cluster=MongoClient(os.getenv("MongoDB"))
db=cluster["Quasar"]
collection=db["prefix"]

default_prefixes = ['/']

async def get_prefix(bot, msg):
    guild = collection.find_one({"guild":msg.guild.id})
    if guild == None:
        return default_prefixes
    else:
        guild=collection.find_one({"guild":msg.guild.id})
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
    changeStatus.start()
    print(f'Successfully logged in and booted...!')

@tasks.loop(seconds = 60)
async def changeStatus():
	activity = discord.Game(name=f"Est connecté à {len(bot.guilds)} serveurs | Développé par Veloxx#4705", type=3)
	await bot.change_presence(status = discord.Status.online, activity = activity)

@bot.command(name="ping")
async def ping(ctx):
    embed = discord.Embed(title="🏓 Pong")
    embed.add_field(name="Temps", value="Temps de réaction du message")
    embed.set_footer(text=f"Requête de {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.command(name="infoserveur")
async def InfoServeur(ctx):
    serveur = ctx.guild
    nombreRoles = len(serveur.roles)
    nombreDeChainesTexte = len(serveur.text_channels)
    nombreDeChainesVocale = len(serveur.voice_channels)
    Description_du_serveur = serveur.description
    Nombre_de_personnes = serveur.member_count
    nomServeur = serveur.name
    embed = discord.Embed(title=f"Info du serveur __***{nomServeur}***__")
    embed.set_thumbnail(url=serveur.icon_url)
    if Description_du_serveur != None:
        embed.add_field(name="Description", value=Description_du_serveur, inline=False)
    embed.add_field(name="Membres", value=Nombre_de_personnes, inline=True)
    embed.add_field(name="Rôles", value=nombreRoles, inline=True)
    embed.add_field(name="Text channels", value=nombreDeChainesTexte, inline=False)
    embed.add_field(name="Voice channels", value=nombreDeChainesVocale, inline=True)
    embed.set_footer(text=f"Requête de {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.command(name="jeu")
async def jeu(ctx):
    await ctx.send("Choisissez un jeu")

bot.add_cog(owner.Owner(bot))
bot.run(os.getenv("TOKEN"))