"""Lxcky Build - Python Discord bot template."""
import os
import logging
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

from command_loader import load_commands

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

TOKEN = os.getenv("TOKEN", "").strip()
GUILD_ID = os.getenv("GUILD_ID", "").strip()


class LxckyBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self) -> None:
        await load_commands(self)

        # Set GUILD_ID in .env for fast development sync to one server.
        # Leave it blank to sync globally (global commands can take a while to appear).
        if GUILD_ID.isdigit():
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            logging.info("Synced %s slash command(s) to guild %s", len(synced), GUILD_ID)
        else:
            synced = await self.tree.sync()
            logging.info("Synced %s global slash command(s)", len(synced))

    async def on_ready(self) -> None:
        logging.info("Logged in as %s (ID: %s)", self.user, self.user.id if self.user else "unknown")


async def main() -> None:
    if not TOKEN or TOKEN == "your_bot_token_here":
        raise SystemExit("Missing TOKEN. Add your bot token to the .env file (see .env.example).")

    bot = LxckyBot()
    async with bot:
        await bot.start(TOKEN)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
