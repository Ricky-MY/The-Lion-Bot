import discord
import random
import datetime
import yaml

from discord.ext import commands
from discord.ext.commands import Cog

class Authenticator(Cog):

	def __init__(self, bot):
		self.bot = bot
		with open("config.yaml", 'r') as file:
			config = yaml.load(file, Loader=yaml.SafeLoader)
		self.resources = config["directories"]["assets"]
		self.color = config["asthetics"]["verifierColor"]
		self.error_color = config["asthetics"]["errorColor"]

		self.alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
			 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y' 'z']

	def get_otp(self, layer):
		key = ''
		for i in range(random.randint(1,layer)):
			letter = random.choice(self.alphabets)
			key += letter
			number = random.randint(1,1000)
			key += str(number)
		return key

	@commands.group(name= "authenticator", invoke_without_command=True, aliases=['auth', 'a'])
	@commands.guild_only()
	async def authenticator(self, ctx, *, key):
		"""This command is used to authenticate as a EP(exclusive permissable) using a key provided by the admins"""

		with open(self.resources + 'keys.txt', 'r') as file:
			keys = [key_item[:-1] for key_item in file]
		if key in keys:
			embed = discord.Embed(title='Success!',
								description=f'You have successfully authenticated using your one time code!',
								color=self.color)
			await ctx.reply(embed=embed)
		else:
			embed = discord.Embed(title=f'ERROR...', description=f'Invalid Code -- please try again! \n`NOTE: This operation is Case Sensitve`', color=self.error_color)
			embed.set_footer(text=f'Usage: {ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}', icon_url=self.bot.user.avatar_url)
			await ctx.reply(embed=embed)

		leftover_keys = [item for item in keys if item != key]
		with open(self.resources + 'keys.txt', 'w') as file:
			for a_key in leftover_keys:
				file.write(f'{a_key}\n')

	@authenticator.command(name = "create")
	@commands.has_guild_permissions(manage_guild =True)
	async def create(self, ctx, *, limit = 1):
		"""Creates unique authentication keys that can be used to access a component. If no limit is provided, it will create only one key."""

		if limit <= 0 or limit > 100:
			embed = discord.Embed(title=f'ERROR...', description=f'You have entered an invalid limit!\nMake sure to set a limit between 1 to 100.', color=self.error_color)
			embed.set_footer(text=f'Usage: {ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}', icon_url=self.bot.user.avatar_url)
			await ctx.send(embed=embed)
		else:
			embed = discord.Embed(title=f'Keys successfully created!', description='```DISCLOSING ANY KEY(S) CAN RESULT IN SECURITY BREACHES```', color=self.color)
			all_keys= []
			count = 0
			while count != limit:
				key = self.get_otp(10)
				all_keys.append(key)
			with open(self.resources + 'keys.txt', 'w') as file:
				for a_key in all_keys:
					file.write(f'{a_key}\n')

			thumbnail = ctx.guild.icon_url
			embed.set_thumbnail(url=thumbnail)
			embed.timestamp = datetime.datetime.utcnow()
			await ctx.send(embed=embed)

	@authenticator.command(name = "dump", aliases =["clear", "delete", "flush"])
	@commands.has_guild_permissions(manage_guild =True)
	async def dump(self, ctx):
		"""Removes all active authentication keys for the server. Refer to the aegis help menu for further commands."""
		
		channel = ctx.channel
		embed = discord.Embed(title=f'HOLD UPPP...', description=f'Type in `confirm` to confirm the deletion of all keys.', color=self.error_color)
		embed.set_footer(text=f'THIS PROCESS IS IRREVERTIBLE',
								 icon_url=self.bot.user.avatar_url)
		await ctx.send(embed=embed)
		await self.bot.wait_for('message', timeout=60.0, check=lambda message: message.content.lower() == 'confirm' and message.channel == channel and message.author == ctx.author)
		with open(self.resources + 'keys.txt', 'w') as file:
			file.write('')
		embed = discord.Embed(title='Success!',
								description=f'Successfully dumped all valid keys',
								color=discord.Colour.dark_teal())
		await ctx.send(embed=embed)

	@authenticator.command(aliases=['stats'])
	@commands.has_guild_permissions(manage_guild =True)
	async def statistics(self, ctx):
		"""Checks how many active authentication keys there are on the current server."""
		
		with open(self.resources+ 'keys.txt','r') as file:
			keys = [key for key in file]
		embed = discord.Embed(title=f'Authenticator statistics', description=f'Total valid keys left : {len(keys)}', color=self.color)
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Authenticator(bot))
	print('Authenticator.cog is loaded')
