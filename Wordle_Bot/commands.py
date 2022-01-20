import discord
import discord.ext.commands as cmds
from tabulate import tabulate

from Wordle_Bot.logger import logger

HEADERS = ["Name", "Average Score", "Completed"]


class WordleCommands(cmds.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @cmds.Cog.listener("on_ready")
    async def refresh_scores(self):
        logger.info("Refreshing scores...")
        await self.bot.refresh_scores()
        logger.info("Scores refreshed. Bot ready.")

    @cmds.Cog.listener("on_message")
    async def check_new_message(self, message: discord.Message):
        self.bot.check_for_wordle(message)

    @cmds.command(name="score")
    async def show_scores(self, ctx, *members: discord.Member):
        """
        Displays the scores of the members passed in. If no members are passed in,
        the score of the current user is displayed.
        """
        if not self.bot._initialized:
            await ctx.send(
                "Scores not finished tabulating from history. Please wait a minute and try again."
            )
            return

        if not members:
            members = (ctx.message.author,)

        table = [
            [
                member.display_name,
                self.bot.get_average_wordle_score(member),
                self.bot.get_wordles_completed(member),
            ]
            for member in members
        ]

        await ctx.send(
            "```\n" + tabulate(table, headers=HEADERS, tablefmt="psql") + "```"
        )

    @cmds.command()
    async def leaderboard(self, ctx, scope=None):
        """
        Displays the leaderboard for the current server.
        If scope is set to "global", displays the global leaderboard.
        """
        if not self.bot._initialized:
            await ctx.send(
                "Scores not finished tabulating from history. Please wait a minute and try again."
            )
            return

        if scope == "global":
            table = [
                [
                    member.name,
                    self.bot.get_average_wordle_score(member),
                    self.bot.get_wordles_completed(member),
                ]
                for member in self.bot.get_all_members()
            ]
        else:
            table = [
                [
                    member.display_name,
                    self.bot.get_average_wordle_score(member),
                    self.bot.get_wordles_completed(member),
                ]
                for member in ctx.guild.members
            ]

        await ctx.send(
            "```\n" + tabulate(table, headers=HEADERS, tablefmt="psql") + "```"
        )
