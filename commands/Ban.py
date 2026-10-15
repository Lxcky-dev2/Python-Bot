import discord
from discord import app_commands
from discord.ext import commands
from embeds import success, error

async def setup(bot: commands.Bot) -> None:
    @bot.tree.command(name="ban", description="Ban a member from this server")
    @app_commands.describe(member="Member to ban", reason="Reason for the ban", delete_message_days="Days of recent messages to delete (0-7)")
    @app_commands.default_permissions(ban_members=True)
    @app_commands.guild_only()
    async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided", delete_message_days: app_commands.Range[int, 0, 7] = 0) -> None:
        guild = interaction.guild
        if not guild or not interaction.user.guild_permissions.ban_members:
            return await interaction.response.send_message(embed=error("Missing Permission", "You need **Ban Members** permission."), ephemeral=True)
        if member.id == interaction.user.id:
            return await interaction.response.send_message(embed=error("Invalid Target", "You can't ban yourself."), ephemeral=True)
        if member.id == bot.user.id:
            return await interaction.response.send_message(embed=error("Invalid Target", "I can't ban myself."), ephemeral=True)
        if member.top_role >= interaction.user.top_role and guild.owner_id != interaction.user.id:
            return await interaction.response.send_message(embed=error("Role Hierarchy", "Your highest role must be above the target's highest role."), ephemeral=True)
        if member.top_role >= guild.me.top_role:
            return await interaction.response.send_message(embed=error("Role Hierarchy", "My highest role must be above the target's highest role."), ephemeral=True)
        try:
            await guild.ban(member, reason=f"{reason} | Moderator: {interaction.user} ({interaction.user.id})", delete_message_seconds=delete_message_days * 86400)
        except discord.Forbidden:
            return await interaction.response.send_message(embed=error("Failed", "I don't have permission to ban that member."), ephemeral=True)
        await interaction.response.send_message(embed=success("Member Banned", f"**Member:** {discord.utils.escape_markdown(str(member))} (`{member.id}`)\n**Reason:** {reason}\n**Messages deleted:** {delete_message_days} day(s)"))
