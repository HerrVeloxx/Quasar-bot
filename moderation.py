import discord
from discord.ext import commands

def setup(bot):
    bot.add_cog(commandsModerator(bot))

class commandsModerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["clear", "del"])
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx, number: int):
        messages = await ctx.channel.history(limit=number + 1).flatten()
        for msg in messages:
            await msg.delete()

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user : discord.User, *, raison):
        await ctx.guild.kick(user, reason=raison)
        embed = discord.Embed(color=0xC63E21)
        embed.set_author(name=f"[KICK] {user}", icon_url=user.avatar_url)
        embed.add_field(name="User", value=user, inline=True)
        embed.add_field(name="Reason", value=raison, inline=True)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user : discord.User, *, raison):
        await ctx.guild.ban(user, reason=raison)
        embed = discord.Embed(color=0xFE1B00)
        embed.set_author(name=f"[BAN] {user}", icon_url=user.avatar_url)
        embed.add_field(name="User", value=user, inline=True)
        embed.add_field(name="Reason", value=raison, inline=True)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        await ctx.send(embed=embed)