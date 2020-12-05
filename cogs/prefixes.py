import discord
from discord.ext import commands
import json


class Prefixes(commands.Cog):

	def __init__(self, client):
		self.client = client

	def botAdminCheck(ctx):
		return ctx.message.author.id == 368671236370464769


	# Prefix finding Command
	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	@commands.check(botAdminCheck)
	async def prefix(self, ctx):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		embed=discord.Embed(title=f"Preset", description=f"CURRENT SERVER PREFIX : \n1. '`{prefixes[str(ctx.guild.id)]}`' \n2.{ctx.guild.me.mention}\nExecute `{prefixes[str(ctx.guild.id)]}prefix change <new_prefix>` command to change prefixes!", colour=discord.Colour.dark_teal())
		await ctx.send(embed=embed)
	

	@prefix.command()
	async def change(self, ctx, prefix):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		prefixes[str(ctx.guild.id)] = prefix
		with open('prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent=4)
		embed=discord.Embed(title=f"Success!", description=f'PREFIX SUCCESSFULLY CHANGED INTO : `{prefix}`\nExecute `{prefix}prefix` command to check the local prefix anytime!', colour=discord.Colour.dark_teal())
		await ctx.send(embed=embed)
		

def setup(client):
	client.add_cog(Prefixes(client))
	print('Prefixes.cog is loaded')
