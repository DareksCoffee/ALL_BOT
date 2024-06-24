import nextcord
from nextcord import SlashOption
from nextcord.ext import commands
import random

class Rps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="rps", description="Play Rock-Paper-Scissors with the bot")
    async def rps(self, interaction: nextcord.Interaction, choice: str = SlashOption(name="choice", description="Choose between Rock, Paper, and Scissors", choices=["Rock", "Paper", "Scissors"])):
        """
        Rock, paper, scissors!

        Parameters
        ----------
        choice:
            Choose between Rock, Paper, and Scissors.
        """
        choices = ["rock", "paper", "scissors"]
        player_choice = choice.lower()

        bot_choice = random.choice(choices)

        if player_choice == bot_choice:
            result = "It's a tie!"
        elif (player_choice == "rock" and bot_choice == "scissors") or \
             (player_choice == "paper" and bot_choice == "rock") or \
             (player_choice == "scissors" and bot_choice == "paper"):
            result = "You win!"
        else:
            result = "You lose!"

        await interaction.response.send_message(f"You chose {choice}. I chose {bot_choice}. {result}")

def setup(bot):
    bot.add_cog(Rps(bot))