import discord
from discord.ext import commands
import asyncio
from .abc import Dialog


class Confirmation(Dialog):
    """ Represents a message to let the user confirm a specific action. """

    def __init__(self, client: discord.Client, color: hex = 0x000000, message: discord.Message = None):
        super().__init__(color=color)

        self._client = client
        self.color = color
        self.emojis = {"✅": True, "❌": False}
        self._confirmed = None
        self.message = message
        self._embed: discord.Embed = None

    @property
    def confirmed(self):
        return self._confirmed

    async def confirm(self, text: str, user: discord.User, channel: discord.TextChannel = None)\
            -> bool or None:
        """


        :param text: The confirmation text.
        :param user: The user who has to confirm.
        :param channel: The channel the message will be sent to. Must only be specified if `self.message` is None.
        :return: True when it's been confirmed, otherwise False. Will return None when a timeout occurs.
        """

        emb = discord.Embed(
            title=text,
            color=self.color
        )
        emb.set_author(
            name=str(user),
            icon_url=user.avatar_url
        )

        self._embed = emb

        if channel is None and self.message is not None:
            channel = self.message.channel
        elif channel is None:
            raise TypeError("Missing argument. You need to specify a target channel.")

        msg = await channel.send(embed=emb)
        self.message = msg

        for emoji in self.emojis:
            await msg.add_reaction(emoji)

        try:
            reaction, user = await self._client.wait_for(
                'reaction_add',
                check=lambda r, u: (r.message.id == msg.id) and (u.id == user.id) and (r.emoji in self.emojis),
                timeout=20
            )
        except asyncio.TimeoutError:
            self._confirmed = None
            return
        finally:
            await msg.clear_reactions()

        confirmed = self.emojis[reaction.emoji]

        self._confirmed = confirmed
        return confirmed


class BotConfirmation(Confirmation):
    def __init__(self, ctx: commands.Context, color: hex = 0x000000, message: discord.Message = None):
        self._ctx = ctx

        super().__init__(ctx.bot, color, message)

    async def confirm(self, text: str, user: discord.User = None, channel: discord.TextChannel = None) \
            -> bool or None:

        if user is None:
            user = self._ctx.author

        if self.message is None and channel is None:
            channel = self._ctx.channel

        return await super().confirm(text, user, channel)
