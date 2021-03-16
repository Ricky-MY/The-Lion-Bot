import discord
import random
import io
import os
import asyncio

from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # 8ball Command
    @commands.command(name="8ball")
    @commands.guild_only()
    async def _8ball(self, ctx, *, text):
        """
        Basic 8 ball command that answers your question with answers ranging from an astounding yes to an absolute no.
        """
        pos_response = ["Yes", "are you fucking mad? nah I'm playing hell yes", "indeed!",
                        "Yes, yes, yes!", "yes and thats on periodt 💅", "I'd rather not answer.", "are you a human being? (furries are not ok)",
                        "Most likely.", "An astounding yes!!!", "For sure!", "Definitely!"]
        neg_response = ["Absolutely Not.", "no <3", "That would be a hell no.", "No, Probably not.",  "You must find this out yourself, I refuse to provide you an answer.",
                        "I'm sorry but no.", "Obvvviously not-", "Are you out of yo god damn mind?, of course not lol.",
                        "Bro you messing with me, hell nah", "Stop playing with me man", "well im sorry to say but thats a fuck no ass hat"]
        text = random.choice(pos_response + neg_response)
        font = ImageFont.truetype("arial.ttf", 24)
        w, h = font.getsize(text)

        image = Image.new('RGBA', (w + 10, h + 10), (255, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.text((5, 5), text, (255, 255, 255), font=font)
        with io.BytesIO() as output:
            image.save(output, format="PNG")
            output.seek(0)
            await ctx.reply(file=discord.File(fp=output, filename="image.png"), mention_author=False)

    # Ping Command
    @commands.command(name="latency", aliases=["ping"])
    @commands.guild_only()
    async def ping(self, ctx):
        """Shows bot's latency to the discord server"""
        await ctx.send('Pong!')
        await ctx.send(f'Ping: {round(self.bot.latency * 1000)}ms')

    # Joke Command
    @commands.command(name="joke")
    @commands.guild_only()
    async def joke(self, ctx):
        """
        Sends a random joke
        """
        jokes = open("cogs/fun_cosmetics/jokes.txt", "r")
        await ctx.send(random.choice(list(jokes)))

    # Poop Command
    @commands.command(name="poop")
    @commands.guild_only()
    async def poop(self, ctx):
        """
        Pooping publicly in random places. Caution; can lead to an immediate arrests for indecent exposure
        """
        poop_gifs = open("cogs/fun_cosmetics/poop_gifs.txt", "r")
        embed = discord.Embed(description=f"Omg ewww, {ctx.author.mention} just pooped!1!",
                              color=discord.Colour.purple())
        embed.set_image(url=random.choice(list(poop_gifs)))
        await ctx.send(embed=embed)

    # Slap Command
    @commands.command(name="slap")
    @commands.guild_only()
    async def slap(self, ctx, member: discord.Member = None):
        """
        Slaps a user. If no user is mentioned, a random user is picked.
        """
        slap_gifs = open("cogs/fun_cosmetics/slap_gifs.txt", "r")
        if member is None:
            victim = random.choice(ctx.guild.members)
            rembed = discord.Embed(title='🦁 Violence is never the answer....',
                                   description=f'BUT, OH MY GOD LADIES AND GENTLEMAN 📣, THAT WAS A CLEAN SLAP TO THE RIGHT CHEEK BY {ctx.author.mention} TO 🤜 {victim.mention}. UN B E L I E V E A B L E. K/O',
                                   color=discord.Colour.purple())
            rembed.set_footer(
                text=f'{ctx.author.name} 👋 {victim.name}', icon_url=ctx.author.avatar_url)
            rembed.set_image(url=random.choice(list(slap_gifs)))
            await ctx.send(embed=rembed)
        else:
            embed = discord.Embed(title='🦁 Violence is never the answer....',
                                  description=f'BUT, OH MY GOD LADIES AND GENTLEMAN 📣, THAT WAS A CLEAN SLAP TO THE RIGHT CHEEK BY {ctx.author.mention} TO 🤜 {member.mention}. UN B E L I E V E A B L E. K/O',
                                  color=discord.Colour.purple())
            embed.set_footer(
                text=f'{ctx.author.name} 👋 {member.name}', icon_url=ctx.author.avatar_url)
            embed.set_image(url=random.choice(list(slap_gifs)))
            await ctx.send(embed=embed)

    @commands.command(name="diceroll", aliases=["roll"])
    @commands.guild_only()
    async def diceroll(self, ctx, sides=6):
        """
        A dice roll. The dice has 6 sides by default but you can still pass in sides as an argument
        """
        dice = random.randint(1, sides)
        await ctx.reply(f"🎲 {dice}", mention_author=False)

    @commands.command(name="selfban", aliases=['fakeban', 'fb', 'pb'])
    @commands.guild_only()
    async def fakeban(self, ctx, *, reason='Unspecified reason'):
        """
        Fake ban or a self ban that does not ban the user in actuality.
        """
        await ctx.send(f"🚴🔨 {ctx.author.mention} has banned themselves for {reason}, adios.")

    @commands.command(name="hug")
    @commands.guild_only()
    async def hug(self, ctx, member: discord.Member = None):
        """
        Hugs a user. If no user is mentioned, it will hug a random user.
        """
        hug_gifs = open("cogs/fun_cosmetics/hug_gifs.txt", "r")
        if member is None:
            victim = random.choice(
                [member for member in ctx.guild.members if not member.is_bot()])
            rembed = discord.Embed(title='🦁 Cutie Cupcakes!',
                                   description=f'{ctx.author.mention} had hugged {victim.mention}.🥺',
                                   color=discord.Colour.purple())
            rembed.set_footer(
                text=f'{ctx.author.name} 💕 {victim.name}', icon_url=ctx.author.avatar_url)
            rembed.set_image(url=random.choice(list(hug_gifs)))
            await ctx.send(embed=rembed)
        else:
            embed = discord.Embed(title='🦁 Cutie Cupcakes!',
                                  description=f'{ctx.author.mention} had hugged {member.mention}.🥺',
                                  color=discord.Colour.purple())
            embed.set_footer(
                text=f'{ctx.author.name} � {member.name}', icon_url=ctx.author.avatar_url)
            embed.set_image(url=random.choice(list(hug_gifs)))
            await ctx.send(embed=embed)

    @commands.command(name="kiss")
    @commands.guild_only()
    async def kiss(self, ctx, member: discord.Member):
        """
        Kisses a user. If no user is mentioned, it will kiss a random user, ouch! That might be a bit awkward.
        """
        victim = member
        kiss_gifs = open("cogs/fun_cosmetics/kiss_gifs.txt", "r")
        rembed = discord.Embed(description=f"Awww!, {ctx.author.mention} mwahed {victim.mention}!!",
                               color=discord.Colour.purple())
        rembed.set_footer(
            text=f"OMG!!, What do you do now?!,\nReact with 👋 to slap this bubble-tea lookin mfer that had just harassed you!, Or react with 💋 to spread the love {victim.name}?!")
        rembed.set_image(url=random.choice(list(kiss_gifs)))
        message = await ctx.send(embed=rembed)
        channel = ctx.channel
        await message.add_reaction('👋')
        await message.add_reaction('💋')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '👋' or str(reaction.emoji) == '💋'

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await channel.send('Reaction Timed Out')
        else:
            if reaction.emoji == '👋':
                await channel.send('~~GET SLAPPED PERV~~')
            elif reaction.emoji == '💋':
                await channel.send('~~LOVE IS IN THE AIR~~')

    @commands.command(name="rickroll", aliases=["rickroll'd"])
    @commands.guild_only()
    async def rickroll(self, ctx, member: discord.Member = None):
        """
        Sends a trustable looking link or a gif that later unveils to be a rickroll. Caution: this may cause massive emotional damage towards the victim.
        """
        rickroll = "https://media.giphy.com/media/lgcUUCXgC8mEo/giphy.gif"
        if member is None:
            victim = random.choice(ctx.guild.members)
            embed = discord.Embed(title='🦁 Rick n Roll Baby!', description=f"{victim.mention} just got rickroll'd. 🕺",
                                  color=discord.Colour.purple())
            embed.set_image(url=rickroll)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='🦁 Rick n Roll Baby!', description=f"{member.mention} just got rickroll'd. 🕺",
                                  color=discord.Colour.purple())
            embed.set_image(url=rickroll)
            await ctx.send(embed=embed)
            await member.send("You just got rickroll'd boiiiii")


def setup(bot):
    bot.add_cog(Fun(bot))
    print('Fun.cog is loaded')
