from discord import app_commands, SelectOption
import discord

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

class DropdownTicket(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(value="ajuda",label="Ajuda", emoji="👋"),
            discord.SelectOption(value="atendimento",label="Atendimento", emoji="📨"),
        ]
        super().__init__(
            placeholder="Selecione uma opção...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:dropdown_help"
        )
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "ajuda":
            await interaction.response.send_message("Se você precisar de ajuda, coloque nos comentários do vídeo",ephemeral=True)
        elif self.values[0] == "atendimento":
            await interaction.response.send_message("Clique abaixo para criar um ticket",ephemeral=True,view=CreateTicket())

class DropdownTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(DropdownTicket())

class CreateTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.value=None

    @discord.ui.button(label="Abrir Ticket",style=discord.ButtonStyle.blurple,emoji="➕")
    async def confirm(self,interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

        ticket = None
        for thread in interaction.channel.threads:
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.response.send_message(ephemeral=True,content=f"Você já tem um atendimento em andamento!")
                    return

        async for thread in interaction.channel.archived_threads(private=False):
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.edit_original_response(content=f"Você já tem um atendimento em andamento!",view=None)
                    return
        
        if ticket != None:
            await ticket.edit(archived=False,locked=False)
            await ticket.edit(name=f"{interaction.user.name} ({interaction.user.id})",auto_archive_duration=10080,invitable=False)
        else:
            ticket = await interaction.channel.create_thread(name=f"{interaction.user.name} ({interaction.user.id})",auto_archive_duration=10080)#,type=discord.ChannelType.public_thread)
            await ticket.edit(invitable=False)

        await interaction.response.send_message(ephemeral=True,content=f"Criei um ticket para você! {ticket.mention}")
        await ticket.send(f"📩  **|** {interaction.user.mention} ticket criado! Envie todas as informações possíveis sobre seu caso e aguarde até que um atendente responda.\n\nApós a sua questão ser sanada, você pode usar `/fecharticket` para encerrar o atendimento!")