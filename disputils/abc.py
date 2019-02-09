from abc import ABC
from discord import Message, Embed


class Dialog(ABC):
    def __init__(self, *args, **kwargs):
        self._embed: Embed = None
        self.message: Message = None
        self.color: hex = kwargs.get("color") or kwargs.get("colour") or 0x000000

    async def quit(self, text: str = None):
        """
        Quit the dialog.

        :param text:
        :return:
        """

        if text is None:
            await self.message.delete()
        else:
            await self.message.edit(content=text, embed=None)
            await self.message.clear_reactions()

    async def update(self, text: str, color: hex = None, hide_author: bool = False):
        """
        This will update the confirmation embed.

        :param text: The new text.
        :param color: The new embed color.
        :param hide_author: True if you want to hide the embed author. Default's to False.
        :return: Nothing.
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
        This will edit the confirmation message.

        :param text: The new text.
        :param embed: The new embed.
        :return: Nothing.
        """

        await self.message.edit(content=text, embed=embed)
