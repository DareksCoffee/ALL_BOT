import nextcord
import sqlite3
import aiosqlite
from nextcord.ext import commands, application_checks
import random
from main import embed_color

class JobList(commands.Cog):
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

    @nextcord.slash_command(name="joblist", description="List of available jobs")
    async def joblist(self, interaction: nextcord.Interaction):
        #job_list = "\n\n".join(f"• {job}: ${salary}" for job, salary in self.jobs.items())
        jobs_list = ""
        user_money = await self.get_balance(interaction.user.id, interaction.guild.id)

        for job in self.jobs:
            job_salary = self.jobs.get(job)
            if user_money > (job_salary * 2):
                jobs_list +=f"• {job}: ${job_salary} :green_circle:\n\n"
            else:
                jobs_list +=f"• {job}: ${job_salary} :red_circle:\n\n"
        embed = nextcord.Embed(
            title="Available Jobs",
            description=jobs_list,
            color=embed_color
        )
        embed.set_footer(text= "/job <job> to get hired and start working.", icon_url=self.bot.user.avatar.url)
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(JobList(bot))