# Author - Ricky
# Type Writer COG
import discord
from discord.ext import commands
from discord.ext.commands import Cog
import datetime


class TypeWriter(Cog):

	def __init__(self, client):
		self.client = client

	def botAdminCheck(ctx):
		return ctx.message.author.id in (368671236370464769, 543418509565362186, 348830078152605696)


	@commands.group(name=str("thread"), invoke_without_command=True)
	@commands.guild_only()
	@commands.check(botAdminCheck)
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
	@commands.check(botAdminCheck)
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
	@commands.check(botAdminCheck)
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

	@thread.command(aliases=['edit_colour'])
	@commands.guild_only()
	@commands.check(botAdminCheck)
	async def edit_color(self, ctx, channel : discord.TextChannel, messageID, color):
		message = await channel.fetch_message(messageID)
		embed = message.embeds[0]
		embed.colour = int(color)
		await message.edit(embed=embed)
		await ctx.send("> Success")

	@thread.command()
	@commands.guild_only()
	@commands.check(botAdminCheck)
	async def edit_title(self, ctx, channel : discord.TextChannel, messageID, *, title):
		message = await channel.fetch_message(messageID)
		embed = message.embeds[0]
		embed.title = title
		await message.edit(embed=embed)
		await ctx.send("> Success")

	@thread.command()
	@commands.guild_only()
	@commands.check(botAdminCheck)
	async def edit_desc(self, ctx, channel : discord.TextChannel, messageID, *, description):
		message = await channel.fetch_message(messageID)
		embed = message.embeds[0]
		embed.description = description
		await message.edit(embed=embed)
		await ctx.send("> Success")

	@thread.command()
	@commands.guild_only()
	@commands.check(botAdminCheck)
	async def edit_time(self, ctx, channel : discord.TextChannel, messageID, boolean = 'on'):
		message = await channel.fetch_message(messageID)
		embed = message.embeds[0]
		if boolean == 'on':
			embed.timestamp = datetime.datetime.utcnow()
			await message.edit(embed=embed)
			await ctx.send("> Success")
		else:
			await ctx.send("> Failure, you can only enable time stamps!, use the value 'on' to do so.")

	@commands.command(aliases=['at', 'advthread'])
	@commands.guild_only()
	@commands.check(botAdminCheck)
	async def advThread(self, ctx):
		channel = ctx.channel
		embed = discord.Embed(title='Advance-Threading', description='**What would you like to set the title as?**',
							  color=discord.Color.dark_gold())
		response = await channel.send(embed=embed)

		def check(message):
			return message.channel == channel and message.author == ctx.author

		rawTitle = await self.client.wait_for('message', timeout=60.0, check=check)
		title = rawTitle.content
		embed.description = f'Title setup as:`{title}`\n**What would you like to set the description as?**'
		await response.edit(embed=embed)

		rawDescription = await self.client.wait_for('message', timeout=60.0, check=check)
		description = rawDescription.content
		embed.description = f'Title setup as:`{title}`\nDescription setup as:`{description}`\n**What color would you like to set the embed as?**'
		await response.edit(embed=embed)

		rawColor = await self.client.wait_for('message', timeout=60.0, check=check)
		color = int(rawColor.content)
		embed.description = f'Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\n**Would you like to add a thumbnail, if so paste the direct link of the thumbnail? If not, say no.**'
		embed.color = color
		await response.edit(embed=embed)

		rawThumbnail = await self.client.wait_for('message', timeout=60.0, check=check)
		thumbnail = str(rawThumbnail.content)
		if thumbnail.lower() != 'no':
			# Thumbnail Approval
			embed.description = f'Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\n**Would you like to add a timestamp? yes/no**'
			embed.set_thumbnail(url=thumbnail)
			await response.edit(embed=embed)

			answer = await self.client.wait_for('message', timeout=60.0, check=check)
			answer = str(answer.content)
			if answer.lower() == 'yes':
				# Thumbnail Approved
				# Timestamp Approval
				embed.description = f'Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `approved`\n**Would you like to add the author? yes/no**'
				await response.edit(embed=embed)

				answer = await self.client.wait_for('message', timeout=60.0, check=check)
				answer = str(answer.content)
				if answer.lower() == 'yes':
					# Thumbnail Approved
					# Timestamp Approved
					# Author Approval
					embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `approved`\nAuthor is `approved`\n**Would you like to add the announcer's template? yes/no**"

					await response.edit(embed=embed)

					answer = await self.client.wait_for('message', timeout=60.0, check=check)
					answer = str(answer.content)
					if answer.lower() == 'yes':
						# Thumbnail Approved
						# Timestamp Approved
						# Author Approved
						# Template Approved
						embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `approved`\nAuthor is `approved`\nTemplate is `approved`"
						embed.set_thumbnail(url=thumbnail)
						await response.edit(embed=embed)

						await channel.send(f'RESULT:')
						embed = discord.Embed(title=title, description=description, color=color)
						embed.set_thumbnail(url=thumbnail)
						embed.timestamp = datetime.datetime.utcnow()
						embed.set_footer(text=f'By {ctx.author.name}', icon_url=ctx.author.avatar_url)
						embed.set_author(name="ANNOUNCEMENT!", icon_url=ctx.guild.icon_url)
						await channel.send(embed=embed)
						await channel.send("> Mention the channel in which you'd like to send the created embed")
						rawChannel = await self.client.wait_for('message', timeout=60.0, check=check)
						channel = rawChannel.channel_mentions[0]
						await channel.send(embed=embed)
						await ctx.send('> Success')

					elif answer.lower() == 'no':
						# Thumbnail Approved
						# Timestamp Approved
						# Author Approved
						# Template Disapproved
						embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `approved`\nAuthor is `approved`\nTemplate is `disapproved`"
						embed.set_thumbnail(url=thumbnail)
						await response.edit(embed=embed)

						await channel.send(f'RESULT:')
						embed = discord.Embed(title=title, description=description, color=color)
						embed.set_thumbnail(url=thumbnail)
						embed.timestamp = datetime.datetime.utcnow()
						embed.set_footer(text=f'By {ctx.author.name}', icon_url=ctx.author.avatar_url)
						await channel.send(embed=embed)
						await channel.send("> Mention the channel in which you'd like to send the created embed")
						rawChannel = await self.client.wait_for('message', timeout=60.0, check=check)
						channel = rawChannel.channel_mentions[0]
						await channel.send(embed=embed)
						await ctx.send('> Success')

				elif answer.lower() == 'no':
					# Thumbnail Approved
					# Timestamp Approved
					# Author Disapproved
					embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `approved`\nAuthor is `disapproved`\n**Would you like to add the announcer's template? yes/no**"
					await response.edit(embed=embed)

					answer = await self.client.wait_for('message', timeout=60.0, check=check)
					answer = str(answer.content)
					if answer.lower() == 'yes':
						# Thumbnail Approved
						# Timestamp Approved
						# Author Disapproved
						# Template Approved
						embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `approved`\nAuthor is `disapproved`\nTemplate is `approved`"
						embed.set_thumbnail(url=thumbnail)
						await response.edit(embed=embed)

						await channel.send(f'RESULT:')
						embed = discord.Embed(title=title, description=description, color=color)
						embed.set_thumbnail(url=thumbnail)
						embed.timestamp = datetime.datetime.utcnow()
						embed.set_author(name="ANNOUNCEMENT!", icon_url=ctx.guild.icon_url)
						await channel.send(embed=embed)
						await channel.send("> Mention the channel in which you'd like to send the created embed")
						rawChannel = await self.client.wait_for('message', timeout=60.0, check=check)
						channel = rawChannel.channel_mentions[0]
						await channel.send(embed=embed)
						await ctx.send('> Success')
					elif answer.lower() == 'no':
						# Thumbnail Approved
						# Timestamp Approved
						# Author Disapproved
						# Template Disapproved
						embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `approved`\nAuthor is `disapproved`\nTemplate is `disapproved`"
						embed.set_thumbnail(url=thumbnail)
						await response.edit(embed=embed)

						await channel.send(f'RESULT:')
						embed = discord.Embed(title=title, description=description, color=color)
						embed.set_thumbnail(url=thumbnail)
						embed.timestamp = datetime.datetime.utcnow()
						await channel.send(embed=embed)
						await channel.send("> Mention the channel in which you'd like to send the created embed")
						rawChannel = await self.client.wait_for('message', timeout=60.0, check=check)
						channel = rawChannel.channel_mentions[0]
						await channel.send(embed=embed)
						await ctx.send('> Success')

			elif answer.lower() == 'no':
				# Thumbnails Approved
				# TimeStamp Disapproval
				embed.description = embed.description = f'Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `disapproved`\n**Would you like to add the author? yes/no**'
				await response.edit(embed=embed)

				answer = await self.client.wait_for('message', timeout=60.0, check=check)
				answer = str(answer.content)
				if answer.lower() == 'yes':
					# Thumbnails Approved
					# TimeStamp Disapproval
					# Author Approval
					embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `disapproved`\nAuthor is `approved`\n**Would you like to add the announcer's template? yes/no**"
					await response.edit(embed=embed)

					answer = await self.client.wait_for('message', timeout=60.0, check=check)
					answer = str(answer.content)

					if answer.lower() == 'yes':
						# Thumbnail Approved
						# Timestamp Disapproved
						# Author Approved
						# Template Approved
						embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `disapproved`\nAuthor is `approved`\nTemplate is `approved`"
						embed.set_thumbnail(url=thumbnail)
						await response.edit(embed=embed)

						await channel.send(f'RESULT:')
						embed = discord.Embed(title=title, description=description, color=color)
						embed.set_thumbnail(url=thumbnail)
						embed.set_footer(text=f'By {ctx.author.name}', icon_url=ctx.author.avatar_url)
						embed.set_author(name="ANNOUNCEMENT!", icon_url=ctx.guild.icon_url)
						await channel.send(embed=embed)
						await channel.send("> Mention the channel in which you'd like to send the created embed")
						rawChannel = await self.client.wait_for('message', timeout=60.0, check=check)
						channel = rawChannel.channel_mentions[0]
						await channel.send(embed=embed)
						await ctx.send('> Success')
					elif answer.lower() == 'no':
						# Thumbnail Approved
						# Timestamp Disapproved
						# Author Approved
						# Template Disapproved
						embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `disapproved`\nAuthor is `approved`\nTemplate is `disapproved`"
						embed.set_thumbnail(url=thumbnail)
						await response.edit(embed=embed)

						await channel.send(f'RESULT:')
						embed = discord.Embed(title=title, description=description, color=color)
						embed.set_thumbnail(url=thumbnail)
						embed.set_footer(text=f'By {ctx.author.name}', icon_url=ctx.author.avatar_url)
						await channel.send(embed=embed)
						await channel.send("> Mention the channel in which you'd like to send the created embed")
						rawChannel = await self.client.wait_for('message', timeout=60.0, check=check)
						channel = rawChannel.channel_mentions[0]
						await channel.send(embed=embed)
						await ctx.send('> Success')

				elif answer.lower() == 'no':
					# Thumbnails Approved
					# TimeStamp Disapproved
					# Author Disapproval
					embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `disapproved`\nAuthor is `disapproved`\n**Would you like to add the announcer's template? yes/no**"
					await response.edit(embed=embed)

					answer = await self.client.wait_for('message', timeout=60.0, check=check)
					answer = str(answer.content)

					if answer.lower() == 'yes':
						# Thumbnail Approved
						# Timestamp Disapproved
						# Author Disapproved
						# Template Approved
						embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `disapproved`\nAuthor is `disapproved`\nTemplate is `approved`"
						embed.set_thumbnail(url=thumbnail)
						await response.edit(embed=embed)

						await channel.send(f'RESULT:')
						embed = discord.Embed(title=title, description=description, color=color)
						embed.set_thumbnail(url=thumbnail)
						embed.set_author(name="ANNOUNCEMENT!", icon_url=ctx.guild.icon_url)
						await channel.send(embed=embed)
						await channel.send("> Mention the channel in which you'd like to send the created embed")
						rawChannel = await self.client.wait_for('message', timeout=60.0, check=check)
						channel = rawChannel.channel_mentions[0]
						await channel.send(embed=embed)
						await ctx.send('> Success')
					elif answer.lower() == 'no':
						# Thumbnail Approved
						# Timestamp Disapproved
						# Author Disapproved
						# Template Disapproved
						embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `disapproved`\nAuthor is `disapproved`\nTemplate is `disapproved`"
						embed.set_thumbnail(url=thumbnail)
						await response.edit(embed=embed)

						await channel.send(f'RESULT:')
						embed = discord.Embed(title=title, description=description, color=color)
						embed.set_thumbnail(url=thumbnail)
						await channel.send(embed=embed)
						await channel.send("> Mention the channel in which you'd like to send the created embed")
						rawChannel = await self.client.wait_for('message', timeout=60.0, check=check)
						channel = rawChannel.channel_mentions[0]
						await channel.send(embed=embed)
						await ctx.send('> Success')
		else:
			# Thumbnail Disapproval
			embed.description = f'Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\n**Would you like to add a timestamp? yes/no**'
			await response.edit(embed=embed)
			answer = await self.client.wait_for('message', timeout=60.0, check=check)
			answer = str(answer.content)
			if answer.lower() == 'yes':
				# Thumbnail DISAPPROVED
				# Timestamp APPROVAL
				embed.description = embed.description = f'Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nTimeStamp is `approved`\n**Would you like to add the author? yes/no**'
				await response.edit(embed=embed)

				answer = await self.client.wait_for('message', timeout=60.0, check=check)
				answer = str(answer.content)
				if answer.lower() == 'yes':
					# Thumbnail DISAPPROVED
					# TimeStamp APPROVED
					# Author APPROVAL
					embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nTimeStamp is `approved`\nAuthor is `approved`\n**Would you like to add the announcer's template? yes/no**"

					await response.edit(embed=embed)

					answer = await self.client.wait_for('message', timeout=60.0, check=check)
					answer = str(answer.content)

					if answer.lower() == 'yes':
						# Thumbnail Disapproved
						# Timestamp Approved
						# Author Approved
						# Template Approved
						embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `approved`\nAuthor is `approved`\nTemplate is `approved`"

						await response.edit(embed=embed)

						await channel.send(f'RESULT:')
						embed = discord.Embed(title=title, description=description, color=color)
						embed.set_author(name="ANNOUNCEMENT!", icon_url=ctx.guild.icon_url)
						embed.timestamp = datetime.datetime.utcnow()
						embed.set_footer(text=f'By {ctx.author.name}', icon_url=ctx.author.avatar_url)
						await channel.send(embed=embed)
						await channel.send("> Mention the channel in which you'd like to send the created embed")
						rawChannel = await self.client.wait_for('message', timeout=60.0, check=check)
						channel = rawChannel.channel_mentions[0]
						await channel.send(embed=embed)
						await ctx.send('> Success')
					elif answer.lower() == 'no':
						# Thumbnail Disapproved
						# Timestamp Approved
						# Author Approved
						# Template Disapproved
						embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `approved`\nAuthor is `approved`\nTemplate is `disapproved`"

						await response.edit(embed=embed)

						await channel.send(f'RESULT:')
						embed = discord.Embed(title=title, description=description, color=color)
						embed.set_footer(text=f'By {ctx.author.name}', icon_url=ctx.author.avatar_url)
						embed.timestamp = datetime.datetime.utcnow()
						await channel.send(embed=embed)
						await channel.send("> Mention the channel in which you'd like to send the created embed")
						rawChannel = await self.client.wait_for('message', timeout=60.0, check=check)
						channel = rawChannel.channel_mentions[0]
						await channel.send(embed=embed)
						await ctx.send('> Success')

				elif answer.lower() == 'no':
					# Thumbnail DISAPPROVED
					# TimeStamp APPROVED
					# Author DISAPPROVAL
					embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nTimeStamp is `approved`\nAuthor is `disapproved`\n**Would you like to add the announcer's template? yes/no**"
					await response.edit(embed=embed)

					answer = await self.client.wait_for('message', timeout=60.0, check=check)
					answer = str(answer.content)

					if answer.lower() == 'yes':
						# Thumbnail Disapproved
						# Timestamp Approved
						# Author Disapproved
						# Template Approved
						embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `approved`\nAuthor is `disapproved`\nTemplate is `approved`"
						await response.edit(embed=embed)

						await channel.send(f'RESULT:')
						embed = discord.Embed(title=title, description=description, color=color)
						embed.set_author(name="ANNOUNCEMENT!", icon_url=ctx.guild.icon_url)
						embed.timestamp = datetime.datetime.utcnow()
						await channel.send(embed=embed)
						await channel.send("> Mention the channel in which you'd like to send the created embed")
						rawChannel = await self.client.wait_for('message', timeout=60.0, check=check)
						channel = rawChannel.channel_mentions[0]
						await channel.send(embed=embed)
						await ctx.send('> Success')
					elif answer.lower() == 'no':
						# Thumbnail Disapproved
						# Timestamp Approved
						# Author Disapproved
						# Template Disapproved
						embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `approved`\nAuthor is `disapproved`\nTemplate is `disapproved`"

						await response.edit(embed=embed)

						await channel.send(f'RESULT:')
						embed = discord.Embed(title=title, description=description, color=color)
						embed.timestamp = datetime.datetime.utcnow()
						await channel.send(embed=embed)
						await channel.send("> Mention the channel in which you'd like to send the created embed")
						rawChannel = await self.client.wait_for('message', timeout=60.0, check=check)
						channel = rawChannel.channel_mentions[0]
						await channel.send(embed=embed)
						await ctx.send('> Success')

			elif answer.lower() == 'no':
				# Thumbnail Disapproved
				# TimeStamp DISAPPROVAL
				embed.description = embed.description = f'Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nTimeStamp is `disapproved`\n**Would you like to add the author? yes/no**'
				await response.edit(embed=embed)

				answer = await self.client.wait_for('message', timeout=60.0, check=check)
				answer = str(answer.content)
				if answer.lower() == 'yes':
					# Thumbnail Disapproved
					# Timestamp Disapproved
					# Author APPROVAL
					embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nTimeStamp is `disapproved`\nAuthor is `approved`\n**Would you like to add the announcer's template? yes/no**"

					await response.edit(embed=embed)

					answer = await self.client.wait_for('message', timeout=60.0, check=check)
					answer = str(answer.content)

					if answer.lower() == 'yes':
						# Thumbnail Disapproved
						# Timestamp Disapproved
						# Author Approved
						# Template Approved
						embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `disapproved`\nAuthor is `approved`\nTemplate is `approved`"
						await response.edit(embed=embed)

						await channel.send(f'RESULT:')
						embed = discord.Embed(title=title, description=description, color=color)
						embed.set_author(name="ANNOUNCEMENT!", icon_url=ctx.guild.icon_url)
						embed.set_footer(text=f'By {ctx.author.name}', icon_url=ctx.author.avatar_url)
						await channel.send(embed=embed)
						await channel.send("> Mention the channel in which you'd like to send the created embed")
						rawChannel = await self.client.wait_for('message', timeout=60.0, check=check)
						channel = rawChannel.channel_mentions[0]
						await channel.send(embed=embed)
						await ctx.send('> Success')
					elif answer.lower() == 'no':
						# Thumbnail Disapproved
						# Timestamp Disapproved
						# Author Approved
						# Template Disapproved
						embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `disapproved`\nAuthor is `approved`\nTemplate is `disapproved`"

						await response.edit(embed=embed)

						await channel.send(f'RESULT:')
						embed = discord.Embed(title=title, description=description, color=color)
						embed.set_footer(text=f'By {ctx.author.name}', icon_url=ctx.author.avatar_url)
						await channel.send(embed=embed)
						await channel.send("> Mention the channel in which you'd like to send the created embed")
						rawChannel = await self.client.wait_for('message', timeout=60.0, check=check)
						channel = rawChannel.channel_mentions[0]
						await channel.send(embed=embed)
						await ctx.send('> Success')

				elif answer.lower() == 'no':
					# Thumbnail Disapproved
					# TimeStamp Disapproved
					# Author DISAPPROVAL
					embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nTimeStamp is `disapproved`\nAuthor is `disapproved`\n**Would you like to add the announcer's template? yes/no**"
					await response.edit(embed=embed)

					answer = await self.client.wait_for('message', timeout=60.0, check=check)

					answer = str(answer.content)

					if answer.lower() == 'yes':
						# Thumbnail Disapproved
						# Timestamp Disapproved
						# Author Disapproved
						# Template Approved
						embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `disapproved`\nAuthor is `disapproved`\nTemplate is `approved`"
						await response.edit(embed=embed)

						await channel.send(f'RESULT:')
						embed = discord.Embed(title=title, description=description, color=color)
						embed.set_author(name="ANNOUNCEMENT!", icon_url=ctx.guild.icon_url)
						await channel.send(embed=embed)
						await channel.send("> Mention the channel in which you'd like to send the created embed")
						rawChannel = await self.client.wait_for('message', timeout=60.0, check=check)
						channel = rawChannel.channel_mentions[0]
						await channel.send(embed=embed)
						await ctx.send('> Success')
					elif answer.lower() == 'no':
						# Thumbnail Disapproved
						# Timestamp Disapproved
						# Author Disapproved
						# Template Disapproved
						embed.description = f"Title setup as:`{title}`\nDescription setup as:`{description}`\nColor setup as:`CURRENT EMBED COLOR`\nThumbnail setup as:`CURRENT THUMBNAIL`\nTimeStamp is `disapproved`\nAuthor is `disapproved`\nTemplate is `disapproved`"

						await response.edit(embed=embed)

						await channel.send(f'RESULT:')
						embed = discord.Embed(title=title, description=description, color=color)
						await channel.send(embed=embed)
						await channel.send("> Mention the channel in which you'd like to send the created embed")
						rawChannel = await self.client.wait_for('message', timeout=60.0, check=check)
						channel = rawChannel.channel_mentions[0]
						await channel.send(embed=embed)
						await ctx.send('> Success')
						

def setup(client):
	client.add_cog(TypeWriter(client))
	print('TypeWriter.cog is loaded')
