# Author - Ricky
# Type Writer COG
import discord
import datetime
import yaml

from discord.ext import commands
from discord.ext.commands import Cog

from bot.utils.checks import is_admin
from bot.constants import Colour

class TypeWriter(Cog):

	def __init__(self, bot):
		self.bot = bot
		self.color = Colour.SUNSHINE

	@commands.group(name=str("thread"), invoke_without_command=True)
	@commands.guild_only()
	async def thread(self, ctx, channel: discord.TextChannel, color, *, properties):
		content = properties.split('%')
		rawTitle = content[0]
		rawDescription = content[1]
		rawTitle2 = rawTitle.split('-')
		rawDescription2 = rawDescription.split('|')
		title = ''
		description = ''
		for word in rawTitle2:
			title += f'{word} '
		for sentence in rawDescription2:
			description += f'{sentence}\n'
		embed = discord.Embed(title=title, description=description, color=int(color))
		await channel.send(embed=embed)
		await ctx.send("> Success")

	@thread.command()
	@commands.guild_only()
	async def preview(self, ctx, color, *, properties):
		content = properties.split('%')
		rawTitle = content[0]
		rawDescription = content[1]
		rawTitle2 = rawTitle.split('-')
		rawDescription2 = rawDescription.split('|')
		title = ''
		description = ''
		for word in rawTitle2:
			title += f'{word} '
		for sentence in rawDescription2:
			description += f'{sentence}\n'
		embed = discord.Embed(title=title, description=description, color=int(color))
		await ctx.send(embed=embed)

	@thread.command()
	@commands.guild_only()
	async def edit(self, ctx, channel: discord.TextChannel, messageID, color, *, properties):
		content = properties.split('%')
		rawTitle = content[0]
		rawDescription = content[1]
		rawTitle2 = rawTitle.split('-')
		rawDescription2 = rawDescription.split('|')
		title = ''
		description = ''
		for word in rawTitle2:
			title += f'{word} '
		for sentence in rawDescription2:
			description += f'{sentence}\n'
		embed = discord.Embed(title=title, description=description, color=int(color))
		message = await channel.fetch_message(messageID)
		await message.edit(embed=embed)
		await ctx.send("> Success")

	@thread.command(name= "adv", aliases=['advance'])
	@commands.guild_only()
	async def advance(self, ctx):
		channel = ctx.channel
		properties = []
		elements = ["Description", "Color", "Thumbnail url", "Image", "Timestamp", "Footer"]
		embed = discord.Embed(title='Advance-Threading',
							  color=self.color)
		
		def check(message):
			return message.channel == channel and message.author == ctx.author

		options = ''
		embed.description='**What would you like to set the title as? Type `none` if you wish to set it as nothing.**'
		prompt = await channel.send(embed=embed)
		response = await self.bot.wait_for('message', timeout=60.0, check=check)
		options += f"Title set as: `{response.content}`\n"
		properties.append(response.content)
		await response.delete()
		
		for i in range(6):
			embed.description = options + f"\n\n**What would you like to set the {elements[i]} as? Type `none` if you wish to set it as nothing or to use default values.**"
			await prompt.edit(embed=embed)
			response = await self.bot.wait_for('message', timeout=60.0, check=check)
			content = response.content
			if i == 1:
				try:
					int(content)
				except ValueError:
					content = discord.Color.default()
				else:
					content = int(content)
				finally:
					embed.color = content
			if i == 2 and content.lower() != "none":
				embed.set_thumbnail(url=content)
			if i == 3 and content.lower() != "none":
				embed.set_image(url=content)
			options += f"\n{elements[i]} set as **`{content}`**"
			properties.append(content)
			await response.delete()
		
		resultant_embed = discord.Embed(title=properties[0] if properties[0].lower() != "none" else '', description= properties[1] if properties[1].lower() != "none" else '', color=properties[2])
		if properties[3].strip.lower() != "none":
			resultant_embed.set_thumbnail(url=properties[3])
		if properties[4].strip.lower() != "none":
			resultant_embed.set_image(url=properties[4])
		if properties[5].strip.lower() != "none":
			resultant_embed.timestamp = datetime.datetime.utcnow()
		await ctx.send("> Where would you like to send this to?")
		prompt.edit(embed=resultant_embed)
		channel = await self.bot.wait_for('message', timeout=60.0, check=check).channel_mentions[0]
		await channel.send(embed=resultant_embed)

def setup(bot):
	bot.add_cog(TypeWriter(bot))
	print('TypeWriter.cog is loaded')
