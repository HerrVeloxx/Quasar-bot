import discord
from discord.ext import commands

def setup(bot):
    bot.add_cog(Autres(bot))

class Autres(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        embed = discord.Embed(title="🏓 Pong")
        embed.add_field(name="Temps", value="Temps de réaction du message")
        embed.set_footer(text=f"Requête de {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @commands.command(aliases=["serverinfo", "infoserver", "infoserveur", "serveurinfo","si"])
    async def InfoServeur(self, ctx):
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
