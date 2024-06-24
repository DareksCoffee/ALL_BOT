import nextcord
from nextcord.ext import commands, application_checks
import aiosqlite
from main import embed_color, ThrowError
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.levelup_background = "https://i.imgur.com/32U2iim.png"
    def xp_for_level(self, level):
        return 100 * level

    @nextcord.slash_command(name="level", description="Leveling")
    async def level(self, interaction: nextcord.Interaction):
        pass

    @level.subcommand()
    async def profile(self, interaction: nextcord.Interaction, user: nextcord.Member = None):
        image_path = ".\\assets\\levelup-background.png"
        title_font_path = ".\\assets\\fonts\\Ginto_Nord_Black.ttf"
        regular_font_path = ".\\assets\\fonts\\Ginto_Medium.ttf"
        
        try:
            image = Image.open(image_path)
            guild_id = interaction.guild.id
            user_id = interaction.user.id if not user else user.id
            if not user:
                user = interaction.user
            if user.bot:
                await ThrowError(interaction=interaction, error="", error_type="Leveling")

            if await self.is_leveling_enabled(guild_id):
                async with aiosqlite.connect("leveling.db") as db:
                    async with db.execute('SELECT xp, level FROM levels WHERE guild_id = ? AND user_id = ?', (guild_id, user_id)) as cursor:
                        result = await cursor.fetchone()
                        if result:
                            xp, level = result
                            required_xp = self.xp_for_level(level + 1)

                            avatar_url = user.avatar.url
                            avatar_response = requests.get(avatar_url)
                            user_avatar = Image.open(BytesIO(avatar_response.content))
                            
                            avatar_size = (135, 135)
                            user_avatar = user_avatar.resize(avatar_size)

                            mask = Image.new("RGBA", avatar_size, (0, 0, 0, 0))
                            draw = ImageDraw.Draw(mask)
                            draw.ellipse((0, 0) + avatar_size, fill=(255, 255, 255, 255))

                            user_avatar.putalpha(mask.split()[3])

                            draw = ImageDraw.Draw(image)
                            display_name = user.global_name if user.global_name else user.name
                            username = user.name
                            text_color = (255, 255, 255)  
                            display_font = ImageFont.truetype(title_font_path, 36)
                            name_font = ImageFont.truetype(title_font_path, 16)

                            display_name_x_position, display_name_y_position = 319,50
                            name_x_position, name_y_position = 340,85

                            level_x_position, level_y_position = 319, 120
                            xp_x_position, xp_y_position = 319, 140

                            level_text = f"LEVEL: {level}"
                            xp_text = f"XP: {xp}/{required_xp}"

                            avatar_position = (50, 25) 
                            image.paste(user_avatar, avatar_position, user_avatar)
                            test = draw.textlength("test", font=title_font_path)
                            print(test)
                            draw.text((display_name_x_position, display_name_y_position), display_name, fill=text_color, font=display_font)
                            draw.text((name_x_position, name_y_position), username, fill=text_color, font=name_font)

                            draw.text((level_x_position, level_y_position), level_text, fill=text_color, font=name_font)
                            draw.text((xp_x_position, xp_y_position), xp_text, fill=text_color, font=name_font)

                            modified_image_bytes = BytesIO()
                            image.save(modified_image_bytes, format="PNG")
                            modified_image_bytes.seek(0)

                            await interaction.response.send_message(content=f"The profile for {user.name}", file=nextcord.File(modified_image_bytes, "crazy.png"))
                        else:
                            await ThrowError(interaction=interaction, error="You have not talked in the server yet!", error_type="Leveling")
            else:
                await ThrowError(interaction=interaction, error="Leveling is not enabled in this server.\nUse `/toggle_leveling` if you are the server administrator.", error_type="Leveling")
        except FileNotFoundError:
            await interaction.response.send_message("I got an error lol")
    @level.subcommand()
    @application_checks.has_permissions(administrator=True)
    async def add_xp(self, interaction: nextcord.Interaction, user: nextcord.Member, xp: int):
        guild_id = interaction.guild.id
        user_id = user.id

        if await self.is_leveling_enabled(guild_id):
            async with aiosqlite.connect("leveling.db") as db:
                async with db.execute('SELECT xp, level FROM levels WHERE guild_id = ? AND user_id = ?', (guild_id, user_id)) as cursor:
                    result = await cursor.fetchone()
                    if result:
                        current_xp, level = result
                        new_xp = current_xp + xp

                        while new_xp >= self.xp_for_level(level + 1):
                            level += 1
                            new_xp -= self.xp_for_level(level)
                        
                        await db.execute('UPDATE levels SET xp = ?, level = ? WHERE guild_id = ? AND user_id = ?', (new_xp, level, guild_id, user_id))
                        await db.commit()
                        await interaction.response.send_message(content=f"Successfully added {xp} XP to {user.display_name}.")
                    else:
                        await ThrowError(interaction=interaction, error="User not found in database.", error_type="Leveling")
        else:
            await ThrowError(interaction=interaction, error="Leveling is not enabled in this server.\nUse `/toggle_leveling` if you are the server administrator.", error_type="Leveling")

    async def is_leveling_enabled(self, guild_id):
        async with aiosqlite.connect("leveling.db") as db:
            async with db.execute('SELECT enabled FROM leveling_enabled WHERE guild_id = ?', (guild_id,)) as cursor:
                result = await cursor.fetchone()
                return result[0] if result else True

def setup(bot):
    bot.add_cog(Level(bot))