import discord
import discord.ext.commands as cmds

from Wordle_Bot.logger import logger


class Maintenance(cmds.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @cmds.Cog.listener("on_ready")
    async def load_all_scores(self):
        logger.info("Loading scores...")
        await self.bot.refresh_scores()
        logger.info("Scores refreshed. Bot ready.")

    @cmds.command(hidden=True)
    async def refresh_global(self, ctx, wipe_scores=False):
        """
        Refreshes the scores for the current server.
        """
        await ctx.send("Globally refreshing scores. This may take a few minutes...")
        await self.refresh_scores(wipe_scores)
        await ctx.send("Scores refreshed.")

    @cmds.command(name="rf", aliases=["refresh"])
    async def refresh(self, ctx, channel: discord.TextChannel):
        """
        Refreshes the scores count for a channel.
        """
        await ctx.send(
            f"Refreshing score count in #{channel.name}. This may take a minutes..."
        )
        await self.bot.refresh_channel(channel)
        await ctx.send("Scores refreshed.")

    @cmds.command(name="addch", aliases=["addchannel"])
    async def addchannel(self, ctx, channel: discord.TextChannel):
        """
        Adds a text channel to the list of channels to track wordle scores in.
        This must be done before the bot can track wordle scores in the channel.
        Best practice is to have a channel just for #wordle, but multiple channels is fine.
        """
        if self.bot.is_channel_tracked(channel):
            await ctx.send("Channel already added.")
            return

        self.bot.track_channel(channel)
        await ctx.send(f"Added channel {ctx.channel.name}.")

    @cmds.command(name="remch", aliases=["removech"])
    async def removechannel(self, ctx, channel: discord.TextChannel):
        """
        Removes a text channel from the list of channels to track wordle scores in.
        """
        if not self.bot.is_channel_tracked(channel):
            await ctx.send("Channel not in list.")
            return

        self.bot.untrack_channel(channel)
        await ctx.send(f"Removed channel {ctx.channel.name}.")

    @cmds.command(name="chl", aliases=["chlist"])
    async def channel_list(self, ctx):
        """
        Displays the list of channels to track wordle scores in.
        """
        if not self.bot.channels_tracked(ctx):
            await ctx.send("No channels are being tracked.")
            return

        await ctx.send(
            "```\n"
            + "\n".join(
                [f"#{channel.name}" for channel in self.bot.channels_tracked(ctx)]
            )
            + "```"
        )
