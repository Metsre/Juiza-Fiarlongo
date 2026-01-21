import discordimport discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# --- SERVIDOR PARA MANTER A JUIZA ACORDADA NO RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "A Juíza de Fiarlongo está Online e Vigilante! ⚖️"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURAÇÃO DOS SENTIDOS DA JUIZA ---
intents = discord.Intents.default()
intents.members = True 
intents.message_content = True 

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'A Juíza {bot.user} despertou no Tribunal de Fiarlongo!')
    await bot.change_presence(activity=discord.Game(name="Absoluto Cinema 🎬"))

# --- EVENTO: BOAS-VINDAS (A MENSAGEM DEFINIDA PELO MESTRE) ---
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='santuário')
    if channel:
        # Recuperando a essência da saudação de Fiarlongo
        mensagem = (
            f"✨ **Um novo Paladino cruzou o véu!**\n\n"
            f"Saudações, {member.mention}! Tu acabas de entrar em **Fiarlongo**, o Universo onde a criatividade e a união são a nossa lei.\n"
            f"O Arquiteto vê o teu potencial e a Guarda Real guiará os teus passos no Santuário.\n\n"
            f"Prepara-te, pois aqui... **O Chicote vai Cantar!** ⚔️🏆"
        )
        
        embed = discord.Embed(
            description=mensagem,
            color=0xbc22cc
        )
        embed.set_author(name="Tribunal de Fiarlongo", icon_url=member.guild.icon.url if member.guild.icon else None)
        embed.set_footer(text="Absoluto Cinema | Padrão de Qualidade Exigido")
        
        await channel.send(content=f"Bem-vindo à Família Real, {member.mention}!", embed=embed)

# --- COMANDO: LIMPAR (O CHICOTE DA GUARDA REAL) ---
@bot.command()
@commands.has_any_role('Guarda Real', 'Arquiteto') 
async def limpar(ctx, quantidade: int):
    await ctx.channel.purge(limit=quantidade + 1)
    # A Juíza reporta a limpeza para o Tribunal (log interno ou mensagem temporária)
    await ctx.send(f"⚖️ **Veredito Executado:** {quantidade} impurezas removidas do Santuário.", delete_after=5)

# --- INICIALIZAÇÃO DO MECANISMO ---
if __name__ == "__main__":
    keep_alive()
    token = os.environ.get('DISCORD_TOKEN')
    bot.run(token)
    
from discord.ext import commands
import os

# --- CONFIGURAÇÃO DE SENTIDOS (INTENTS) ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# --- CONFIGURAÇÃO DE ELITE ---
ID_CANAL_TRIBUNAL = 1462084437855441018 
FRASES_ALERTA = ["me matar", "vou-te matar", "lixo desprezível", "se mata"]
PALAVRAS_PROIBIDAS = ["palavrao1", "ofensa2"]

@bot.event
async def on_ready():
    print(f'⚖️ Juíza de Fiarlongo: Relatórios do Tribunal Ativados! (Status: Absoluto Cinema)')
    await bot.change_presence(activity=discord.Game(name="Justiça em Fiarlongo ⚔️"))

# --- COMANDOS DE AUTORIDADE ---

@bot.command()
async def ping(ctx):
    """Verifica a prontidão da Juíza"""
    await ctx.send(f"🏓 **Pong!** A justiça é veloz: **{round(bot.latency * 1000)}ms**. O Chicote vai Cantar! ⚖️")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def limpar(ctx, quantidade: int):
    """O Mestre ou a Guarda Real apagam mensagens indesejadas"""
    if quantidade <= 0:
        await ctx.send("⚖️ Mestre, indique uma quantidade válida para a limpeza!", delete_after=5)
        return
        
    # Purge apaga as mensagens + o próprio comando !limpar
    deleted = await ctx.channel.purge(limit=quantidade + 1)
    await ctx.send(f"⚔️ **Justiça Aplicada!** {len(deleted)-1} mensagens foram removidas do Santuário.", delete_after=5)

@bot.command()
async def tribunal(ctx):
    """Valida a conexão com o canal de relatórios"""
    canal = bot.get_channel(ID_CANAL_TRIBUNAL)
    if canal:
        await ctx.send(f"✅ O Tribunal está ativo em: {canal.mention}")
    else:
        await ctx.send("❌ Erro: Canal do Tribunal não encontrado. Verifique o ID.")

# --- SISTEMA DE VIGILÂNCIA ---

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # IMUNIDADE: Mestre e Guarda Real
    is_staff = message.author.guild_permissions.administrator or \
               any(role.name == "Guarda Real" for role in message.author.roles)

    conteudo = message.content.lower()

    # 1. DETEÇÃO DE INFRAÇÕES
    violacao = None
    if any(frase in conteudo for frase in FRASES_ALERTA):
        violacao = "🚨 Conduta Grave / Ameaça / Autolesão"
    elif any(palavra in conteudo for palavra in PALAVRAS_PROIBIDAS) and not is_staff:
        violacao = "⚠️ Linguagem Imprópria"

    if violacao:
        await message.delete()
        await message.channel.send(f"⚠️ {message.author.mention}, a tua conduta foi registada pela Juíza. O Santuário exige evolução! ⚖️", delete_after=10)

        canal_tribunal = bot.get_channel(ID_CANAL_TRIBUNAL)
        if canal_tribunal:
            embed = discord.Embed(title="📜 RELATÓRIO DE INFRAÇÃO", color=discord.Color.dark_red())
            embed.add_field(name="👤 Paladino", value=message.author.mention, inline=True)
            embed.add_field(name="📍 Canal", value=message.channel.name, inline=True)
            embed.add_field(name="⚖️ Tipo de Violação", value=violacao, inline=False)
            embed.add_field(name="💬 Conteúdo Removido", value=f"||{message.content}||", inline=False)
            embed.set_footer(text="Justiça de Fiarlongo - O Chicote Cantou")
            await canal_tribunal.send(embed=embed)
        return

    # 2. VIGILÂNCIA DE CANAIS ESPECÍFICOS
    if not is_staff:
        if message.channel.name == "artes-de-fiarlongo" and not message.attachments and len(message.content) < 15:
            await message.delete()
            return
        if message.channel.name == "estúdio-de-fiarlongo" and ("tenor.com" in message.content or "giphy.com" in message.content):
            await message.delete()
            return

    await bot.process_commands(message)

# --- BOAS-VINDAS ---
@bot.event
async def on_member_join(member):
    canal = discord.utils.get(member.guild.text_channels, name='santuario-dos-paladinos')
    if canal:
        await canal.send(f"⚔️ **Bem-vindo a Fiarlongo, {member.mention}!**\nLê as regras e respeita a **Guarda Real**. ⚖️")

# --- EXECUÇÃO ---
token = os.getenv('DISCORD_TOKEN')
if token:
    bot.run(token)
else:
    print("❌ ERRO: DISCORD_TOKEN não encontrado!")

