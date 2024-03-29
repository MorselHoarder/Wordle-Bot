import os
import re
import statistics as stats
import json
import datetime as dt

import asyncpg

import discord
from discord.ext.commands import Bot

from Wordle_Bot.logger import logger

CHANNELS_JSON_FILE = "channels.json"
WORDLE_PATTERN = re.compile(r"\bWordle (\d+) (\d|X)/\d\n")
EARLIEST_WORDLE_DATE = dt.datetime(2021, 6, 17)


class WordleBot(Bot):
    """
    The Wordle Bot.

    Connects to a PostgreSQL database with the following structure:

    CREATE TABLE guilds (
        guild_id numeric PRIMARY KEY,
        channel_ids numeric[]
    )

    CREATE TABLE $(channel_id) (
        user_id numeric PRIMARY KEY,
        ???
    )
    This table stores each guild's tracked channel ids.
    Server admins determine what channels are tracked.

    For each tracked channel, the bot will create a table:
    # TODO add member_IDs somewhere
    CREATE TABLE $(channel_id) (
        day integer PRIMARY KEY,
        score smallint,
        DNF boolean,
        message_id numeric,
    )

    Scores structure: Dict of Dicts
    {
        Member_ID: {
            Wordle_day: score
        }
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scores = {}
        self.initialized = False

    async def init_db(self):
        """
        Initializes a connection pool for the PostgreSQL database.
        """
        self.db = await asyncpg.create_pool(
            host=os.environ["PG_HOSTNAME"],
            user=os.environ["PG_USERNAME"],
            password=os.environ["PG_PASSWORD"],
            database=os.environ["PG_DATABASE"],
        )

    async def start(self, *args, **kwargs):
        """
        Reimplement the start method to run the init_db method.
        """
        await self.init_db()
        await super().start(*args, **kwargs)

    async def refresh_scores(self, wipe_scores=False):
        """
        Refreshes the scores dict. This is a global function, so it will refresh all scores.
        """
        if not self.initialized:
            self._load_channel_ids()

        if wipe_scores:
            self.scores = {}

        for guild in self.guilds:
            await self.refresh_server(guild)

        if not self.initialized:
            self.initialized = True

    async def refresh_server(self, guild: discord.Guild):
        """
        Refreshes the scores dict for the server.
        """
        for channel in guild.text_channels:
            await self.refresh_channel(channel)

    async def refresh_channel(self, channel: discord.TextChannel):
        """
        Refreshes the scores dict for the channel.
        """
        if not self.guild_is_tracked(channel.guild):
            self.track_guild(channel.guild)
        if channel.id in self.channel_ids_list[channel.guild.id]:
            async for message in channel.history(
                limit=None, after=EARLIEST_WORDLE_DATE
            ):
                self.check_for_wordle(message)

    def check_for_wordle(self, message: discord.Message):
        """
        Checks if the message is a Wordle. If so, adds the scores to the score dict.
        """
        if m := WORDLE_PATTERN.search(message.content):
            day = int(m.group(1))
            score = int(m.group(2)) if m.group(2) != "X" else 7
            if message.author.id not in self.scores:
                self.scores[message.author.id] = {}
            self.scores[message.author.id][day] = score

    def check_for_wordle_removed(self, message: discord.Message):
        """
        Checks if the message is a wordle. If so, attempts to remove the score from the scores dict.
        """
        if m := WORDLE_PATTERN.search(message.content):
            day = int(m.group(1))
            if (
                message.author.id in self.scores
                and day in self.scores[message.author.id]
            ):
                del self.scores[message.author.id][day]

    def get_average_wordle_score(self, member: discord.Member):
        """
        Returns the average wordle score of the member.
        """
        return (
            round(stats.mean(self.scores[member.id].values()), 2)
            if member.id in self.scores
            else "N/A"
        )

    def get_wordles_completed(self, member: discord.Member):
        """
        Returns the number of completed wordles of the member.
        """
        return len(self.scores[member.id]) if member.id in self.scores else 0

    def channels_tracked(self, ctx: discord.ext.commands.Context):
        """
        Returns a list of tracked channel names in the current server.
        """
        if not self.guild_is_tracked(ctx.guild):
            return []

        channels = []
        for channel_id in self.channel_ids_list[ctx.guild.id]:
            channel = discord.utils.get(ctx.guild.text_channels, id=channel_id)
            if channel is not None:
                channels.append(channel.name)

        return channels

    def is_channel_tracked(self, channel: discord.TextChannel):
        """
        Checks if the channel is in the channel ids list.
        """
        if not self.guild_is_tracked(channel.guild):
            return False
        return channel.id in self.channel_ids_list[channel.guild.id]

    def track_channel(self, channel: discord.TextChannel):
        """
        Adds the channel to the channel ids list.
        """
        if not self.guild_is_tracked(channel.guild):
            self.track_guild(channel.guild)
        self.channel_ids_list[channel.guild.id].append(channel.id)
        self._save_channel_ids()

    def untrack_channel(self, channel: discord.TextChannel):
        """
        Removes the channel from the channel ids list.
        """
        if not self.guild_is_tracked(channel.guild):
            return
        self.channel_ids_list[channel.guild.id].remove(channel.id)
        self._save_channel_ids()

    def guild_is_tracked(self, guild: discord.Guild):
        """
        Checks if the guild is in the channel ids list.
        """
        return guild.id in self.channel_ids_list

    def track_guild(self, guild: discord.Guild):
        """
        Adds the guild to the channel ids list.
        """
        self.channel_ids_list[guild.id] = []
        self._save_channel_ids()

    def untrack_guild(self, guild: discord.Guild):
        """
        Removes the guild from the channel ids list.
        """
        if self.guild_is_tracked(guild):
            del self.channel_ids_list[guild.id]
        self._save_channel_ids()

    def _save_channel_ids(self):
        """
        Saves the channel names to a json file.
        """
        with open(CHANNELS_JSON_FILE, "w") as f:
            json.dump(self.channel_ids_list, f)

    def _load_channel_ids(self):
        """
        Loads the channel names from a json file.
        """
        try:
            with open(CHANNELS_JSON_FILE, "r") as f:
                d = json.load(f)
                self.channel_ids_list = {int(key): value for key, value in d.items()}
        except FileNotFoundError:
            logger.info("No channel names file found.")
            self.channel_ids_list = {guild.id: [] for guild in self.guilds}

    def stop(self):
        """
        Stops the bot.
        """
        self.loop.stop()
