import discord
from discord.ext import commands

def setup(bot):
    bot.add_cog(Owner(bot))

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def id_check(ctx):
        return ctx.message.author.id == 415438702547042304 or ctx.message.author.id == 318494616355602432

    @commands.command(name="reload", hidden=True)
    @commands.check(id_check)
    async def reload(self, ctx, name=None):
        if name:
            try:
                self.bot.reload_extension(name)
                await ctx.send(f"L'extension {name} a bien été reload !")
            except:
                self.bot.load_extension(name)
                await ctx.send(f"L'extension {name} a bien été load !")
