import discord
import json

from discord.ext import commands

class Prefixes(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.prefix_directory = 'bot/assets/prefixes.json'
  
	def get_prefix(bot, message):
		with open('bot/assets/prefixes.json', 'r') as f:
			prefixes = json.load(f)
		try:
			return commands.when_mentioned_or(prefixes[str(message.guild.id)])(bot, message)
		except KeyError:
			prefixes[str(message.guild.id)] = "p!"
			with open('bot/assets/prefixes.json', 'w') as f:
				json.dump(prefixes, f, indent=4)
			return commands.when_mentioned_or(prefixes[str(message.guild.id)])(bot, message)

	def fetch_prefix(guild_id):
		with open('bot/assets/prefixes.json', 'r') as f:
			prefixes = json.load(f)

		try:
			return prefixes[str(guild_id)]
		except KeyError:
			prefixes[str(guild_id)] = "p!"
			with open('bot/assets/prefixes.json', 'w') as f:
				json.dump(prefixes, f, indent=4)
		finally:
			return prefixes[str(guild_id)]

	# Prefix finding Command
	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	async def prefix(self, ctx):
		with open(self.prefix_directory, 'r') as f:
			prefixes = json.load(f)
		embed=discord.Embed(title=f"Preset", description=f"CURRENT SERVER PREFIX : \n1. '`{prefixes[str(ctx.guild.id)]}`' \n2.{ctx.guild.me.mention}\nTry `{prefixes[str(ctx.guild.id)]}prefix change <new_prefix>` command to change prefixes!", colour=discord.Colour.dark_teal())
		await ctx.send(embed=embed)
	
	@prefix.command()
	@commands.has_guild_permissions(manage_guild = True)
	async def change(self, ctx, prefix):
		with open(self.prefix_directory, 'r') as f:
			prefixes = json.load(f)
		prefixes[str(ctx.guild.id)] = prefix
		with open(self.prefix_directory, 'w') as f:
			json.dump(prefixes, f, indent=4)
		embed=discord.Embed(title=f"Success!", description=f'PREFIX SUCCESSFULLY CHANGED INTO : `{prefix}`\nTry `{prefix}prefix` command to check the local prefix anytime!', colour=discord.Colour.dark_teal())
		await ctx.send(embed=embed)
		
def setup(bot):
	bot.add_cog(Prefixes(bot))
	print('Prefixes.cog is loaded')