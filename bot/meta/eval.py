import discord
import time
import re
import aiohttp
import yaml

from signal import Signals

from discord.ext import commands

FORMATTED_CODE_REGEX = re.compile(
    # code delimiter: 1-3 backticks; (?P=block) only matches if it's a block
    r"(?P<delim>(?P<block>```)|``?)"
    # if we're in a block, match optional language (only letters plus newline)
    r"(?(block)(?:(?P<lang>[a-z]+)\n)?)"
    # any blank (empty or tabs/spaces only) lines before the code
    r"(?:[ \t]*\n)*"
    r"(?P<code>.*?)"                        # extract all code inside the markup
    # any more whitespace before the end of the code markup
    r"\s*"
    # match the exact same delimiter from the start again
    r"(?P=delim)",
    # "." also matches newlines, case insensitive
    re.DOTALL | re.IGNORECASE
)
RAW_CODE_REGEX = re.compile(
    # any blank (empty or tabs/spaces only) lines before the code
    r"^(?:[ \t]*\n)*"
    r"(?P<code>.*?)"                        # extract all the rest as code
    # any trailing whitespace until the end of the string
    r"\s*$",
    re.DOTALL                               # "." also matches newlines
)


class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.jobs = {}
        with open("config.yaml", 'r') as file:
            config = yaml.load(file, Loader=yaml.SafeLoader)
        with open(config["directories"]["prompts"], encoding="utf-8") as file:
            self.prompts = yaml.load(file, Loader=yaml.SafeLoader)["help"]
        self.icon_url = self.prompts["main"]["author_url"]
        self.color = config["asthetics"]["mainColor"]
        self.error_color = config["asthetics"]["errorColor"]

    async def upload_output(self, output: str) -> str:
        data = bytes(output, 'utf-8')
        async with aiohttp.ClientSession() as cs:
            async with cs.post('https://mystb.in/documents', data = data) as r:
                res = await r.json(content_type="application/json")
                key = res["key"]
        return f'https://mystb.in/{key}'

    def clean_code(self, content: str) -> str:
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:][:-3])

        return content

    async def post_eval(self, code: str) -> dict:
        """Send a POST request to the Snekbox API to evaluate code and return the results."""
        url = "http://localhost:8060/eval"
        data = {"input": code}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, raise_for_status=True) as resp:
                return await resp.json()

    def get_results_message(self, results: dict):
        """Return a user-friendly message and error corresponding to the process's return code."""

        stdout, returncode = results["stdout"], results["returncode"]
        msg = f"Your eval job has completed with return code {returncode}"
        error = ""

        if returncode is None:
            msg = "Your eval job has failed"
            error = stdout.strip()
        elif returncode == 128 + 9:
            msg = "Your eval job timed out or ran out of memory"
        elif returncode == 255:
            msg = "Your eval job has failed"
            error = "A fatal NsJail error occurred"
        else:
            # Try to append signal's name if one exists
            try:
                name = Signals(returncode - 128).name
                msg = f"{msg} ({name})"
            except ValueError:
                pass

        return msg, error, returncode

    async def format_output(self, output: str):
        """
        Format the output and return a tuple of the formatted output and a URL to the full output.
        Prepend each line with a line number. Truncate if there are over 10 lines or 1000 characters
        and upload the full output to a paste service.
        """

        output = output.rstrip("\n")
        original_output = output  # To be uploaded to a pasting service if needed
        paste_link = None

        if "<@" in output:
            output = output.replace("<@", "<@\u200B")  # Zero-width space

        if "<!@" in output:
            output = output.replace("<!@", "<!@\u200B")  # Zero-width space

        truncated = False
        lines = output.count("\n")

        if lines > 0:
            output = [f"{i:03d} | {line}" for i,
                      line in enumerate(output.split('\n'), 1)]
            output = output[:11]  # Limiting to only 11 lines
            output = "\n".join(output)

        if lines > 10:
            truncated = True
            if len(output) >= 1000:
                output = f"{output[:1000]}\n... (truncated - too long, too many lines)"
            else:
                output = f"{output}\n... (truncated - too many lines)"
        elif len(output) >= 1000:
            truncated = True
            output = f"{output[:1000]}\n... (truncated - too long)"

        if truncated:
            paste_link = await self.upload_output(original_output)

        output = output or "[No output]"

        return output, paste_link

    def prepare_input(self, code: str) -> str:
        """
        Extract code from the Markdown, format it, and insert it into the code template.
        If there is any code block, ignore text outside the code block.
        Use the first code block, but prefer a fenced code block.
        If there are several fenced code blocks, concatenate only the fenced code blocks.
        """
        if match := list(FORMATTED_CODE_REGEX.finditer(code)):
            blocks = [block for block in match if block.group("block")]

            if len(blocks) > 1:
                code = '\n'.join(block.group("code") for block in blocks)
                info = "Several code blocks detected"
            else:
                match = match[0] if len(blocks) == 0 else blocks[0]
                code, block, lang, delim = match.group(
                    "code", "block", "lang", "delim")
                if block:
                    info = (
                        f"Formatted code block")
                else:
                    info = f"{delim}-enclosed inline code"
        else:
            code = RAW_CODE_REGEX.fullmatch(code).group("code")
            info = "Unformatted or badly formatted code, refer to p!gtag markdown"

        return code, info

    async def send_eval(self, ctx, code, info):
        """
        Evaluate code, format it, and send the output to the corresponding channel.
        Return the bot response.
        """
        async with ctx.typing():
            results = await self.post_eval(code)
            msg, error, returncode = self.get_results_message(results)

            if error:
                output, paste_link = error, None
            else:
                output, paste_link = await self.format_output(results["stdout"][-600:])
            now = time.time()
            description=f"{msg}.\n\n```\n{output}\n```"
            embed = discord.Embed(title=f"Finished in {round(now - self.jobs[ctx.author.id])} seconds",
                                  color=self.color if returncode == 0 else self.error_color)
            embed.set_author(
                name=f"Carried out{ctx.author.display_name}'s eval", icon_url=self.icon_url)
            embed.set_footer(text=info)
            if paste_link:
                description += f"Full output is **[here]({paste_link})**."
            embed.description = description
            response = await ctx.reply(embed=embed)
        if response:
            return True
        elif not response:
            return False

    @commands.command(name="eval", aliases=["e", "exe"])
    @commands.cooldown(1, 3, type=commands.BucketType.user)
    async def _eval(self, ctx, *, code):
        """
        Runs python code provided in a sandbox and returns the value. 
        """
        self.jobs[ctx.author.id] = time.time()
        code, info = self.prepare_input(code)
        try:
            await self.send_eval(ctx, code, info)
        finally:
            try:
                del self.jobs[ctx.author.id]
            except KeyError:
                pass


def setup(bot):
    bot.add_cog(Eval(bot))
    print('Eval.cog is loaded')
