import nextcord
from nextcord.ext import commands
from datetime import datetime
from main import embed_color

class Selection(nextcord.ui.Select):
    def __init__(self, bot):
        options = [
            nextcord.SelectOption(label="Go Back", description="Go back to the introduction"),
            nextcord.SelectOption(label="Admin Helper", description="Powerful moderation bot")
        ]
        super().__init__(placeholder="Select a bot", options=options)
        self.bot = bot

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == "Go Back":
            embed = nextcord.Embed(
                title="Discover our partners",
                description="Partnering with us facilitates widespread recognition across other Discord servers, benefiting both our partnered and ALL's bot.",
                color=embed_color
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.add_field(name="Want to be a partner with us?", value="Please contact one of the developers in our [support server](https://discord.gg/4sExeqZnHT).", inline=False)
            embed.timestamp = datetime.now()
            embed.set_footer(text='ALL bot', icon_url=self.bot.user.avatar.url)
            await interaction.message.edit(embed=embed)
        elif self.values[0] == "Admin Helper":
            embed = nextcord.Embed(
                title="Admin Helper",
                description="Admin Helper is perfect for communities of all sizes. It offers numerous detailed commands and a free advertisement feature to promote your Discord server. Additionally, it provides many user-friendly and modern moderation tools.",
                color=embed_color
            )
            embed.add_field(name="Information", value="**Server count**: 60\n**(approx.) Application commands**: 60+\n**TopGG page**: [click here](https://top.gg/bot/982628261718798384)", inline=False)
            embed.add_field(name="Feeling interested?", value="Invite [Admin Helper](https://discord.com/api/oauth2/authorize?client_id=982628261718798384&permissions=67546916454103&scope=bot) to your community and join the [support server](https://discord.gg/Q7APUuwT76) if you wish to inquire additional information and receive the latest updates of the bot.")
            embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/BIHuCtsegn7rv_aKqBgxahOGQl7uNhfeAZb3dDuoUzU/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/982628261718798384/a_c9355b70f0f9cc3c1fd0ea829731d468.gif?width=300&height=300")
            embed.timestamp = datetime.now()
            embed.set_footer(text='Developer: veryappropriatename | ID: 545015390020042752', icon_url="https://images-ext-1.discordapp.net/external/BIHuCtsegn7rv_aKqBgxahOGQl7uNhfeAZb3dDuoUzU/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/982628261718798384/a_c9355b70f0f9cc3c1fd0ea829731d468.gif?width=300&height=300")
            await interaction.message.edit(embed=embed)

class SelectionView(nextcord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.add_item(Selection(bot))

class Partners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="partner", description="partner commands")
    async def partner(self, interaction: nextcord.Interaction):
        pass

    @partner.subcommand(name="discover", description="discover ALL's bot partners")
    async def discover(self, interaction: nextcord.Interaction):
        view = SelectionView(self.bot)
        embed = nextcord.Embed(
            title="Discover our partners",
            description="Partnering with bots facilitates widespread recognition across other Discord servers, benefiting both our partnered and ALL's bot.",
            color=embed_color
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name="Want to be a partner with us?", value="Please contact one of the developers in our [support server](https://discord.gg/4sExeqZnHT).", inline=False)
        embed.timestamp = datetime.now()
        embed.set_footer(text='ALL bot', icon_url=self.bot.user.avatar.url)
        await interaction.response.send_message(embed=embed, view=view)

def setup(bot):
    bot.add_cog(Partners(bot))