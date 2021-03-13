import discord
from discord.ext import commands, tasks

from datetime import datetime


class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.remove_timed_muted.start()
        self.timed_muted_list = []

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member in [i[0] for i in self.timed_muted_list]:
            await member.add_roles(self.mute_role)

    async def prepare_mute_role(self, ctx):
        for role in ctx.guild.roles:
            if role.name == "Muted":
                return role
        muting = discord.PermissionOverwrite(send_messages=False)
        mute = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(mute, overwrite=muting)
        return mute

    async def temp_mute_initiate(self, ctx, member, time):
        H, M, S = (int(datetime.now().strftime("%H")),
                   int(datetime.now().strftime("%M")),
                   int(datetime.now().strftime("%S")))

        expiry_time_M = M + int(time)
        expiry_time_H = H
        expiry_time_S = S
        while expiry_time_M > 60:
            expiry_time_H += 1
            expiry_time_M -= 60
        self.timed_muted_list.append(
            (member, (expiry_time_H, expiry_time_M, expiry_time_S)))

    @commands.command(name="permanentmute", aliases=["permute", "permmute", "pmute"])
    @commands.guild_only()
    @commands.has_guild_permissions(mute_members=True)
    async def permanent_mute(self, ctx, member: discord.Member):
        """Permanently restrict send message access from the user. This process is evadable by re-join. Consider using blacklist."""
        self.mute_role = await self.prepare_mute_role(ctx)
        if member not in [i[0] for i in self.timed_muted_list] and self.mute_role not in member.roles:
            await member.add_roles(self.mute_role)
            await ctx.reply(f"🗣️👌 {member} is muted by {ctx.author.mention}.")
        else:
            await ctx.reply("⁉️ Member already muted.")

    @commands.command(name="mute", aliases=["tmute", "tempmute"])
    @commands.guild_only()
    @commands.has_guild_permissions(mute_members=True)
    async def temporary_mute(self, ctx, member: discord.Member, time='10m'):
        """Restrict send message access from a user for a set amount of time. If no duration is provided, the user will be muted for 10 minutes. This process is unevadable by re-joins."""
        self.mute_role = await self.prepare_mute_role(ctx)
        if member not in [i[0] for i in self.timed_muted_list] and self.mute_role not in member.roles:
            mode = 'minute'
            mode_definator = time[-1].lower()
            if mode_definator == 'd':
                time = int(time[:-1]) * 1, 440
                mode = 'day'
            elif mode_definator == 'h':
                time = int(time[:-1]) * 60
                mode = 'hour'
            elif mode_definator == 'm':
                time = int(time[:-1])
                mode = 'minute'
            else:
                time = int(time[:])
            await member.add_roles(self.mute_role)
            await ctx.reply(f"🗣️👌 {member} is muted by {ctx.author.mention} for {time} {mode + 's' if time > 1 else mode}.")
            await self.temp_mute_initiate(ctx, member, time)
        else:
            await ctx.reply("⁉️ Member already muted.")

    @commands.command(name="selfmute", aliases=["smute"])
    @commands.guild_only()
    async def self_temporary_mute(self, ctx, time='10m'):
        """Restrict send message access for yourself server-wide. If no duration is provided, you will be muted for 10 minutes. The bot will tuck you into bed, goodnight."""
        self.mute_role = await self.prepare_mute_role(ctx)
        member = ctx.author
        mode = 'minute'
        mode_definator = time[-1].lower()
        if mode_definator == 'd':
            time = int(time[:-1]) * 1, 440
            mode = 'day'
        elif mode_definator == 'h':
            time = int(time[:-1]) * 60
            mode = 'hour'
        elif mode_definator == 'm':
            time = int(time[:-1])
            mode = 'minute'
        else:
            time = int(time[:])
        await member.add_roles(self.mute_role)
        await ctx.reply(f"🗣️👌 Goodnight bud, for {time} {mode + 's' if time > 1 else mode}.")
        await self.temp_mute_initiate(ctx, member, time)

    @commands.command(name="mutesetup")
    @commands.has_guild_permissions(mute_members=True)
    async def mute_setup(self, ctx):
        """Prepares the server for a mute role that strips away send message access from the user."""
        guild = ctx.guild
        for role in guild.roles:
            if role.name == "Muted":
                self.mute_role = role
        for channel in guild.text_channels:
            await channel.set_permissions(self.mute_role, overwrite=discord.PermissionOverwrite(send_messages=False))
        await ctx.send("Success!")

    @commands.command(name="unmute")
    @commands.has_guild_permissions(mute_members=True)
    async def unmute(self, ctx, member: discord.Member):
        """Removes an active mute from a user whether it be permanent or temporary."""
        self.mute_role = await self.prepare_mute_role(ctx)
        if member in [i[0] for i in self.timed_muted_list] or self.mute_role in member.roles:
            await member.remove_roles(self.mute_role)
            try:
                self.timed_muted_list.remove(
                    [i for i in self.timed_muted_list if i[0] == member][0])
            except:
                pass
            await ctx.send(f"🗣️ {member} is unmuted by {ctx.author.mention}.")
            return
        else:
            "⁉️ Member is not muted"

    @tasks.loop(minutes=1)
    async def remove_timed_muted(self):
        H, M, S = (int(datetime.now().strftime("%H")),
                   int(datetime.now().strftime("%M")),
                   int(datetime.now().strftime("%S")))
        for entry in self.timed_muted_list:
            if entry[1][0] < H: # by hour difference
                self.timed_muted_list.remove(entry)
                await entry[0].remove_roles(self.mute_role)
            elif entry[1][0] == H and entry[1][1] <= M: # by minute difference
                self.timed_muted_list.remove(entry)
                await entry[0].remove_roles(self.mute_role)
            elif entry[1][0] == H and entry[1][1] == M and entry[1][2] <= S: # by second difference
                self.timed_muted_list.remove(entry)
                await entry[0].remove_roles(self.mute_role)
            else:
                pass

def setup(bot):
    bot.add_cog(Mute(bot))
    print("Mute is loaded")
