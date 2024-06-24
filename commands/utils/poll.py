import nextcord
from nextcord.ext import commands
from main import embed_color

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.poll_results_requested = set()

    async def calculate_poll_result(self, message, interaction):
        one_count = 0
        two_count = 0
        for reaction in message.reactions:
            if reaction.emoji == "1️⃣":
                one_count = reaction.count - 1
            elif reaction.emoji == "2️⃣":
                two_count = reaction.count - 1

        total_votes = one_count + two_count
        if total_votes > 0:
            one_percentage = (one_count / total_votes) * 100
            two_percentage = (two_count / total_votes) * 100

            poll_title = message.embeds[0].title
            description = message.embeds[0].description.split("\n")
            choice1 = description[0].replace(":one:", "")
            choice2 = description[2].replace(":two:", "")

            bar_length = 20
            remaining_space = '░' * bar_length

            one_bar = '█' * bar_length
            two_bar = '█' * bar_length

            one_blocks = int(one_percentage / 100 * bar_length)
            two_blocks = int(two_percentage / 100 * bar_length)
            one_bar = '█' * one_blocks + '░' * (bar_length - one_blocks)
            two_bar = '█' * two_blocks + '░' * (bar_length - two_blocks)

            result_embed = nextcord.Embed(
                title=poll_title,
                description=f"{choice1}:\n{one_bar} ({one_percentage:.2f}%) \n{choice2}:\n{two_bar} ({two_percentage:.2f}%)",
                color=embed_color
            )
            await interaction.response.send_message(embed=result_embed)
        else:
            await interaction.response.send_message("No votes recorded for this poll.")


    @nextcord.slash_command(name="poll", description="Create a poll!")
    async def poll(self, interaction: nextcord.Interaction):
        pass

    @poll.subcommand(name="create", description="Create a poll")
    async def create(self, interaction: nextcord.Interaction, message: str, choice1: str, choice2: str):
        poll = nextcord.Embed(
            title=f"Poll: {message}",
            description=f":one: {choice1}\n\n:two: {choice2}",
            color=embed_color
        )
        poll.set_footer(text=f"Poll by {interaction.user}")
        embed = nextcord.Embed(
            description="Successfully created poll.",
            color=embed_color
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)
        poll_message = await interaction.send(embed=poll)

        await poll_message.add_reaction("1️⃣")
        await poll_message.add_reaction("2️⃣")

    @poll.subcommand(name="result", description="Get the result of a poll")
    async def poll_result(self, interaction: nextcord.Interaction, message_id: str):
        channel = interaction.channel
        message = await channel.fetch_message(message_id)
        if message.author == self.bot.user and len(message.embeds) > 0 and message.embeds[0].title.startswith("Poll:"):
            self.poll_results_requested.add(message.id)
            await self.calculate_poll_result(message, interaction)
        else:
            await interaction.response.send_message("Invalid poll message ID or no poll found.", ephemeral=True)

def setup(bot):
    bot.add_cog(Poll(bot))