from __future__ import annotations

import pathlib

import disnake
from disnake.ext import commands

from core.errors import ErrorHandlerImpl
from core.logger import create_logging_setup
from core.utils import BotBase, ColorLike, EnvironmentVariables, load_and_verify_envs, parse_cogs

__all__: tuple[str] = ("HelperBot",)


class HelperBot(ErrorHandlerImpl, BotBase):
    envs: EnvironmentVariables = load_and_verify_envs()
    logger = create_logging_setup()

    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            strip_after_prefix=True,
            case_insensitive=True,
            intents=disnake.Intents(
                dm_messages=True,
                guild_messages=True,
                message_content=True,
                members=True,
                presences=True,
                emojis=True,
                guild_reactions=True,
                guilds=True,
            ),
            allowed_mentions=disnake.AllowedMentions(everyone=False, replied_user=False),
        )
        self.load_extension("jishaku")
        for file in pathlib.Path("cogs/").glob("*.py"):
            list(map(lambda cog: self.add_cog(cog(self)), parse_cogs(file).values()))

    @staticmethod
    def generic_embed(
        ctx: commands.Context[HelperBot], description: str, *, color: ColorLike = disnake.Color.blurple()
    ) -> disnake.Embed:
        return disnake.Embed(description=description, color=color).set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar
        )
