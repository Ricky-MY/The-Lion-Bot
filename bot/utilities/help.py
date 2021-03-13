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

    def usage(self, prefix, command):
        return f"{prefix}{command.name} {command.signature}"

    def get_cmd_from_cog(self, cogs):
        # sum() flattens the list
        return sorted(sum([self.bot.get_cog(cog).get_commands() for cog in cogs], []), key= lambda command: len(self.usage('p!', command)), reverse = False)

    @commands.group(name=str("help"), invoke_without_command=True)
    @commands.guild_only()
    async def help(self, ctx, module=None):
        """Main help command that shows you an index of all the modules and their respective help command."""
        if module is not None:
            embed = await self.get_cog_help(ctx, module)
            await ctx.reply(embed=embed, mention_author=False)
            return

        prefix = Prefixes.fetch_prefix(ctx.guild.id)
        embed = self.embed.copy()
        embed.description = self.prompts["main"]["desc"]
        fields = [('⚒️ Moderation', f"**[{prefix}help moderation](https://google.com \"Moderation related help\")**"),
                  ('🧰 Miscellaneous',
                   f"**[{prefix}help misc](https://google.com \"Miscellaneous commands\")**"),
                  ('🙏 Greeting',
                   f"**[{prefix}help greet](https://google.com \"Welcome and goodbye messages\")** `on the works`"),
                  ('🛡️ Aegis',
                   f"**[{prefix}help aegis](https://google.com \"Anti-nuke and security system\")** `on the works`"),
                  ('🪄 Magic',
                   f"**[{prefix}help magic](https://google.com \"Fun commands\")** `on the works`"),
                  ('✍️ TypeWriter',
                   f"**[{prefix}help typewriter](https://google.com \"Embed creation command\")** `on the works`"),
                  ('🪄 Magic', f"**[{prefix}help magic](https://google.com)**")]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=True)
        embed.set_thumbnail(
            url=self.prompts["main"]["thumbnail"])
        await ctx.send(embed=embed)

    def get_mainname(self, module):
        if module.lower() in ("mod", "moderation"):
            return "moderation"
        elif module.lower() in ("misc", "miscellaneous"):
            return "miscellaneous"
        elif module.lower() in ("magic", "fun", "games"):
            return "magic"
        return None

    async def get_cog_help(self, ctx, module):
        cogs = {"moderation": (("Moderation", "Mute", "Silent"), "⚒️ Moderation"),
                "miscellaneous": (("Misc", "TypeWriter", "Prefixes", "GetSource"), "🧰 Miscellaneous"),
                "magic": (("Fun",), "🪄 Magic")}
        module = self.get_mainname(module)
        embed = self.embed.copy()
        embed.title = cogs[module][1]
        administrative = ""
        user = ""
        commands = self.get_cmd_from_cog(cogs[module][0])
        for command in commands:
            if checks := [check for check in command.checks if check.__qualname__ != "guild_only.<locals>.predicate"]:
                administrative += f"`{self.usage(ctx.prefix, command)}`\n"
            elif not checks:
                user += f"`{self.usage(ctx.prefix, command)}`\n"
        adm_prompt = '__**[Administrative](https://google.com \"Try p!help cmd <command> to check permissions!\")**__' if administrative else ''
        usr_prompt = '__**[User](https://google.com \"Default permissions!\")**__' if user else ''
        embed.description = f"{adm_prompt}\n{administrative}\n{usr_prompt}\n{user}"
        return embed

    @help.command(name="greet", aliases=["welcomesys"])
    @commands.guild_only()
    async def greet(self, ctx):
        embed = self.embed.copy()
        embed.title = "🙏 Welcome and Goodbye messages"
        embed.description = self.prompts["greet"]["desc"]
        await ctx.reply(embed=embed, mention_author=False)

    @help.command(name="typewriter", aliases=['type', "typew"])
    @commands.guild_only()
    async def type_writer_help(self, ctx):
        embed = self.embed.copy()
        embed.title = "✍️ TypeWriter Commands"
        embed.description = "Typewriter helps you create embeds to finally package it into a channel. Use the notation `%` to divide the title and the description.\n\n__**[Threading](https://google.com \"Manage channel permissions required.\")**__\n> `advThread`\n> `thread (#channel) (decimal_color_code) (title%description)`\n> `thread preview (decimal_color_code) (title%description)`\n> `thread edit (target object) (#channel) (messageID) (value)`"
        await ctx.reply(embed=embed, mention_author=False)

    @help.command(name="command", aliases=["cmd"])
    async def command_support(self, ctx, command):
        command = self.bot.get_command(command)
        if command is not None:
            usage = f"{ctx.prefix}{command.name} {command.signature}"
            embed = self.embed.copy()
            embed.title = f"{ctx.prefix}{command}"
            embed.set_author(name="Pill's command help",
                             icon_url="https://cdn.discordapp.com/emojis/818820065834303488.png?v=1")
            embed.description = f"__**Description**__\n```{command.short_doc if command.short_doc not in (None, '') else 'Undocumented'}```\n**`p!code {command}`** to view the source code of the command.\n\n__**Usage**__\n`{usage}`"
            if aliases := command.aliases:
                embed.add_field(name="Aliases", value=", ".join(
                    aliases), inline=False)
            await ctx.reply(embed=embed, mention_author=False)
        if command is None:
            await ctx.send("command not found")

def setup(bot):
    bot.add_cog(Help(bot))
    print('Help.cog is loaded')
