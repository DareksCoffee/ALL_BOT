import nextcord
from nextcord.ext import commands
from PIL import Image
import imghdr
from io import BytesIO

class ImageManipulation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="image", description="Image manipulation")
    async def image(self, interaction: nextcord.Interaction):
        pass
    
    @image.subcommand(name="togif", description="Convert image to GIF")
    async def gif(self, interaction: nextcord.Interaction, file: nextcord.Attachment):
        """
        Convert image to GIF

        Parameters
        ----------
        file:
            Choose an attachment
        """
        message = await interaction.response.send_message("Processing...")
        image_data = await file.read()
        image_format = imghdr.what(None, h=image_data)
        if image_format in ['jpeg', 'png', 'gif']:
            with Image.open(BytesIO(image_data)) as img:
                gif_path = f"{file.filename}.gif"
                img.save(gif_path, save_all=True, append_images=[img], loop=0, duration=100)
                await message.edit(content="", file=nextcord.File(gif_path))
        else:
            await message.edit(content="Please provide a valid image file.")
    @image.subcommand(name="spin", description="Spin the image")
    async def spin(self, interaction: nextcord.Interaction, file: nextcord.Attachment):
        """
        Spin the image

        Parameters
        ----------
        file:
            Choose an attachment
        """
        await interaction.response.defer()

        image_data = await file.read() 

        with Image.open(BytesIO(image_data)) as img:
            img_resized = img.resize((600, 600))
            frames = [img_resized.rotate(angle) for angle in range(0, 360, 30)]
            gif_bytes = BytesIO() 
            frames[0].save(gif_bytes, format="GIF", save_all=True, append_images=frames[1:], duration=85, loop=0)
            gif_bytes.seek(0) 

        await interaction.followup.send(file=nextcord.File(gif_bytes, filename="spinnyimage.gif"))

    @image.subcommand(name="zoom", description="Zoom in and out of the image")
    async def zoom(self, interaction: nextcord.Interaction, file: nextcord.Attachment):
        """
        Zoom in and out of the image

        Parameters
        ----------
        file:
            Choose an attachment
        """
        await interaction.response.defer()

        image_data = await file.read()

        with Image.open(BytesIO(image_data)) as img:
            original_size = img.size
            zoomed_frames = []

            # Zoom out
            for scale in range(100, 50, -5):
                resized_img = img.resize((int(original_size[0] * scale / 100), int(original_size[1] * scale / 100)), resample=Image.BICUBIC)
                zoomed_frames.append(resized_img)

            # Zoom in
            for scale in range(50, 101, 5):
                resized_img = img.resize((int(original_size[0] * scale / 100), int(original_size[1] * scale / 100)), resample=Image.BICUBIC)
                zoomed_frames.append(resized_img)

            gif_bytes = BytesIO()
            zoomed_frames[0].save(
                gif_bytes,
                format="GIF",
                save_all=True,
                append_images=zoomed_frames[1:],
                duration=100,
                loop=0,  
            )
            gif_bytes.seek(0)

        await interaction.followup.send(file=nextcord.File(gif_bytes, filename="crazy.gif"))
def setup(bot):
    bot.add_cog(ImageManipulation(bot))
