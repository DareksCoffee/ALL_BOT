import nextcord
from nextcord.ext import commands
from main import embed_color, default_footer

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="invite", description="Receive the link to invite ALL")
    async def invite(self, interaction: nextcord.Interaction):
        server_count = len(self.bot.guilds)
        member_count = sum(guild.member_count for guild in self.bot.guilds)

        embed = nextcord.Embed(
            title="Invite ALL",
            description="[Click here](https://discord.com/oauth2/authorize?client_id=826513811393609798&permissions=8&scope=bot%20applications.commands) to invite me on your server!",
            color=embed_color
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Invite(bot))