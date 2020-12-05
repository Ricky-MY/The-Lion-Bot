import discord
from discord.ext import commands
from discord.ext.commands import Cog
import sqlite3
import datetime
  

class Welcome(Cog):

	def __init__(self, client):
		self.client = client

	@commands.group(name="greet", aliases=['wel'], invoke_without_command=True)
	async def welcome(self, ctx, channel: discord.TextChannel, color=int(000000), *, msg):
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute("SELECT channel_id, msg FROM welcome WHERE guild_id = ?", (ctx.guild.id,))
		result = cursor.fetchone()
		if result is None:
			sql = ("INSERT INTO welcome(guild_id, channel_id, msg, color) VALUES (?, ?, ?, ?)")
			val = (ctx.guild.id, channel.id, msg, str(color))
			cursor.execute(sql, val)
			embed=discord.Embed(title=f"Success!", description=f"SUCCESSFULLY CONFIGURED INTO \n> `Channel`: {channel.mention}\n> `Color` = #{color}\n> `Message` = {msg}\n Execute: `{ctx.prefix}welcome check` to check the embeded welcome message!", colour=discord.Colour.dark_teal())
			await ctx.send(embed=embed)
		elif result is not None:
			sql = ("UPDATE welcome SET channel_id = ?, msg = ?, color = ? WHERE guild_id = ?")
			val = (channel.id, msg, str(color), ctx.guild.id)
			cursor.execute(sql, val)
			embed=discord.Embed(title=f"Success!", description=f"SUCCESSFULLY RECONFIGURED INTO \n> `Channel`: {channel.mention} \n> `Color` = #{color}\n> `Message` = {msg}\n Execute: `{ctx.prefix}welcome check` to check the embeded welcome message!", colour=discord.Colour.dark_teal())
			await ctx.send(embed=embed)
		db.commit()
		cursor.close()
		db.close()

	@welcome.command()
	async def check(self, ctx):
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute("SELECT msg, channel_id, color FROM welcome WHERE guild_id = ?", (ctx.guild.id,))
		result = cursor.fetchone()
		if result is None:
			embed=discord.Embed(title=f"N/A!", description=f"> NO PRESETS FOUND!\nExecute : `{ctx.prefix}welcome <channel> <hex_color_code> <message>` to set an embeded welcome message!", colour=discord.Colour.dark_red())
			await ctx.send(embed=embed)
		else:
			members = len(list(ctx.guild.members))
			mention = ctx.author.mention
			guild = ctx.guild.name
			user = ctx.author.name
			channel = self.client.get_channel(id=int(result[1]))
			embed = discord.Embed(
				description=str(result[0]).format(members=members, mention=mention, user=user, guild=guild),
				color=int(result[2]))
			embed.set_thumbnail(url=f"{self.client.user.avatar_url}")
			embed.set_author(name=f"{ctx.author}")
			embed.add_field(name="Channel is set to:", value=f"{channel.mention}")
			embed.set_footer(text=f"Above is an example of how your text would look like when its used.")
			embed.timestamp = datetime.datetime.utcnow()
			await ctx.send(embed=embed)

	@welcome.command()
	async def clear(self, ctx):
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute("DELETE FROM welcome WHERE guild_id = ?", (ctx.guild.id,))
		db.commit()
		cursor.close()
		db.close()
		embed=discord.Embed(title=f"Success!", description=f"> SUCCESSFULLY CLEARED PREFERENCES IF FOUND!\nExecute: `{ctx.prefix}welcome <channel> <hex_color_code> <message>` to set an embeded welcome message!", colour=discord.Colour.dark_teal())
		await ctx.send(embed=embed)

	@commands.Cog.listener()
	async def on_member_join(self, member):
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute("SELECT channel_id, msg FROM welcome WHERE guild_id = ?", (member.guild.id,))
		result = cursor.fetchone()
		if result[0] is None:
			return
		else:
			cursor.execute("SELECT msg, color FROM welcome WHERE guild_id = ?", (member.guild.id,))
			result1 = cursor.fetchone()
			members = len(list(member.guild.members))
			mention = member.mention
			guild = member.guild.name
			user = member.name
			channel = self.client.get_channel(id=int(result[0]))
			embed = discord.Embed(
				description=str(result1[0]).format(members=members, mention=mention, user=user, guild=guild),
				color=int(result1[1]))
			embed.set_thumbnail(url=f"{member.avatar_url}")
			embed.set_author(name=f"{member}")
			embed.timestamp = datetime.datetime.utcnow()
			await channel.send(embed=embed)


def setup(client):
	client.add_cog(Welcome(client))
	print('Welcome.cog is loaded')
