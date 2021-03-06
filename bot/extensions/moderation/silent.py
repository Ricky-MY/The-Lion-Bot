from discord.ext import commands

def cog_check(ctx):
    return not ctx.guild is not None

class Silent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0xC0C0C0
        self.silented_channels = []
    
    @commands.command(name="silent", aliases=["silence", "hush", "bedtime", "sleepy"])
    @commands.has_guild_permissions(manage_channels = True)
    async def silent(self, ctx):
        """Removes texting access from everyone on the channel invoked in."""
        channel = ctx.channel
        if channel not in self.silented_channels:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            self.silented_channels.append(channel)
            await ctx.send(f"<:textchannel:793503479582425108>👌 {ctx.channel.mention} is put silent by {ctx.author.mention}.")
        elif channel in self.silented_channels:
            await ctx.send(f"⁉️ Channel is already silenced.")

    @commands.command(name="unsilent", aliases=["unsilence", "wakeup", "unhush"])
    @commands.has_guild_permissions(manage_channels = True)
    async def unsilent(self, ctx):
        """Reverts channel silencing, thus giving back texting access to everyone for the channel invoked in."""
        channel = ctx.channel
        if channel in self.silented_channels:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
            await ctx.send(f"<:textchannel:793503479582425108> {ctx.channel.mention} is put active by {ctx.author.mention}.")
            self.silented_channels.remove(channel)
        elif channel not in self.silented_channels:
            await ctx.send(f"⁉️ Channel is not silenced.")

def setup(bot):
    bot.add_cog(Silent(bot))
    print('Silent is loaded')
