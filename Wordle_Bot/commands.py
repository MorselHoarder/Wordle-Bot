import discord
import discord.ext.commands as cmds
from tabulate import tabulate

from Wordle_Bot.logger import logger

HEADERS = ["Name", "Average Score", "Completed"]


class GameCommands(cmds.Cog):
    """See scores and leaderboards!"""

    def __init__(self, bot) -> None:
        self.bot = bot

    @cmds.command(name="score", aliases=["s", "scores"])
    async def show_scores(self, ctx, *members: discord.Member):
        """
        Displays the score of each member passed in.
        If no members are passed in, the score of the current user is displayed.
        [member] can be a mention, a name, or an ID.
        Examples:  w!score
                   w!s @ServerMember12 FunnyNicknameGuy42 Bro#1234
        """
        if not self.bot.initialized:
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

    @cmds.command(name="lb", aliases=["leaderboard"])
    async def leaderboard(self, ctx, scope=None):
        """
        Displays the leaderboard for the current server.
        If scope is set to "global", displays the global leaderboard.
        """
        if not self.bot.initialized:
            await ctx.send(
                "Scores not finished tabulating from history. Please wait a minute and try again."
            )
            return

        if scope in ["global", "g"]:
            table = sorted(
                [
                    [
                        member.name + "#" + member.discriminator,
                        self.bot.get_average_wordle_score(member),
                        self.bot.get_wordles_completed(member),
                    ]
                    for member in self.bot.get_all_members()
                    if self.bot.get_wordles_completed(member) != 0
                ],
                key=lambda x: x[1],
            )
        else:
            table = sorted(
                [
                    [
                        member.display_name,
                        self.bot.get_average_wordle_score(member),
                        self.bot.get_wordles_completed(member),
                    ]
                    for member in ctx.guild.members
                    if self.bot.get_wordles_completed(member) != 0
                ],
                key=lambda x: x[1],
            )

        await ctx.send(
            "```\n" + tabulate(table, headers=HEADERS, tablefmt="psql") + "```"
        )
