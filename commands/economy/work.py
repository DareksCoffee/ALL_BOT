import nextcord
import random
from nextcord.ext import commands
import aiosqlite
from main import embed_color, ThrowError
from cooldown import Cooldown

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown = Cooldown()
        self.jobs = {
            "Office Job": 500,
            "Photographer": 1200,
            "Chef": 800,
            "Streamer": 1500,
            "Gardener": 700,
            "Artist": 1000,
            "Tutor": 900,
            "Fitness Instructor": 1100
        }

    async def get_job(self, user_id, guild_id):
        async with aiosqlite.connect("economy.db") as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER,
                    guild_id INTEGER,
                    balance INTEGER DEFAULT 0,
                    bank INTEGER DEFAULT 0,
                    job TEXT DEFAULT NULL,
                    PRIMARY KEY (user_id, guild_id)
                )
                """
            )
            await db.commit()
            cursor = await db.execute(
                "SELECT job FROM users WHERE user_id = ? AND guild_id = ?",
                (user_id, guild_id)
            )
            row = await cursor.fetchone()
            return row[0] if row else None

    async def update_balance(self, user_id, guild_id, amount):
        async with aiosqlite.connect("economy.db") as db:
            await db.execute(
                "INSERT INTO users (user_id, guild_id, balance) VALUES (?, ?, ?) ON CONFLICT(user_id, guild_id) DO UPDATE SET balance = balance + ?",
                (user_id, guild_id, amount, amount,)
            )
            await db.commit()

    @nextcord.slash_command(name="work", description="Earn a couple dollars by working!")
    async def work(self, interaction: nextcord.Interaction):
        remaining_time = await self.cooldown.check_cooldown(interaction.user.id, interaction.guild.id)
        if remaining_time:
            await ThrowError(interaction=interaction, error=f"You are tired! Wait {remaining_time:.2f} seconds to work again.", error_type="Cooldown")
            return

        job = await self.get_job(interaction.user.id, interaction.guild.id)
        if not job:
            await ThrowError(interaction=interaction, error="You need to have a job to work!", error_type="Economy")
            return

        earnings = random.randint(100, self.jobs.get(job))
        if earnings is None:
            await ThrowError(interaction=interaction, error="You need to have a job to work!", error_type="Economy")
            return

        await self.update_balance(interaction.user.id, interaction.guild.id, earnings)
        embed = nextcord.Embed(
            description=f"{interaction.user.display_name} successfully earned {earnings} :coin: from working as a {job}.",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed)
        await self.cooldown.start_cooldown(120, interaction.user.id, interaction.guild.id) 

def setup(bot):
    bot.add_cog(Work(bot))