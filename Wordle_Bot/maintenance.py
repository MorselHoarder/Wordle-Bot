import discord
import discord.ext.commands as cmds

from Wordle_Bot.logger import logger


class Maintenance(cmds.Cog):
    """These help you set up the bot."""

    def __init__(self, bot) -> None:
        self.bot = bot

    @cmds.command(name="refreshglobal", hidden=True)
    @cmds.is_owner()
    async def refresh_global(self, ctx, wipe_scores=False):
        """
        Globally recounts scores across all servers and tracked channels.
        """
        await ctx.send("Globally refreshing scores. This may take a few minutes...")
        await self.bot.refresh_scores(wipe_scores)
        await ctx.send("Scores refreshed.")

    @cmds.command(name="refresh", aliases=["rf"])
    async def refresh_all_channels(self, ctx):
        """
        Recounts the scores for all tracked channels in the server.
        Equivalent to calling 'w!rfch' for each channel.
        """
        await ctx.send("Refreshing scores for this server...")
        await self.bot.refresh_server(ctx.guild)
        await ctx.send("Scores refreshed.")

    @cmds.command(name="refreshch", aliases=["rfch", "refreshchannel"])
    async def refresh_channel(self, ctx, channel: discord.TextChannel):
        """
        Recounts scores for a specified tracked channel.
        Use this when you need to add scores from a new channel.
        """
        await ctx.send(
            f"Refreshing score count in #{channel.name}. This may take a minute..."
        )
        await self.bot.refresh_channel(channel)
        await ctx.send("Scores refreshed.")

    @cmds.command(name="addch", aliases=["addchannel"])
    async def add_channel(self, ctx, channel: discord.TextChannel):
        """
        Adds a text channel to the list of channels that track wordle scores.
        This must be done before the bot can track wordle scores in the channel.
        Best practice is to have a channel just for #wordle, but multiple channels is fine.
        """
        if self.bot.is_channel_tracked(channel):
            await ctx.send("Channel already added.")
            return

        self.bot.track_channel(channel)
        await ctx.send(f"Added channel '#{channel.name}'.")

    @cmds.command(name="remch", aliases=["removech"])
    async def remove_channel(self, ctx, channel: discord.TextChannel):
        """
        Removes a text channel from the list of tracked channels.
        """
        if not self.bot.channels_tracked(ctx):
            await ctx.send("No channels are being tracked.")
            return

        if not self.bot.is_channel_tracked(channel):
            await ctx.send("Channel not in list.")
            return

        self.bot.untrack_channel(channel)
        await ctx.send(f"Removed channel '#{channel.name}'.")

    @cmds.command(name="chlist", aliases=["chl"])
    async def channel_list(self, ctx):
        """
        Displays the list of tracked channels.
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

    @cmds.command(name="setup")
    async def setup_instructions(self, ctx):
        """
        Displays intructions for how to set up the bot for use in your server.
        """
        e = discord.Embed(
            title="Setup Instructions",
            color=discord.Color.gold(),
            description="Follow these steps to set up the bot:",
        )
        e.add_field(
            name="1) Track channels",
            value="> Track the channels that have, or will contain, Wordle scores. Use `w!addch [channel]` to add a channel. You may want to make a #wordle channel to contain the score spam if you haven't already.",
            inline=False,
        )
        e.add_field(
            name="2) Refresh scores",
            value="> Use `w!refresh` to refresh the bot's cache of Wordle scores. Once the bot is finished refreshing, you're done!\n ",
            inline=False,
        )
        e.set_footer(
            text="\nPosting a Wordle score in a tracked channel automatically adds it to the bot's cache.\n\nRefreshing a tracked channel accesses the channel's history and checks for Wordle scores. If the history is extensive this operation can take a while, which is why limiting this access to a few tracked channels is recommended."
        )
        await ctx.send(embed=e)
