import discord
from discord.ext import commands

def setup(bot):
    bot.add_cog(Genepix(bot))

class Genepix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, ctx):
        channel=ctx.guild.get_channel(796807012947591192)
        bot_members=([m for m in ctx.guild.members if m.bot])
        members=self.bot.users
        await channel.edit(reason="Un membre est arrivé.", name=str(len(members)-len(bot_members)))
        
    @commands.Cog.listener()
    async def on_member_remove(self, ctx):
        channel=ctx.guild.get_channel(796807012947591192)
        bot_members=([m for m in ctx.guild.members if m.bot])
        members=self.bot.users
        await channel.edit(reason="Un membre est parti.", name=str(len(members)-len(bot_members)-1))