import discord
import random
import asyncio
import datetime

from discord.ext import commands
from discord.ext.commands import Cog

class Authenticator(Cog):

	def __init__(self, bot):
		self.bot = bot
		self.resources = 'bot/resources/'

	def botAdminCheck(ctx):
		return ctx.message.author.id == 368671236370464769

	@commands.command()
	@commands.guild_only()
	async def verify(self, ctx):
		guild = ctx.guild
		user_id = ctx.author.id
		channel = ctx.channel
		member = guild.get_member(user_id)
		alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
					'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
					'u', 'v', 'w', 'x', 'y' 'z']
		key = ''
		for i in range(random.randint(1,10)):
			letter = random.choice(alphabets)
			key += letter
			number = random.randint(1,1000)
			key += str(number)
		cmd_message = ctx.message
		for reaction in ('💬','🇩', '🇲'):
			await cmd_message.add_reaction(reaction)

		embed = discord.Embed(title='Verification', description=f'Please enter this key in the verification channel : ```{key}```', color=discord.Colour.dark_green())
		embed.set_footer(text='Powered by the random module')
		await member.send(embed=embed)
		try:
			message = await self.bot.wait_for('message', timeout=60.0, check=lambda message: message.content == key and message.channel == channel and message.author == ctx.author)
			await message.add_reaction('☑')
			# THIS IS WHERE YOU CAN DO STUFF FOR THE VERIFIED PEOPLE
			await channel.send(embed=discord.Embed(title='Verified!', color=discord.Colour.dark_green()))
		except asyncio.TimeoutError:
			await ctx.send(embed=discord.Embed(title='Verification timed out! Please try again later.', color=discord.Colour.dark_red()))

	@commands.group(name=str("authenticator"), invoke_without_command=True, aliases=['auth', 'a'])
	@commands.guild_only()
	@commands.check(botAdminCheck)
	async def authenticator(self, ctx, *, key):
		with open(self.resources + 'keys.txt', 'r') as file:
			keys = [key_item[:-1] for key_item in file]

		if key in keys:
			embed = discord.Embed(title='Success!',
								description=f'You have successfully authenticated using your one time code!',
								color=discord.Colour.dark_teal())
			await ctx.send(embed=embed)
		else:
			embed = discord.Embed(title=f'ERROR...', description=f'Invalid Code -- please try again! \n`NOTE: This operation is Case Sensitve`', color=discord.Colour.dark_red())
			embed.set_footer(text=f'Usage: {ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}', icon_url=self.bot.user.avatar_url)
			await ctx.send(embed=embed)

		leftover_keys = [item for item in keys if item != key]
		with open(self.resources + 'keys.txt', 'w') as file:
			for a_key in leftover_keys:
				file.write(f'{a_key}\n')

	@authenticator.command()
	async def create(self, ctx, *, limit = 1):
		if limit <= 0 or limit > 100:
			embed = discord.Embed(title=f'ERROR...', description=f'You have entered an invalid limit!\nMake sure to set a limit between 1 to 100.', color=discord.Colour.dark_red())
			embed.set_footer(text=f'Usage: {ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}', icon_url=self.bot.user.avatar_url)
			await ctx.send(embed=embed)
		else:
			embed = discord.Embed(title=f'Keys successfully created!', description='```DISCLOSING ANY KEY(S) WILL RESULT IN SECURITY BREACHES```', color=discord.Colour.dark_gold())
			all_keys= []
			count = 0
			alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y' 'z']
			while count != limit:
				key = ''
				for i in range(random.randint(5,10)):
					letter = random.choice(alphabets)
					key += letter
					number = random.randint(1,1000)
					key += str(number)
				count +=1
				all_keys.append(key)
			with open(self.resources + 'keys.txt', 'w') as file:
				for a_key in all_keys:
					file.write(f'{a_key}\n')

			thumbnail = ctx.guild.icon_url
			embed.set_thumbnail(url=thumbnail)
			embed.timestamp = datetime.datetime.utcnow()
			await ctx.send(embed=embed)

	@authenticator.command()
	async def dump(self, ctx):
		channel = ctx.channel
		embed = discord.Embed(title=f'HOLD UPPP...', description=f'Type in `confirm` to confirm the deletion of all keys.', color=discord.Colour.dark_red())
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
	async def statistics(self, ctx):
		with open(self.resources+ 'keys.txt','r') as file:
			keys = [key for key in file]
		embed = discord.Embed(title=f'Authenticator statistics', description=f'Total valid keys left : {len(keys)}', color=discord.Colour.dark_gold())
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Authenticator(bot))
	print('Authenticator.cog is loaded')
