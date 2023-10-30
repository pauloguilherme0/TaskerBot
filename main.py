import discord
import os

from dotenv import load_dotenv
from discord import app_commands

from commands import ajuda, inserir, limpar, listar, setup, fecharticket
from atividade_manager import AtividadeManager

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
        ajuda(tree, atividade_manager)
        inserir(tree, atividade_manager)
        limpar(tree, atividade_manager)
        listar(tree, atividade_manager)
        setup(tree)
        fecharticket(tree)

    load_dotenv()
    TOKEN = os.getenv("DISCORD_BOT_SECRET")
    aclient.run(TOKEN)