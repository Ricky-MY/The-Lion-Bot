import discord
from discord.ext import commands
import traceback
import datetime


class errors(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		try:
			if hasattr(ctx.command, 'on_error'):
				return
			else:
				if {ctx.author} == 'NEO#9173':
					nembed = discord.Embed(title=f'ERROR...', description=f'{error}', color=discord.Colour.dark_red())
					nembed.set_footer(text=f'Usage: {ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}',
									  icon_url=self.client.user.avatar_url)
					await ctx.send(embed=nembed)
					print(f'________________________________________________________________________________________________________________________\nExecuted by : {ctx.author} | Guild : {ctx.guild.name}\n{error}\n________________________________________________________________________________________________________________________')
				else:
					pass
		except:
			if isinstance(error, commands.CommandNotFound):
				pass

def setup(client):
	client.add_cog(errors(client))
	print('errors.cog is loaded')
