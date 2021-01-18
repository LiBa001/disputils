from abc import ABC
from discord import Message, Embed
from typing import Optional


class Dialog(ABC):
    """ Abstract base class defining a general embed dialog interaction. """

    def __init__(self, *args, **kwargs):
        self._embed: Optional[Embed] = None
        self.message: Optional[Message] = None
        self.color: hex = kwargs.get("color") or kwargs.get("colour") or 0x000000

    async def quit(self, text: str = None):
        """
        Quit the dialog.

        :param text: message text to display when dialog is closed
        :type text: :class:`str`, optional

        :rtype: ``None``
        """

        if text is None:
            await self.message.delete()
        else:
            await self.message.edit(content=text, embed=None)
            await self.message.clear_reactions()

    async def update(self, text: str, color: hex = None, hide_author: bool = False):
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

        await self.display(embed=self._embed)

    async def display(self, text: str = None, embed: Embed = None):
        """
        This will edit the dialog message.

        :param text: The new text.
        :param embed: The new embed.
        :rtype: ``None``
        """

        await self.message.edit(content=text, embed=embed)
