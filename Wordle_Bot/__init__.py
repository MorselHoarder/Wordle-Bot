import discord
from pretty_help import PrettyHelp, DefaultMenu
from Wordle_Bot.bot import WordleBot
from Wordle_Bot.commands import GameCommands
from Wordle_Bot.listeners import Listeners
from Wordle_Bot.maintenance import Maintenance
from Wordle_Bot.errors import Errors


def create_bot(
    command_prefix="w!",
    description=None,
    intents=None,
):
    if intents is None:
        intents = discord.Intents.default()
        intents.members = True
        intents.guilds = True

    if description is None:
        description = """Hi! I'm the Wordle Bot! I help server members compete in deciding who is the hottest Wordle aficionado. 
    
    You may be wondering how to participate in the Wordle game. The rules are simple:

    1. Play the game here: https://www.powerlanguage.co.uk/wordle/ 
       Then, hit the `Share` button to copy it.

    2. Post your wordle score in a text channel that is tracked by the bot. 
       Usually this is #wordle. You can check this with `w!chlist`.

    Your post should be in the format:
    ```
    Wordle ### #/6

    ⬛⬛⬛⬛⬛
    ⬛🟨⬛🟨⬛
    ⬛⬛⬛⬛⬛
    🟩⬛⬛⬛🟩
    🟩🟩🟩🟩🟩
    ⬛⬛⬛⬛⬛
    ```
    (all you need is the first line, really)

    Your individual scores are tracked by Discord ID, so it will be consistent across all servers. If you post it in one server, it will be reflected in your score for all.

    Other notes:
    - Each day's score is cached immediately upon posting. 
    - Failing scores of X/6 are counted as 7/6 for calculations. Git gud.
    - Don't be square and avoid posting your bad scores, or you will be roasted.
    - Don't post un-earned 1s. You will be roasted further. 
    - This is for FUN, not serious competition. Enjoy yourselves!

    See the following command categories below for more information:
    """

    bot = WordleBot(
        command_prefix=command_prefix,
        description=description,
        intents=intents,
        help_command=PrettyHelp(
            menu=DefaultMenu(active_time=120),
            color=discord.Color.green(),
            index_title="The Wordle Bot",
            ending_note="""Type `w!help <command>` for more info on a command.\nUse ◀️▶️ reactions to navigate category pages, and ❌ to exit.""",
        ),
    )
    bot.add_cog(GameCommands(bot))
    bot.add_cog(Maintenance(bot))
    bot.add_cog(Listeners(bot))
    bot.add_cog(Errors(bot))
    return bot
