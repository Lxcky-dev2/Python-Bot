import discord
from discord import app_commands
from discord.ext import commands
from embeds import primary

async def setup(bot: commands.Bot) -> None:
    @bot.tree.command(name="serverinfo", description="Show information about this server")
    @app_commands.guild_only()
    async def serverinfo(interaction: discord.Interaction) -> None:
        guild = interaction.guild
        embed = primary("Server Information", f"**{guild.name}**")
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="Server ID", value=f"`{guild.id}`", inline=True)
        embed.add_field(name="Owner", value=f"<@{guild.owner_id}>" if guild.owner_id else "Unknown", inline=True)
        embed.add_field(name="Members", value=str(guild.member_count or "Unknown"), inline=True)
        embed.add_field(name="Created", value=discord.utils.format_dt(guild.created_at, style="F"), inline=False)
        embed.add_field(name="Channels", value=str(len(guild.channels)), inline=True)
        embed.add_field(name="Roles", value=str(len(guild.roles)), inline=True)
        embed.add_field(name="Boost level", value=str(guild.premium_tier), inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)
