import nextcord
from nextcord.ext import commands
from main import embed_color
from emojis import Emojis
from datetime import datetime

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_thumbnail = "https://i.imgur.com/hdtXYbj.png"

    @nextcord.slash_command(name="server", description="server commands")
    async def server(self, interaction: nextcord.Interaction):
        pass

    @server.subcommand(name="info", description="Display information about the server")
    async def info(self, interaction: nextcord.Interaction):
        guild = interaction.guild
        emojis = Emojis()

        server_name = guild.name
        server_id = guild.id
        server_owner = guild.owner
        server_region = guild.region
        server_boost_level = guild.premium_tier
        member_count = guild.member_count
        creation_date = guild.created_at.strftime("%B %d, %Y")

        embed = nextcord.Embed(
            title=f"{server_name}'s Information",
            description=f"Informations regarding {server_name}",
            color=embed_color
        )
        embed.add_field(name="Server ID", value=server_id, inline=True)
        embed.add_field(name="Server Owner", value=server_owner.mention, inline=True)
        embed.add_field(name="Server Region", value=server_region, inline=True)
        embed.add_field(name="Member Count", value=member_count, inline=True)
        embed.add_field(name="Creation Date", value=creation_date, inline=True)
        embed.add_field(name="Boost level", value=f"Level {server_boost_level}", inline=True)
        embed.set_thumbnail(url="https://i.imgur.com/hdtXYbj.png" if not guild.icon else guild.icon.url)

        embed.timestamp = datetime.now()
        embed.set_footer(text='ALL bot', icon_url=self.bot.user.avatar.url)
        
        await interaction.response.send_message(embed=embed)

    @server.subcommand(name="count", description="User/Bot count for the server")
    async def count(self, interaction: nextcord.Interaction):
        guild = interaction.guild

        bot_count = sum(1 for member in guild.members if member.bot)
        user_count = guild.member_count - bot_count

        embed = nextcord.Embed(
            title="Member count",
            description=f"Server count for {guild.name}\n**Members**: {user_count}\n**Bots**: {bot_count}\n**Total** : {guild.member_count}",
            color=embed_color
        )
        embed.set_thumbnail(url="https://i.imgur.com/hdtXYbj.png" if not guild.icon else guild.icon.url)
        embed.timestamp = datetime.now()
        embed.set_footer(text='ALL bot', icon_url=self.bot.user.avatar.url)
        await interaction.response.send_message(embed=embed)
    @server.subcommand(name="configuration", description= "The server configuration for the bot")
    async def configuration(self, interaction: nextcord.Interaction):

        embed = nextcord.Embed(
            title= "Server Configuration",
            description= f"The configuration of {interaction.guild.name}\n\n",
            color= embed_color
        )
        embed.add_field(
            name="Security",
            value="Anti-Raid: `Enabled`\n"
                  "Anti-Link: `Enabled`\n"
                  "Anti-Invite: `Disabled\n`"
                  "Anti-Spam: `Enabled`\n"
            )
        embed.add_field(
            name="Misc",
            value="Leveling: `Enabled`\n"
                  "Economy: `Disabled`",
            inline=False
            )
        embed.timestamp = datetime.now()
        embed.set_footer(text='ALL bot', icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url="https://i.imgur.com/hdtXYbj.png" if not interaction.guild.icon else interaction.guild.icon.url)
        await interaction.response.send_message(embed=embed)
        

def setup(bot):
    bot.add_cog(Server(bot))