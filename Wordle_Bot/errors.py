import discord
import discord.ext.commands as cmds

from Wordle_Bot.logger import logger


class Errors(cmds.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @cmds.Cog.listener("on_command_error")
    async def on_command_error(self, ctx, error):
        if isinstance(error, cmds.CommandNotFound):
            await ctx.send("Command not found. Please use a valid command.")
            return
        elif isinstance(error, cmds.MissingRequiredArgument):
            await ctx.send("Missing required argument. Please check usage with w!help.")
            return
        elif isinstance(error, cmds.MemberNotFound):
            await ctx.send(
                f"Cannot find member '{error.argument}'. Try spelling with the correct case, use their full username, or use a mention."
            )
            return
        elif isinstance(error, cmds.ChannelNotFound):
            await ctx.send(
                f"Channel '{error.argument}' not found. Please use a valid channel."
            )
            return
        elif isinstance(error, cmds.BadArgument):
            await ctx.send("Argument syntax error. Please use a valid argument.")
            return
        elif isinstance(error, cmds.NotOwner):
            await ctx.send("Only the bot owner can use this command.")
            return

        logger.error(error)
        await ctx.send(
            "An error occurred. Please contact the bot owner if this persists."
        )
