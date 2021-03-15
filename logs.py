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
        try:
            texte = msg.content.split("<")
            début=texte[0]
            suite=texte[1].split(">")
            fin=suite[1]
            id=texte[0]
            if id[0]=="#":
                #channel
            elif id[0]=="@":
                #user
            else:
                contenu=msg.content
        except:
            contenu=msg.content
                    
        embed = discord.Embed(color=0xff0000)
        embed.set_author(name=contenu)
        await channel.send(f"❌ Le message de **{msg.author}** a été supprimé dans <#{msg.channel.id}> : ", embed=embed)
