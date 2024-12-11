import discord
import settings
import re
import lang
import datetime
import os
from db import MySql
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw

class Stats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.sql = MySql()
        self.now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @commands.Cog.listener()
    async def on_ready(self):
        print('Stats Cog loaded')

    @app_commands.command(name="stats", description="Displays stats over top players or groups")
    @app_commands.describe(stats="View stats")
    @app_commands.choices(stats=[
        app_commands.Choice(name="Players", value="Players"),
        app_commands.Choice(name="Groups", value="Groups"),
        app_commands.Choice(name="My own", value="My own"),
        ])
    async def raid_add(self, interaction: discord.Interaction, stats: str):
        dir = os.getcwd()

        if stats == "Players":
            height = 290
            result = self.sql.playerStats()
            main_image = Image.open(f"{dir}\\assets\\img\\top10players.jpg")
            title_font = ImageFont.truetype(f"{dir}\\assets\\font\\TangoSans.ttf", 20)
            image_editable = ImageDraw.Draw(main_image)
            header_font = ImageFont.truetype(f"{dir}\\assets\\font\\TangoSans.ttf", 50)
            image_editable.text((272,102), f"Top 10 Players", (0,0,0), font=header_font)
            image_editable.text((270,100), f"Top 10 Players", (255,255,255), font=header_font)

            for player in result:
                image_editable.text((70,height), player[0], (255,255,255), font=title_font),
                image_editable.text((490,height), f"Hosted {str(player[2])}", (255,255,255), font=title_font),
                image_editable.text((640,height), f"Joined {str(player[1])}", (255,255,255), font=title_font)
                height = height+40

            image_path = f"{dir}\\assets\\img\\screens\\"
            main_image.save(f"{image_path}top10players.jpg")

            await interaction.response.send_message(file=discord.File(f"{image_path}top10players.jpg"), ephemeral=True)
        elif stats == "Groups":
            height = 310
            result = self.sql.groupStats()
            
            main_image = Image.open(f"{dir}\\assets\\img\\ttc_groups.jpg")
            title_font = ImageFont.truetype(f"{dir}\\assets\\font\\TangoSans.ttf", 30)
            image_editable = ImageDraw.Draw(main_image)
            header_font = ImageFont.truetype(f"{dir}\\assets\\font\\TangoSans.ttf", 70)
            image_editable.text((272,102), f"Groups", (0,0,0), font=header_font)
            image_editable.text((270,100), f"Groups", (255,255,255), font=header_font)

            for group in result:
                getName = group[0].split("-")
                channel = re.sub(r'[^a-zA-Z0-9]', '',getName[0])
                image_editable.text((90,height), f"{channel}", (255,255,255), font=title_font),
                image_editable.text((600,height), f"{group[1]}", (255,255,255), font=title_font)
                height = height+50

            image_path = f"{dir}\\assets\\img\\screens\\"
            main_image.save(f"{image_path}ttc_groups.jpg")

            await interaction.response.send_message(file=discord.File(f"{image_path}ttc_groups.jpg"), ephemeral=True)
        elif stats == "My own":
            result = self.sql.ownStats(interaction.user.id)
            embed = discord.Embed(
                title=f"{interaction.user.name}'s Stats", 
                color=0x2ecc71
            )
            embed.add_field(name="Trainer code", value=f"{result[0][3]}", inline=True)
            embed.add_field(name="Level", value=f"{result[0][4]}", inline=True)
            embed.add_field(name="Country", value=f"{result[0][5]}", inline=True)
            embed.add_field(name="Team", value=f"{result[0][6]}", inline=True)
            embed.add_field(name="Raids Joined", value=f"{result[0][7]}", inline=True)
            embed.add_field(name="Raids Hosted", value=f"{result[0][8]}", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else: 
            await interaction.response.send_message(lang.PROFILE_ADMIN_ERROR, delete_after=15.0, ephemeral=True)

    
       
async def setup(bot):
    await bot.add_cog(Stats(bot), guilds=[discord.Object(id=settings.DEFAULT_GUILD)])