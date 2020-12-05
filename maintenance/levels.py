import discord
import random
import asyncio
import datetime
from discord.ext import commands
import math
import sqlite3

class Levelling(commands.Cog):

	def __init__(self, client):
		self.client=client

	@commands.Cog.listener()
	async def on_message(self, message):
		db =  sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT user_id FROM levels WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
		result = cursor.fetchone()
		if result is None:
			sql = ("INSERT INTO levels(guild_id, user_id, xp, lvl) VALUES(?,?,?,?)")
			val = (message.guild.id, message.author.id, 0, 0)
			cursor.execute(sql, val)
			db.commit()
			cursor.close()
			db.close()
		elif result[0] == '717784768216957108':
			cursor.execute(f"DELETE FROM levels WHERE user_id =717784768216957108")
			db.commit()
			cursor.close()
			db.close()
		else:
			cursor.execute(f"SELECT user_id, xp, lvl FROM levels WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
			result = cursor.fetchone()
			xp = int(result[1])
			sql = ("UPDATE levels SET xp = ? WHERE guild_id = ? and user_id = ?")
			val = (xp+2, str(message.guild.id), str(message.author.id))
			cursor.execute(sql, val)
			db.commit()

			cursor.execute(f"SELECT user_id, xp, lvl FROM levels WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
			result2 = cursor.fetchone()

			xp_start = int(result2[1])
			lvl_start = int(result2[2])
			xp_check = math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100)
			if xp_check < xp_start:
				await message.channel.send(f'Hoooray!! {message.author.mention} has leveled up to level {lvl_start+1}')
				sql = ("UPDATE levels SET lvl = ? WHERE guild_id = ? and user_id = ?")
				val = (int(lvl_start + 1), str(message.guild.id), str(message.author.id))
				cursor.execute (sql, val)
				db.commit()
				sql = ("UPDATE levels SET xp = ? WHERE guild_id = ? and user_id = ?")
				val = (0, str(message.guild.id), str(message.author.id))
				cursor.execute (sql, val)
				db.commit()
				cursor.close()
				db.close()

	@commands.group(invoke_without_command=True)
	async def level(self, ctx, user: discord.User= None):
		db =  sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		sql = (f"INSERT INTO levels(guild_id) VALUES(?)")
		val = {ctx.guild.id}
		cursor.execute(sql, var)
		db.commit()
		cursor.close()
		db.close()
	@level.command()
	async def rank(self, ctx, user: discord.User= None):
		if user is not None:
			db =  sqlite3.connect('main.sqlite')
			cursor = db.cursor()
			cursor.execute(f"SELECT user_id, xp, lvl FROM levels WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{user.id}'")
			result = cursor.fetchone()
			if result is None:
				await ctx.send('That user is not yet ranked')
			else:
				await ctx.send(f"{user.name} is currently level '{str(result[2])}' and has '{str(result[1])}' xp.")
			cursor.close()
			db.close()
		elif user is None:
			db =  sqlite3.connect('main.sqlite')
			cursor = db.cursor()
			cursor.execute(f"SELECT user_id, xp, lvl FROM levels WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
			result = cursor.fetchone()
			if result is None:
				await ctx.send('That user is not yet ranked')
			else:
				await ctx.send(f"{ctx.message.author.name} is currently level '{str(result[2])}' and has '{str(result[1])}' xp.")
			cursor.close()
			db.close()

	@level.command()
	async def reset(self, ctx, user: discord.User= None):
		db =  sqlite3.connect('main.sqlite')
		cursor = db.cursor()
		result = cursor.fetchone()
		cursor.close()
		db.close()
def setup(client):
	client.add_cog(Levelling(client))
	print('Levelling.cog loaded')
