import discord
from discord import app_commands
from discord.ext import commands
from embeds import primary, error

async def setup(bot: commands.Bot) -> None:
    group = app_commands.Group(name="account", description="Look up basic public Discord account information")

    @group.command(name="search", description="Look up a Discord account by its user ID")
    @app_commands.describe(user_id="The numeric Discord user ID")
    async def search(interaction: discord.Interaction, user_id: str) -> None:
        if not user_id.isdigit() or len(user_id) < 17 or len(user_id) > 20:
            return await interaction.response.send_message(embed=error("Invalid User ID", "Enter a numeric Discord user ID (usually 17–20 digits)."), ephemeral=True)
        await interaction.response.defer(ephemeral=True, thinking=True)
        try:
            user = await bot.fetch_user(int(user_id))
        except (discord.NotFound, discord.HTTPException):
            return await interaction.followup.send(embed=error("Account Not Found", "Discord couldn't return an account for that ID."), ephemeral=True)
        embed = primary("Discord Account Lookup", f"Information publicly available through Discord for **{discord.utils.escape_markdown(str(user))}**")
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="Username", value=f"`{user.name}`", inline=True)
        embed.add_field(name="Display name", value=discord.utils.escape_markdown(user.global_name or user.name), inline=True)
        embed.add_field(name="User ID", value=f"`{user.id}`", inline=False)
        embed.add_field(name="Account created", value=discord.utils.format_dt(user.created_at, style="F") + "\n" + discord.utils.format_dt(user.created_at, style="R"), inline=False)
        embed.add_field(name="Bot account", value="Yes" if user.bot else "No", inline=True)
        if user.public_flags.all():
            flags = [flag.name.replace("_", " ").title() for flag in user.public_flags.all()]
            embed.add_field(name="Public profile badges", value=", ".join(flags)[:1024], inline=False)
        embed.set_footer(text="Only information exposed by Discord is shown. No IP, email, or private account data is available.")
        await interaction.followup.send(embed=embed, ephemeral=True)

    bot.tree.add_command(group)
