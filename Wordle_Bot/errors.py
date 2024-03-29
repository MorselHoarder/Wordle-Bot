import discord.ext.commands as cmds

from Wordle_Bot.logger import logger


class Errors(cmds.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @cmds.Cog.listener("on_command_error")
    async def on_command_error(self, ctx, error):
        if isinstance(error, cmds.CommandNotFound):
            await ctx.send("Command not found. Use `w!help` to see a list of commands.")
            return
        elif isinstance(error, cmds.MissingRequiredArgument):
            await ctx.send(
                "Missing required argument. Please check usage with `w!help`."
            )
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
        elif isinstance(error, cmds.ChannelNotReadable):
            await ctx.send(
                f"Channel '{error.argument}' is not readable. Please make sure that I have channel access."
            )
            return
        elif isinstance(error, cmds.MissingPermissions):
            await ctx.send(
                "You do not have permission to use this command. Please contact a server administrator."
            )
            return
        elif isinstance(error, cmds.BotMissingPermissions):
            await ctx.send(
                f"I do not have permission to use this command. I require the following permissions: {error.missing_perms}."
            )
            return
        elif isinstance(error, cmds.RoleNotFound):
            await ctx.send(
                f"Role '{error.argument}' not found. Please use a valid role."
            )
            return
        elif isinstance(error, cmds.MissingRole):
            await ctx.send(
                "You do not have the required role to use this command. Please contact a server administrator."
            )
            return
        elif isinstance(error, cmds.BotMissingRole):
            await ctx.send(
                f"I do not have the required role to use this command. I require the following role: {error.missing_role}."
            )
            return
        elif isinstance(error, cmds.MissingAnyRole):
            await ctx.send(
                "You do not have the required role(s) to use this command. Please contact a server administrator."
            )
            return
        elif isinstance(error, cmds.BotMissingAnyRole):
            await ctx.send(
                f"I do not have the required role(s) to use this command. I require the following role(s): {error.missing_role}."
            )
            return
        elif isinstance(error, cmds.BadArgument):
            await ctx.send("Argument syntax error. Please use a valid argument.")
            return
        elif isinstance(error, cmds.NotOwner):
            await ctx.send("Only the bot owner can use this command.")
            return

        logger.error(error, exc_info=True)
        await ctx.send(
            "An error occurred. Please contact the bot owner if this persists."
        )

    @cmds.command(hidden=True)
    @cmds.is_owner()
    async def stop(self, ctx):
        """
        Stops the event loop, killing the bot.
        """
        await ctx.send("Stopping event loop...")
        self.bot.stop()
