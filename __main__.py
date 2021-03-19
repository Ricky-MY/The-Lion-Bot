from os import getenv
from dotenv import load_dotenv
from discord import Intents, Status, Game
from discord.ext import commands

from bot.constants import Defaults
from bot.utils.extensions import EXTENSIONS

intents = Intents.default()
intents.reactions = True

# Bot constructor
bot = commands.Bot(command_prefix = Defaults.PREFIX,
                    intents = intents,
                    status = Status.do_not_disturb, activity = Game("New Bot"))

# On ready event
bot.remove_command('help')
@bot.event
async def on_ready():
	print(f"{bot.user.name} is on standby")

for ext in EXTENSIONS:
    bot.load_extension(ext)

load_dotenv()
TOKEN = getenv('TOKEN')
bot.run(TOKEN)