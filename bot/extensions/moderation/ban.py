import discord
import asyncio

from discord.ext import commands
from discord.ext.commands import Context

from bot.utils.checks import has_higher_role

def cog_check(ctx):
    return not ctx.guild is not None

class Ban(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(1.0, 4.0, commands.BucketType.user)

    async def cog_check(self, ctx: Context) -> bool:
        bucket = self._cd.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            await ctx.message.reply(f"🖐️ Cooldown for {round(retry_after)} seconds!")
            return False
        return True

    @commands.command(name="kick")
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members = True)
    async def kick(self, ctx: Context, member: discord.Member, *, reason="Unspecified"):
        """
        Removes a user from the server. Beware that the user can still re-join, 
        consider using ban to restrict accessibility of this server to the user.
        """
        if not has_higher_role(ctx.author, member):
            await ctx.message.reply("🔴 You can't do this action. Your attempt is recorded.")
            return
        await member.kick(reason=reason)
        await ctx.send(f"🚴🦶 {member.mention} has been kicked for {reason} by {ctx.author.mention}")

    @commands.command(name="ban")
    @commands.has_guild_permissions(ban_members = True)
    @commands.guild_only()
    async def ban(self, ctx: Context, member: discord.Member, *, reason="Unspecified"):
        """
        Places a permanent ban on a user.
        """
        if not has_higher_role(ctx.author, member):
            await ctx.message.reply("🔴 You can't do this action. Your attempt is recorded.")
            return
        await member.ban(reason=reason)
        await ctx.send(f"🚴🔨 {member.mention} has been banned for {reason} by {ctx.author.mention}.")

    @commands.command(name="unban")
    @commands.has_guild_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(self, ctx: Context, id_: int, *, reason = "Unspecified"):
        """
        Lifts an active ban on a user.
        """
        bans = await ctx.guild.bans()
        for ban_entry in bans:
            if ban_entry.user.id == int(id_):
                await ctx.guild.unban(ban_entry.user, reason=reason)
                await ctx.send(f"🛂 {ban_entry.user.mention} has been unbanned by {ctx.author.mention}.")
                return
        await ctx.send(f"🛂 <@{id_}> is not banned.")
                
    @commands.command(name="clear", aliases=["purge"])
    @commands.has_guild_permissions(manage_messages=True)
    async def clear(self, ctx: Context, amount: int =5, user: discord.Member = None):
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
    """Setup function that loads the cog on startup"""
    bot.add_cog(Ban(bot))
    print('Ban and kick is loaded')
