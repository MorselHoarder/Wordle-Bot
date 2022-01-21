import re
import statistics as stats
import json

import discord
from discord.ext.commands import Bot

from Wordle_Bot.logger import logger

CHANNELS_JSON_FILE = "channels.json"
WORDLE_PATTERN = re.compile(r"\bWordle (\d+) (\d)/\d\n")


class WordleBot(Bot):
    """
    The Wordle Bot.

    Scores structure: Dict of Dicts
    {
        Member_ID: {
            Wordle_day: score
        }
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_channel_ids()
        self.scores = {}
        self._initialized = False

    async def refresh_scores(self, wipe_scores=False):
        """
        Refreshes the scores dict.
        """
        if wipe_scores:
            self.scores = {}
        for channel in self.get_all_channels():
            if channel.id in self.channel_ids_list[channel.guild.id]:
                async for message in channel.history(limit=None):
                    self.check_for_wordle(message)

        self._initialized = True

    def check_for_wordle(self, message: discord.Message):
        """
        Checks if the message is a Wordle. If so, adds the scores to the score dict.
        """
        m = WORDLE_PATTERN.search(message.content)
        if m:
            day = int(m.group(1))
            score = int(m.group(2)) if m.group(2) != "X" else 7
            if message.author.id not in self.scores:
                self.scores[message.author.id] = {}
            self.scores[message.author.id][day] = score

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

    def _channels_tracked(self, ctx: discord.ext.commands.Context):
        """
        Returns a list of tracked channel names in the current server.
        """
        return [channel.name for channel in self.channel_ids_list[ctx.guild.id]]
        # TODO fix this because it needs to get the channel object first

    def _is_channel_tracked(self, channel: discord.TextChannel):
        """
        Checks if the channel is in the channel ids list.
        """
        return channel.id in self.channel_ids_list[channel.guild.id]

    def _track_channel(self, channel: discord.TextChannel):
        """
        Adds the channel to the channel ids list.
        """
        self.channel_ids_list[channel.guild.id].append(channel.id)
        self._save_channel_ids()

    def _untrack_channel(self, channel: discord.TextChannel):
        """
        Removes the channel from the channel ids list.
        """
        self.channel_ids_list[channel.guild.id].remove(channel.id)
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
                self.channel_ids_list = json.load(f)
        except FileNotFoundError:
            logger.info("No channel names file found.")
            self.channel_ids_list = {guild.id: [] for guild in self.guilds}
