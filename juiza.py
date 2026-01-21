import discord
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
    # Procura o canal chamado santuário (garante que o nome no Discord está igual)
    channel = discord.utils.get(member.guild.text_channels, name='santuário')
    if channel:
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
        icon_url = member.guild.icon.url if member.guild.icon else None
        embed.set_author(name="Tribunal de Fiarlongo", icon_url=icon_url)
        embed.set_footer(text="Absoluto Cinema | Padrão de Qualidade Exigido")
        
        await channel.send(content=f"Bem-vindo à Família Real, {member.mention}!", embed=embed)

# --- COMANDO: LIMPAR (O CHICOTE DA GUARDA REAL) ---
@bot.command()
@commands.has_any_role('Guarda Real', 'Arquiteto', 'Moderador') 
async def limpar(ctx, quantidade: int):
    await ctx.channel.purge(limit=quantidade + 1)
    await ctx.send(f"⚖️ **Veredito Executado:** {quantidade} impurezas removidas do Santuário.", delete_after=5)

# --- INICIALIZAÇÃO DO MECANISMO ---
if __name__ == "__main__":
    keep_alive()
    token = os.environ.get('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print("Erro: DISCORD_TOKEN não encontrado nas variáveis de ambiente!")
        import discord
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
    # Procura o canal chamado santuário
    channel = discord.utils.get(member.guild.text_channels, name='santuário')
    if channel:
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
        icon_url = member.guild.icon.url if member.guild.icon else None
        embed.set_author(name="Tribunal de Fiarlongo", icon_url=icon_url)
        embed.set_footer(text="Absoluto Cinema | Padrão de Qualidade Exigido")
        
        await channel.send(content=f"Bem-vindo à Família Real, {member.mention}!", embed=embed)

# --- COMANDO: LIMPAR (O CHICOTE DA GUARDA REAL) ---
@bot.command()
@commands.has_any_role('Guarda Real', 'Arquiteto', 'Moderador') 
async def limpar(ctx, quantidade: int):
    await ctx.channel.purge(limit=quantidade + 1)
    await ctx.send(f"⚖️ **Veredito Executado:** {quantidade} impurezas removidas do Santuário.", delete_after=5)

# --- INICIALIZAÇÃO DO MECANISMO ---
if __name__ == "__main__":
    keep_alive()
    token = os.environ.get('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print("Erro: DISCORD_TOKEN não encontrado nas variáveis de ambiente!")

