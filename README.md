# Bot de Atividades do Discord

Este é um bot do Discord que ajuda a gerenciar atividades em um servidor. Ele permite que os usuários insiram, listem e limpem atividades. Além disso, o bot também suporta a criação e o gerenciamento de tickets para atendimento ao usuário.

## Funcionalidades

- **Inserir atividades**: Os usuários podem inserir uma nova atividade no banco de dados.
- **Listar atividades**: Os usuários podem listar todas as atividades do banco de dados.
- **Limpar atividades**: Os usuários podem limpar todas as atividades do banco de dados.
- **Gerenciamento de tickets**: Os usuários podem criar um novo ticket para atendimento. Eles também podem fechar um ticket existente.

## Dependências

Este projeto depende das seguintes bibliotecas Python:

- `sqlite3`
- `python-dotenv`
- `discord.py`

Você pode instalar todas essas dependências de uma vez com o comando `pip install -r requirements.txt`.

## Configuração

Para configurar o bot, você precisa definir as seguintes variáveis de ambiente:

- `DB_NAME`: O nome do banco de dados SQLite que o bot usará para armazenar as atividades. Se essa variável não estiver definida, o bot usará `'default.db'` como o nome do banco de dados.
- `DISCORD_BOT_SECRET`: O token do seu bot do Discord. Este é um segredo que o Discord usa para autenticar o seu bot. Você pode obter esse token no Portal de Desenvolvedores do Discord.
- `ROLE_ID`: O ID do cargo que tem permissão para fechar tickets no Discord.

Você pode definir essas variáveis de ambiente no seu sistema operacional ou no seu ambiente de desenvolvimento. Alternativamente, você pode criar um arquivo `.env` no diretório raiz do projeto e definir as variáveis lá, como neste exemplo:

## Como Adicionar o Bot a um Servidor

Para adicionar este bot a um servidor do Discord, siga estas etapas:

1. Vá para o Portal do Desenvolvedor do Discord.
2. Clique no bot que você deseja compartilhar.
3. No painel lateral, clique em "OAuth2".
4. Na seção "Scopes", selecione "bot" e "applications.commands".
5. Na seção "Bot Permissions", selecione as permissões necessárias para o seu bot. Para este bot de atividades, você precisará das permissões "Ver Canais", "Enviar Mensagens", "Gerenciar Mensagens", "Ler Histórico de Mensagens", "Mencionar Todos" e "Adicionar Reações".
6. Copie o link gerado na parte inferior da seção "Scopes". Este é o link de convite do seu bot.

Você pode compartilhar este link com qualquer pessoa que queira adicionar o bot ao servidor do Discord. Lembre-se de que apenas administradores de servidores podem adicionar bots.