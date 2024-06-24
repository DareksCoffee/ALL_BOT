import nextcord
from nextcord.ext import commands
from main import embed_color, default_footer

class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="about", description="Information regarding ALL")
    async def about(self, interaction: nextcord.Interaction):
        server_count = len(self.bot.guilds)
        member_count = sum(guild.member_count for guild in self.bot.guilds)

        embed = nextcord.Embed(
            title="About ALL",
            description="ALL is a security/moderation bot that aims to make your Discord server more secure.",
            color=embed_color
        )
        embed.add_field(name="Server Count", value=f"ALL is in {server_count} servers with over {member_count} members.", inline=True)
        embed.add_field(name="Additional Information", value="ALL is made with nextcord python and is fully Open-Source.", inline=True)
        embed.add_field(name="Credits", value="ALL is made and hosted by wdarek.", inline=True)
        embed.set_image(url="https://i.imgur.com/AVa3wtk.png")
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(About(bot))