from disputils import EmbedPaginator, Confirmation, MultipleChoice
import discord
from discord import Embed
import os


client = discord.Client()


@client.event
async def on_message(message):
    if message.content.lower().startswith('+choice'):
        multiple_choice = MultipleChoice(client, ['one', 'two', 'three', 'four', 'five', 'six'], "Testing lol")
        await multiple_choice.run([message.author], message.channel)

        while True:
            await multiple_choice.message.edit(content=f"Your choice: `{multiple_choice.choice}`")

            if multiple_choice.choice is None:
                await multiple_choice.quit("Canceled")
                break
            else:
                await multiple_choice.run([message.author])

    elif message.content.lower().startswith('+paginate'):
        embeds = [
            Embed(title="test page 1", description="This is just some tests content!", color=0x115599),
            Embed(title="test page 2", description="Nothing interesting here.", color=0x5599ff),
            Embed(title="test page 3", description="Why are you still here?", color=0x191638)
        ]

        paginator = EmbedPaginator(client, embeds)
        await paginator.run([message.author], channel=message.channel)

    elif message.content.lower().startswith('+confirm'):
        confirmation = Confirmation(client, 0x012345)
        await confirmation.confirm("Are you sure?", user=message.author, channel=message.channel)

        if confirmation.confirmed:
            await confirmation.update("Confirmed", color=0x55ff55)
        else:
            await confirmation.update("Not confirmed", hide_author=True, color=0xff5555)


client.run(os.getenv('BOT_TOKEN'))
