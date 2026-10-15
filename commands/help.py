import discord
from embeds import primary


async def setup(bot) -> None:
    @bot.tree.command(name="help", description="View the available bot commands")
    async def help_command(interaction: discord.Interaction) -> None:
        commands_list = sorted(bot.tree.get_commands(), key=lambda command: command.name)
        lines = [f"`/{command.name}` — {command.description}" for command in commands_list]
        description = "\n".join(lines) if lines else "No commands are loaded yet."
        await interaction.response.send_message(
            embed=primary("Command Guide", description),
            ephemeral=True,
        )
