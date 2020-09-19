async def mass_purge(channel, limit: int, inclusive=False):
    amount = abs(limit)
    if amount > 100:
        iterations, rem = divmod(amount, 100)
        if inclusive:
            for i in range(iterations):
                await channel.purge(limit=100)
            await channel.purge(limit=rem)
        else:
            for i in range(iterations):
                messages = channel.history(limit=100).flatten()
                for message in range(0, len(messages)):
                    if message != 0:
                        await messages[message].delete()
            async for message in channel.history(limit=rem):
                await message.delete()
    else:
        messages = channel.history(limit=amount).flatten()
        for message in range(0, len(messages)):
            if not inclusive and message != 0:
                await messages[message].delete()
