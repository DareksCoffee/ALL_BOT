import nextcord
import random
import sqlite3
import aiosqlite
from nextcord.ext import commands
from main import embed_color, ThrowError
from cooldown import Cooldown

class DailyMoney(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown = Cooldown()

    async def update_balance(self, user_id, guild_id, amount):
        async with aiosqlite.connect("economy.db") as db:
            await db.execute(
                "INSERT INTO users (user_id, guild_id, balance) VALUES (?, ?, ?) ON CONFLICT(user_id, guild_id) DO UPDATE SET balance = balance + ?",
                (user_id, guild_id, amount, amount,)
            )
            await db.commit()

    @nextcord.slash_command(name="daily", description="Earn a couple coins daily")
    async def daily(self, interaction: nextcord.Interaction):
        remaining_time = await self.cooldown.check_cooldown(interaction.user.id, interaction.guild.id)
        if remaining_time:
            await ThrowError(interaction=interaction, error=f"You have to wait 5 hours in order to get your daily coins", error_type="Cooldown")
            return
        earnings = random.randint(250, 1500)
        await self.update_balance(interaction.user.id, interaction.guild.id, earnings)
        embed = nextcord.Embed(
            title="Daily Coins",
            description=f"You've earned {earnings} :coin:\nYou can use the command again in 5 hours.",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed)
        await self.cooldown.start_cooldown(18000, interaction.user.id, interaction.guild.id)

def setup(bot):
    bot.add_cog(DailyMoney(bot))