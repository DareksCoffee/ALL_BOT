import nextcord
from nextcord.ext import commands
from main import embed_color, default_footer

class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_title = "Generic Title"
        self.default_description = "This is a default description!"
        self.default_thumbnail = "https://i.imgur.com/hdtXYbj.png"
        self.default_image = "https://i.imgur.com/hdtXYbj.png"

    @nextcord.slash_command(name="embed", description="create an embed message")
    async def embed(
        self,
        interaction: nextcord.Interaction,
        title: str = None,
        description: str = None,
        footer_text: str = None,
        color: str = None,
        thumbnail: str = None,
        image: str = None
    ):
        """
        Make an embed message!

        Parameters
        ----------
        title:
            Title of the embed.
        description:
            Description of the embed.
        footer_text:
            The footer text of the embed.
        color:
            The color of the embed (in HEX)
        thumbnail:
            Thumbnail of the embed (url)
        image:
            The image of the embed.    
        """

        title = self.default_title if title is None else title
        description = self.default_description if description is None else description
        if color is None:
            color = embed_color
        else:
            color = int(color.lstrip('#'), 16)

        embed = nextcord.Embed(
            title=title,
            description=description,
            color=color
        )
        if thumbnail is not None:
            embed.set_thumbnail(url=thumbnail)
        if image is not None:
            embed.set_image(url=image)
        if footer_text is not None:
            embed.set_footer(text=footer_text)

        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Embed(bot))