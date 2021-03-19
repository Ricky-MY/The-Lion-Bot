from datetime import datetime
import discord

from typing import Optional

from discord.ext.commands.context import Context

from bot.utils.checks import has_higher_role
from discord.ext import commands, tasks

AWARENESS = 1

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.remove_timed_muted.start()
        self.timed_muted_list = []

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member in [i[0] for i in self.timed_muted_list]:
            await member.add_roles(self.mute_role)

    def find_mute_role(self, member: discord.Member) -> Optional[discord.Role]:
        for role in member.roles:
            if not role.permissions.send_messages:
                return role

    async def get_mute_role(self, guild: discord.Guild) -> Optional[discord.Role]:
        """
        Gets the context to get the guild where the command was invoked in.
        Loops through the roles inside the guild to find a mute role and returns
        it.
        """
        for role in guild.roles:
            if role.name.lower() in ("muted", "mute", "muter"):
                return role
        muting = discord.PermissionOverwrite(send_messages=False)
        mute = await guild.create_role(name="Muted")
        for channel in guild.text_channels:
            await channel.set_permissions(mute, overwrite=muting)
        return mute

    async def enforce_mute(self, ctx: Context, member: discord.Member):
        """
        Performs the action that restricts send_message permissions
        from the user
        """
        role = await self.get_mute_role(ctx.guild)
        await member.add_roles(role)

    async def timeit_tempmute(self, member: discord.Member, time: int):
        """
        Gets the member and the time. Calculates the ending time of the mute and
        appends the member and endtime to an instance variable. 
        The instance variable gets iterated through every 1 minute to check 
        if any of the mutes have timed out.
        """
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

    def get_duration_tempmute(self, time: int):
        """
        Converts the time passed in into minutes using a definator
        passed in and returns it.
        """
        mode_definator = 'm'
        mode = 'minute'
        realtime = time[:-1]
        try:
            int(time[-1])
        except:
            mode_definator = time[-1]
        else:
            pass
        mode_definator = time[-1].lower()
        if mode_definator == 'd':
            time = int(time[:-1]) * 1440
            mode = 'day'
        elif mode_definator == 'h':
            time = int(time[:-1]) * 60
            mode = 'hour'
        elif mode_definator == 'm':
            time = int(time[:-1])
            mode = 'minute'
        return mode, int(time), realtime

    @commands.command(name="permanentmute", aliases=["permute", "permmute", "pmute"])
    @commands.has_guild_permissions(mute_members=True)
    @commands.guild_only()
    async def permanent_mute(self, ctx: Context, member: discord.Member):
        """
        Permanently restrict send message access from the user. 
        This process is evadable by re-join. Consider using blacklist.
        """
        if not has_higher_role(ctx.author, member):
            await ctx.message.reply("🔴 You can't do this action. Your attempt is recorded.")
            return
        mute_role = await self.get_mute_role(ctx.guild)
        if (member not in self.timed_muted_list) and (mute_role not in member.roles):
            await self.enforce_mute(ctx, member)
            await ctx.reply(f"🗣️👌 {member} is permanently muted by {ctx.author.mention}.")
        elif (member in self.timed_muted_list) or (mute_role in member.roles):
            await ctx.reply("⁉️ Member already muted.")

    @commands.command(name="mute", aliases=["tmute", "tempmute", "nightnight"])
    @commands.has_guild_permissions(mute_members=True)
    @commands.guild_only()
    async def temporary_mute(self, ctx: Context, member: discord.Member, time='10m'):
        """
        Temporarily restrict send message access from a user for a set amount of time. 
        If no duration is provided, the user will be muted for 10 minutes. 
        This process is unevadable by re-joins.
        """
        if not has_higher_role(ctx.author, member):
            await ctx.message.reply("🔴 You can't do this action. Your attempt is recorded.")
            return
        mute_role = await self.get_mute_role(ctx.guild)
        if (member not in self.timed_muted_list) and (mute_role not in member.roles):
            mode, time, realtime = self.get_duration_tempmute(time)
            await self.timeit_tempmute(member, time)
            await self.enforce_mute(ctx, member)
            await ctx.reply(f"🗣️👌 {member} is muted by {ctx.author.mention} for {realtime} {mode + 's' if time > 1 else mode}.")
        elif (member in self.timed_muted_list) or (mute_role in member.roles):
            await ctx.reply("⁉️ Member already muted.")

    @commands.command(name="selfmute", aliases=["smute", "zoology"])
    @commands.guild_only()
    async def self_temporary_mute(self, ctx: Context, time='10m'):
        """
        Restrict send message access for yourself server-wide. 
        If no duration is provided, you will be muted for 10 minutes. 
        The bot will tuck you into bed, goodnight.
        """
        member = ctx.author
        mute_role = await self.get_mute_role(ctx.guild)
        if (member not in self.timed_muted_list) and (mute_role not in member.roles):
            mode, time, realtime = self.get_duration_tempmute(time)
            await self.timeit_tempmute(member, time)
            await self.enforce_mute(ctx, member)
            await ctx.reply(f"🗣️👌 {member} is muted by {ctx.author.mention} for {realtime} {mode + 's' if time > 1 else mode}.")
        elif (member in self.timed_muted_list) or (mute_role in member.roles):
            await ctx.reply("⁉️ Member already muted.")

    @commands.command(name="mutesetup")
    @commands.has_guild_permissions(mute_members=True)
    async def mute_setup(self, ctx: Context):
        """
        Prepares the server for a mute role that strips away send message access from the user.
        """
        guild = ctx.guild
        mute_role = await self.get_mute_role(ctx.guild)
        for channel in guild.text_channels:
            await channel.set_permissions(mute_role, overwrite=discord.PermissionOverwrite(send_messages=False))
        await ctx.send("Success!")

    @commands.command(name="unmute")
    @commands.has_guild_permissions(mute_members=True)
    async def unmute(self, ctx: Context, member: discord.Member):
        """
        Removes an active mute from a user whether it be permanent or temporary.
        """
        mute_role = await self.get_mute_role(ctx.guild)
        if member in [i[0] for i in self.timed_muted_list] or mute_role in member.roles:
            await member.remove_roles(mute_role)
            try:
                self.timed_muted_list.remove(
                    [i for i in self.timed_muted_list if i[0] == member][0])
            except:
                pass
            await ctx.send(f"🗣️ {member} is unmuted by {ctx.author.mention}.")
            return
        else:
            "⁉️ Member is not muted"

    @tasks.loop(minutes=AWARENESS)
    async def remove_timed_muted(self):
        H, M, S = (int(datetime.now().strftime("%H")),
                int(datetime.now().strftime("%M")),
                int(datetime.now().strftime("%S")))
        for entry in self.timed_muted_list:
            mute_role = self.find_mute_role(entry[0])
            if entry[1][0] < H:  # by hour difference
                self.timed_muted_list.remove(entry)
                await entry[0].remove_roles(mute_role)
            elif entry[1][0] == H and entry[1][1] <= M:  # by minute difference
                self.timed_muted_list.remove(entry)
                await entry[0].remove_roles(mute_role)
            elif entry[1][0] == H and entry[1][1] == M and entry[1][2] <= S:  # by second difference
                self.timed_muted_list.remove(entry)
                await entry[0].remove_roles(mute_role)
            else:
                pass

def setup(bot):
    bot.add_cog(Mute(bot))
    print("Mute is loaded")
