import discord
import discord.ext.commands as cmds
from tabulate import tabulate

from Wordle_Bot.logger import logger

HEADERS = ["Name", "Average Score", "Completed"]


class WordleGameCommands(cmds.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @cmds.Cog.listener("on_message")
    async def check_new_message(self, message: discord.Message):
        self.bot.check_for_wordle(message)

    @cmds.command(name="score", aliases=["scores", "s"])
    async def show_scores(self, ctx, *members: discord.Member):
        """
        Displays the score of each member passed in.
        If no members are passed in, the score of the current user is displayed.
        [member] can be a mention, a name, or an ID.
        Usage examples:  w!score
                         w!s @ServerMember12 FunnyNicknameGuy42 Bro#1234 ...
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

    @show_scores.error
    async def show_scores_error(self, ctx, error):
        if isinstance(error, cmds.MemberNotFound):
            await ctx.send(
                f"Cannot find member '{error.argument}'. Try spelling with the correct case, use their full username, or use a mention."
            )

    @cmds.command(aliases=["lb", "leaderboards"])
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
