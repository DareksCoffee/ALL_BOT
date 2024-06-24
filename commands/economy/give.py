import nextcord
from nextcord.ext import commands, application_checks
import random
import sqlite3
import aiosqlite
import time
import asyncio
from cooldown import Cooldown
from main import embed_color, ThrowError

class Give(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown = Cooldown()

    async def get_balance(self, user_id):
        async with aiosqlite.connect("economy.db") as db:
            cursor = await db.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
            row = await cursor.fetchone()
            return row[0] if row else 0

    async def update_balance(self, user_id, guild_id, amount):
        async with aiosqlite.connect("economy.db") as db:
            await db.execute(
                "INSERT INTO users (user_id, guild_id, balance) VALUES (?, ?, ?) ON CONFLICT(user_id, guild_id) DO UPDATE SET balance = balance + ?",
                (user_id, guild_id, amount, amount)
            )
            await db.commit()
        
    @nextcord.slash_command(name="give", description="Give money to another user.")
    async def give(self, interaction: nextcord.Interaction, recipient: nextcord.User, amount: int):
        remaining_time = await self.cooldown.check_cooldown(interaction.user.id, interaction.guild.id)
        if remaining_time:
            await ThrowError(interaction=interaction, error=f"Woah there generous guy! Wait {remaining_time:.2f} seconds until you can give coins again", error_type="Cooldown")
            return

        if amount <= 0:
            await ThrowError(interaction=interaction, error=f"You cannot transfer a negative number.", error_type="Negative")
            return

        sender_balance = await self.get_balance(interaction.user.id)
        if amount > sender_balance:
            await ThrowError(interaction=interaction, error=f"You don't have enough money to give {recipient} {amount} (you need {amount - sender_balance} more coins)", error_type="Poorness")
            return

        if interaction.user.id == recipient.id:
            await ThrowError(interaction=interaction, error=f"You cannot give money to yourself", error_type="404")
            return

        await self.update_balance(interaction.user.id, interaction.guild.id, -amount)
        await self.update_balance(recipient.id, interaction.guild.id, amount)

        embed = nextcord.Embed(
            title= "Success",
            description= f"You have given {amount} :coin: to {recipient.global_name}",
            color= embed_color
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.send(F"{recipient.mention} you have been given {amount} :coin: by {interaction.user.mention}")

def setup(bot):
    bot.add_cog(Give(bot))