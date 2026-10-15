import discord
from discord import app_commands
from discord.ext import commands
from embeds import success, error

async def setup(bot: commands.Bot) -> None:
    @bot.tree.command(name="kick", description="Kick a member from this server")
    @app_commands.describe(member="Member to kick", reason="Reason for the kick")
    @app_commands.default_permissions(kick_members=True)
    @app_commands.guild_only()
    async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided") -> None:
        if not interaction.guild or not interaction.user.guild_permissions.kick_members:
            return await interaction.response.send_message(embed=error("Missing Permission", "You need **Kick Members** permission."), ephemeral=True)
        if member.id == interaction.user.id:
            return await interaction.response.send_message(embed=error("Invalid Target", "You can't kick yourself."), ephemeral=True)
        if member.id == bot.user.id:
            return await interaction.response.send_message(embed=error("Invalid Target", "I can't kick myself."), ephemeral=True)
        if member.top_role >= interaction.user.top_role and interaction.guild.owner_id != interaction.user.id:
            return await interaction.response.send_message(embed=error("Role Hierarchy", "Your highest role must be above the target's highest role."), ephemeral=True)
        if member.top_role >= interaction.guild.me.top_role:
            return await interaction.response.send_message(embed=error("Role Hierarchy", "My highest role must be above the target's highest role."), ephemeral=True)
        try:
            await member.kick(reason=f"{reason} | Moderator: {interaction.user} ({interaction.user.id})")
        except discord.Forbidden:
            return await interaction.response.send_message(embed=error("Failed", "I don't have permission to kick that member."), ephemeral=True)
        await interaction.response.send_message(embed=success("Member Kicked", f"**Member:** {member.mention}\n**Reason:** {reason}"))
