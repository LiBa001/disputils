from abc import ABC
from discord import Message, Embed, TextChannel, errors
from typing import Optional


class Dialog(ABC):
    """ Abstract base class defining a general embed dialog interaction. """

    def __init__(self, *args, **kwargs):
        self._embed: Optional[Embed] = None
        self.message: Optional[Message] = None
        self.color: hex = kwargs.get("color") or kwargs.get("colour") or 0x000000

    async def _publish(self, channel: Optional[TextChannel], **kwargs) -> TextChannel:
        if channel is None and self.message is None:
            raise TypeError(
                "Missing argument. You need to specify a target channel or message."
            )

        if channel is None:
            try:
                await self.message.edit(**kwargs)
            except errors.NotFound:
                self.message = None

        if self.message is None:
            self.message = await channel.send(**kwargs)

        return self.message.channel

    async def quit(self, text: str = None):
        """
        Quit the dialog.

        :param text: message text to display when dialog is closed
        :type text: :class:`str`, optional

        :rtype: ``None``
        """

        if text is None:
            await self.message.delete()
            self.message = None
        else:
            await self.display(text)
            try:
                await self.message.clear_reactions()
            except errors.Forbidden:
                pass

    async def update(self, text: str, color: hex = None, hide_author: bool = False, delete_after: int = None):
        """
        This will update the dialog embed.

        :param text: The new text.
        :param color: The new embed color.
        :param hide_author: True if you want to hide the embed author
            (default: ``False``).
        :rtype: ``None``
        """

        if color is None:
            color = self.color

        self._embed.colour = color
        self._embed.title = text

        if hide_author:
            self._embed.set_author(name="")

        await self.display(embed=self._embed, delete_after=delete_after)

    async def display(self, text: str = None, embed: Embed = None,  delete_after: int = None):
        """
        This will edit the dialog message.

        :param text: The new text.
        :param embed: The new embed.
        :rtype: ``None``
        """

        await self.message.edit(content=text, embed=embed, delete_after=delete_after)
