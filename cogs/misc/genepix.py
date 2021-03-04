import discord
from discord.ext import commands

def setup(bot):
    bot.add_cog(Genepix(bot))

class Genepix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    #@commands.Cog.listener()
    @commands.command(name="channel")
    async def channel(self, ctx):
        channel=ctx.guild.get_channel(796807012947591192)
        real_members = []
        for member in ctx.guild.members:
            print(member)
            if member.bot == False:
                real_members.append(member)
        await channel.edit(reason="Nouveau membre", name=str(len(real_members)))