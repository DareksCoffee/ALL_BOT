import nextcord
import sqlite3
import aiosqlite
from nextcord.ext import commands, application_checks
import random
from main import embed_color, ThrowError

class Job(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
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
    async def get_balance(self, user_id, guild_id):
        async with aiosqlite.connect("economy.db") as db:
            async with db.execute("SELECT balance FROM users WHERE user_id = ? AND guild_id = ?", (user_id, guild_id,)) as cursor:
                result = await cursor.fetchone()
                return result[0] if result else 0

    async def get_job_salary(self, job_name):
        return self.jobs.get(job_name)

    async def has_job(self, user_id, guild_id):
        async with aiosqlite.connect("economy.db") as db:
            async with db.execute("SELECT job FROM users WHERE user_id = ? AND guild_id = ?", (user_id, guild_id)) as cursor:
                existing_job = await cursor.fetchone()
                return existing_job[0] is not None if existing_job else False

    async def update_job(self, user_id, guild_id, job_name):
        async with aiosqlite.connect("economy.db") as db:
            await db.execute(
                "INSERT INTO users (user_id, guild_id, job) VALUES (?, ?, ?) ON CONFLICT(user_id, guild_id) DO UPDATE SET job = excluded.job",
                (user_id, guild_id, job_name)
            )
            await db.commit()

    @nextcord.slash_command(name="job", description="Start working on a job")
    async def job(self, interaction: nextcord.Interaction, job: str):
        if not await self.has_job(interaction.id, interaction.guild.id):
            if job.lower() not in [job_name.lower() for job_name in self.jobs]:
                await ThrowError(interaction=interaction, error="This job is unavailable, use `/joblist` to get the full list of available jobs", error_type="Economy")
                return

            salary = await self.get_job_salary(job)
            user_money = await self.get_balance(interaction.user.id, interaction.guild.id)
            if salary is None:
                await ThrowError(interaction=interaction, error="This job is unavailable, use `/joblist` to get the full list of available jobs", error_type="Economy")
                return

            if user_money < (salary * 2):
                await ThrowError(interaction=interaction, error=f"You are not ready yet to be a {job}, you need at least {(salary * 2) - user_money}", error_type="Economy")
                return        

            user_id = interaction.user.id
            guild_id = interaction.guild.id

            await self.update_job(user_id, guild_id, job)
            embed = nextcord.Embed(
                title="Congratulations!",
                description=f"You have been hired as a {job}, your starting salary is {salary}:coin:",
                color=embed_color
            )
            embed.add_field(name="How to work?", value=f"Use /work every 2 minutes to earn between 250-{salary}:coin:")
            await interaction.response.send_message(embed=embed)
        else:
            embed = nextcord.Embed(
                title="You already have a job!",
                description="You cannot get hired to another job since you already have one.\nUse `/resign` to resign to your current job.",
                color=embed_color
            )
            await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Job(bot))