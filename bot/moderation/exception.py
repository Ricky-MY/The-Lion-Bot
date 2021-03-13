import discord
import traceback
import sys
import yaml

from discord.ext import commands
from discord import errors

from bot.moderation.admin import bot_admin_check

class ExceptionHandler(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        with open("config.yaml", 'r') as file:
            config = yaml.load(file, Loader=yaml.SafeLoader)
        self.color = config["asthetics"]["mainColor"]
        self.error_color = config["asthetics"]["errorColor"]
        self.help_channel = config["moderation"]["helpChannel"]
        self.debug_mode = False

    async def raise_norm(self, ctx, error):
        if self.debug_mode:
            report = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
            embed = discord.Embed(title='🖐️ Unhandled exception...', description=f"```py\n{report + '```' if len(report) < 2000 else report[-2000:] + f'``` and {len(report) - 2000} more characters...'}", color=discord.Color.dark_grey())
            embed.add_field(name="Error", value=f"```{error}```")
            if bot_admin_check(ctx):
                await ctx.reply(embed=embed)
            elif not bot_admin_check(ctx):
                channel = self.bot.get_channel(int(self.help_channel))
                embed.set_footer(text=f"Command {ctx.command.name} used by {ctx.author.name}#{ctx.author.discriminator} in {ctx.guild.name}")
                await channel.send(embed=embed)
            return
        print(f'Ignoring exception in command {ctx.command}:')
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_usage(self, ctx):
        return f'{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}'

    @commands.command(name = "debug", aliases=['d'])
    @commands.check(bot_admin_check)
    async def enable_debug(self, ctx):
        """Redirect tracebacks from the console to the channel of which the command that caused the error was invoked in."""
        self.debug_mode = not self.debug_mode
        await ctx.reply(f"Debug mode is turned {'on' if self.debug_mode else 'off'}", mention_author = False)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound)
        error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'⚠️ {ctx.command} has been disabled.')

        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'⚠️ {str(ctx.command).upper()} cannot be used in Private Messages.')
            except discord.HTTPException:
                pass

        if isinstance(error, errors.Forbidden):
            embed = discord.Embed(title='🖐️ Hold it...', description=f"⁉️ Required permission is missing or unattainable.", color=self.error_color)
            embed.set_footer(text="Unable to carry out this task.")
            await ctx.send(embed=embed)

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="⚠️ Unable to proceed...", description=f"Vital argument `{error.param.name}` is missing.", color=self.error_color)
            embed.set_footer(text=self.get_usage(ctx))
            await ctx.send(embed=embed)
        
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"🖐️ Cooldown for {round(error.cooldown.per)} seconds!")

        else:
            if ctx.command.qualified_name.lower() in ('reload', 'unload', 'load'):
                if isinstance(error, commands.ExtensionNotFound):
                    await ctx.send("⚠️ Extension is not found.")
                elif isinstance(error, commands.ExtensionNotLoaded):
                    await ctx.send("⚠️ Extension is not loaded.")
                elif isinstance(error, commands.ExtensionAlreadyLoaded):
                    await ctx.send("⚠️ Extension has been already loaded.")
                else:
                    await self.raise_norm(ctx, error)

            elif cog.qualified_name in ('Verifier', 'Authenticator'):
                if isinstance(error, commands.BadArgument):
                    embed = discord.Embed(title="⚠️ Unable to proceed...", description=f"I cannot find the user specified.", color=self.error_color)
                    embed.set_footer(text=self.get_usage(ctx))
                    await ctx.send(embed=embed)
                else:
                    await self.raise_norm(ctx, error)
            elif ctx.command.qualified_name in ('kick', 'ban', 'mute'):
                if isinstance(error, commands.BadArgument):
                    embed = discord.Embed(title='⚠️ Unable to proceed...', description=f"I cannot find the user specified.", color=self.error_color)
                    embed.set_footer(text=self.get_usage(ctx))
                    await ctx.send(embed=embed)
                else:
                    await self.raise_norm(ctx, error)
            else:
                await self.raise_norm(ctx, error)

def setup(bot):
    bot.add_cog(ExceptionHandler(bot))
    print('Exception handler is loaded')

