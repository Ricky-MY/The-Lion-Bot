import discord
import sqlite3
import yaml
import asyncio

from discord.ext import commands
from datetime import datetime


class Misc(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		with open("config.yaml", 'r') as file:
			config = yaml.load(file, Loader=yaml.SafeLoader)
		self.color = config["asthetics"]["mainColor"]

	@commands.command(name="addrole", aliases=["ar", "makerole", "mkrole"])
	@commands.guild_only()
	@commands.has_guild_permissions(manage_roles=True)
	async def addrole(self, ctx, name, hex_colour_code=discord.Colour.default(), hoist=False):
		"""Creates a role with basic permissions and a specifiable name, color and hoist choices."""
		guild = ctx.guild
		role = await guild.create_role(name=name, colour=hex_colour_code, hoist=hoist)
		embed = discord.Embed(
		    title="Success!", description=f'{role.mention}', color=self.color)
		embed.add_field(name='Colour', value=f"{hex_colour_code}")
		embed.add_field(name='Displays Seperatey', value=f"{hoist}")
		await ctx.send(embed=embed)

	@commands.command(name="delrole", aliases=['dr', "deleterole", "removerole", "remrole"])
	@commands.guild_only()
	@commands.has_guild_permissions(manage_roles=True)
	async def delrole(self, ctx, *, roles: commands.Greedy[discord.Role]):
		"""Remove roles in bulk."""
		for role in roles:
			await role.delete()
			await asyncio.sleep(0.3)

		embed = discord.Embed(title="Success!", description=f'Roles successfuly deleted!',
							  color=self.color)
		await ctx.reply(embed=embed, mention_author=False)

	@commands.command(name="avatar", aliases=['profile'])
	@commands.guild_only()
	async def avatar(self, ctx, member: discord.Member = None):
		"""Retrieves the avatar of a user."""
		await ctx.reply(member.avatar_url if member is not None else ctx.author.avatar_url, mention_author=False)

	@commands.command(name="invite")
	async def invite(self, ctx):
		"""Gets the invite link for the support server of the bot."""
		await ctx.send('https://discord.gg/mh7pZ8K')

	@commands.command(name="userinfo", aliases=['details', 'memberinfo', 'info'])
	@commands.guild_only()
	async def user_info(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		embed = discord.Embed(title=f"User Information", color=self.color,
								timestamp=datetime.datetime.utcnow())
		embed.set_thumbnail(url=ctx.author.avatar_url)
		embed.set_thumbnail(url=ctx.guild.icon_url)
		fields = (("ID:", ctx.author.id),
				("Name:", ctx.author.name),
				("Bot:", ctx.author.bot),
				("Primary Role:", ctx.author.top_role),
				("Discord Status:", str(ctx.author.status).title()),
				("Created at:", ctx.author.created_at.strftime("%d/%m/%Y %H:%M:%S")),
				("Joined at:", ctx.author.joined_at.strftime("%d/%m/%Y %H:%M:%S")),
				("Booster:", bool(ctx.author.premium_since)))
		for name, value in fields:
			embed.add_field(name=name, value=value, inline=True)
		await ctx.reply(embed=embed, mention_author=False)

	@commands.group(name="membercounter", aliases=['mbc'], invoke_without_command=True)
	@commands.guild_only()
	@commands.has_permissions(administrator=True)
	async def membercounter(self, ctx, channel: discord.VoiceChannel):
		db=sqlite3.connect('main.sqlite')
		cursor=db.cursor()
		cursor.execute(
		    "SELECT channel_id FROM member_count_channel WHERE guild_id = ?", (ctx.guild.id,))
		result=cursor.fetchone()
		if result is None:
			sql=("INSERT INTO member_count_channel(guild_id, channel_id) VALUES (?, ?)")
			val=(ctx.guild.id, channel.id)
			cursor.execute(sql, val)
			db.commit()
			embed=discord.Embed(
			    title=f"Preset", description=f"> SUCCESSFULLY RECONFIGURED CHANNEL : {channel.mention}\nExecute `{ctx.prefix}mbc check` to check the preset anytime!", colour=self.color)
			await ctx.send(embed=embed)
			cursor.close()
			db.close()
		elif result is not None:
			sql=("UPDATE member_count_channel SET channel_id = ? WHERE guild_id = ?")
			val=(channel.id, ctx.guild.id)
			cursor.execute(sql, val)
			db.commit()
			embed=discord.Embed(
			    title=f"Preset", description=f"> SUCCESSFULLY CONFIGURED CHANNEL : {channel.mention}\nExecute `{ctx.prefix}mbc check` to check the preset anytime!", colour=self.color)
			await ctx.send(embed=embed)
			cursor.close()
			db.close()

	@membercounter.command()
	async def check(self, ctx):
		db=sqlite3.connect('main.sqlite')
		cursor=db.cursor()
		cursor.execute(
		    "SELECT channel_id FROM member_count_channel WHERE guild_id = ?", (ctx.guild.id,))
		result=cursor.fetchone()
		if result is None:
			embed=discord.Embed(
			    title=f"N/A!", description=f"> NO PRESETS FOUND!\nExecute `{ctx.prefix}mbc (<#VoiceChannelId>)` to select a voice channel as your member counter!", colour=discord.Colour.dark_red())
			await ctx.send(embed=embed)
		elif result is not None:
			channel=self.bot.get_channel(result[0])
			embed=discord.Embed(
			    title=f"Preset", description=f"> CONFIGURED CHANNEL : {channel.mention}\nExecute `{ctx.prefix}mbc (<#VoiceChannelId>)` to change which voice channel to use as the server member counter!", colour=self.color)
			await ctx.send(embed=embed)

	@membercounter.command()
	async def clear(self, ctx):
		db=sqlite3.connect('main.sqlite')
		cursor=db.cursor()
		cursor.execute(
		    "DELETE FROM member_count_channel WHERE guild_id = ? ", (ctx.guild.id,))
		db.commit()
		cursor.close()
		db.close()
		embed=discord.Embed(
		    title=f"Success!", description=f"> SUCCESSFULLY CLEARED PREFERENCES IF FOUND!\nExecute `{ctx.prefix}mbc (<#VoiceChannelId>)` to select a voice channel as your member counter!", colour=self.color)
		await ctx.send(embed=embed)

	@commands.command(name="migrate")
	@commands.has_guild_permissions(move_members=True)
	async def migrate(self, ctx, ini_id, end_id):
		ini_channel=ctx.guild.get_channel(int(ini_id))
		end_channel=ctx.guild.get_channel(int(end_id))
		all_members=ini_channel.members
		for member in all_members:
			await member.move_to(end_channel)
		await ctx.send("**`Successfully moved everyone`**")

def setup(bot):
	bot.add_cog(Misc(bot))
	print('Misc.cog is loaded')
