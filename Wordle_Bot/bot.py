import re
import numpy as np

import discord
from discord.ext.commands import Bot

from Wordle_Bot.logger import logger

CHANNEL_NAMES_LIST = ["wordle", "general", "games"]
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
        self.channel_names_list = (
            CHANNEL_NAMES_LIST  # Intended to be overwritten after initialization
        )
        self.scores = {}
        self._initialized = False

    async def refresh_scores(self):
        """
        Refreshes the scores dict.
        """
        self.scores = {}
        for channel in self.get_all_channels():
            if (
                channel.name in self.channel_names_list
                and channel.type == discord.ChannelType.text
            ):
                async for message in channel.history(limit=None, oldest_first=True):
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
            round(np.mean(list(self.scores[member.id].values())), 2)
            if member.id in self.scores
            else "N/A"
        )

    def get_wordles_completed(self, member: discord.Member):
        """
        Returns the number of completed wordles of the member.
        """
        return len(self.scores[member.id]) if member.id in self.scores else 0
