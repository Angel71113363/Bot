import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot online come {bot.user}")

@bot.command()
async def ciao(ctx):
    await ctx.send(f"Ciao {ctx.author.mention}!")

@bot.command()
async def somma(ctx, a: int, b: int):
    await ctx.send(f"Il risultato è {a + b}")

bot.run(os.environ["TOKEN"])
