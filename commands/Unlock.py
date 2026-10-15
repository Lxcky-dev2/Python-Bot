import discord
from discord import app_commands
from discord.ext import commands
from embeds import success, error

async def setup(bot: commands.Bot) -> None:
    @bot.tree.command(name="unlock", description="Restore the @everyone send-messages setting")
    @app_commands.describe(reason="Reason for unlocking the channel")
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.guild_only()
    async def unlock(interaction: discord.Interaction, reason: str = "No reason provided") -> None:
        channel = interaction.channel
        if not isinstance(channel, discord.TextChannel):
            return await interaction.response.send_message(embed=error("Unsupported Channel", "Use this in a text channel."), ephemeral=True)
        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.response.send_message(embed=error("Missing Permission", "You need **Manage Channels** permission."), ephemeral=True)
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = None
        try:
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite, reason=f"Unlocked by {interaction.user}: {reason}")
        except discord.Forbidden:
            return await interaction.response.send_message(embed=error("Failed", "I need **Manage Roles** permission and a suitable role position."), ephemeral=True)
        await interaction.response.send_message(embed=success("Channel Unlocked", f"{channel.mention} has its default send-messages setting restored.\n**Reason:** {reason}"))
