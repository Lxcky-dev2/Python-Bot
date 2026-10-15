import discord
from discord import app_commands
from discord.ext import commands
from embeds import success, error

async def setup(bot: commands.Bot) -> None:
    @bot.tree.command(name="lock", description="Prevent @everyone from sending messages here")
    @app_commands.describe(reason="Reason for locking the channel")
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.guild_only()
    async def lock(interaction: discord.Interaction, reason: str = "No reason provided") -> None:
        channel = interaction.channel
        if not isinstance(channel, discord.TextChannel):
            return await interaction.response.send_message(embed=error("Unsupported Channel", "Use this in a text channel."), ephemeral=True)
        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.response.send_message(embed=error("Missing Permission", "You need **Manage Channels** permission."), ephemeral=True)
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = False
        try:
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite, reason=f"Locked by {interaction.user}: {reason}")
        except discord.Forbidden:
            return await interaction.response.send_message(embed=error("Failed", "I need **Manage Roles** permission and a suitable role position."), ephemeral=True)
        await interaction.response.send_message(embed=success("Channel Locked", f"{channel.mention} is locked for @everyone.\n**Reason:** {reason}"))
