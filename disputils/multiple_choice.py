import discord
from discord import Message, Client, TextChannel, User
from discord.ext.commands import Context
import asyncio
from typing import Tuple, List, Optional, Union
from .abc import Dialog


class MultipleChoice(Dialog):
    """
    Generate and manage a reaction controlled rich embed multiple choice poll in
    Discord.

    :param title: Embed title.
    :type title: :class:`str`

    :param description: Embed description.
    :type description: :class:`str`

    :param options: Options to choose from. Each option is going to be a separate embed
        field.
    :type options: list[:class:`str`]
    """

    def __init__(
        self,
        client: Client,
        options: List[str],
        title: str,
        description: str = "",
        **kwargs
    ):
        super().__init__(**kwargs)

        self._client: Client = client
        self.options: List[str] = options
        self.title: str = title
        self.description: str = description

        self.message: Optional[Message] = None
        self._parse_kwargs(**kwargs)

        self._embed: Optional[discord.Embed] = None
        self._emojis: List[str] = []

        self.close_emoji = "❌"

        self._choice = None

    def _parse_kwargs(self, **kwargs):
        self.message: Message = (
            kwargs.get("message") or kwargs.get("msg") or self.message
        )

    def _generate_emojis(self) -> List[str]:
        self._emojis.clear()

        if len(self.options) > 10:
            for i in range(len(self.options)):  # generates unicode emojis [A,B,C,…]
                hex_str = hex(224 + (6 + i))[2:]
                emoji = b"\\U0001f1a".replace(b"a", bytes(hex_str, "utf-8"))
                emoji = emoji.decode("unicode-escape")
                self._emojis.append(emoji)

        else:
            for i in range(len(self.options)):  # generates unicode emojis [1,2,3,…]
                if i < 9:
                    emoji = "x\u20e3".replace("x", str(i + 1))
                else:
                    emoji = "\U0001f51f"

                self._emojis.append(emoji)

        return self._emojis

    def _generate_embed(self) -> discord.Embed:
        config_embed = discord.Embed(
            title=self.title, description=self.description, color=self.color
        )

        emojis = self._generate_emojis()

        for i in range(len(self.options)):
            config_embed.add_field(name=emojis[i], value=self.options[i], inline=False)

        self._embed = config_embed
        return config_embed

    @property
    def embed(self) -> discord.Embed:
        """ The generated embed. """

        if self._embed is None:
            self._generate_embed()

        return self._embed

    @property
    def choice(self) -> str:
        """ The option that the user chose. """

        return self._choice

    async def run(
        self,
        users: Union[User, List[User]] = None,
        channel: TextChannel = None,
        **kwargs
    ) -> Tuple[Optional[str], Message]:
        """
        Run the multiple choice dialog.

        :param users: Users that can use the reactions (default: `None`).
            If this is ``None``: Any user can interact.

        :type users: list[:class:`discord.User`]

        :param channel: The channel to send the message to.
        :type channel: :class:`discord.TextChannel`, optional

        :param kwargs:
            - message :class:`discord.Message`
            - timeout :class:`int` (seconds, default: ``60``),
            - closable :class:`bool` (default: ``True``)

        :return: selected option and used :class:`discord.Message`
        :rtype: tuple[:class:`str`, :class:`discord.Message`]
        """

        if type(users) == User:
            users = [users]

        self._parse_kwargs(**kwargs)
        timeout = kwargs.get("timeout", 60)
        closable: bool = kwargs.get("closable", True)

        config_embed = self.embed

        if channel is not None:
            self.message = await channel.send(embed=config_embed)
        elif self.message is not None:
            await self.message.clear_reactions()
            await self.message.edit(content=self.message.content, embed=config_embed)
        else:
            raise TypeError(
                "Missing argument. "
                + "You need to specify either 'channel' or 'message' as a target."
            )

        for emoji in self._emojis:
            await self.message.add_reaction(emoji)

        if closable:
            await self.message.add_reaction(self.close_emoji)

        def check(r, u):
            res = (r.message.id == self.message.id) and u.id != self._client.user.id

            if users is not None:
                res = res and (u.id in [_u.id for _u in users])

            is_valid_emoji = r.emoji in self._emojis
            if closable:
                is_valid_emoji = is_valid_emoji or r.emoji == self.close_emoji

            res = res and is_valid_emoji

            return res

        try:
            reaction, user = await self._client.wait_for(
                "reaction_add", check=check, timeout=timeout
            )
        except asyncio.TimeoutError:
            self._choice = None
            return None, self.message

        if reaction.emoji == self.close_emoji:
            self._choice = None
            return None, self.message

        index = self._emojis.index(reaction.emoji)
        self._choice = self.options[index]

        return self._choice, self.message


class BotMultipleChoice(MultipleChoice):
    """
    Same as :class:`MultipleChoice`, except for the discord.py commands extension.
    """

    def __init__(
        self, ctx: Context, options: list, title: str, description: str = "", **kwargs
    ):
        super().__init__(ctx.bot, options, title, description, **kwargs)

        self._ctx = ctx

    async def run(
        self,
        users: Union[User, List[User]] = None,
        channel: TextChannel = None,
        **kwargs
    ) -> Tuple[Optional[str], Message]:

        if self.message is None and channel is None:
            channel = self._ctx.channel

        return await super().run(users, channel, **kwargs)
