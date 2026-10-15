import discord
from discord import app_commands
from discord.ext import commands
from embeds import success, error

async def setup(bot: commands.Bot) -> None:
    @bot.tree.command(name="purge", description="Bulk-delete recent messages in this channel")
    @app_commands.describe(amount="Number of messages to delete (1-100)")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.guild_only()
    async def purge(interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]) -> None:
        if not isinstance(interaction.channel, discord.TextChannel):
            return await interaction.response.send_message(embed=error("Unsupported Channel", "Use this command in a text channel."), ephemeral=True)
        if not interaction.user.guild_permissions.manage_messages:
            return await interaction.response.send_message(embed=error("Missing Permission", "You need **Manage Messages** permission."), ephemeral=True)
        if not interaction.channel.permissions_for(interaction.guild.me).manage_messages:
            return await interaction.response.send_message(embed=error("Bot Permission Missing", "I need **Manage Messages** permission in this channel."), ephemeral=True)
        await interaction.response.defer(ephemeral=True, thinking=True)
        try:
            deleted = await interaction.channel.purge(limit=amount, bulk=True, reason=f"Purged by {interaction.user} ({interaction.user.id})")
        except discord.Forbidden:
            return await interaction.followup.send(embed=error("Failed", "Discord denied the message deletion."), ephemeral=True)
        await interaction.followup.send(embed=success("Messages Purged", f"Deleted **{len(deleted)}** message(s)."), ephemeral=True)
