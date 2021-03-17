import discord

from discord.ext import commands
from discord.ext.commands import BadArgument, UserConverter


class FetchDiscordUser(UserConverter):
    """
    Converts to a `discord.User` or, if it fails, a `discord.Object`.
    Unlike the default `UserConverter`, which only does lookups via the global user cache, this
    converter attempts to fetch the user via an API call to Discord when the using the cache is
    unsuccessful.
    If the fetch also fails and the error doesn't imply the user doesn't exist, then a
    `discord.Object` is returned via the `user_proxy` converter.
    The lookup strategy is as follows (in order):
    1. Lookup by ID.
    2. Lookup by mention.
    3. Lookup by name#discrim
    4. Lookup by name
    """

    async def convert(self, ctx: commands.Context, arg: str):
        """Convert the `arg` to a `discord.User` or `discord.Object`."""
        try:
            return await super().convert(ctx, arg)
        except BadArgument:
            pass
        try:
            user_id = int(arg)
            return await ctx.bot.fetch_user(user_id)
        except ValueError:
            raise BadArgument(f"The provided argument can't be turned into integer: `{arg}`")
        except discord.HTTPException as e:
            raise BadArgument(f"User `{arg}` does not exist")