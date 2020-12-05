import discord, random
from discord.ext import commands
from discord.ext.commands import Cog
import json


class SEEvents(Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(guild.id)] = '/'
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id))
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        print(guild.id)
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute("DELETE FROM welcome WHERE guild_id = ?", (guild.id,))
        cursor.execute("DELETE FROM member_count_channel WHERE guild_id = ?", (guild.id,))
        cursor.execute("DELETE FROM levels WHERE guild_id = ?", (guild.id,))
        cursor.execute("DELETE FROM rrole WHERE guild_id = ?", (guild.id,))
        db.commit()
        cursor.close()
        db.close()
        print("Record Removed")


def setup(client):
    client.add_cog(SEEvents(client))
    print('start_end_events.cog is loaded')
