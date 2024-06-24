import nextcord
import requests
import random
from nextcord.ext import commands
from nextcord.ui import Button, View, Modal
from main import embed_color

class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = "AIzaSyCrwUVSK7TTS21sa3pfhjmy4eetxxIKF8Y"
        self.search_engine_id = "c42ed479efbab41f6"
        self.query = ""

    @nextcord.slash_command(name="search", description="Search something")
    async def search(self, interaction: nextcord.Interaction):
        pass

    @search.subcommand(name="image", description="Search an image in the World Wide Web")
    async def image(self, interaction: nextcord.Interaction, query: str):
        try:
            self.query = query
            image_url = self.get_random_image(query)
            print("Image URL:", image_url) 
            embed = nextcord.Embed(
                title=f"{query}",
                description=f"Search result for {query}",
                color=embed_color
            )
            if image_url:
                embed.set_image(url=image_url)
                message = await interaction.response.send_message(embed=embed, view=ImageView(self, embed))
            else:
                await interaction.response.send_message("No image found for the query.", ephemeral=True)
        except Exception as e:
            print("An error occurred:", e)
            await interaction.response.send_message("An error occurred while fetching the image.", ephemeral=True)

    def get_random_image(self, query):
        google_url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={self.search_engine_id}&searchType=image&key={self.api_key}"
        response = requests.get(google_url)
        image_urls = self.extract_image_urls(response.json())
        if image_urls:
            return random.choice(image_urls)
        else:
            return None

    def extract_image_urls(self, response_json):
        if 'items' in response_json:
            return [item['link'] for item in response_json['items']]
        else:
            return []

class SearchAgain(Modal):
    def __init__(self, search_cog, embed):
        super().__init__("Google")
        self.search_cog = search_cog
        self.embed = embed

        self.query = nextcord.ui.TextInput(label="Search", min_length=1, max_length=200, required=True, placeholder="Search your image")
        self.add_item(self.query)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        image_url = self.search_cog.get_random_image(self.query)
        if image_url:
            self.embed.set_image(url=image_url)
            await interaction.response.edit_message(embed=self.embed)
        else:
            await interaction.response.followup.send("No image found for the query.", ephemeral=True)

class ImageView(View):
    def __init__(self, search_cog, embed):
        super().__init__()
        self.search_cog = search_cog
        self.embed = embed

    @nextcord.ui.button(label="Next", style=nextcord.ButtonStyle.primary, emoji="⏭️")
    async def randomize_image(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        image_url = self.search_cog.get_random_image(self.search_cog.query)
        if image_url:
            self.embed.set_image(url=image_url)
            await interaction.response.edit_message(embed=self.embed)
        else:
            await interaction.response.followup.send("No image found for the query.")

    @nextcord.ui.button(label="Search again", style=nextcord.ButtonStyle.primary, emoji="🔄")
    async def search_again(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(SearchAgain(self.search_cog, self.embed))

def setup(bot):
    bot.add_cog(Search(bot))