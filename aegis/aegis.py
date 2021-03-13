import discord

from discord.ext import commands

class Aegis(commands.Cog):

	def __init__(self, bot):
		self.bot=bot

	@commands.group()
	@commands.guild_only()
	async def aegis(self, ctx):
		if ctx.invoked_subcommand is None:
			embed=discord.Embed(title='=Aegis Module Accessed=', description="Aegis module is designed to provide protectection to guilds and to prevent raids. NOTE: GRATZ TO YOU FINDING THIS UNINDEXED MODULE BUT CAUTION, IT IS EXTREMELY BUGGED AND IT COULD CAUSE HUGE ERRORS, DO NOT USE THE COMMANDS", color=discord.Color.dark_gold())
			embed.add_field(name='Void', value=f"`Aegis V0id implements all acessible invites to be exiled. Putting the server in v0id.`")
 			embed.add_field(name='Smoke', value=f'`Aegis smoke strips away the ability of everyone to see text channels. BUGGED`')
			embed.add_field(name='Chernobyl', value=f'`Aegis Chernobyl removes members that had joined before a specified time. This is a kick. V0id and Chernobyl can be used to prevent alts joining in.`')
			embed.add_field(name='Paris', value=f'`==`')
			embed.add_field(name='LoveCanal', value=f'`==`')
			await ctx.send(embed=embed)

	@aegis.command()
	@commands.guild_only()
	async def void(self, ctx):
		guild = ctx.guild
		invites = await guild.invites()
		for invite in invites:
			await invite.delete()
		embed=discord.Embed(title='🦁 Aegis Void Activated', description="All exisiting valid invites has sucessfully been exiled.", color=discord.Color.dark_gold())
		embed.set_footer(text=f"By {ctx.author.name}", icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)

	@aegis.command()
	@commands.guild_only()
	async def smoke(self, ctx):
		guild = ctx.guild
		blinding = discord.PermissionOverwrite(read_messages=False)
		for channel in guild.text_channels:
			await channel.set_permissions(guild.default_role, overwrite=blinding)
		embed=discord.Embed(title='🦁 Aegis Smoke Activated', description="Default roles no longer have the ability to read any channels.", color=discord.Color.dark_gold())
		embed.set_footer(text=f"By {ctx.author.name}", icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)

	@aegis.command()
	@commands.guild_only()
	async def chernobyl(self, ctx, *, values):
		embed=discord.Embed(title='🦁 Aegis Chernobly Activated', description="**Effect**:\n```This is a minor secuirty enhancement. Newly joined members will not be able to access all channels until they're authorised by admins.```", color=discord.Color.dark_gold())
		embed.set_footer(text=f"By {ctx.author.name}", icon_url=ctx.author.avatar_url)
		embed.add_field(name="Guide:", value="```If you had just joined, wait patiently for an admin to authorise you. Admins will be alerted of your presence.```\n`This is no serious matter! Have a wonderful stay here.`")
		embed.add_field(name='Will be taken into effect for:', value='```1440 minutes```')
		await ctx.send(embed=embed)

	@commands.command()
	@commands.guild_only()
	async def unaegis(self, ctx, *, action=None, time=None):
		guild = ctx.guild
		everyone= ctx.guild.default_role
		await everyone.edit(create_instant_invites=True)
		if action is None:
			embed=discord.Embed(title='=UNAegis Module Accessed=', description="UnAegis module is designed to rollback any aegis protocols that had been made.", color=discord.Color.dark_gold())
			embed.add_field(name='Usage', value=f"`{ctx.prefix}unaegis (action)`")
			await ctx.send(embed=embed)
		elif action=="void":
			yesinvite = discord.PermissionOverwrite(create_instant_invite=True)
			for channel in guild.text_channels:
				await channel.set_permissions(guild.default_role, overwrite=yesinvite)
			embed=discord.Embed(title='🦁 Aegis Void RollBacked', description="Ageis V0id has been rollbacked.", color=discord.Color.dark_gold())
			embed.set_footer(text=f"By {ctx.author.name}", icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
		elif action=="smoke":
			change = discord.PermissionOverwrite(read_messages=True)
			for channel in guild.text_channels:
				await channel.set_permissions(guild.default_role, overwrite=change)
			embed=discord.Embed(title='🦁 Aegis Smoke RollBacked', description="Default roles regained the ability to read every channels.", color=discord.Color.dark_gold())
			embed.set_footer(text=f"By {ctx.author.name}", icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)
		elif action=="chernobyl":
			pass
		else:
			embed = discord.Embed (title='ERROR...', description=f"Invalid action chosen!", color=discord.Colour.dark_red())
			embed.set_footer(text=f'Execute "{ctx.prefix}aegis" to see available actions')
			await ctx.send (embed=embed)

def setup(bot):
	bot.add_cog(Aegis(bot))
	print('Aegis.cog loaded')
