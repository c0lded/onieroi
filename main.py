import discord
import os
import dotenv

from discord.ext import commands

dotenv.load_dotenv()
my_secret: str = os.environ['TOKEN']
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Bot is Ready!!")


@bot.command()
async def echo(ctx, *, text: str):
    await ctx.message.delete()
    embed_color = 0x706cfc
    channel = ctx.channel
    message = text

    if text.startswith('<#') and '>' in text:
        space_index = text.find(' ')
        if space_index != -1:
            possible_channel_id = text[2:space_index - 1]
            if possible_channel_id.isdigit():
                found_channel = ctx.guild.get_channel(int(possible_channel_id))
                if found_channel:
                    channel = found_channel
                    message = text[space_index + 1:]

    if not channel.permissions_for(ctx.author).send_messages:
        embed = discord.Embed(
            description=
            "You do not have permission to send messages in the specified channel.",
            color=embed_color)
        await ctx.send(embed=embed)
        return

    if not channel.permissions_for(ctx.guild.me).send_messages:
        embed = discord.Embed(
            description=
            "I do not have permission to send messages in that channel.",
            color=embed_color)
        await ctx.send(embed=embed)
        return

    try:
        if ctx.message.attachments:
            attachments = [
                await attachment.to_file()
                for attachment in ctx.message.attachments
            ]
            await channel.send(message,
                               files=attachments if attachments else None)
        else:
            await channel.send(message)
    except discord.Forbidden:
        embed = discord.Embed(
            description=
            "I encountered a 'Forbidden' error while trying to send the message.",
            color=embed_color)
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(description=f"An error occurred: {e}",
                              color=embed_color)
        await ctx.send(embed=embed)


bot.run(my_secret)
