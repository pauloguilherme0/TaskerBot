import discord
import os

from discord import app_commands
from discord.ext import commands

from dropdown import DropdownView, DropdownTicketView
from atividade_manager import AtividadeManager
from enums import Status, Tags

def ajuda(tree: app_commands.CommandTree, manager: AtividadeManager):
    @tree.command(guild=None, name='ajuda', description='Mostra uma lista de comandos disponíveis.')
    async def _ajuda(interaction: discord.Interaction):
        embed = discord.Embed(title="Lista de Comandos", description="Aqui estão todos os comandos disponíveis:", color=discord.Color.blue())

        embed.add_field(name="/inserir <nome> <status> <tag>", value="Insere uma nova atividade no banco de dados", inline=False)
        embed.add_field(name="/listar", value="Lista todas as atividades do banco de dados", inline=False)
        embed.add_field(name="/limpar", value="Limpa todas as atividades do banco de dados", inline=False)

        await interaction.response.send_message(embed=embed)

def inserir(tree: app_commands.CommandTree, manager: AtividadeManager):
    @tree.command(guild=None, name='inserir', description='Insere uma nova atividade no banco de dados')
    async def _inserir(interaction: discord.Interaction, nome: str, status: Status, tag: Tags):
        user_id = interaction.user.id
        server_id = interaction.guild.id
        manager.inserir_atividade(nome, status.value, tag.value, user_id, server_id)
        await interaction.response.send_message(f"Atividade {nome} inserida com sucesso.")

def limpar(tree: app_commands.CommandTree, manager: AtividadeManager):
    @tree.command(guild=None, name='limpar', description='Limpa todas as atividades do banco de dados')
    async def _limpar(interaction: discord.Interaction):
        manager.limpar_atividades()
        await interaction.response.send_message("Todas as atividades foram removidas.")

def listar(tree: app_commands.CommandTree, manager: AtividadeManager):
    @tree.command(guild=None, name='listar', description='Lista todas as atividades do banco de dados')
    async def _listar(interaction: discord.Interaction):
        user_id = interaction.user.id
        server_id = interaction.guild.id
        atividades = manager.listar_atividades(user_id, server_id)
        
        if not atividades:
            await interaction.response.send_message("Você não tem atividades para listar.")
        else:
            dropdown_options = [
                discord.SelectOption(value=str(atividade['id']), label=atividade['nome'])
                for atividade in atividades
            ]
            
            await interaction.response.send_message("Lista de Atividades", view=DropdownView(options=dropdown_options, atividades=atividades))

def setup(tree: app_commands.CommandTree):
    @tree.command(guild=None, name='setup', description='Setup')
    @commands.has_permissions(manage_guild=True)
    async def _setup(interaction: discord.Interaction):
        await interaction.response.send_message("Painel criado",ephemeral=True)

        embed = discord.Embed(
            colour=discord.Color.blurple(),
            title="Central de Ajuda do Servidor",
            description="Nessa seção, você pode entrar em contato com a nossa equipe do servidor."
        )
        embed.set_image(url="https://i.imgur.com/quBpIIg.png")

        await interaction.channel.send(embed=embed, view=DropdownTicketView())

def fecharticket(tree: app_commands.CommandTree):
    @tree.command(guild=None, name="fecharticket",description='Feche um atendimento atual.')
    async def _fecharticket(interaction: discord.Interaction):
        mod = interaction.guild.get_role(int(os.getenv("ROLE_ID")))
        if str(interaction.user.id) in interaction.channel.name or mod in interaction.author.roles:
            await interaction.response.send_message(f"O ticket foi arquivado por {interaction.user.mention}, obrigado por entrar em contato!")
            await interaction.channel.edit(archived=True,locked=True)
        else:
            await interaction.response.send_message("Isso não pode ser feito aqui...")