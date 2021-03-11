import discord
from discord.ext import commands

def setup(bot):
    bot.add_cog(Logs(bot))

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        ctx=await self.bot.get_context(msg)
        channel=ctx.guild.get_channel(818564737339228180)
        contenu=[]
        for i in enumerate(msg.content):
            if i.isdigit():
                try:
                    user=ctx.guild.get_channel(i)
                    contenu.append(user)
                except:
                    contenu.append(i)
                finally:
                    continue
            contenu.append(i)
                    
        embed = discord.Embed(color=0xff0000)
        embed.set_author(name=contenu)
        await channel.send(f"❌ Le message de **{msg.author}** a été supprimé dans <#{msg.channel.id}> : ", embed=embed)