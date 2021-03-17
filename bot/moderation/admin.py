import discord
import yaml

from os import listdir
from discord.ext import commands
from discord.ext.commands.errors import ExtensionNotFound
from discord.ext.commands.errors import ExtensionNotLoaded

def bot_admin_check(ctx):
	return ctx.message.author.id == 368671236370464769

def has_higher_role(author, comparable):
	return author.top_role >= comparable.top_role

class Admin(commands.Cog):
	
	'''Administration and maintenance based commands and functions
	
	- Reload / load / unload
	- Pushing updates and threads to guild owners
	- Restarting / Shutting down the bot'''

	def __init__(self, bot):
		self.bot = bot
		with open("config.yaml", 'r') as file:
			config = yaml.load(file, Loader=yaml.SafeLoader)
		self.color = config["asthetics"]["mainColor"]
		self.main_directory = config["dirLayout"]["d"]

	def botAdminCheck(ctx):
		return ctx.message.author.id == 368671236370464769 # change this number to your ID

	@commands.command(name="guilds")
	@commands.guild_only()
	@commands.check(botAdminCheck)
	async def guilds(self, ctx):
		"""
		Checks how many guilds the bot is in with each and every guild specified in an embed.
		"""
		guilds = [i.name for i in self.bot.guilds]
		text = '\n'.join(guilds)
		embed = discord.Embed(title="Guilds Joined", description = f"{text}", colour=self.color)
		embed.set_footer(text=f'Total of {len(guilds)} guild(s) joined')
		await ctx.send(embed=embed)
		await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(f'~help | {len(self.bot.guilds)} guilds'))

	# Load Unload and Reload command
	@commands.command(name="load", aliases=['l'])
	@commands.check(botAdminCheck)
	async def load_cog(self, ctx, extension: str):
		"""
		Loads an unloaded cog to the bot.
		"""
		for subdir in listdir(f'{self.main_directory}'):
			try:
				self.bot.load_extension(f'{self.main_directory}.{subdir}.{extension}')
			except ExtensionNotLoaded:
				pass
			except ExtensionNotFound:
				pass
			else:
				await ctx.message.add_reaction("☑️")
				return
		raise ExtensionNotFound(extension)

	# Unload command
	@commands.command(name="unload", aliases=['ul'])
	@commands.check(botAdminCheck)
	async def unload_cog(self, ctx, extension: str):
		"""
		Unloads an unloaded cog to the bot.
		"""
		for subdir in listdir(f'{self.main_directory}'):
			try:
				self.bot.unload_extension(f'{self.main_directory}.{subdir}.{extension}')
			except ExtensionNotLoaded:
				pass
			except ExtensionNotFound:
				pass
			else:
				await ctx.message.add_reaction("☑️")
				return
		raise ExtensionNotFound(extension)

	# Reload command
	@commands.command(name="reload", aliases=['rl'])
	@commands.check(botAdminCheck)
	async def reload_cog(self, ctx, extension: str):
		"""
		Reloads an unloaded cog to the bot.
		"""
		for subdir in listdir(f'{self.main_directory}'):
			try:
				self.bot.reload_extension(f'{self.main_directory}.{subdir}.{extension}')
			except ExtensionNotLoaded:
				pass
			except ExtensionNotFound:
				pass
			else:
				await ctx.message.add_reaction("☑️")
				return
		raise ExtensionNotFound(extension)

	# Load and reload all {self.main_directory}
	@commands.command(name="restart", aliases=['rst', 'sync'])
	@commands.check(botAdminCheck)
	async def restart(self, ctx):
		"""
		Reloads every cog connected to the bot.
		"""
		for subdir in listdir(f'./{self.main_directory}/'):
			for files in listdir(f'./{self.main_directory}/{subdir}/'):
				if files.endswith('.py') and not files.startswith('_'):
					self.bot.reload_extension(f'{self.main_directory}.{subdir}.{files[:-3]}')
		await ctx.message.add_reaction("☑️")

	@commands.command(name='alter status', aliases = ['as', 'changeStatus', 'chs', 'changestatus', 'change_status'])
	@commands.check(botAdminCheck)
	async def alter_status(self, ctx, *, status: str):
		"""
		Changes bot status
		"""
		await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(f'{status}'))
		await ctx.send(f"Status successfully changed into |{status}|")

def setup(bot):
	bot.add_cog(Admin(bot))
	print('Admin.cog is loaded')