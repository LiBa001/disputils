from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice
from discord.ext import commands
from discord import Embed
import os


bot = commands.Bot("+")


@bot.command()
async def paginate(ctx):
    embeds = [
        Embed(
            title="test page 1",
            description="This is just some test content!",
            color=0x115599,
        ),
        Embed(
            title="test page 2", description="Nothing interesting here.", color=0x5599FF
        ),
        Embed(
            title="test page 3", description="Why are you still here?", color=0x191638
        ),
    ]

    paginator = BotEmbedPaginator(ctx, embeds)
    await paginator.run()


@bot.command()
async def confirm(ctx):
    confirmation = BotConfirmation(ctx, 0x012345)
    await confirmation.confirm("Are you sure?")

    if confirmation.confirmed:
        await confirmation.update("Confirmed", color=0x55FF55)
    else:
        await confirmation.update("Not confirmed", hide_author=True, color=0xFF5555)


@bot.command()
async def choice(ctx):
    multiple_choice = BotMultipleChoice(
        ctx, ["one", "two", "three", "four", "five", "six"], "Testing stuff"
    )
    await multiple_choice.run()

    await multiple_choice.quit(multiple_choice.choice)


bot.run(os.getenv("BOT_TOKEN"))
