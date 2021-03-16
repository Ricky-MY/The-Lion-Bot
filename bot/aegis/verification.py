import discord
import random
import asyncio
import yaml
import io

from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw

ALPHABETS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
			 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y' 'z']

class Verifier(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		with open("config.yaml", 'r') as file:
			config = yaml.load(file, Loader=yaml.SafeLoader)
		self.color = config["asthetics"]["verifierColor"]

	def get_capcha(self, layer) -> str:
		key = ''
		for i in range(random.randint(5,layer)):
			letter = random.choice(ALPHABETS)
			key += letter
			number = random.randint(1,1000)
			key += str(number)
		font = ImageFont.truetype("arial.ttf", 24)
		w, h = font.getsize(key)
		image = Image.new('RGBA', (w + 10, h + 10), (255, 0, 0, 0))
		draw = ImageDraw.Draw(image)
		draw.text((10, 10), key, (255, 255, 255), font=font)
		for i in range(2):
			draw.line(((0,0), (random.randint(0, w), random.randint(0, h))), fill=255, width = 5)
		with io.BytesIO() as output:
			image.save(output, format="PNG")
			output.seek(0)
			file = discord.File(fp=output, filename="image.png")
		return file, key

	@commands.command(name = "verify", alisaes="vf")
	@commands.guild_only()
	async def verify(self, ctx):
		"""
		One time verification process that validates whether if the user is a human.
		
		It creates a OTP or a one time password that is directly dmed to the user requesting
		authentication.
		"""

		guild = ctx.guild
		user_id = ctx.author.id
		channel = ctx.channel
		member = guild.get_member(user_id)
		capcha, key = self.get_capcha(random.randint(10, 20))
		cmd_message = ctx.message

		embed = discord.Embed(title='Verification', description=f'Please enter this key in the verification channel', color=self.color)
		embed.set_footer(text='Powered by  PIL and random module')
		embed.set_image(url="attachment://image.png")
		for reaction in ('💬', '🇩', '🇲'):
			await cmd_message.add_reaction(reaction)
		
		await member.send(embed = embed, file = capcha)
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
