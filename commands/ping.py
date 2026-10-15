import discord
from discord import app_commands
from embeds import primary


async def setup(bot) -> None:
    @bot.tree.command(name="ping", description="Check the bot's latency")
    async def ping(interaction: discord.Interaction) -> None:
        latency_ms = round(interaction.client.latency * 1000)
        await interaction.response.send_message(
            embed=primary("Pong!", f"Gateway latency: **{latency_ms} ms**"),
            ephemeral=True,
        )
