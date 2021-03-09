import discord
from discord.ext import commands
import sqlite3

class Tags(commands.Cog):

	def __init__(self, client):
		self.client = client
	def botAdminCheck(ctx):
		return ctx.message.author.id == 368671236370464769

	@commands.group(name="gtag", aliases=["gt", "globtag"], invoke_without_command=True)
	async def global_tags(self, ctx, name):
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute("SELECT content FROM global_tags WHERE name = ?", (name,))
		result = cursor.fetchone()
		if name == 'fucking_village':
			await ctx.send(result[0])
		else:
			embed=discord.Embed(title=f"Tag : {name}", description=result[0], color = 0x778899)
			await ctx.send(embed=embed)
		cursor.close()
		db.close()
	@global_tags.command()
	@commands.check(botAdminCheck)
	async def add(self, ctx, name, *, content):
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		sql = ("INSERT INTO global_tags(name, content) VALUES (?, ?)")
		val = (name, content)
		cursor.execute(sql, val)
		embed=discord.Embed(title=f"Success!", description=f"Name:{name}\nContent:{content}", colour=discord.Colour.dark_teal())
		await ctx.send(embed=embed)
		db.commit()
		cursor.close()
		db.close()
		
	@global_tags.command()
	@commands.check(botAdminCheck)
	async def remove(self, ctx, name):
		db = sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute("DELETE FROM global_tags WHERE name = ?", (name,))
		embed=discord.Embed(title=f"Success!", description=f"Successfully removed {name} tag.", colour=discord.Colour.dark_teal())
		await ctx.send(embed=embed)
		db.commit()
		cursor.close()
		db.close()


def setup(client):
	client.add_cog(Tags(client))
	print('Tags.cog is loaded')
