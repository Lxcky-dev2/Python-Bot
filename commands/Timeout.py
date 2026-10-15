from datetime import timedelta
import discord
from discord import app_commands
from discord.ext import commands
from embeds import success, error

async def setup(bot: commands.Bot) -> None:
    group = app_commands.Group(name="timeout", description="Timeout or remove a member's timeout")

    @group.command(name="add", description="Timeout a member for up to 28 days")
    @app_commands.describe(member="Member to timeout", minutes="Duration in minutes (1-40320)", reason="Reason for the timeout")
    @app_commands.default_permissions(moderate_members=True)
    async def add(interaction: discord.Interaction, member: discord.Member, minutes: app_commands.Range[int, 1, 40320], reason: str = "No reason provided") -> None:
        guild = interaction.guild
        if not guild or not interaction.user.guild_permissions.moderate_members:
            return await interaction.response.send_message(embed=error("Missing Permission", "You need **Moderate Members** permission."), ephemeral=True)
        if member.id == interaction.user.id:
            return await interaction.response.send_message(embed=error("Invalid Target", "You can't timeout yourself."), ephemeral=True)
        if member.guild_permissions.administrator:
            return await interaction.response.send_message(embed=error("Invalid Target", "Members with Administrator can't be timed out."), ephemeral=True)
        if member.top_role >= interaction.user.top_role and guild.owner_id != interaction.user.id:
            return await interaction.response.send_message(embed=error("Role Hierarchy", "Your highest role must be above the target's highest role."), ephemeral=True)
        if member.top_role >= guild.me.top_role:
            return await interaction.response.send_message(embed=error("Role Hierarchy", "My highest role must be above the target's highest role."), ephemeral=True)
        try:
            await member.timeout(timedelta(minutes=minutes), reason=f"{reason} | Moderator: {interaction.user} ({interaction.user.id})")
        except discord.Forbidden:
            return await interaction.response.send_message(embed=error("Failed", "I don't have permission to timeout that member."), ephemeral=True)
        await interaction.response.send_message(embed=success("Member Timed Out", f"**Member:** {member.mention}\n**Duration:** {minutes} minute(s)\n**Reason:** {reason}"))

    @group.command(name="remove", description="Remove a member's timeout")
    @app_commands.describe(member="Member to untimeout", reason="Reason for removing the timeout")
    @app_commands.default_permissions(moderate_members=True)
    async def remove(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided") -> None:
        guild = interaction.guild
        if not guild or not interaction.user.guild_permissions.moderate_members:
            return await interaction.response.send_message(embed=error("Missing Permission", "You need **Moderate Members** permission."), ephemeral=True)
        try:
            await member.timeout(None, reason=f"{reason} | Moderator: {interaction.user} ({interaction.user.id})")
        except discord.Forbidden:
            return await interaction.response.send_message(embed=error("Failed", "I don't have permission to remove that timeout."), ephemeral=True)
        await interaction.response.send_message(embed=success("Timeout Removed", f"Removed the timeout for {member.mention}.\n**Reason:** {reason}"))

    bot.tree.add_command(group)
