import nextcord
from nextcord.ext import commands
from main import embed_color

class Emotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="emotes", description="Shows all the emotes of the server")
    async def emotes(self, interaction: nextcord.Interaction):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("This command can only be used in a server.")
            return
        
        static_emotes = [str(emoji) for emoji in guild.emojis if not emoji.animated]
        animated_emotes = [str(emoji) for emoji in guild.emojis if emoji.animated]
        
        static_count = len(static_emotes)
        animated_count = len(animated_emotes)

        embed = nextcord.Embed(
            title=f"Emotes in {guild.name}",
            color=embed_color
        )
        embed.description = ""

        if static_count:
            embed.title += f" | Static ({static_count}) "
            embed.description += "\n**Static Emotes:**\n" + " ".join(static_emotes)

        if animated_count:
            embed.title += f" | Animated ({animated_count}) "
            if static_count:
                embed.description += "\n\n"
            embed.description += "**Animated Emotes:**\n" + " ".join(animated_emotes)

        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Emotes(bot))