import discord
import lang
import datetime
import settings
import re
from db import MySql
from discord import app_commands
from discord.ext import commands

class Profile(commands.GroupCog, name="profile"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.sql = MySql()

    #Sync commands
    @commands.command()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.message.delete()
        await ctx.send(f'Synced {len(fmt)} commands', delete_after=settings.MESSAGETIMEOUT)

    @commands.Cog.listener()
    async def on_ready(self):
        print(lang.PROFILE_COG_LOADED)
    

    @app_commands.command(name="setup", description=lang.PROFILE_SETUP)
    async def profile_setup(self, interaction: discord.Interaction) -> None:
        user_check = self.sql.getProfile( interaction.user.id)
        if not user_check:
            await interaction.response.send_modal(SetupModal())
        else:
            await interaction.response.send_message(lang.PROFILE_EXISTS, ephemeral=True, delete_after=settings.ERRORTIMEOUT)

    @app_commands.command(name="change", description=lang.PROFILE_CHANGE)
    async def profile_change(self, interaction: discord.Interaction) -> None:
        user_check = self.sql.getProfile( interaction.user.id)
        if not user_check:
            await interaction.response.send_message(lang.PROFILE_NOT_FOUND, ephemeral=True, delete_after=settings.ERRORTIMEOUT)
        else:
            await interaction.response.send_modal(ChangeModal())

    @app_commands.command(name="delete", description=lang.PROFILE_DELETE_DESC)
    async def profile_delete(self, interaction: discord.Interaction) -> None:
        user_check = self.sql.getProfile( interaction.user.id)
        if not user_check:
            await interaction.response.send_message(lang.PROFILE_NOT_FOUND, ephemeral=True, delete_after=settings.ERRORTIMEOUT)
        else:
            self.sql.deleteProfile(interaction.user.id)
            await interaction.response.send_message(lang.PROFILE_DELETED, ephemeral=True, delete_after=settings.MESSAGETIMEOUT)

def cleanTC(string):
    if ' ' in string:
        tc = string.replace(" ", "")
        trainercode = " ".join(tc[i:i+4] for i in range(0, len(tc), 4))
    else:
        trainercode = " ".join(string[i:i+4] for i in range(0, len(string), 4))
    return trainercode

class SetupModal(discord.ui.Modal, title="Setup a Profile"):

    ign = discord.ui.TextInput(label="Ingame Name", style=discord.TextStyle.short, placeholder="Ingame Name", required=True, max_length=20)
    trainercode = discord.ui.TextInput(label="Trainer Code", style=discord.TextStyle.short, placeholder="Trainer Code", required=False, max_length=15)
    level = discord.ui.TextInput(label="Level", style=discord.TextStyle.short, placeholder="Level 1-50", required=False, max_length=2)
    country = discord.ui.TextInput(label="Country", style=discord.TextStyle.short, placeholder="Country",  required=False, max_length=30)
    team = discord.ui.TextInput(label="Team", style=discord.TextStyle.short, placeholder="Mystic/Instinct/Valor", required=False, max_length=21)
    
    async def on_submit(self, interaction:discord.Interaction):
        ign = re.sub(r'[^a-zA-Z0-9]', '',self.ign.value)
        if self.team.value:
            teamValue = re.sub(r'[^a-zA-Z]', '',self.team.value)
            if teamValue[0].lower() == 'm':
                team = 'Mystic'
            elif teamValue[0].lower() == 'i':
                team = 'Instinct'
            elif teamValue[0].lower() == 'v':
                team = 'Valor'
        else:
            team = ''
            
        level = re.sub(r'[^0-9]', '',self.level.value)
        country = re.sub(r'[^a-zA-Z]', '',self.country.value)
        trainercode = cleanTC(self.trainercode.value)
        MySql().profileSetup(interaction.user.id, interaction.user.display_name, ign, trainercode, level, country, team)
        await interaction.response.send_message(f"{lang.PROFILE_CREATED}", ephemeral=True, delete_after=settings.MESSAGETIMEOUT)


class ChangeModal(discord.ui.Modal, title="Change a Profile"):
    ign = discord.ui.TextInput(label="Ingame Name", style=discord.TextStyle.short, placeholder="Ingame Name", required=False, max_length=20)
    trainercode = discord.ui.TextInput(label="Trainer Code", style=discord.TextStyle.short, placeholder="Trainer Code", required=False, max_length=15)
    level = discord.ui.TextInput(label="Level", style=discord.TextStyle.short, placeholder="Level 1-50", required=False, max_length=2)
    country = discord.ui.TextInput(label="Country", style=discord.TextStyle.short, placeholder="Country",  required=False, max_length=30)
    team = discord.ui.TextInput(label="Team", style=discord.TextStyle.short, placeholder="Mystic/Instinct/Valor", required=False, max_length=21)

    async def on_submit(self, interaction:discord.Interaction):
        queryString = ""

        if self.ign.value:
            ign = re.sub(r'[^a-zA-Z0-9]', '',self.ign.value)
            queryString += f"`ingame_name` = '{ign}' ,"
        if self.trainercode.value:
            trainercode = cleanTC(self.trainercode.value)
            queryString += f"`trainer_code` = '{trainercode}' ,"
        if self.level.value:
            level = re.sub(r'[^0-9]', '',self.level.value)
            queryString += f"`level` = '{level}' ,"
        if self.country.value:
            queryString += f"`country` = '{self.country.value}' ,"
        if self.team.value:
            teamValue = re.sub(r'[^a-zA-Z]', '',self.team.value)
            if teamValue[0].lower() == 'm':
                team = 'Mystic'
            elif teamValue[0].lower() == 'i':
                team = 'Instinct'
            elif teamValue[0].lower() == 'v':
                team = 'Valor'
            queryString += f"`team` = '{team}' ,"
        MySql().profileChange(queryString, interaction.user.id)
        await interaction.response.send_message(f"{lang.PROFILE_UPDATED}", ephemeral=True, delete_after=settings.MESSAGETIMEOUT)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Profile(bot), guilds=[discord.Object(id=settings.DEFAULT_GUILD)])