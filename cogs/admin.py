import discord
import json
import os
from discord.ext import commands


class Admin(commands.Cog):

	def __init__(self, client):
		self.client = client

	def botAdminCheck(ctx):
		return ctx.message.author.id == 368671236370464769

	# Guilds Checker
	@commands.command(name="guilds")
	@commands.check(botAdminCheck)
	async def guilds(self, ctx):
		count = int(0)
		inGuilds = self.client.guilds
		embed = discord.Embed(title="Guilds Joined", colour= discord.Colour.dark_teal())
		for guild in inGuilds:
			count = count + 1
			embed.add_field(name=count, value=f'`{guild}`')
		embed.set_footer(text=f'_Total of {count} guild(s) joined_')
		await ctx.send(embed=embed)

	# Leaving
	@commands.command(name="allleave")
	@commands.check(botAdminCheck)
	async def allleave(self, ctx):
		for guild in self.client.guilds:
			if guild != ctx.guild:
				await guild.leave()
				embed = discord.Embed(title='Success!',
                                 description='All guilds successfully left',
                                 color=discord.Colour.dark_teal())
				await ctx.send(embed=embed)
			else:
				pass

	# Guide Menu
	@commands.group(name="admin", invoke_without_command=True)
	@commands.check(botAdminCheck)
	async def admin(self, ctx, module=None):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		current_prefix = str(prefixes[str(ctx.guild.id)])
		embed = discord.Embed(color=0xCD5C5C)
		embed.set_author(name="-=The Lion's Help Menu (ADMIN GATEWAY FOR DEVELOPER)=-"),
		fields = [('[Moderation]', f"`{current_prefix}help moderation`\nA guide on everything moderation related"),
				  ('[Magic]', f"`{current_prefix}help magic`\nMystic arts from harry potter"),
				  ('[Miscellaneous]', f"`{current_prefix}help misc`\nA miscellaneous guide"),
				  ('[Greeting]', f"`{current_prefix}help greet`\nA guide on the Greeting System"),
				  ('[Levelling]', f"`{current_prefix}help level`\nA guide on the Levelling system"),
				  ('[MemberCounter]', f"`{current_prefix}help mbc`\nA guide on everything MemberCounter related"),
				  ('[Aegis]', f"`{current_prefix}admin aegis`\nA guide to using Aegis"),
				  ('[Authenticator]', f"`{current_prefix}admin auth`\nA guide to using the authenticator"),
				  ('[System]', f"`{current_prefix}admin sys`\nA guide system commands")]
		for name, value in fields:
			embed.add_field(name=name, value=value)
		await ctx.send(embed=embed)

	@admin.command(name="system",aliases=['sys'])
	@commands.check(botAdminCheck)
	async def system_commands(self, ctx):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		current_prefix = str(prefixes[str(ctx.guild.id)])
		embed = discord.Embed(title="=System Guide=", description='A guide for systemic commands', color=0xCD5C5C)
		fields = [('Load', f'`{current_prefix}load <cog>`\nLoads a cog'),
				  ('Unload', f'`{current_prefix}unload <cog>`\n Unloads a cog'),
				  ('Reload', f'`{current_prefix}reload <cog>`\n Unloads and loads a cog'),
				  ('ShutDown', f'`{current_prefix}shutdown`\n Shutdown the bot'),
				  ('AllLeave',
				   f'`{current_prefix}allleave`\n Leaves all joined server except the guild the command was executed on'),
				  ('Guilds', f'`{current_prefix}guilds`\n Returns a list of guilds the bot is in')]
		for name, value in fields:
			embed.add_field(name=name, value=value)
		await ctx.send(embed=embed)

	@admin.command(name="authenticator",aliases=['auth'])
	@commands.check(botAdminCheck)
	async def authenticator_commands(self, ctx):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		current_prefix = str(prefixes[str(ctx.guild.id)])
		embed = discord.Embed(title="=Authenticator Guide=", description='A guide for authenticative commands', color=0xCD5C5C)
		fields = [('Verify', f'`{current_prefix}verify`\nSends the user a one time verification code for a HIP check.'),
				  ('Key-Creation', f'`{current_prefix}auth create <limit>`\nCreates random keys with respect to the limit'),
				  ('Key-Verification', f'`{current_prefix}auth <key>`\nValidation that requires a pre-existing key. Goes invalid after usage'),
				  ('Key-Refresh', f'`{current_prefix}shutdown`\nDumps all valid keys\n`THIS CAN RESULT IN DATA LOSSES, MAKE SURE TO PROCEED WITH CAUTION`'),
				  ('Key-Statistics',
				   f'`{current_prefix}auth stats`\nStatistical data for keys')]
		for name, value in fields:
			embed.add_field(name=name, value=value)
		await ctx.send(embed=embed)


	@admin.command(name="aegis",aliases=['aeg'])
	@commands.check(botAdminCheck)
	async def aegis_commands(self, ctx):
		embed = discord.Embed(title='=Aegis Module Accessed=',
							  description="Aegis module is designed to provide protectection to guilds and to prevent raids. NOTE: GRATZ TO YOU FINDING THIS UNINDEXED MODULE BUT CAUTION, IT IS EXTREMELY BUGGED AND IT COULD CAUSE HUGE ERRORS, DO NOT USE THE COMMANDS",
							  color=0xCD5C5C)
		fields = [('Void',
				   f"`Aegis V0id implements all acessible invites to be exiled. Putting the server in v0id.`"),
				  ('Smoke', f'`Aegis smoke strips away the ability of everyone to see text channels. BUGGED`'),
				  ('Chernobyl',
				   f'`Aegis Chernobyl removes members that had joined before a specified time. This is a kick. V0id and Chernobyl can be used to prevent alts joining in.`'),
				  ('Paris', f'`==`'),
				  ('LoveCanal', f'`==`')]
		for name, value in fields:
			embed.add_field(name=name, value=value)
		await ctx.send(embed=embed)

	# Load Unload and Reload command
	@commands.command(name="load", aliases=['l'])
	@commands.check(botAdminCheck)
	async def load_cogs(self, ctx, extension):
		self.client.load_extension(f'cogs.{extension}')
		lembed = discord.Embed(title='Success!', description=f'{extension} is loaded.',
							   color=discord.Colour.dark_teal())
		await ctx.send(embed=lembed)

	@commands.command(name="unload", aliases=['ul'])
	@commands.check(botAdminCheck)
	async def unload_cogs(self, ctx, extension):
		self.client.unload_extension(f'cogs.{extension}')
		ulembed = discord.Embed(title='Success!', description=f'{extension} is unloaded.',
								color=discord.Colour.dark_teal())
		await ctx.send(embed=ulembed)

	@commands.command(name="reload", aliases=['rl'])
	@commands.check(botAdminCheck)
	async def reload_cogs(self, ctx, extension):
		embed = discord.Embed(title='Success!', description=f'{extension} is reloaded.',
									color=discord.Colour.dark_teal())
		try:
			self.client.unload_extension(f'cogs.{extension}')
			self.client.load_extension(f'cogs.{extension}')
			await ctx.send(embed=embed)
		except ExtensionNotFound:
			self.client.load_extension(f'cogs.{extension}')
			self.client.unload_extension(f'cogs.{extension}')
			self.client.load_extension(f'cogs.{extension}')
			await ctx.send(embed=embed)
			
	@commands.command(name="restart", aliases=['rst', 'sync'])
	@commands.check(botAdminCheck)
	async def restart(self, ctx):
		for filename in os.listdir('./cogs'):
			if filename.endswith('.py'):
				self.client.unload_extension(f'cogs.{filename[:-3]}')
				self.client.load_extension(f'cogs.{filename[:-3]}')
				rlembed = discord.Embed(title='Success!', description=f'{filename[:-3]} is reloaded.',
								color=discord.Colour.dark_teal())
				await ctx.send(embed=rlembed)

def setup(client):
	client.add_cog(Admin(client))
	print('Admin.cog is loaded')
