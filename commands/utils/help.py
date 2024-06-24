import nextcord
from nextcord import SlashOption, application_command
from nextcord.ext import commands
from typing import Union, List
from typing_extensions import Annotated, Literal
from main import embed_color, default_footer
from datetime import datetime
import os
import difflib


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_command_list():
        global data
        commands_list = []
        for root, _, files in os.walk('commands'):
            for file in files:
                if file.endswith('.py') and not file.startswith('_'):
                    command_name = file[:-3]
                    commands_list.append(command_name)
        return commands_list
    
    @nextcord.slash_command(name="help", description="Display commands list")
    async def help(self, interaction: nextcord.Interaction, command: str = None):
        categories = self.get_categories()

        embed = nextcord.Embed(
            title="Welcome to ALL!",
            description="ALL Bot is a multi-purpose bot that aims to make your server secure and entertain your community.\n\n"
                        f"Visit our [support server](https://discord.gg/4sExeqZnHT) to stay informed about the latest news of the bot!\n"
                        "Please select a category to view commands:",
            color=embed_color
        )
        embed.set_image(url="https://i.imgur.com/7q5WDnS.png")
        embed.timestamp = datetime.now()
        embed.set_footer(text='ALL bot', icon_url=self.bot.user.avatar.url)

        view = nextcord.ui.View()
        view.add_item(Selection(categories, self.bot, embed))

        await interaction.response.send_message(embed=embed, view=view)

    @help.on_autocomplete("command")
    async def help_autocomplete(self, interaction: nextcord.Interaction, command: str):
        input_command = command.lower()
        commands = self.get_command_list()

        similarity_scores = {cmd: difflib.SequenceMatcher(None, input_command, cmd.lower()).ratio() for cmd in commands}
        sorted_commands = sorted(similarity_scores, key=similarity_scores.get, reverse=True)
    
        top_commands = sorted_commands[:25]
        
        await interaction.response.send_autocomplete(top_commands)

    def get_categories(self):
        categories = {}
        for root, dirs, files in os.walk('commands'):
            for file in files:
                if file.endswith('.py') and not file.startswith('_'):
                    category_name = os.path.basename(root)
                    if category_name not in categories:
                        categories[category_name] = []
                    categories[category_name].append(file[:-3])
        return categories


class Selection(nextcord.ui.Select):
    def __init__(self, categories, bot, default_embed):
        options = [
            nextcord.SelectOption(label="Go Back", value="back", description="Return to the main selection menu"),
            nextcord.SelectOption(label="Moderation", value="moderation", description="Commands to manage your server"),
            nextcord.SelectOption(label="Security", value="security", description="Keep your server safe and secure"),
            nextcord.SelectOption(label="Utility", value="utils", description="Handy utilities for server management"),
            nextcord.SelectOption(label="Fun", value="fun", description="Fun and entertaining commands"),
        ]
        super().__init__(placeholder="Select a category", options=options)
        self.categories = categories
        self.bot = bot
        self.default_embed = default_embed
        self.image_url = ""
        self.images = [
            "https://i.imgur.com/KGH75xC.png",
            "https://i.imgur.com/nFg9oEk.png",
            "https://i.imgur.com/6g0hKy4.png",
            "https://i.imgur.com/oBKsAUa.png"
        ]

    async def callback(self, interaction: nextcord.Interaction):
        category = self.values[0]
        category_description = ""
        if category == "back":
            await interaction.message.edit(embed=self.default_embed)
            return
        if category == "moderation":
            self.image_url = self.images[0]
            category_description = "Here are the moderation commands of ALL"
        elif category == "security":
            self.image_url = self.images[1]
            category_description = "Here are the security based commands of ALL"
        elif category == "utils":
            self.image_url = self.images[2]
            category_description = "Here are the utility commands of ALL"
        elif category == "fun":
            self.image_url = self.images[3]
            category_description = "Here are entertaining commands of ALL"

        commands_list = self.categories.get(category, [])
        embed = nextcord.Embed(
            title=f"{category.capitalize()} Commands ({len(commands_list)})",
            description=f"{category_description}\n\n",
            color=embed_color
        )
        if commands_list:
            embed.description += "```"
            embed.description += ", ".join(f"{command}" for command in commands_list)
            embed.description += "```"
        else:
            embed.description += "No commands found for this category"
        embed.set_image(url=self.image_url)
        embed.timestamp = datetime.now()
        embed.set_footer(text='ALL bot', icon_url=self.bot.user.avatar.url)

        await interaction.message.edit(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))