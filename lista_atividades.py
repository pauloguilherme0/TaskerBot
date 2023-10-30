import discord
import sqlite3
import os

from discord import app_commands, SelectOption
from discord.ext import commands
from dotenv import load_dotenv
from typing import Literal
from enum import Enum

intents = discord.Intents.default()
intents.message_content = True

class Status(Enum):
    TODO = "To Do"
    DOING = "Doing"
    DONE = "Done"
    
class Tags(Enum):
    BUG = "Bug"
    CORRECAO = "Correção"
    MELHORIA = "Melhoria"
    CHAMADO = "Chamado"
    OFFTOPIC = "Off Topic"

class AtividadeManager:
    def __init__(self, db_name='atividades.db'):
        self.conn = sqlite3.connect(db_name)
        self.conn.execute("CREATE TABLE IF NOT EXISTS atividades (id INTEGER PRIMARY KEY, nome TEXT, status TEXT, tag TEXT, user_id INTEGER, server_id INTEGER)")
        self.conn.commit()

    def __enter__(self):
        self.c = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()

    def inserir_atividade(self, nome, status, tag, user_id, server_id):
        self.c.execute("INSERT INTO atividades (nome, status, tag, user_id, server_id) VALUES (?, ?, ?, ?, ?)", (nome, status, tag, user_id, server_id))
        self.conn.commit()

    def listar_atividades(self, user_id, server_id):
        self.c.execute("SELECT * FROM atividades WHERE user_id = ? AND server_id = ?", (user_id, server_id,))
        atividades = self.c.fetchall()
        output = []
        for atividade in atividades:
            output.append({"id": atividade[0], "nome": atividade[1], "status": atividade[2], "tag": atividade[3]})
        return output

    def limpar_atividades(self):
        self.c.execute("DELETE FROM atividades")
        self.conn.commit()

class Dropdown(discord.ui.Select):
    def __init__(self, options, atividades):
        super().__init__(
            placeholder="Selecione uma opção...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:dropdown_help"
        )
        self.atividades = atividades

    async def callback(self, interaction: discord.Interaction):
        atividade_id = int(self.values[0])
        atividade = next((a for a in self.atividades if a['id'] == atividade_id), None)
        if atividade:
            cor = {
                'Bug': discord.Color.red(),
                'Correção': discord.Color.green(),
                'Melhoria': discord.Color.blue(),
                'Chamado': discord.Color.orange(),
                'Off Topic': discord.Color.greyple()
            }.get(atividade['tag'], discord.Color.default())
            
            embed = discord.Embed(title="Detalhes da Atividade", colour=cor)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            embed.add_field(name="Nome da Atividade", value=atividade['nome'], inline=False)
            embed.add_field(name="Status", value=atividade['status'], inline=True)
            embed.add_field(name="Tag", value=atividade['tag'], inline=True).color=cor
            embed.set_footer(text="ID da Atividade: " + str(atividade_id))
            
            await interaction.response.send_message(embed=embed)

class DropdownView(discord.ui.View):
    def __init__(self, options, atividades):
        super().__init__(timeout=None)
        dropdown = Dropdown(options=options, atividades=atividades)
        self.add_item(dropdown)

class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        global tree
        if not self.synced:
            await tree.sync(guild=None)
            self.synced = True
        print(f"Entramos como {self.user}.")
        await self.change_presence(activity=discord.Game(name="Digite /ajuda para obter ajuda"))

aclient = Client()
tree = app_commands.CommandTree(aclient)

if __name__ == "__main__":
    with AtividadeManager() as atividade_manager:
        # Comando de Ajuda
        @tree.command(guild=None, name='ajuda', description='Mostra uma lista de comandos disponíveis.')
        async def ajuda(interaction: discord.Interaction):
            embed = discord.Embed(title="Lista de Comandos", description="Aqui estão todos os comandos disponíveis:", color=discord.Color.blue())

            embed.add_field(name="/inserir <nome> <status> <tag>", value="Insere uma nova atividade no banco de dados", inline=False)
            embed.add_field(name="/listar", value="Lista todas as atividades do banco de dados", inline=False)
            embed.add_field(name="/limpar", value="Limpa todas as atividades do banco de dados", inline=False)

            await interaction.response.send_message(embed=embed)

        # Comando de Inserir
        @tree.command(guild=None, name='inserir', description='Insere uma nova atividade no banco de dados')
        async def inserir(interaction: discord.Interaction, nome: str, status: Status, tag: Tags):
            user_id = interaction.user.id
            atividade_manager.inserir_atividade(nome, status.value, tag.value, user_id)
            await interaction.response.send_message(f"Atividade {nome} inserida com sucesso.")

        
        # Comando de Limpar
        @tree.command(guild=None, name='limpar', description='Limpa todas as atividades do banco de dados')
        async def limpar(interaction: discord.Interaction):
            atividade_manager.limpar_atividades()
            await interaction.response.send_message("Todas as atividades foram removidas.")

        # Comando de Listar
        @tree.command(guild=None, name='listar', description='Lista todas as atividades do banco de dados')
        async def listar(interaction: discord.Interaction):
            user_id = interaction.user.id
            server_id = interaction.channel_id
            atividades = atividade_manager.listar_atividades(user_id, server_id)
            
            if not atividades:
                await interaction.response.send_message("Você não tem atividades para listar.")
            else:
                dropdown_options = [
                    discord.SelectOption(value=str(atividade['id']), label=atividade['nome'])
                    for atividade in atividades
                ]
                
                await interaction.response.send_message("Lista de Atividades", view=DropdownView(options=dropdown_options, atividades=atividades))

    load_dotenv()
    TOKEN = os.getenv("DISCORD_BOT_SECRET")
    aclient.run(TOKEN)