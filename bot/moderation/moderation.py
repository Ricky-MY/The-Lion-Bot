import discord
import asyncio

from discord.ext import commands

def cog_check(ctx):
    return not ctx.guild is not None

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.color = 0xC0C0C0

    @commands.command(name="kick")
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason):
        """
        Removes a user from the server. Beware that the user can still re-join, 
        consider using ban to restrict accessibility of this server to the user.
        """
        await member.kick(reason=reason)
        await ctx.send(f"🚴🦶 {member.mention} has been kicked for {reason} by {ctx.author.mention}")

    @commands.command(name="ban")
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason):
        """
        Places a permanent ban on a user.
        """
        await member.ban(reason=reason)
        await ctx.send(f"🚴🔨 {member.mention} has been banned for {reason} by {ctx.author.mention}.")

    @commands.command(name="unban")
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, id_, *, reason="Unspecified"):
        """
        Lifts an active ban on a user.
        """
        bans = await ctx.guild.bans()
        for ban_entry in bans:
            if ban_entry.user.id == int(id_):
                await ctx.guild.unban(ban_entry.user, reason=reason)
                await ctx.send(f"🛂 {ban_entry.user.mention} has been unbanned by {ctx.author.mention}.")
                return

    @commands.command(name="clear", aliases=["purge"])
    @commands.has_guild_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5, user: discord.Member = None):
        """
        Removes a certain amount of messages from the channel of which the command is used in. 
        If the amount isn't specified, it will default to 5.
        """
        channel = ctx.channel

        def is_user(message):
            if user is not None:
                return user == message.author
            else:
                return True
        await channel.purge(limit=amount + 1, check=is_user)
        delete = await ctx.send(f"♻️ {amount} messages have been successfully cleared!")
        await asyncio.sleep(5)
        await delete.delete()

def setup(bot):
    """
    Setup function that loads the cog on startup
    """
    bot.add_cog(Moderation(bot))
    print('Moderations is loaded')
