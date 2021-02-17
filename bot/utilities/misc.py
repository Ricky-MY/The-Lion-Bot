import discord
import sqlite3
import pytz 

from discord.ext import commands, tasks
from datetime import datetime 

class Misc(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.time_changer.start()

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.message_id == 776373093929189418:
			member = payload.member
			emoji = str(payload.emoji)
			guild = discord.utils.find(lambda g : g.id == payload.guild_id, self.client.guilds)
			if emoji == '❤️':
				role = guild.get_role(776371863785046027)
				await member.add_roles(role)
			elif emoji == '🔵':
				role = guild.get_role(776341343235735572)
				await member.add_roles(role)
			elif emoji == '🟨':
				role = guild.get_role(776341346364686346)
				await member.add_roles(role)
			elif emoji == '🔷':
				role = guild.get_role(776341580159385620)
				await member.add_roles(role)
			elif emoji == '🌳':
				role = guild.get_role(776372310340403220)
				await member.add_roles(role)
			elif emoji == '⬛':
				role = guild.get_role(776372214341697566)
				await member.add_roles(role)
		elif payload.message_id == 783679164544188437:
			member = payload.member
			emoji = str(payload.emoji)
			guild = discord.utils.find(lambda g : g.id == payload.guild_id, self.client.guilds)
			if emoji == '🐍':
				role = guild.get_role(783676031680774174)
				await member.add_roles(role)
			elif emoji == '☕':
				role = guild.get_role(783676027107934248)
				await member.add_roles(role)
				

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self,payload):
		if payload.message_id == 776373093929189418:
			emoji = str(payload.emoji)
			guild = discord.utils.find(lambda g : g.id == payload.guild_id, self.client.guilds)
			member = guild.get_member(payload.user_id)
			roles = [776371863785046027,776341343235735572,776341346364686346,776341580159385620,776372310340403220,776372214341697566]
			roles_obj = []
			for role in roles:
				roles_obj.append(guild.get_role(role))
			for i in roles_obj:
				await member.remove_roles(i)

	# MemberCount Command
	@commands.command(name="members", aliases=['u', 'm'])
	@commands.guild_only()
	async def users(self, ctx): 
		guild = ctx.guild # 776341580159385620 776341346364686346 776341343235735572
		usembed = discord.Embed(description=f'Members: {guild.member_count}', color=discord.Colour.dark_gold())
		usembed.set_author(name=f'{guild}', icon_url=guild.icon_url)
		await ctx.channel.send(embed=usembed)

	# Role Creation Command
	@commands.command(name="addrole", aliases=['ar'])
	@commands.guild_only()
	@commands.has_guild_permissions(manage_roles=True)
	async def addrole(self, ctx, name, hex_colour_code=discord.Colour.default(), hoist=False):
		guild = ctx.guild
		role = await guild.create_role(name=name, colour=hex_colour_code, hoist=hoist)
		embed = discord.Embed(title="Success!", description=f'{role.mention}', color=discord.Colour.dark_teal())
		embed.add_field(name='Colour', value=f"{hex_colour_code}")
		embed.add_field(name='Displays Seperatey', value=f"{hoist}")
		await ctx.send(embed=embed)

	# Role Deletion Command
	@commands.command(name="delrole", aliases=['dr'])
	@commands.guild_only()
	@commands.has_guild_permissions(manage_roles=True)
	async def delrole(self, ctx, *, role: discord.Role):
		guild = ctx.guild
		await role.delete()
		embed = discord.Embed(title="Success!", description=f'Role is successfuly deleted!',
							  color=discord.Colour.dark_teal())
		await ctx.send(embed=embed)

	# Role giving Command
	@commands.command(name="giverole", aliases=['gr'])
	@commands.guild_only()
	@commands.has_guild_permissions(manage_roles=True)
	async def giverole(self, ctx, member: discord.Member, role: discord.Role):
		await member.add_roles(role)
		embed = discord.Embed(title="Success!",
							  description=f'{role.mention} role has successfuly been assigned to {member.mention}',
							  color=discord.Colour.dark_teal())
		embed.set_footer(text=f'By {ctx.author.name}', icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)

	# Avatar Command
	@commands.command(name="avatar", aliases=['profile'])
	@commands.guild_only()
	async def avatar(self, ctx, member: discord.Member):
		url = member.avatar_url
		await ctx.send(url)

	# Invite Command
	@commands.command(name="invite")
	async def invite(self, ctx):
		await ctx.send('https://discord.gg/mh7pZ8K')

	# Hello Command
	@commands.command()
	async def hello(self, ctx):
		await ctx.send(f'Hi! {ctx.author.name} ;3')

	# Announce command
	@commands.group(name="announce", invoke_without_command=True)
	@commands.guild_only()
	@commands.has_guild_permissions(manage_roles=True)
	async def announce(self, ctx, channel: discord.TextChannel, *, msg):
		embed = discord.Embed(description=msg, colour=discord.Colour.dark_gold())
		embed.set_author(name="ANNOUNCEMENT!", icon_url=ctx.guild.icon_url)
		embed.timestamp = datetime.datetime.utcnow()
		await channel.send(embed=embed)
		sembed = discord.Embed(title='Success!',
								description=f'Successfully announced `{msg}` in {channel.mention}',
								color=discord.Colour.dark_teal())
		await ctx.send(embed=sembed)
	@announce.command()
	@commands.has_guild_permissions(manage_messages=True)
	async def everyone(self, ctx, channel: discord.TextChannel, *, msg):
		embed = discord.Embed(description=msg, colour=discord.Colour.dark_gold())
		embed.set_author(name="ANNOUNCEMENT!", icon_url=ctx.guild.icon_url)
		embed.timestamp = datetime.datetime.utcnow()
		await channel.send(embed=embed)
		await channel.send("@everyone")
		sembed = discord.Embed(title='Success!',
								description=f'Successfully announced `{msg}` in {channel.mention} with @everyone',
								color=discord.Colour.dark_teal())
		await ctx.send(embed=sembed)

	@announce.command()
	@commands.has_guild_permissions(manage_messages=True)
	async def here(self, ctx, channel: discord.TextChannel, *, msg):
		embed = discord.Embed(description=msg, colour=discord.Colour.dark_gold())
		embed.set_author(name="ANNOUNCEMENT!", icon_url=ctx.guild.icon_url)
		embed.timestamp = datetime.datetime.utcnow()
		await channel.send(embed=embed)
		await channel.send("@here")
		sembed = discord.Embed(title='Success!',
								description=f'Successfully announced `{msg}` in {channel.mention} with @here',
								color=discord.Colour.dark_teal())
		await ctx.send(embed=sembed)

	@announce.command()
	@commands.has_guild_permissions(manage_messages=True)
	async def selective(self, ctx, channel: discord.TextChannel, *, msg):
		embed = discord.Embed(description=msg, colour=discord.Colour.dark_gold())
		embed.set_author(name="ANNOUNCEMENT!", icon_url=ctx.guild.icon_url)
		embed.timestamp = datetime.datetime.utcnow()
		await channel.send(embed=embed)
		await channel.send("<@&756865729550090330>")
		sembed = discord.Embed(title='Success!',
								description=f'Successfully announced `{msg}` in {channel.mention} with <@&756865729550090330>',
								color=discord.Colour.dark_teal())
		await ctx.send(embed=sembed)

	# User info checker
	@commands.command(name="userinfo", aliases=['ui', 'memberinfo', 'mi'])
	@commands.guild_only()
	async def user_info(self, ctx, member: discord.Member = None):
		if member is None:
			embed = discord.Embed(title=f"User Information", color=discord.Colour.dark_gold(),
								  timestamp=datetime.datetime.utcnow())
			embed.set_thumbnail(url=ctx.author.avatar_url)
			embed.set_thumbnail(url=ctx.guild.icon_url)
			embed.add_field(name="ID:", value=ctx.author.id, inline=False)
			embed.add_field(name="Name:", value=ctx.author.name, inline=True)
			embed.add_field(name="Bot:", value=ctx.author.bot, inline=True)
			embed.add_field(name="Primary Role:", value=ctx.author.top_role, inline=True)
			embed.add_field(name="Discord Status:", value=str(ctx.author.status).title(), inline=True)
			embed.add_field(name="Created at:", value=ctx.author.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
			embed.add_field(name="Joined at:", value=ctx.author.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
			embed.add_field(name="Booster:", value=bool(ctx.author.premium_since), inline=True)
			await ctx.send(embed=embed)
		else:
			embed = discord.Embed(title=f"User Information", color=discord.Colour.dark_gold(),
								  timestamp=datetime.datetime.utcnow())
			embed.set_thumbnail(url=member.avatar_url)
			embed.set_thumbnail(url=ctx.guild.icon_url)
			embed.add_field(name="ID:", value=member.id, inline=False)
			embed.add_field(name="Name:", value=member.name, inline=True)
			embed.add_field(name="Bot:", value=member.bot, inline=True)
			embed.add_field(name="Primary Role:", value=member.top_role, inline=True)
			embed.add_field(name="Discord Status:", value=str(member.status).title(), inline=True)
			embed.add_field(name="Created at:", value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
			embed.add_field(name="Joined at:", value=member.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
			embed.add_field(name="Booster:", value=bool(member.premium_since), inline=True)
			await ctx.send(embed=embed)

	@commands.command(name="find")
	@commands.guild_only()
	async def find(self, ctx, member: discord.Member = None):
		if member is None:
			await ctx.send('Please specify a member from default.role@everyone')

	@commands.command()
	async def time(self, ctx):
		guild = ctx.guild
		channel = ctx.channel
		embed = discord.Embed(title="Timezones & Time", color = discord.Color.dark_gold())
		UTC = pytz.utc
		# it will get the time zone
		# of the specified location 
		AUS = pytz.timezone('Australia/Melbourne')
		datetime_ist = datetime.now(AUS) 
		AUStime = datetime_ist.strftime('%H:%M').split(':')
		AUStime[0], AUStime[1] = int(AUStime[0]), int(AUStime[1])
		if AUStime[0] >  12:
			AUStime[0] -= 12
			suffix2 = 'pm'
		elif AUStime[0] == 12:
			suffix2 = 'pm'
		elif AUStime[0] < 12:
			suffix2 = 'am'
		if len(list(str(AUStime[1]))) < 2:
			AUStime[1] = f'0{AUStime[1]}'
		embed.add_field(name= "\u200b",value=f'**AUS**: {AUStime[0]}:{AUStime[1]} {suffix2}',inline=False)
		MMYR = pytz.timezone('Asia/Yangon') 
		datetime_ist = datetime.now(MMYR) 
		MMYRtime = datetime_ist.strftime('%H:%M').split(':')
		MMYRtime[0], MMYRtime[1] = int(MMYRtime[0]), int(MMYRtime[1])
		if MMYRtime[0] >  12:
			MMYRtime[0] -= 12
			suffix = 'pm'
		elif MMYRtime[0] == 12:
			suffix = 'pm'
		elif MMYRtime[0] < 12:
			suffix = 'am'
		if len(list(str(MMYRtime[1]))) < 2:
			MMYRtime[1] = f'0{MMYRtime[1]}'
		embed.add_field(name='\u200b',value=f'**MMYR**: {MMYRtime[0]}:{MMYRtime[1]} {suffix}', inline=False)
		await ctx.send(embed=embed)

	# Membercount Command
	@commands.group(name="membercounter", aliases=['mbc'], invoke_without_command=True)
	@commands.guild_only()
	@commands.has_permissions(administrator=True)
	async def membercounter(self, ctx, channel: discord.VoiceChannel):
		guild = ctx.guild
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute("SELECT channel_id FROM member_count_channel WHERE guild_id = ?", (ctx.guild.id,))
		result = cursor.fetchone()
		if result is None:
			sql = ("INSERT INTO member_count_channel(guild_id, channel_id) VALUES (?, ?)")
			val = (ctx.guild.id, channel.id)
			cursor.execute(sql, val)
			db.commit()
			embed=discord.Embed(title=f"Preset", description=f"> SUCCESSFULLY RECONFIGURED CHANNEL : {channel.mention}\nExecute `{ctx.prefix}mbc check` to check the preset anytime!", colour=discord.Colour.dark_teal())
			await ctx.send(embed=embed)
			cursor.close()
			db.close()
		elif result is not None:
			sql = ("UPDATE member_count_channel SET channel_id = ? WHERE guild_id = ?")
			val = (channel.id, ctx.guild.id)
			cursor.execute(sql, val)
			db.commit()
			embed=discord.Embed(title=f"Preset", description=f"> SUCCESSFULLY CONFIGURED CHANNEL : {channel.mention}\nExecute `{ctx.prefix}mbc check` to check the preset anytime!", colour=discord.Colour.dark_teal())
			await ctx.send(embed=embed)
			cursor.close()
			db.close()

	@membercounter.command()
	async def check(self, ctx):
		guild = ctx.guild
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute("SELECT channel_id FROM member_count_channel WHERE guild_id = ?", (ctx.guild.id,))
		result = cursor.fetchone()
		if result is None:
			embed=discord.Embed(title=f"N/A!", description=f"> NO PRESETS FOUND!\nExecute `{ctx.prefix}mbc (<#VoiceChannelId>)` to select a voice channel as your member counter!", colour=discord.Colour.dark_red())
			await ctx.send(embed=embed)
		elif result is not None:
			channel = self.client.get_channel(result[0])
			embed=discord.Embed(title=f"Preset", description=f"> CONFIGURED CHANNEL : {channel.mention}\nExecute `{ctx.prefix}mbc (<#VoiceChannelId>)` to change which voice channel to use as the server member counter!", colour=discord.Colour.dark_teal())
			await ctx.send(embed=embed)

	@membercounter.command()
	async def clear(self, ctx):
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute("DELETE FROM member_count_channel WHERE guild_id = ? ", (ctx.guild.id,))
		db.commit()
		cursor.close()
		db.close()
		embed=discord.Embed(title=f"Success!", description=f"> SUCCESSFULLY CLEARED PREFERENCES IF FOUND!\nExecute `{ctx.prefix}mbc (<#VoiceChannelId>)` to select a voice channel as your member counter!", colour=discord.Colour.dark_teal())
		await ctx.send(embed=embed)	
	
	@commands.command()
	@commands.has_guild_permissions(move_members=True)
	async def move(self, ctx, ini_id,end_id):
		ini_channel = ctx.guild.get_channel(int(ini_id))
		end_channel = ctx.guild.get_channel(int(end_id))
		all_members = ini_channel.members
		for member in all_members:
			await member.move_to(end_channel)
		await ctx.send("**`Successfully moved everyone`**")
	
	@commands.command(name="test")
	async def test(self, ctx):
		await ctx.send(embed = discord.Embed(title= "This is a title", description="This is a description", color = 255128213))
	
	@tasks.loop(minutes = 10)
	async def time_changer(self):
		try:
			guild = self.client.get_guild(702714944558202933)
			count_channel = guild.get_channel(702714945124696068) # MMYR
			await count_channel.edit(name=f'Members : {guild.member_count}')
		except:
			pass

def setup(client):
	client.add_cog(Misc(client))
	print('Misc.cog is loaded')
