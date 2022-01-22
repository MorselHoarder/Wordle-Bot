import discord
from Wordle_Bot.bot import WordleBot
from Wordle_Bot.commands import WordleGameCommands
from Wordle_Bot.maintenance import Maintenance
from Wordle_Bot.errors import Errors


def create_bot(
    command_prefix="w!",
    description="""Hi! I track statistics for the Wordle players in the server.""",
    intents=None,
):
    if intents is None:
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True
        intents.guilds = True

    bot = WordleBot(
        command_prefix=command_prefix, description=description, intents=intents
    )
    bot.add_cog(WordleGameCommands(bot))
    bot.add_cog(Maintenance(bot))
    bot.add_cog(Errors(bot))
    return bot
