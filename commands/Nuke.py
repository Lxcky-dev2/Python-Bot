import discord
from discord import app_commands
from discord.ext import commands
from embeds import success, error, warning

async def setup(bot: commands.Bot) -> None:
    @bot.tree.command(name="nuke", description="Replace this channel with a fresh copy (destructive)")
    @app_commands.describe(confirm="Set this to True to confirm deleting and replacing the current channel")
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.guild_only()
    async def nuke(interaction: discord.Interaction, confirm: bool = False) -> None:
        channel = interaction.channel
        guild = interaction.guild
        if not guild or not isinstance(channel, (discord.TextChannel, discord.ForumChannel, discord.VoiceChannel, discord.StageChannel)):
            return await interaction.response.send_message(embed=error("Unsupported Channel", "Use this command in a server text, forum, voice, or stage channel."), ephemeral=True)
        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.response.send_message(embed=error("Missing Permission", "You need **Manage Channels** permission."), ephemeral=True)
        if not confirm:
            return await interaction.response.send_message(embed=warning("Confirm Channel Replacement", f"This will replace **#{channel.name}** with a fresh copy. Existing messages will not be copied. Run `/nuke confirm:True` to proceed."), ephemeral=True)
        await interaction.response.defer(ephemeral=True, thinking=True)
        try:
            replacement = await channel.clone(name=channel.name, reason=f"Channel replaced by {interaction.user} ({interaction.user.id}) via /nuke")
            await replacement.edit(position=channel.position, reason="Restore channel position after replacement")
            await channel.delete(reason=f"Replaced by /nuke from {interaction.user} ({interaction.user.id})")
        except discord.Forbidden:
            return await interaction.followup.send(embed=error("Failed", "I need **Manage Channels** permission to clone and delete this channel."), ephemeral=True)
        except discord.HTTPException as exc:
            return await interaction.followup.send(embed=error("Discord Error", f"Discord couldn't complete the channel replacement: {exc}"), ephemeral=True)
        await interaction.followup.send(embed=success("Channel Replaced", f"Replaced **#{channel.name}** with {replacement.mention}. Previous messages were not copied."), ephemeral=True)
