import discord
import yaml

from discord.ext import commands

from bot.utilities.prefixes import Prefixes


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open("config.yaml", 'r') as file:
            config = yaml.load(file, Loader=yaml.SafeLoader)
        self.color = config["asthetics"]["mainColor"]

        with open(config["directories"]["prompts"], encoding="utf-8") as file:
            self.prompts = yaml.load(file, Loader=yaml.SafeLoader)["help"]
        self.embed = discord.Embed(color=self.color)
        self.embed.set_author(
            name="Pill's help menu", icon_url=self.prompts["main"]["author_url"])
        self.embed.set_footer(
            text="Type p!help cmd <command> for an in-depth command help")

    @commands.group(name=str("help"), invoke_without_command=True)
    @commands.guild_only()
    async def help(self, ctx):
        prefix = Prefixes.fetch_prefix(ctx.guild.id)
        embed = self.embed.copy()
        embed.description = self.prompts["main"]["desc"]
        fields = [('⚒️ Moderation', f"**[{prefix}help moderation](https://google.com \"Moderation related help\")**"),
                  ('🧰 Miscellaneous',
                   f"**[{prefix}help misc](https://google.com \"Miscellaneous commands\")**"),
                  ('🙏 Greeting',
                   f"**[{prefix}help greet](https://google.com \"Welcome and goodbye messages\")**"),
                  ('🛡️ Aegis',
                   f"**[{prefix}help aegis](https://google.com \"Anti-nuke and security system\")**"),
                  ('🛑 Tag',
                   f"**[{prefix}help tag](https://google.com \"Global and guild tags\")**"),
                  ('✍️ TypeWriter',
                   f"**[{prefix}help typewriter](https://google.com \"Embed creation command\")**"),
                  ('🪄 Magic', f"**[{prefix}help magic](https://google.com)**")]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=True)
        embed.set_thumbnail(
            url=self.prompts["main"]["thumbnail"])
        await ctx.send(embed=embed)

    @help.command(name="moderation")
    @commands.guild_only()
    async def moderation(self, ctx):
        embed = self.embed.copy()
        embed.title = "⚒️ Moderation"
        embed.description = self.prompts["moderation"]["desc"]
        await ctx.reply(embed=embed, mention_author=False)

    @help.command(name="magic")
    @commands.guild_only()
    async def magic(self, ctx):
        embed = self.embed.copy()
        embed.title = "🪄 Magic"
        embed.description = self.prompts["magic"]["desc"]
        await ctx.reply(embed=embed, mention_author=False)

    @help.command(name="misc")
    @commands.guild_only()
    async def misc(self, ctx):
        embed = self.embed.copy()
        embed.title = "🧰 Miscellaneous"
        lines = self.prompts["misc"]["body"]
        embed.description = '\n'.join(lines)
        await ctx.reply(embed=embed, mention_author=False)

    @help.command(name="greet")
    @commands.guild_only()
    async def greet(self, ctx):
        embed = self.embed.copy()
        embed.title = "🙏 Welcome and Goodbye messages"
        embed.description = self.prompts["greet"]["desc"]
        await ctx.reply(embed=embed, mention_author=False)

    @help.command(name="tag")
    @commands.guild_only()
    async def tag(self, ctx):
        embed = self.embed.copy()
        embed.title = '🛑 Tag Commands'
        embed.add_field(name="Global tags",
                        value="`globtag (name)`", inline=False)
        embed.add_field(
            name="Local tags", value="__**[Setup](https://google.com \"Manage server permissions required.\")**__\n`tag add (name) (content)`\n`tag remove (name)`\n\n__**[User](https://google.com \"Default permissions.\")**__\n`tag (name)`", inline=False)
        await ctx.reply(embed=embed, mention_author=False)

    @help.command(name="typewriter", aliases=['tw'])
    @commands.guild_only()
    async def type_writer_help(self, ctx):
        embed = self.embed.copy()
        embed.title = "✍️ TypeWriter Commands"
        embed.description = "Typewriter helps you create embeds to finally package it into a channel. Use the notation `%` to divide the title and the description.\n\n__**[Threading](https://google.com \"Manage channel permissions required.\")**__\n> `advThread`\n> `thread (#channel) (decimal_color_code) (title%description)`\n> `thread preview (decimal_color_code) (title%description)`\n> `thread edit (target object) (#channel) (messageID) (value)`"
        await ctx.reply(embed=embed, mention_author=False)

    @help.command(name="reactionrole", aliases=["rr"])
    @commands.guild_only()
    async def rrole(self, ctx):
        prefix = Prefixes.fetch_prefix(ctx.guild.id)
        embed = discord.Embed(title='=Reaction Role Guide=', color=self.color)
        embed.add_field(name='Setup',
                        value=f"`{prefix}rrole (#channel) (message_id) (emoji) (@role)`\nThis command allows you to setup reactionroles\n(#channel) : _Mention the channel where the message with reactionrole will be_\n(message_id) : _Insert the message ID of the message you'd like people to react to, to get roles_\n(emoji) : _The emoji people would react with to get the role mentioned_\n(@role) : _The role people would get when reacted with the set emoji_")
        embed.add_field(name='Check',
                        value=f'`{prefix}rrole check`\n Checks all reaction role objects for your server')
        embed.add_field(name='Clear',
                        value=f'`{prefix}welcome clear (message_id)`\n Clear all reaction role objects corresponding to the message ID')
        await ctx.reply(embed=embed, mention_author=False)

    @help.command(name="command", aliases=["cmd"])
    async def command_support(self, ctx, command):
        command = self.bot.get_command(command)
        if command is not None:
            embed = self.embed.copy()
            embed.title = f"{ctx.prefix}{command}"
            embed.set_author(name="Pill's command help",
                             icon_url="https://cdn.discordapp.com/emojis/818820065834303488.png?v=1")
            embed.description = f"__**Description**__\n```{command.short_doc if command.short_doc not in (None, '') else 'Undocumented'}```\n**`p!code {command}`** to view the source code of the command.\n\n__**Usage**__\n`{ctx.prefix}{command.name}{command.signature}`"
            if aliases := command.aliases:
                embed.add_field(name="Aliases", value=", ".join(
                    aliases), inline=False)
            await ctx.reply(embed=embed, mention_author=False)
        if command is None:
            await ctx.send("command not found")


def setup(bot):
    bot.add_cog(Help(bot))
    print('Help.cog is loaded')
