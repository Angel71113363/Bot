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

import aiohttp
from datetime import datetime

@bot.command()
async def discordinfo(ctx, user_id: int):
    try:
        user = await bot.fetch_user(user_id)
        
        created_at = user.created_at.strftime("%d/%m/%Y %H:%M")
        account_age = (datetime.utcnow() - user.created_at.replace(tzinfo=None)).days
        
        embed = discord.Embed(title="Informazioni Discord", color=discord.Color.blue())
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="Nome", value=str(user), inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Account creato", value=created_at, inline=False)
        embed.add_field(name="Età account", value=f"{account_age} giorni", inline=False)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send("Utente non trovato o ID non valido.")

@bot.command()
async def roblox(ctx, username: str):
    async with aiohttp.ClientSession() as session:
        # Prima trovo l'ID dell'utente
        async with session.post("https://users.roblox.com/v1/usernames/users", json={
            "usernames": [username],
            "excludeBannedUsers": True
        }) as resp:
            data = await resp.json()
            
            if not data.get("data"):
                return await ctx.send("Utente Roblox non trovato.")
            
            user_id = data["data"][0]["id"]
            display_name = data["data"][0]["displayName"]
            name = data["data"][0]["name"]
        
        # Prendo altre info
        async with session.get(f"https://users.roblox.com/v1/users/{user_id}") as resp:
            info = await resp.json()
            created = info.get("created", "Sconosciuto")
            description = info.get("description", "Nessuna descrizione")
        
        embed = discord.Embed(title="Informazioni Roblox", color=discord.Color.green())
        embed.add_field(name="Username", value=name, inline=True)
        embed.add_field(name="Display Name", value=display_name, inline=True)
        embed.add_field(name="ID", value=user_id, inline=True)
        embed.add_field(name="Account creato", value=created[:10], inline=False)
        embed.add_field(name="Descrizione", value=description[:200] or "Nessuna", inline=False)
        
        await ctx.send(embed=embed)
        
bot.run(os.environ["TOKEN"])
