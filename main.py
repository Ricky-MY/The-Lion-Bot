# The Lion Bot
# Author - Ricky
# Created at 5th of August 2020

import discord
from discord.ext import commands
import os
import json

def get_prefix(client, message):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)
	try:
		return commands.when_mentioned_or(prefixes[str(message.guild.id)])(client, message)
	except KeyError:
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		prefixes[str(message.guild.id)] = "/"
		with open('prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent=4)
		return commands.when_mentioned_or(prefixes[str(message.guild.id)])(client, message)

def botAdminCheck(ctx):
	return ctx.message.author.id == 368671236370464769

intents = discord.Intents.default()
intents.reactions = True
intents.members = True

client = commands.Bot(command_prefix=get_prefix, intents = intents)
client.remove_command('help')

# Shut Down Command
@client.command(name="shutdown")
@commands.guild_only()
@commands.check(botAdminCheck)
async def shutdown(ctx):
	await ctx.send('Bot has been shut down.')
	await client.logout()


@client.event
async def on_ready():
	print("________________________________________________________________________________________________________________________\nThe Lion bot is on standby\n________________________________________________________________________________________________________________________")
	await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game("Gerald's game >:)"))


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

THIS_MA_TOKEN_HEHE = open('THIS_MA_TOKEN_HEHE.txt', 'r').readline()
client.run(THIS_MA_TOKEN_HEHE)
