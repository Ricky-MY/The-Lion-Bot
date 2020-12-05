import socialblade
import discord, random
from discord.ext import commands
from socialblade import YouTubeChannel
import traceback
import asyncio
import datetime
import csv
from datetime import datetime
import locale

class SocialBlade(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command(name="subcount", aliases=["sc", "socialblade"])
	async def sub_count(self, ctx, youtube_channel):
		youtube_channel = YouTubeChannel(youtube_channel)
		await ctx.send(youtube_channel.get_subscriber_count())

def setup(client):
	client.add_cog(SocialBlade(client))
	print('SocialBlade.cog loaded')
