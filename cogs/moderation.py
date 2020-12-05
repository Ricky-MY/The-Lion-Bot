import discord
from discord.ext import commands


class Moderation(commands.Cog):

	def __init__(self, client):
		self.client = client

	# Kick Command
	@commands.command()
	@commands.guild_only()
	@commands.has_guild_permissions(kick_members=True)
	async def kick(self, ctx, member: discord.Member, *, reason='Unspecified reason'):
		await member.kick(reason=reason)
		ksembed = discord.Embed(title='Success!',
								description=f'{member.mention} has been successfully kicked for {reason}',
								color=discord.Colour.dark_teal())
		ksembed.set_footer(text=f'By {ctx.author.name}', icon_url=ctx.author.avatar_url)
		await ctx.send(embed=ksembed)


	# Kick Specific errors
	@kick.error
	async def mr4k(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			mr4kembed = discord.Embed(title='ERROR...',
									  description=f"You do not have the required permission to execute this command!",
									  color=discord.Colour.dark_red())
			mr4kembed.set_footer(text=f'You need the {error.missing_permissions} permission!')
			await ctx.send(embed=mr4kembed)
		if isinstance(error, commands.BadArgument):
			ba4kembed = discord.Embed(title='ERROR...', description=f"Invalid user specified!",
									  color=discord.Colour.dark_red())
			ba4kembed.set_footer(text=f'{ctx.prefix}{ctx.command} (@user) [reason]')
			await ctx.send(embed=ba4kembed)
		if isinstance(error, commands.MissingRequiredArgument):
			mra4bembed = discord.Embed(title='ERROR...', description=f"Please specify a user to kick!",
									   color=discord.Colour.dark_red())
			mra4bembed.set_footer(text=f'{ctx.prefix}{ctx.command} (@user)[reason]')
			await ctx.send(embed=mra4bembed)


	# Ban Command
	@commands.command()
	@commands.guild_only()
	@commands.has_guild_permissions(ban_members=True)
	async def ban(self, ctx, member: discord.Member = None, *, reason=f'Unspecified reason'):
		if ctx.guild.id == 702714944558202933:
			embed = discord.Embed(title='ERROR...', description=f"Current guild is prohibited from using the ban command.",color=discord.Colour.dark_red())
			embed.set_footer(text=f'FAILURE TO PROCEED')
			await ctx.send(embed=embed)
			return
		if member is None:
			return
		await member.send(f"https://media.giphy.com/media/LPHbzPcICc86EVte9C/giphy.gif from {ctx.guild.name}")
		await member.send(f"You have been banned from {ctx.guild} for {reason}")
		await member.ban(reason=reason)
		pbsembed = discord.Embed(title='Success!',
								 description=f'{member.mention} has been successfully banned for {reason}.',
								 color=discord.Colour.dark_teal())
		pbsembed.set_footer(text=f'By {ctx.author.name}', icon_url=ctx.author.avatar_url)
		await ctx.send(embed=pbsembed)


	# Ban Specific errors
	@ban.error
	async def mr4b(self, ctx, error):
		if isinstance(error, commands.MissingRole):
			mr4bembed = discord.Embed(title='ERROR...',
									  description=f"You do not have the required permission to execute this command!",
									  color=discord.Colour.dark_red())
			mr4bembed.set_footer(text=f'You need the {error.missing_role} role!')
			await ctx.send(embed=mr4bembed)
		if isinstance(error, commands.BadArgument):
			ba4bembed = discord.Embed(title='ERROR...', description=f"Invalid user specified!",
									  color=discord.Colour.dark_red())
			ba4bembed.set_footer(text=f'{ctx.prefix}{ctx.command} (@user) [reason]')
			await ctx.send(embed=ba4bembed)
		if isinstance(error, commands.MissingRequiredArgument):
			mra4bembed = discord.Embed(title='ERROR...', description=f"Please specify a user to ban!",
									   color=discord.Colour.dark_red())
			mra4bembed.set_footer(text=f'{ctx.prefix}{ctx.command} (@user)[reason]')
			await ctx.send(embed=mra4bembed)


	# Unban Command
	@commands.command()
	@commands.guild_only()
	@commands.has_guild_permissions(ban_members=True)
	async def unban(self, ctx, *, member):
		banned_users = await ctx.guild.bans()
		member_name, member_discriminator = member.split('#')
		for ban_entry in banned_users:
			user = ban_entry.user
			if (user.name, user.discriminator) == (member_name, member_discriminator):
				await ctx.guild.unban(user)
				ubsembed = discord.Embed(title='Success!', description=f'{member} has been successfully unbanned.',
										 color=discord.Colour.dark_teal())
				ubsembed.set_footer(text=f'By {ctx.author.name}', icon_url=ctx.author.avatar_url)
				await ctx.send(embed=ubsembed)


	# Unban specific errors
	@unban.error
	async def mr4ub(self, ctx, error):
		if isinstance(error, commands.MissingRole):
			mr4ubembed = discord.Embed(title='ERROR...',
									   description=f"You do not have the required permission to execute this command!",
									   color=discord.Colour.dark_red())
			mr4ubembed.set_footer(text=f'You need the {error.missing_role} role!')
			await ctx.send(embed=mr4ubembed)
		if isinstance(error, commands.BadArgument):
			ba4ubembed = discord.Embed(title='ERROR...', description=f"Invalid user specified!",
									   color=discord.Colour.dark_red())
			ba4ubembed.set_footer(text=f'{ctx.prefix}{ctx.command} (@user) [reason]')
			await ctx.send(embed=ba4ubembed)
		if isinstance(error, commands.MissingRequiredArgument):
			mra4ubembed = discord.Embed(title='ERROR...', description=f"Please specify a user to unban!",
										color=discord.Colour.dark_red())
			mra4ubembed.set_footer(text=f'{ctx.prefix}{ctx.command} (@user)')
			await ctx.send(embed=mra4ubembed)


	# Mute Command
	@commands.command()
	@commands.guild_only()
	@commands.has_guild_permissions(mute_members=True)
	async def mute(self, ctx, member: discord.Member):
		guild = ctx.guild
		for role in guild.roles:
			if role.name == "Muted":
				await member.add_roles(role)
				await ctx.send(f"{member} is successfully muted.")
				return
		muting = discord.PermissionOverwrite(send_messages=False)
		newRole = await guild.create_role(name="Muted")
		for channel in guild.text_channels:
			await channel.set_permissions(newRole, overwrite=muting)
		await member.add_roles(newRole)
		await ctx.send(f"{member} has been muted.")


	# Unmute Command
	@commands.command()
	@commands.guild_only()
	@commands.has_guild_permissions(mute_members=True)
	async def unmute(self, ctx, member: discord.Member):
		guild = ctx.guild
		for role in guild.roles:
			if role.name == "Muted":
				await member.remove_roles(role)
				await ctx.send(f"{member} successfully unmuted")
				return


	# Purge
	@commands.command()
	@commands.guild_only()
	@commands.has_guild_permissions(manage_messages=True)
	async def clear(self, ctx, amount=5):
		channel = ctx.channel
		await channel.purge(limit=amount)
		embed = discord.Embed(description=f"{amount} messages successfully cleared!", color=discord.Colour.dark_teal())
		delete = await ctx.send(embed=embed)
		await delete.delete()


def setup(client):
	client.add_cog(Moderation(client))
	print('moderation.cog is loaded')
