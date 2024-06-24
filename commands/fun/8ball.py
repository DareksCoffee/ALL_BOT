import random
import nextcord
from nextcord.ext import commands
from main import embed_color, default_footer

class _8Ball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.positive_answers = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes, definitely.",
                                 "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.",
                                 "Yes.", "Signs point to yes."]
        self.negative_answers = ["Don't count on it.", "My sources say no.", "Outlook not so good.", "Very doubtful.",
                                 "Reply hazy, try again.", "Ask again later."]

    @nextcord.slash_command(name="8ball", description="Ask the 8ball a question")
    async def eightball(self, interaction: nextcord.Interaction, *, question):    
        """
        The magic eightball!

        Parameters
        ----------
        question:
            Ask your question.
        """

        answer = random.choice(self.positive_answers + self.negative_answers)
        emoji = ":green_circle:" if answer in self.positive_answers else ":red_circle:"
        embed = nextcord.Embed(
            title="8Ball Spoke",
            description=f"**Question**: {question}\n**Answer**: {answer} {emoji} ",
            color=embed_color
        )
        embed.set_footer(text=default_footer)
        embed.set_author(name="Requested by " + str(interaction.user), icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(_8Ball(bot))