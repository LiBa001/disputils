import discord
from discord.ext import commands
import asyncio
from .abc import Dialog


class Confirmation(Dialog):
    """ Represents a message to let the user confirm a specific action."""

    def __init__(self, client: discord.Client, color: hex = 0x000000, message: discord.Message = None):
        """Initialize the class variables."""
        super().__init__(color=color)

        self._client = client
        self.color = color
        self.emojis = {"✅": True, "❌": False}
        self._confirmed = None
        self.message = message
        self._embed = None

    @property
    def confirmed(self):
        """Return whether confirmed."""
        return self._confirmed

    async def confirm(
        self, text: str, user: discord.User, channel: discord.TextChannel = None
    ) -> bool or None:
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

    async def confirm(
        self, text: str, user: discord.User = None, channel: discord.TextChannel = None
    ) -> bool or None:

        if user is None:
            user = self._ctx.author

        if self.message is None and channel is None:
            channel = self._ctx.channel

        return await super().confirm(text, user, channel)

    async def text_confirmation(
        self, text: str, color: discord.Color, author: discord.User, show_author: bool, channel: discord.Channel, timeout: int = None
    ) -> bool:
        def input_check(msg: Message) -> bool:
            return msg.author == self._ctx.author and msg.channel == self._ctx.channel

        text += "Type `YES` to Accept, Else Decline."

        embed = discord.Embed(
            title="Do you Accept?",
            description=text,
            color=color
        )

        reply = await self._client.wait_for("message", check=input_check, timeout=timeout if not None).content  # extract the text at one go!

        if reply[0].lower() == "y":
            return True
        return False
