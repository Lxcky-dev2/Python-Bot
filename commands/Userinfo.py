import discord
from discord import app_commands
from discord.ext import commands
from embeds import primary, error

async def setup(bot: commands.Bot) -> None:
    @bot.tree.command(name="userinfo", description="Show information about a server member")
    @app_commands.describe(member="Member to inspect; defaults to you")
    @app_commands.guild_only()
    async def userinfo(interaction: discord.Interaction, member: discord.Member | None = None) -> None:
        member = member or interaction.user
        if not isinstance(member, discord.Member):
            return await interaction.response.send_message(embed=error("Unavailable", "This command needs a server member."), ephemeral=True)
        embed = primary("Member Information", f"Details for {member.mention}")
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Username", value=f"`{member}`", inline=True)
        embed.add_field(name="User ID", value=f"`{member.id}`", inline=True)
        embed.add_field(name="Account created", value=discord.utils.format_dt(member.created_at, style="F"), inline=False)
        embed.add_field(name="Joined server", value=discord.utils.format_dt(member.joined_at, style="F") if member.joined_at else "Unknown", inline=False)
        roles = [role.mention for role in reversed(member.roles[1:])]
        embed.add_field(name=f"Roles ({len(roles)})", value=", ".join(roles)[:1024] or "No roles", inline=False)
        embed.add_field(name="Server permissions", value="Administrator" if member.guild_permissions.administrator else "Manage Server" if member.guild_permissions.manage_guild else "Standard member", inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)
