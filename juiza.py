import discord
from discord.ext import commands
import os

# --- CONFIGURAÇÃO DE SENTIDOS (INTENTS) ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# --- CONFIGURAÇÃO DE ELITE DE FIARLONGO ---
# Certifique-se de que o ID do Canal está correto no seu Discord
ID_CANAL_TRIBUNAL = 1462084437855441018 
FRASES_ALERTA = ["me matar", "vou-te matar", "lixo desprezível", "se mata"]
PALAVRAS_PROIBIDAS = ["palavrao1", "ofensa2"] # Adicione aqui as palavras banidas

@bot.event
async def on_ready():
    print(f'⚖️ Juíza de Fiarlongo: Relatórios do Tribunal Ativados! (Status: Absoluto Cinema)')
    # Define a atividade da Juíza no Discord
    await bot.change_presence(activity=discord.Game(name="Justiça em Fiarlongo ⚔️"))

# --- COMANDOS MANUAIS ---
@bot.command()
async def ping(ctx):
    """Comando para testar a prontidão da Juíza"""
    await ctx.send(f"🏓 **Pong!** A justiça é veloz em Fiarlongo: **{round(bot.latency * 1000)}ms**. O Chicote vai Cantar! ⚖️")

@bot.command()
async def tribunal(ctx):
    """Verifica se o canal de relatórios está configurado corretamente"""
    canal = bot.get_channel(ID_CANAL_TRIBUNAL)
    if canal:
        await ctx.send(f"✅ O Tribunal de Fiarlongo está ativo no canal: {canal.mention}")
    else:
        await ctx.send("❌ Erro: O canal do Tribunal não foi encontrado. Verifique o ID.")

# --- SISTEMA DE VIGILÂNCIA (MODERAÇÃO) ---
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
        
        # Aviso educativo público (Foco na evolução humana)
        await message.channel.send(f"⚠️ {message.author.mention}, a tua conduta foi registada pela Juíza. O Santuário exige respeito e evolução! ⚖️", delete_after=10)

        # ENVIO DE RELATÓRIO PARA O TRIBUNAL
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

    # 2. VIGILÂNCIA DE ARTES E ESTÚDIO
    if not is_staff:
        if message.channel.name == "artes-de-fiarlongo" and not message.attachments and len(message.content) < 15:
            await message.delete()
            return
        if message.channel.name == "estúdio-de-fiarlongo" and ("tenor.com" in message.content or "giphy.com" in message.content):
            await message.delete()
            return

    # IMPORTANTE: Permite que os comandos funcionem mesmo com o on_message ativo
    await bot.process_commands(message)

# --- BOAS-VINDAS AO SANTUÁRIO ---
@bot.event
async def on_member_join(member):
    # Procure pelo canal 'santuario-dos-paladinos' ou use o ID específico
    canal = discord.utils.get(member.guild.text_channels, name='santuario-dos-paladinos')
    if canal:
        await canal.send(f"⚔️ **Bem-vindo a Fiarlongo, {member.mention}!**\nLê as regras em #avisos-oficiais-de-fiarlongo e respeita a **Guarda Real**. Boas conversas! ⚖️")

# --- CONEXÃO COM O COFRE ---
token = os.getenv('DISCORD_TOKEN')
if token:
    bot.run(token)
else:
    print("❌ ERRO: DISCORD_TOKEN não encontrado no Ambiente!")
