import nextcord
from nextcord.ext import commands
from main import embed_color

class ListBans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="banlist", description="List all banned users")
    async def banlist(self, interaction: nextcord.Interaction):
        banned_users = interaction.guild.bans()
        users = ""
        ban_count = 0
        
        async for ban_entry in banned_users:
            user = ban_entry.user
            users += f"{user.name} | {user.id}\n"
            ban_count += 1
            
        embed = nextcord.Embed(
            title="Ban List",
            description=f"There are {ban_count} banned users\n{users}",
            color=embed_color
        )
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(ListBans(bot))