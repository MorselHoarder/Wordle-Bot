import discord
import discord.ext.commands as cmds

from Wordle_Bot.logger import logger


class Listeners(cmds.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @cmds.Cog.listener("on_ready")
    async def load_all_scores(self):
        logger.info("Loading scores...")
        await self.bot.refresh_scores()
        logger.info("Scores refreshed. Bot ready.")

    @cmds.Cog.listener("on_message")
    async def check_new_message(self, message: discord.Message):
        if self.bot.is_channel_tracked(message.channel):
            self.bot.check_for_wordle(message)

    @cmds.Cog.listener("on_message_edit")
    async def check_edited_message(
        self, before: discord.Message, after: discord.Message
    ):
        if self.bot.is_channel_tracked(after.channel):
            self.bot.check_for_wordle(after)

    @cmds.Cog.listener("on_message_delete")
    async def check_deleted_message(self, message: discord.Message):
        if self.bot.is_channel_tracked(message.channel):
            self.bot.check_for_wordle_removed(message)

    @cmds.Cog.listener("on_guild_join")
    async def check_guild_join(self, guild: discord.Guild):
        self.bot.track_guild(guild)

    @cmds.Cog.listener("on_guild_remove")
    async def check_guild_remove(self, guild: discord.Guild):
        self.bot.untrack_guild(guild)

    @cmds.Cog.listener("on_guild_channel_delete")
    async def check_guild_channel_delete(self, channel: discord.TextChannel):
        print("untrack channel")
        if self.bot.is_channel_tracked(channel):
            self.bot.untrack_channel(channel)
