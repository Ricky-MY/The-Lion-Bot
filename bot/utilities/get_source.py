import discord
import inspect
import yaml

from discord.ext import commands

from bot.moderation.admin import bot_admin_check

class getSource(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		with open("config.yaml", 'r') as file:
			config = yaml.load(file, Loader=yaml.SafeLoader)
		self.color = config["asthetics"]["mainColor"]
		self.error_color = config["asthetics"]["errorColor"]
		self.embed = discord.Embed(color=self.color)
		self.embed.set_author(name="Source code inspection", icon_url ="https://cdn.discordapp.com/emojis/818820065834303488.png?v=1")
		self.embed.set_footer(
			text="Type p!help command for an in-depth command help")

	@commands.command(name="code", aliases=["source", "src"])
	@commands.has_guild_permissions(manage_guild=True)
	async def code(self, ctx, command):
		command = self.bot.get_command(command)
		if command.cog_name.lower() not in ("aegis", "admin", "exception") or (command.cog_name.lower() in ("aegis", "admin", "exception") and bot_admin_check(ctx)):
			embed = self.embed.copy()
			source_code = inspect.getsource(command.callback)
			embed.description=f"```py\n{source_code if len(source_code) < 2000 else 'Source code too large for discord, please head over to our open sourced git-hub repository for this inspection.'}```"
			await ctx.reply(embed=embed)
		else:
			embed = self.embed.copy()
			embed.title = "Restricted"
			embed.description = "Sorry, you are prohibited to view the source code of this command."
			embed.color = self.error_color
			await ctx.reply(embed=embed) 
				

def setup(bot):
	bot.add_cog(getSource(bot))
	print('getSource.cog is loaded')
