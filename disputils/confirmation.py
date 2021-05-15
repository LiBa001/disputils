import discord
from discord.ext import commands
import asyncio
from .abc import Dialog
from typing import Optional


class Confirmation(Dialog):
    """ Represents a message to let the user confirm a specific action. """

    def __init__(
        self,
        client: discord.Client,
        color: hex = 0x000000,
        message: discord.Message = None,
    ):
        super().__init__(color=color)

        self._client = client
        self.color = color
        self.emojis = {"✅": True, "❌": False}
        self._confirmed = None
        self.message = message
        self._embed: Optional[discord.Embed] = None

    @property
    def confirmed(self) -> bool:
        """ Whether the user has confirmed the action. """

        return self._confirmed

    async def confirm(
        self,
        text: str,
        user: discord.User,
        channel: discord.TextChannel = None,
        hide_author: bool = False,
    ) -> bool or None:
        """
        Run the confirmation.

        :param text: The confirmation text.
        :type text: :class:`str`

        :param user: The user who has to confirm.
        :type user: :class:`discord.User`

        :param channel: The channel the message will be sent to. Must only be specified
            if ``self.message`` is None.
        :type channel: :class:`discord.TextChannel`, optional

        :param hide_author: Whether or not the ``user`` should be set as embed author.
        :type hide_author: bool, optional

        :return: True when it's been confirmed, otherwise False. Will return None when a
            timeout occurs.
        :rtype: :class:`bool`, optional
        """

        emb = discord.Embed(title=text, color=self.color)
        if not hide_author:
            emb.set_author(name=str(user), icon_url=user.avatar.url)

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
                "reaction_add",
                check=lambda r, u: (r.message.id == msg.id)
                and (u.id == user.id)
                and (r.emoji in self.emojis),
                timeout=20,
            )
        except asyncio.TimeoutError:
            self._confirmed = None
            return
        finally:
            try:
                await msg.clear_reactions()
            except discord.Forbidden:
                pass

        confirmed = self.emojis[reaction.emoji]

        self._confirmed = confirmed
        return confirmed


class BotConfirmation(Confirmation):
    def __init__(
        self,
        ctx: commands.Context,
        color: hex = 0x000000,
        message: discord.Message = None,
    ):
        self._ctx = ctx

        super().__init__(ctx.bot, color, message)

    async def confirm(
        self,
        text: str,
        user: discord.User = None,
        channel: discord.TextChannel = None,
        hide_author: bool = False,
    ) -> bool or None:

        if user is None:
            user = self._ctx.author

        if self.message is None and channel is None:
            channel = self._ctx.channel

        return await super().confirm(text, user, channel, hide_author=hide_author)
