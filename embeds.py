"""Small reusable Discord embed builder."""
import discord

PRIMARY = discord.Colour.from_rgb(45, 27, 78)
SUCCESS = discord.Colour.from_rgb(74, 222, 128)
ERROR = discord.Colour.from_rgb(248, 113, 113)
WARNING = discord.Colour.from_rgb(250, 204, 21)


def primary(title: str, description: str = "") -> discord.Embed:
    return discord.Embed(title=title, description=description or "", colour=PRIMARY)


def success(title: str, description: str = "") -> discord.Embed:
    return discord.Embed(title=title, description=description or "", colour=SUCCESS)


def error(title: str, description: str = "") -> discord.Embed:
    return discord.Embed(title=title, description=description or "", colour=ERROR)


def warning(title: str, description: str = "") -> discord.Embed:
    return discord.Embed(title=title, description=description or "", colour=WARNING)
