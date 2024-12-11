import discord
import settings
import datetime
import typing
import requests
from db import MySql
from discord.ui import View
from discord import app_commands
from discord.ext import commands

class Raid(commands.GroupCog, name="raid"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.sql = MySql()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Raid Cog loaded')
   
    @app_commands.command(name="add", description="Direct add a new raid")
    @app_commands.choices(form=[
        app_commands.Choice(name="Normal", value="Normal"),
        app_commands.Choice(name="Mega", value="Mega"),
        app_commands.Choice(name="Primal", value="Primal"),
        app_commands.Choice(name="Mega X", value="Mega X"),
        app_commands.Choice(name="Mega Y", value="Mega Y"),
        app_commands.Choice(name="Alola", value="Alola"),
        app_commands.Choice(name="Altered", value="Altered"),
        app_commands.Choice(name="Attack", value="Attack"),
        app_commands.Choice(name="Burn", value="Burn"),
        app_commands.Choice(name="Chill", value="Chill"),
        app_commands.Choice(name="Defense", value="Defense"),
        app_commands.Choice(name="Douse", value="Douse"),
        app_commands.Choice(name="Galarian", value="Galarian"),
        app_commands.Choice(name="Gigantamax", value="Gigantamax"),
        app_commands.Choice(name="Hisuian", value="Hisuian"),
        app_commands.Choice(name="Incarnate", value="Incarnate"),
        app_commands.Choice(name="Origin", value="Origin"),
    ])
    @app_commands.describe(wb="Is it weather boosted?")
    @app_commands.choices(wb=[
        app_commands.Choice(name="No", value="No"),
        app_commands.Choice(name="Yes", value="Yes")
    ])
    async def raid_add(self, interaction: discord.Interaction, form: typing.Optional[app_commands.Choice[str]], pokemon: str, wb: typing.Optional[app_commands.Choice[str]]) -> None:
        user_check = self.sql.getProfile(interaction.user.id)
        if user_check:
            channelID = self.sql.getChannel(interaction.channel_id)
            try:
                api_url=f"https://pokemon-go-api.github.io/pokemon-go-api/api/pokedex/name/{pokemon.upper()}.json"
                response = requests.get(api_url)
                data = response.json()
                
                EMform = ""
                EMwb = ""

                if form:
                    EMform = f"{form.value}"
                    
                if wb:
                    EMwb = "(WB)"

                if EMform == "":
                    EMimage = data['assets']['image']
                else:
                    SearchForm = EMform.replace(" ", "_")
                    for assetsForm in data['assetForms']:
                        if assetsForm['form'] == SearchForm.upper():
                            EMimage = assetsForm['image']

                raidAddEmbed = discord.Embed(
                    title=f"{EMform} {data['names'][settings.LANGUAGE].capitalize()} #{data['dexNr']} {EMwb}", 
                    description=f"If you want to join this raid, please press join below\nPlease be sure to add the host before the raid starts, the code is\n**{str(user_check[0][1])}**",
                    color=0x2ecc71
                )
                
                raidAddEmbed.set_thumbnail( url=EMimage )
                raidAddEmbed.add_field(name=f"Type", value=f"{data['primaryType']['names'][settings.LANGUAGE]}", inline=True)  
                raidAddEmbed.set_footer(text=f"Added by {interaction.user.display_name}" )
                channelrole = discord.AllowedMentions(roles=True)
                view = raidView(interaction.user.id, user_check[0][0], data, channelID)
                await interaction.response.send_message(content=f"{data['names'][settings.LANGUAGE].capitalize()} - <@{interaction.user.id}> - <@&{channelID[0][3]}>", view=view, embed=raidAddEmbed,allowed_mentions=channelrole, delete_after=settings.RAIDTIMEOUT )
            except:
                await interaction.response.send_message("The pokemon you wanted to add could not be found in the dex.\nAre you sure it's written correctly?", delete_after=settings.MESSAGETIMEOUT, ephemeral=True)
        else:
            await interaction.response.send_message(f"You need to register in the bot before you can add raids", delete_after=settings.MESSAGETIMEOUT, ephemeral=True)

class raidView(View):
    def __init__(self, author, username, data, channelID, timeout=600):
        super().__init__(timeout=timeout)
        self.author = author
        self.participants = []
        self.participants_nr = 0
        self.joined = ''
        self.pokemonData = data
        self.username = username
        self.channelID = channelID
        self.sql = MySql()
        self.value = None
        self.now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @discord.ui.button(label="Join (0)", style=discord.ButtonStyle.green, custom_id="join")
    async def join_callback(self, interaction, button):
        user_check = self.sql.getProfile( interaction.user.id)
        if user_check:
            if interaction.user not in self.participants:
                self.participants_nr += 1
                self.participants.append(interaction.user.id)
                button.label=f"Join ({self.participants_nr})"
                await interaction.response.edit_message(view=self)
            else:
                await interaction.response.send_message(f"You already joined", delete_after=settings.ERRORTIMEOUT, ephemeral=True)
        else:
            await interaction.response.send_message("You must create a profile before you can join", delete_after=settings.ERRORTIMEOUT, ephemeral=True)
        
    @discord.ui.button(label="Leave", style=discord.ButtonStyle.danger, custom_id="dropout")
    async def dropout_callback(self, interaction, button):
        if interaction.user in self.participants:
            self.participants_nr -= 1
            self.participants.remove(interaction.user)

            join = [x for x in self.children if x.custom_id=="join"][0]
            join.label=f"Join ({self.participants_nr})"
            await interaction.response.edit_message(view=self)
        return await interaction.response.send_message(f"You must first join", delete_after=settings.ERRORTIMEOUT, ephemeral=True)

    @discord.ui.button(label="Start", style=discord.ButtonStyle.grey, custom_id="start")
    async def start_callback(self, interaction, button):
        if self.author == interaction.user.id:
            if self.participants_nr != 0:
                i=1
                j=1
                participantPrint = ""

                self.sql.addRaidStat(str(self.author), str(self.channelID[0][1]), str(self.pokemonData["id"].lower()))
                self.sql.profileChange('`raids_hosted` = raids_hosted +1', str(self.author))

                for singlePart in self.participants:
                    participantPrint += f"{singlePart}\n"

                raidStartEmbed = discord.Embed(
                    title=self.pokemonData["id"].capitalize(),
                    description=f"**The raid is now starting**", 
                    color=0x9b59b6
                )

                raidStartEmbed.set_thumbnail(url=self.pokemonData['assets']['image'])
                raidStartEmbed.add_field(name=f"Type", value=f"{self.pokemonData['primaryType']['names'][settings.LANGUAGE]}", inline=True)  
                raidStartEmbed.add_field(name=f"Sending invites to", value=participantPrint, inline=False)
                raidStartEmbed.set_footer(text=f"Added by {self.username}" )
                await interaction.response.edit_message(content=None, embed=raidStartEmbed, view=None)
                embedParticipants = self.sql.startRaid(self.participants)
                
                for singleJoined in embedParticipants:
                    self.joined += str(singleJoined[1][0:7])

                    if j == 4:
                        await interaction.followup.send(self.joined, ephemeral=True)
                        self.joined=''
                        j=1
                    else:
                        self.joined+=','
                        j+=1
                        
                if self.joined!='':
                    await interaction.followup.send(self.joined, ephemeral=True)
            else:
                await interaction.response.send_message("No one joined your raid. It's therefore deleted", ephemeral=True, delete_after=settings.MESSAGETIMEOUT)
                await interaction.message.delete()
        else:
            await interaction.response.send_message(f"💀 You are not allowed to start the raid", ephemeral=True, delete_after=settings.ERRORTIMEOUT)

      
    @discord.ui.button(label="Delete", style=discord.ButtonStyle.grey, custom_id="delete")
    async def delete_callback(self, interaction, button):
        if self.author == interaction.user.id:
            await interaction.message.delete()
            print(f"{self.now} - Raid Deleted")
        else:    
            await interaction.response.send_message(f"💀 You are not allowed to delete the raid", ephemeral=True, delete_after=settings.ERRORTIMEOUT)
       
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Raid(bot), guilds=[discord.Object(id=settings.DEFAULT_GUILD)])