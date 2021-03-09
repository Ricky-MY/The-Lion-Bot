# The Lion Bot
# Author - Ricky
# Created at 5th of August 2020
from discord import Intents
from discord import Status
from discord import Game
from discord.ext import commands

from dotenv import load_dotenv
from os import listdir, getenv

from bot.utilities.prefixes import Prefixes
from bot.moderation.admin import bot_admin_check

"""TODO: Continue saving prompts for AEGIS, TAG, TYPEWRITER
Add a hyperlink to the message in FAILURE TO SEND SOURCE CODE
Disable the option to view administrative source code at all
Add commands SILENCE, UNSILENCE, SELFMUTE"""

intents = Intents.default()
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix=Prefixes.get_prefix, intents = intents, status=Status.do_not_disturb, activity=Game("Gerald's game >:)"))
bot.remove_command('help')

# Shut Down Command
@bot.command(name="shutdown")
@commands.guild_only()
@commands.check(bot_admin_check)
async def shutdown(ctx):
	await ctx.send('Bot has been shut down.')
	await bot.logout()

@bot.event
async def on_ready():
	print("____________\nPill is on standby\n____________")

parentdir = 'bot'
for filename in listdir(f'./{parentdir}'):
	if not filename.endswith('.py') and not filename.startswith('_') and not filename.startswith('.'):
		for subdir in listdir(f'./{parentdir}/{filename}/'):
			if subdir.endswith('.py') and not subdir.startswith('_') and not subdir.startswith('.'):
				bot.load_extension(f'{parentdir}.{filename}.{subdir[:-3]}')

load_dotenv()
token = getenv('TOKEN')
bot.run(token)