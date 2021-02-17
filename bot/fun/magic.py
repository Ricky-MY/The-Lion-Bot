import discord
import random
import asyncio

from discord.ext import commands

class Magic(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	# 8ball Command
	@commands.command(aliases=['8ball'])
	@commands.guild_only()
	async def _8ball(self, ctx, *, text):
		response = ["Yes", "indeed!", "Absolutely Not.", "That would be a hell no.", "Yes, yes, yes!",
					"No, Probably not.", "I'd rather not answer.", "You must find this out yourself, I refuse answer",
					"Most likely.", "I'm sorry but no.", "Obvvviously not-", "Most likely!", "For sure!", "Definitely!",
					"Are you out of yo god damn mind?, of course not lol."]
		await ctx.send(random.choice(response))

	# Ping Command
	@commands.command()
	@commands.guild_only()
	async def ping(self, ctx):
		await ctx.send('Pong!')
		await ctx.send(f'Ping: {round(self.bot.latency * 1000)}ms')

	# Joke Command
	@commands.command()
	@commands.guild_only()
	async def joke(self, ctx):
		jokes = open("cogs/fun_cosmetics/jokes.txt", "r")
		await ctx.send(random.choice(list(jokes)))

	# Poop Command
	@commands.command()
	@commands.guild_only()
	async def poop(self, ctx):
		poop_gifs = open("cogs/fun_cosmetics/poop_gifs.txt", "r")
		embed = discord.Embed(description=f"Omg ewww, {ctx.author.mention} just pooped!1!",
							  color=discord.Colour.purple())
		embed.set_image(url=random.choice(list(poop_gifs)))
		await ctx.send(embed=embed)

	# Slap Command
	@commands.command()
	@commands.guild_only()
	async def slap(self, ctx, member: discord.Member = None):
		slap_gifs = open("cogs/fun_cosmetics/slap_gifs.txt", "r")
		if member is None:
			victim = random.choice(ctx.guild.members)
			rembed = discord.Embed(title='🦁 Violence is never the answer....',
								   description=f'BUT, OH MY GOD LADIES AND GENTLEMAN 📣, THAT WAS A CLEAN SLAP TO THE RIGHT CHEEK BY {ctx.author.mention} TO 🤜 {victim.mention}. UN B E L I E V E A B L E. K/O',
								   color=discord.Colour.purple())
			rembed.set_footer(text=f'{ctx.author.name} 👋 {victim.name}', icon_url=ctx.author.avatar_url)
			rembed.set_image(url=random.choice(list(slap_gifs)))
			await ctx.send(embed=rembed)
		else:
			embed = discord.Embed(title='🦁 Violence is never the answer....',
								  description=f'BUT, OH MY GOD LADIES AND GENTLEMAN 📣, THAT WAS A CLEAN SLAP TO THE RIGHT CHEEK BY {ctx.author.mention} TO 🤜 {member.mention}. UN B E L I E V E A B L E. K/O',
								  color=discord.Colour.purple())
			embed.set_footer(text=f'{ctx.author.name} 👋 {member.name}', icon_url=ctx.author.avatar_url)
			embed.set_image(url=random.choice(list(slap_gifs)))
			await ctx.send(embed=embed)

	@commands.command()
	@commands.guild_only()
	async def diceroll(self, ctx):
		dice = random.randint(1,6)
		await ctx.send(f"🎲 {dice}")

	@commands.command(aliases=['fb', 'pb'])
	@commands.guild_only()
	async def fakeban(self, ctx, member:discord.Member, *, reason = 'Unspecified reason'):
		embed = discord.Embed(title='$ucce$$!',
								 description=f'{member.mention} has been successfully banned for {reason}.',
								 color=discord.Colour.dark_teal())
		embed.set_footer(text=f'By {ctx.author.name}', icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
	
	# Hug Command
	@commands.command()
	@commands.guild_only()
	async def hug(self, ctx, member: discord.Member = None):
		hug_gifs = open("cogs/fun_cosmetics/hug_gifs.txt", "r")
		if member is None:
			victim = random.choice(ctx.guild.members)
			rembed = discord.Embed(title='🦁 Cutie Cupcakes!',
								   description=f'{ctx.author.mention} had hugged {victim.mention}.🥺',
								   color=discord.Colour.purple())
			rembed.set_footer(text=f'{ctx.author.name} 💕 {victim.name}', icon_url=ctx.author.avatar_url)
			rembed.set_image(url=random.choice(list(hug_gifs)))
			await ctx.send(embed=rembed)
		else:
			embed = discord.Embed(title='🦁 Cutie Cupcakes!',
								  description=f'{ctx.author.mention} had hugged {member.mention}.🥺',
								  color=discord.Colour.purple())
			embed.set_footer(text=f'{ctx.author.name} 💕 {member.name}', icon_url=ctx.author.avatar_url)
			embed.set_image(url=random.choice(list(hug_gifs)))
			await ctx.send(embed=embed)

	# Kiss Command
	@commands.command()
	@commands.guild_only()
	async def kiss(self, ctx, member: discord.Member):
		victim = member
		kiss_gifs = open("cogs/fun_cosmetics/kiss_gifs.txt", "r")
		slap_gifs = open("cogs/fun_cosmetics/slap_gifs.txt", "r")
		rembed = discord.Embed(description=f"Awww!, {ctx.author.mention} mwahed {victim.mention}!!",
							   color=discord.Colour.purple())
		rembed.set_footer(
			text=f"OMG!!, What do you do now?!,\nReact with 👋 to slap this bubble-tea lookin mfer that had just harassed you!, Or react with 💋 to spread the love {victim.name}?!")
		rembed.set_image(url=random.choice(list(kiss_gifs)))
		message = await ctx.send(embed=rembed)
		channel = ctx.channel
		await message.add_reaction('👋')
		await message.add_reaction('💋')

		def check(reaction, user):
			return user == ctx.author and str(reaction.emoji) == '👋' or str(reaction.emoji) == '💋'

		try:
			reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
		except asyncio.TimeoutError:
			await channel.send('Reaction Timed Out')
		else:
			if reaction.emoji == '👋':
				await channel.send('~~GET SLAPPED PERV~~')
			elif reaction.emoji == '💋':
				await channel.send('~~LOVE IS IN THE AIR~~')

	# Rick Roll
	@commands.command(aliases=["rickroll'd"])
	@commands.guild_only()
	async def rickroll(self, ctx, member: discord.Member = None):
		rickroll = "https://media.giphy.com/media/lgcUUCXgC8mEo/giphy.gif"
		if member is None:
			victim = random.choice(ctx.guild.members)
			embed = discord.Embed(title='🦁 Rick n Roll Baby!', description=f"{victim.mention} just got rickroll'd. 🕺",
								  color=discord.Colour.purple())
			embed.set_image(url=rickroll)
			await ctx.send(embed=embed)
		else:
			embed = discord.Embed(title='🦁 Rick n Roll Baby!', description=f"{member.mention} just got rickroll'd. 🕺",
								  color=discord.Colour.purple())
			embed.set_image(url=rickroll)
			await ctx.send(embed=embed)
			await member.send("You just got rickroll'd boiiiii")

	# Gift command
	@commands.command()
	@commands.guild_only()
	async def gift(self, ctx, member: discord.Member = None):
		poop_gifs = open("cogs/fun_cosmetics/poop_gifs.txt", "r")
		embed = discord.Embed(description=f"Awww, {ctx.author.mention} just gave a milo cookie to {member.mention}!1!",
							  color=discord.Colour.purple())
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Magic(bot))
	print('Magic.cog is loaded')