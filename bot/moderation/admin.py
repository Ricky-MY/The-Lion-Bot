import discord
import json

from discord.ext import commands
from os import listdir
from discord.ext.commands.errors import ExtensionNotFound
from discord.ext.commands.errors import ExtensionNotLoaded

from bot.utilities.prefixes import Prefixes

class Admin(commands.Cog):
	
	'''Administration and maintenance based commands and functions
	
	- Reload / load / unload
	- Pushing updates and threads to guild owners
	- Restarting / Shutting down the bot'''

	def __init__(self, bot):
		self.bot = bot
		self.color = 0x87ceeb
		self.main_directory = 'bot'

	def botAdminCheck(ctx):
		return ctx.message.author.id == 368671236370464769 # change this number to your ID

	'''Utility commands to provide administrator access on the bot'''

	# Guilds Checker
	@commands.command(name="guilds")
	@commands.guild_only()
	@commands.check(botAdminCheck)
	async def guilds(self, ctx):
		guilds = [i.name for i in self.bot.guilds]
		text = '\n'.join(guilds)
		embed = discord.Embed(title="Guilds Joined", description = f"{text}", colour=self.color)
		embed.set_footer(text=f'Total of {len(guilds)} guild(s) joined')
		await ctx.send(embed=embed)
		await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(f'~help | {len(self.bot.guilds)} guilds'))

	# Load Unload and Reload command
	@commands.command(name="load", aliases=['l'])
	@commands.check(botAdminCheck)
	async def load_cog(self, ctx, extension):
		embed = discord.Embed(title='Success!', description=f'{extension} is loaded.',
										color=self.color)
		for subdir in listdir(f'{self.main_directory}'):
			try:
				self.bot.load_extension(f'{self.main_directory}.{subdir}.{extension}')
			except ExtensionNotLoaded:
				pass
			except ExtensionNotFound:
				pass
			else:
				await ctx.send(embed=embed)
				return
		raise ExtensionNotFound(extension)

	# Unload command
	@commands.command(name="unload", aliases=['ul'])
	@commands.check(botAdminCheck)
	async def unload_cog(self, ctx, extension):
		embed = discord.Embed(title='Success!', description=f'{extension} is loaded.',
										color=self.color)
		for subdir in listdir(f'{self.main_directory}'):
			try:
				self.bot.unload_extension(f'{self.main_directory}.{subdir}.{extension}')
			except ExtensionNotLoaded:
				pass
			except ExtensionNotFound:
				pass
			else:
				await ctx.send(embed=embed)
				return
		raise ExtensionNotFound(extension)

	# Reload command
	@commands.command(name="reload", aliases=['rl'])
	@commands.check(botAdminCheck)
	async def reload_cog(self, ctx, extension):
		embed = discord.Embed(title='Success!', description=f'{extension} is reloaded.',
										color=self.color)
		for subdir in listdir(f'{self.main_directory}'):
			try:
				self.bot.reload_extension(f'{self.main_directory}.{subdir}.{extension}')
			except ExtensionNotLoaded:
				pass
			except ExtensionNotFound:
				pass
			else:
				await ctx.send(embed=embed)
				return
		raise ExtensionNotFound(extension)

	# Load and reload all {self.main_directory}
	@commands.command(name="restart", aliases=['rst', 'sync'])
	@commands.check(botAdminCheck)
	async def restart(self, ctx):
		for subdir in listdir(f'./{self.main_directory}/'):
			for files in listdir(f'./{self.main_directory}/{subdir}/'):
				if files.endswith('.py') and not files.startswith('_'):
					self.bot.reload_extension(f'{self.main_directory}.{subdir}.{files[:-3]}')
		await ctx.send(embed=discord.Embed(title='Success!', description=f'Bot has restarted', color=self.color))

	@commands.command(name='alter status', aliases = ['as', 'changeStatus', 'chs', 'changestatus', 'change_status'])
	@commands.check(botAdminCheck)
	async def alter_status(self, ctx, *, status):
		await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(f'{status}'))
		await ctx.send(f"Status successfully changed into |{status}|")

	'''This is purely preferential, this piece of code or loop is used 
	to update the bot status on how many servers it is currently invited into.'''

	# Guide Menu
	@commands.group(name="admin", invoke_without_command=True)
	@commands.check(botAdminCheck)
	async def admin(self, ctx):
		current_prefix = Prefixes.fetch_prefix(ctx.guild.id)
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
	async def system_commands(self, ctx):
		current_prefix = Prefixes.fetch_prefix(ctx.guild.id)
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
	async def authenticator_commands(self, ctx):
		current_prefix = Prefixes.fetch_prefix(ctx.guild.id)
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

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		try:
			await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(f'Lhelp | {len(self.bot.guilds)} guilds'))
		except:
			pass

def setup(bot):
	bot.add_cog(Admin(bot))
	print('Admin.cog is loaded')