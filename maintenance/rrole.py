import discord, random
from discord.ext import commands
from discord.ext.commands import Cog
import sqlite3

class RRoles(Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, reaction):
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		if '<:' in str(reaction.emoji):
			cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM rrole WHERE guild_id = '{reaction.guild_id}' and message_id = '{reaction.message_id}' and emoji = '{reaction.emoji.id}'")
			result = cursor.fetchone()
			guild = self.client.get_guild(reaction.guild_id)
			if result is None:
				return
			elif str(reaction.emoji.id) in str(result[0]):
				on = discord.utils.get(guild.roles, id=int(result[1]))
				user = guild.get_member(reaction.user_id)
				await user.add_roles(on)
			else:
				return
		elif '<:' not in str(reaction.emoji):
			cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM rrole WHERE guild_id = '{reaction.guild_id}' and message_id = '{reaction.message_id}' and emoji = '{reaction.emoji}'")
			result = cursor.fetchone()
			guild = self.client.get_guild(reaction.guild_id)
			if result is None:
				return
			elif result is not None:
				on = discord.utils.get(guild.roles, id=int(result[1]))
				user = guild.get_member(reaction.user_id)
				await user.add_roles(on)
			else:
				return
	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, reaction):
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		if '<:' in str(reaction.emoji):
			cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM rrole WHERE guild_id = '{reaction.guild_id}' and message_id = '{reaction.message_id}' and emoji = '{reaction.emoji.id}'")
			result = cursor.fetchone()
			guild = self.client.get_guild(reaction.guild_id)
			if result is None:
				return
			elif str(reaction.emoji.id) in str(result[0]):
				on = discord.utils.get(guild.roles, id=int(result[1]))
				user = guild.get_member(reaction.user_id)
				await user.remove_roles(on)
			else:
				return
		elif '<:' not in str(reaction.emoji):
			cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM rrole WHERE guild_id = '{reaction.guild_id}' and message_id = '{reaction.message_id}' and emoji = '{reaction.emoji}'")
			result = cursor.fetchone()
			guild = self.client.get_guild(reaction.guild_id)
			if result is None:
				return
			elif result is not None:
				on = discord.utils.get(guild.roles, id=int(result[1]))
				user = guild.get_member(reaction.user_id)
				await user.remove_roles(on)
			else:
				return
	@commands.group(invoke_without_command=True)
	async def rrole(self, ctx, channel:discord.TextChannel, message_id, emoji, role:discord.Role):
		async with ctx.channel.typing():
			db = sqlite3.connect('main.sqlite')
			cursor = db.cursor()
			cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM rrole WHERE guild_id = '{ctx.message.guild.id}' and message_id = '{message_id}'")
			result = cursor.fetchone()
			if '<:' in emoji:
				emm = re.sub(':.*?:', '', emoji).strip('<>')
				if result is None:
					sql = ("INSERT INTO rrole(emoji, role, message_id, channel_id, guild_id) VALUES (?, ?, ?, ?, ?)")
					val = (emm, role.id, message_id, channel.id, ctx.guild.id)
					msg = await channel.fetch_message(int(message_id))
					em = self.client.get_emoji(int(emm))
					await msg.add_reaction(em)
					cursor.execute(sql, val)
					db.commit()
				elif str(message_id) not in str(result[2]):
					sql = ("INSERT INTO rrole(emoji, role, message_id, channel_id, guild_id) VALUES (?, ?, ?, ?, ?)")
					val = (emm, role.id, message_id, channel.id, ctx.guild.id)
					msg = await channel.fetch_message(int(message_id))
					em = self.client.get_emoji(int(emm))
					await msg.add_reaction(em)
					cursor.execute(sql, val)
					db.commit()
			elif '<:' not in emoji:
				if result is None:
					sql = ("INSERT INTO rrole(emoji, role, message_id, channel_id, guild_id) VALUES (?, ?, ?, ?, ?)")
					val = (emoji, role.id, message_id, channel.id, ctx.guild.id)
					msg = await channel.fetch_message(int(message_id))
					await msg.add_reaction(emoji)
					cursor.execute(sql, val)
					db.commit()
				elif str(message_id) not in str(result[2]):
					sql = ("INSERT INTO rrole(emoji, role, message_id, channel_id, guild_id) VALUES (?, ?, ?, ?, ?)")
					val = (emoji, role.id, message_id, channel.id, ctx.guild.id)
					msg = await channel.fetch_message(int(message_id))
					await msg.add_reaction(emoji)
					cursor.execute(sql, val)
					db.commit()
			cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM rrole WHERE guild_id = '{ctx.message.guild.id}'")
			result = cursor.fetchone()
			role = ctx.guild.get_role(int(result[1]))
			channel = ctx.guild.get_channel(int(result[3]))
			embed = discord.Embed(title="Success!", description = f'{role.mention} role will been assigned to members when they react with {emoji} to the message(ID:{message_id}) in channel {channel.mention}.', color=discord.Colour.dark_teal())
			await ctx.send(embed=embed)
			db.commit()
			cursor.close()
			db.close()
	@rrole.command()
	async def clear(self, ctx, message_id):
		async with ctx.channel.typing():
			db = sqlite3.connect('main.sqlite')
			cursor = db.cursor()
			cursor.execute(f"SELECT emoji, channel_id FROM rrole WHERE guild_id = '{ctx.message.guild.id}'")
			result = cursor.fetchone()
			channel = ctx.guild.get_channel(int(result[1]))
			message = await channel.fetch_message(int(message_id))
			await message.remove_reaction(result[0], ctx.me)
			cursor.execute(f"DELETE FROM rrole WHERE message_id = '{message_id}'")
			db.commit()
			cursor.close()
			db.close()
			await ctx.send(f"> **SUCCESSFULLY CLEARED REACTION ROLE OBJECT FOR {message_id}!**")
	@rrole.command()
	async def check(self, ctx):
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT emoji, role, channel_id, message_id FROM rrole WHERE guild_id = '{ctx.message.guild.id}'")
		result = cursor.fetchall()
		embed = discord.Embed(title="All existing reactionrole objects:", color=discord.Colour.dark_gold())
		for objects in result:
		#objects will give [emoji, role, channel_id, message_id]
			emoji=objects[0]
			role=ctx.guild.get_role(int(objects[1]))
			channel=ctx.guild.get_channel(int(objects[2]))
			print(channel)
			embed.add_field(name=f"For MessageID = {objects[3]}", value= f" Emoji={emoji}\nChannel={channel.mention}\nRole={role.mention}")
		await ctx.send(embed=embed)
		cursor.close()
		db.close()

def setup(client):
	client.add_cog(RRoles(client))
	print('RRoles.cog loaded')
