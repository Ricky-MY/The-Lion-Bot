import discord
import random
import asyncio
import yaml

from discord.ext import commands

class Verifier(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		with open("config.yaml", 'r') as file:
			config = yaml.load(file, Loader=yaml.SafeLoader)
		self.color = config["asthetics"]["verifierColor"]
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

	@commands.command(name = "verify", alisaes="vf")
	@commands.guild_only()
	async def verify(self, ctx):
		"""One time verification process that validates whether if the user is a human."""

		guild = ctx.guild
		user_id = ctx.author.id
		channel = ctx.channel
		member = guild.get_member(user_id)
		key = self.get_otp(random.randint(0, 10))
		cmd_message = ctx.message

		for reaction in ('💬', '🇩', '🇲'):
			await cmd_message.add_reaction(reaction)
		embed = discord.Embed(title='Verification', description=f'Please enter this key in the verification channel : ```{key}```', color=self.color)
		embed.set_footer(text='Powered by the random module')
		await member.send(embed=embed)
		try:
			message = await self.bot.wait_for('message', timeout=60.0, check=lambda message: message.content == key and message.channel == channel and message.author == ctx.author)
			await message.add_reaction('☑')
			# THIS IS WHERE YOU CAN DO STUFF FOR THE VERIFIED PEOPLE
			await message.reply('Verified!')
		except asyncio.TimeoutError:
			await ctx.send(embed=discord.Embed(title='Verification timed out! Please try again later.', color=self.color))

def setup(bot):
	bot.add_cog(Verifier(bot))
	print('Verifier.cog is loaded')
