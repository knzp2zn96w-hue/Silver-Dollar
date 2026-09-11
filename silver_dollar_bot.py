import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timezone, timedelta
import json, os, asyncio, re
from dotenv import load_dotenv

load_dotenv()  # Lê o arquivo .env (se existir) e carrega as variáveis de ambiente dele

# ╔══════════════════════════════════════════════════════════════╗
# ║           BOT SILVER DOLLAR BAR – FiveM Bar System            ║
# ╚══════════════════════════════════════════════════════════════╝

TOKEN = os.environ.get("TOKEN")  # ⚠️ Defina a variável de ambiente TOKEN com o token do seu bot
# NUNCA cole o token diretamente aqui no código!
# No Replit: aba "Secrets" -> Key: TOKEN, Value: seu_token
# No terminal: export TOKEN="seu_token_aqui"

NOME_SERVIDOR = "Silver Dollar"
# ⚠️ COLE AQUI O LINK PÚBLICO DA SUA LOGO (a imagem que enviaste).
# Como é um arquivo local, o Discord não consegue usá-lo direto.
# Poste a imagem em qualquer canal do seu servidor, clica com o botão
# direito nela -> "Copiar link" -> cole o link abaixo no lugar do placeholder.
LOGO_URL = "https://cdn.discordapp.com/attachments/1545711644565446697/1547689204580884530/d9fba299-950c-45e6-949f-3e493b530d1c.png?ex=6aa45565&is=6aa303e5&hm=4ee882f5dd30c17b92709ae113ca122b731e18696baa12ead1ef49e520ac58cb&"
# ⚠️ ESTE LINK É DO SERVIDOR ANTIGO E PROVAVELMENTE VAI EXPIRAR/DEIXAR DE FUNCIONAR.
# Sobe a imagem no NOVO servidor, copia o novo link e substitui aqui.

# ══════════════════════════════════════════════════════════════
#   IDs DO SERVIDOR (NOVO SERVIDOR)
# ══════════════════════════════════════════════════════════════

# ─── CANAIS ──────────────────────────────────────────────────
CANAL_LOG_SET_ID          = 1546567399581683854   # 📄 log-set
CANAL_LOG_CALC_ID         = 1546567399581683855   # 📄 log-config (usado para logs de "Trocar Meta" e reset semanal)
CANAL_LOG_AUSENCIA_ID     = 1546567399581683856   # 📄 log-ausencia
CANAL_LOG_ENTRADA_ID      = 1546567399581683857   # 📄 log-entradas (detalhado, só para staff)
CANAL_BEM_VINDO_ID        = 1547999020495016006   # 👋 #bem-vindo — canal público onde toda a gente vê a mensagem de boas-vindas
CANAL_LOG_SAIDA_ID        = 1546567399581683858   # 📄 log-saidas
CANAL_LOG_ADVERTENCIAS_ID = 1546567400084996237   # 📄 log-advertencias
CANAL_LOG_BAU_ID          = 1546567395466936393   # 📄 log-bau

CANAL_ESCALACAO_PAINEL_ID = 1548006343703531631   # ⚔️ escalacao-painel  (botões Participar/Sair/Finalizar)
CANAL_ESCALACAO_POST_ID   = 1548006716183019520   # ⚔️ escalacao-relatorio (embed / registo de ação)

CANAL_ANUNCIO_ADV_ID      = 1546567394565029917   # 📢 canal onde toda advertência aplicada é anunciada

CANAL_APROV_AUSENCIA_ID   = 1546567395466936395   # 😴 aprovacao-ausencia
CANAL_APROV_SET_ID        = 1546567395466936394   # 📋 aprovacao-set (staff aprova registo)

CANAL_META_ID             = 1546567398339911802   # 📊 canal-meta (onde a Meta Semanal fica fixada)
CANAL_INFO_META_ID        = 1546567398339911802   # 📢 #info-meta (anúncio de Meta Geral / @here). ⚠️ igual ao CANAL_META_ID — confirma se é intencional. Se 0, usa CANAL_META_ID como fallback.

CATEGORIA_FARM_ID         = 1546567398339911801   # 📁 Categoria onde os canais de Candidatura são criados

CANAL_LOG_WINLOSE_ID      = 1548004883410714835   # 🗡️ canal onde cada Win/Lose registado será logado
CANAL_LOG_CONTAGEM_ID     = 1548004914100310036   # ☠️ canal onde cada registo de kills será logado

# ─── CARGOS ──────────────────────────────────────────────────
CARGO_MEMBRO_ID      = 1546567392627523760   # ✅ Membro (dado ao ser aprovado no SET)
CARGO_EXTRA_SET_ID   = 1546567392627523758   # 🎖️ Cargo extra, dado junto com Membro ao aprovar o SET
CARGO_GERENTE_ID     = 1546567392669212689   # 👑 Gerente (aprovação farm / finalizar escalação)
CARGO_AUTO_SET_ID    = 1546567392459759788   # 🔰 cargo dado automaticamente ao entrar no servidor
CARGO_AUSENCIA_ID    = 1546567392627523764   # 😴 cargo de Ausência

CARGO_ADV_VERBAL_ID  = 1546567392627523755   # ⚠️ ADV Verbal
CARGO_ADV_WARN1_ID   = 1546567392459759795   # ⚠️ ADV 1
CARGO_ADV_WARN2_ID   = 1546567392459759794   # ⚠️ ADV 2
CARGO_ADV_WARN3_ID   = 1546567392459759793   # ⚠️ ADV 3
CARGO_EXONERADO_ID   = 1546567392459759792   # 🚫 Exonerado

# Cargos que podem ver/gerenciar tickets
CARGOS_STAFF_IDS = [
    1546567392669212689,   # Gerente  ⚠️ mesmo ID que CARGO_GERENTE_ID — confirma se é intencional
    1546567392669212692,   # Liderança
    1546567392669212691,   # Alto Comando
]

# ══════════════════════════════════════════════════════════════
#   CORES  (Silver Dollar)
# ══════════════════════════════════════════════════════════════
COR_PADRAO   = 0x270505   # cor principal (Silver Dollar)
COR_GROVE    = 0x270505   # cor principal (mantido o nome da variável p/ não quebrar o resto do código)
COR_APROVADO = 0x57f287
COR_RECUSADO = 0xed4245
COR_AUSENCIA = 0x270505   # cor principal
COR_ADV      = 0xe67e22
COR_LOG      = 0x270505   # cor principal
COR_AMARELO  = 0xf0c000

# ══════════════════════════════════════════════════════════════
#   DB
# ══════════════════════════════════════════════════════════════
_railway_volume_dir = os.environ.get("RAILWAY_VOLUME_MOUNT_PATH")  # setada automaticamente pelo Railway quando um Volume é anexado ao serviço
DB_FILE = (
    os.environ.get("DB_FILE_PATH")
    or (os.path.join(_railway_volume_dir, "silverdollar_data.json") if _railway_volume_dir else "silverdollar_data.json")
)
# ⚠️ No Railway (e em qualquer hospedagem com disco efêmero), o arquivo acima
# SÓ sobrevive a um redeploy se estiver dentro de um Volume persistente.
# Basta criar um Volume e anexá-lo a este serviço — o caminho é detectado
# sozinho (RAILWAY_VOLUME_MOUNT_PATH). Se quiser forçar um caminho/nome
# customizado, defina a variável DB_FILE_PATH manualmente.

META_PADRAO = {
    "oleo": 30,
    "plastico": 50,
    "garrafas": 20,
    "tinta": 0,
    "crop_maconha": 0,
    "dinheiro_sujo": 100000,
    "message_id": None,
}


TEXTO_COMANDOS_PADRAO = (
    "📋 **Lista de Comandos — Silver Dollar**\n\n"
    "Em breve mais informações aqui.\n"
    "Use `/config_comandos` (apenas staff) para editar este texto."
)


def _proxima_segunda(a_partir_de: datetime) -> datetime:
    """Retorna a próxima segunda-feira às 00:00 UTC a partir da data informada
    (usada para resetar os rankings semanais)."""
    dias_ate_segunda = (7 - a_partir_de.weekday()) % 7
    dias_ate_segunda = 7 if dias_ate_segunda == 0 else dias_ate_segunda
    proxima = (a_partir_de + timedelta(days=dias_ate_segunda)).replace(hour=0, minute=0, second=0, microsecond=0)
    return proxima


def load_db():
    if not os.path.exists(DB_FILE):
        agora = datetime.now(timezone.utc)
        return {
            "ausencias": {}, "advertencias": {}, "meta": dict(META_PADRAO),
            "acoes_stats": {"membros": {}, "acoes": {}, "membros_semanal": {}, "acoes_semanal": {}},
            "config": {"comandos_texto": TEXTO_COMANDOS_PADRAO},
            "semana": {"inicio": agora.isoformat(), "proximo_reset": _proxima_segunda(agora).isoformat()},
            "escalacoes_ativas": {},
        }
    with open(DB_FILE, "r") as f:
        data = json.load(f)
    if "ausencias"    not in data: data["ausencias"]    = {}
    if "advertencias" not in data: data["advertencias"] = {}
    if "meta"         not in data: data["meta"]         = dict(META_PADRAO)
    if "acoes_stats"  not in data: data["acoes_stats"]  = {"membros": {}, "acoes": {}, "membros_semanal": {}, "acoes_semanal": {}}
    if "membros"          not in data["acoes_stats"]: data["acoes_stats"]["membros"]          = {}
    if "acoes"            not in data["acoes_stats"]: data["acoes_stats"]["acoes"]             = {}
    if "membros_semanal"  not in data["acoes_stats"]: data["acoes_stats"]["membros_semanal"]   = {}
    if "acoes_semanal"    not in data["acoes_stats"]: data["acoes_stats"]["acoes_semanal"]      = {}
    if "config"       not in data: data["config"]       = {"comandos_texto": TEXTO_COMANDOS_PADRAO}
    if "comandos_texto" not in data["config"]: data["config"]["comandos_texto"] = TEXTO_COMANDOS_PADRAO
    if "semana" not in data:
        agora = datetime.now(timezone.utc)
        data["semana"] = {"inicio": agora.isoformat(), "proximo_reset": _proxima_segunda(agora).isoformat()}
    if "escalacoes_ativas" not in data: data["escalacoes_ativas"] = {}
    for chave, valor in META_PADRAO.items():
        if chave not in data["meta"]:
            data["meta"][chave] = valor
    return data

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ══════════════════════════════════════════════════════════════
#   INTENTS / BOT
# ══════════════════════════════════════════════════════════════
intents = discord.Intents.default()
intents.members         = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def tem_staff(member: discord.Member) -> bool:
    ids = {r.id for r in member.roles}
    return any(cid in ids for cid in CARGOS_STAFF_IDS) or member.guild_permissions.administrator

def tem_gerente(member: discord.Member) -> bool:
    return (
        any(r.id == CARGO_GERENTE_ID for r in member.roles)
        or member.guild_permissions.administrator
    )

def fmt_valor(valor) -> str:
    """Formata um número (ou texto) como valor monetário/quantidade em pt-BR."""
    try:
        return f"{int(str(valor).replace('.', '').replace(',', '')):,}".replace(",", ".")
    except (ValueError, TypeError):
        return str(valor)

# ══════════════════════════════════════════════════════════════
#   LOGS GERAIS
# ══════════════════════════════════════════════════════════════

@bot.event
async def on_member_join(member):
    cargo = member.guild.get_role(CARGO_AUTO_SET_ID)
    if cargo:
        try:
            await member.add_roles(cargo, reason="Cargo automático ao entrar")
        except Exception as e:
            print(f"[AUTO ROLE] Erro: {e}")

    # Mensagem pública de boas-vindas (visível a todos, simples: só a foto e uma saudação)
    canal_bv = bot.get_channel(CANAL_BEM_VINDO_ID)
    if canal_bv:
        embed_bv = discord.Embed(
            title="👋 Bem-vindo(a) à Silver Dollar!",
            description=f"Seja bem-vindo(a), {member.mention}! Esperamos que aproveites a tua estadia por cá. 💜",
            color=COR_GROVE, timestamp=datetime.now(timezone.utc)
        )
        embed_bv.set_thumbnail(url=member.display_avatar.url)
        embed_bv.set_footer(text="Silver Dollar")
        try:
            await canal_bv.send(content=member.mention, embed=embed_bv)
        except Exception as e:
            print(f"[BOAS-VINDAS] Erro: {e}")

    # Log detalhado (apenas para staff)
    canal = bot.get_channel(CANAL_LOG_ENTRADA_ID)
    if not canal:
        return
    embed = discord.Embed(
        title="🟢 Membro Entrou",
        description=f"{member.mention} entrou no servidor!",
        color=COR_GROVE, timestamp=datetime.now(timezone.utc)
    )
    embed.set_author(name=str(member), icon_url=member.display_avatar.url)
    embed.add_field(name="👤 Utilizador",   value=f"{member.mention}\n`{member}`",                   inline=True)
    embed.add_field(name="🪪 ID",           value=f"`{member.id}`",                                  inline=True)
    embed.add_field(name="📅 Conta criada", value=f"<t:{int(member.created_at.timestamp())}:R>",     inline=False)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"Silver Dollar • ID: {member.id}")
    await canal.send(embed=embed)


@bot.event
async def on_member_remove(member):
    canal = bot.get_channel(CANAL_LOG_SAIDA_ID)
    if not canal:
        return
    embed = discord.Embed(
        title="🔴 Membro Saiu",
        description=f"**{member}** saiu do servidor.",
        color=COR_RECUSADO, timestamp=datetime.now(timezone.utc)
    )
    embed.set_author(name=str(member), icon_url=member.display_avatar.url)
    embed.add_field(name="👤 Utilizador", value=f"{member.mention}\n`{member}`", inline=True)
    embed.add_field(name="🪪 ID",      value=f"`{member.id}`",               inline=True)
    cargos = [r.mention for r in member.roles if r.name != "@everyone"]
    embed.add_field(name="🎖️ Cargos", value=" ".join(cargos) if cargos else "*nenhum*", inline=False)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"Silver Dollar • ID: {member.id}")
    await canal.send(embed=embed)


# ══════════════════════════════════════════════════════════════
#   SET / REGISTO  (sem pendente — torna-se Membro logo após aprovação)
#   Duas categorias (tags): Membro e Parceria.
# ══════════════════════════════════════════════════════════════

class SETModalMembro(discord.ui.Modal, title="Registo – Membro"):
    nick       = discord.ui.TextInput(label="Nick - In Game",     placeholder="Ex: Maria_Bahama", required=True, max_length=80)
    recrutador = discord.ui.TextInput(label="Quem te recrutou?",  placeholder="Nome do recrutador", required=True, max_length=80)

    async def on_submit(self, interaction: discord.Interaction):
        membro = interaction.user
        agora  = datetime.now(timezone.utc)

        canal_aprov = bot.get_channel(CANAL_APROV_SET_ID)
        if canal_aprov:
            embed = discord.Embed(title="📋 Pedido de Registo — Membro", color=COR_GROVE, timestamp=agora)
            embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
            embed.set_thumbnail(url=membro.display_avatar.url)
            embed.add_field(name="Utilizador",     value=membro.mention,        inline=True)
            embed.add_field(name="Nick - In Game", value=self.nick.value,       inline=True)
            embed.add_field(name="Recrutador",     value=self.recrutador.value, inline=True)
            embed.set_footer(text=f"ID Discord: {membro.id}")
            view = AprovarRecusarSETView(user_id=membro.id, tipo="membro", nick=self.nick.value, extra=self.recrutador.value)
            await canal_aprov.send(embed=embed, view=view)

        canal_log = bot.get_channel(CANAL_LOG_SET_ID)
        if canal_log:
            log = discord.Embed(title="📋 SET Solicitado — Membro", color=COR_GROVE, timestamp=agora)
            log.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
            log.set_thumbnail(url=membro.display_avatar.url)
            log.add_field(name="Utilizador",     value=membro.mention,        inline=True)
            log.add_field(name="Nick - In Game", value=self.nick.value,       inline=True)
            log.add_field(name="Recrutador",     value=self.recrutador.value, inline=True)
            log.set_footer(text=f"ID Discord: {membro.id}")
            await canal_log.send(embed=log)

        await interaction.response.send_message(
            "✅ Registo enviado! Aguarda a aprovação da liderança.",
            ephemeral=True
        )


class SETModalParceria(discord.ui.Modal, title="Registo – Parceria"):
    nick = discord.ui.TextInput(label="Nick - In Game", placeholder="Ex: Maria_Bahama", required=True, max_length=80)
    org  = discord.ui.TextInput(label="Nome da ORG",    placeholder="Ex: Nome da organização", required=True, max_length=80)

    async def on_submit(self, interaction: discord.Interaction):
        membro = interaction.user
        agora  = datetime.now(timezone.utc)

        canal_aprov = bot.get_channel(CANAL_APROV_SET_ID)
        if canal_aprov:
            embed = discord.Embed(title="🤝 Pedido de Registo — Parceria", color=COR_GROVE, timestamp=agora)
            embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
            embed.set_thumbnail(url=membro.display_avatar.url)
            embed.add_field(name="Utilizador",     value=membro.mention,  inline=True)
            embed.add_field(name="Nick - In Game", value=self.nick.value, inline=True)
            embed.add_field(name="Organização",    value=self.org.value,  inline=True)
            embed.set_footer(text=f"ID Discord: {membro.id}")
            view = AprovarRecusarSETView(user_id=membro.id, tipo="parceria", nick=self.nick.value, extra=self.org.value)
            await canal_aprov.send(embed=embed, view=view)

        canal_log = bot.get_channel(CANAL_LOG_SET_ID)
        if canal_log:
            log = discord.Embed(title="🤝 SET Solicitado — Parceria", color=COR_GROVE, timestamp=agora)
            log.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
            log.set_thumbnail(url=membro.display_avatar.url)
            log.add_field(name="Utilizador",     value=membro.mention,  inline=True)
            log.add_field(name="Nick - In Game", value=self.nick.value, inline=True)
            log.add_field(name="Organização",    value=self.org.value,  inline=True)
            log.set_footer(text=f"ID Discord: {membro.id}")
            await canal_log.send(embed=log)

        await interaction.response.send_message(
            "✅ Registo de parceria enviado! Aguarda a aprovação da liderança.",
            ephemeral=True
        )


class AprovarRecusarSETView(discord.ui.View):
    def __init__(self, user_id: int = 0, tipo: str = "membro", nick: str = "", extra: str = ""):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.tipo    = tipo    # "membro" ou "parceria"
        self.nick    = nick
        self.extra   = extra   # recrutador (membro) ou nome da org (parceria)

    @discord.ui.button(label="✅ Aprovar", style=discord.ButtonStyle.success, custom_id="btn_apr_set_groove")
    async def aprovar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not tem_staff(interaction.user):
            await interaction.response.send_message("❌ Sem permissão.", ephemeral=True)
            return
        guild  = interaction.guild
        membro = guild.get_member(self.user_id)
        if not membro:
            await interaction.response.send_message("❌ Utilizador não encontrado.", ephemeral=True)
            return

        if self.tipo == "membro":
            # Dá o cargo de Membro (+ cargo extra) diretamente, sem estado pendente
            cargo_m     = guild.get_role(CARGO_MEMBRO_ID)
            cargo_extra = guild.get_role(CARGO_EXTRA_SET_ID)
            cargos_para_dar = [c for c in (cargo_m, cargo_extra) if c]
            if cargos_para_dar:
                await membro.add_roles(*cargos_para_dar, reason=f"SET (Membro) aprovado por {interaction.user}")

        # Renomeia o nick para o Nick - In Game indicado no registo
        try:
            await membro.edit(nick=self.nick, reason="SET aprovado")
        except Exception:
            pass

        embed = interaction.message.embeds[0]
        embed.color = COR_APROVADO
        embed.add_field(name="✅ APROVADO POR", value=interaction.user.mention, inline=False)
        await interaction.response.edit_message(embed=embed, view=None)

        try:
            if self.tipo == "membro":
                await membro.send(
                    f"✅ O teu registo em **{NOME_SERVIDOR}** foi **aprovado**!\n"
                    f"Bem-vindo(a) à família, **{self.nick}**! 💜"
                )
            else:
                await membro.send(
                    f"✅ O teu registo de **parceria** em **{NOME_SERVIDOR}** foi **aprovado**!\n"
                    f"Obrigado por representares **{self.extra}**! 💜"
                )
        except Exception:
            pass

        rotulo = "Membro" if self.tipo == "membro" else "Parceria"
        await interaction.followup.send(f"✅ {membro.mention} aprovado como **{rotulo}**!", ephemeral=True)

    @discord.ui.button(label="❌ Recusar", style=discord.ButtonStyle.danger, custom_id="btn_rec_set_groove")
    async def recusar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not tem_staff(interaction.user):
            await interaction.response.send_message("❌ Sem permissão.", ephemeral=True)
            return
        guild  = interaction.guild
        membro = guild.get_member(self.user_id)
        embed  = interaction.message.embeds[0]
        embed.color = COR_RECUSADO
        embed.add_field(name="❌ RECUSADO POR", value=interaction.user.mention, inline=False)
        await interaction.response.edit_message(embed=embed, view=None)
        if membro:
            try:
                await membro.send(f"❌ O teu registo em **{NOME_SERVIDOR}** foi **recusado**.")
            except Exception:
                pass
        await interaction.followup.send("❌ Registo recusado.", ephemeral=True)


class SETView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="👤 Membro", style=discord.ButtonStyle.success, custom_id="btn_set_membro_groove")
    async def fazer_set_membro(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SETModalMembro())

    @discord.ui.button(label="🤝 Parceria", style=discord.ButtonStyle.primary, custom_id="btn_set_parceria_groove")
    async def fazer_set_parceria(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SETModalParceria())


@bot.tree.command(name="setup_set", description="Envia o painel de registo (SET) no canal.")
@app_commands.checks.has_permissions(administrator=True)
async def setup_set(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📋 Registo – Silver Dollar",
        description=(
            "Bem-vindo(a) à família! 💜\n\n"
            "Clica num dos botões abaixo consoante o teu caso:\n\n"
            "**👤 Membro** — se te vais juntar à organização\n"
            "**🤝 Parceria** — se representas outra organização parceira\n\n"
            "Após a aprovação, serás notificado(a) por mensagem privada."
        ),
        color=COR_GROVE
    )
    embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
    embed.set_thumbnail(url=LOGO_URL)
    embed.set_footer(text="Silver Dollar")
    await interaction.channel.send(embed=embed, view=SETView())
    await interaction.response.send_message("✅ Painel de registo enviado!", ephemeral=True)


# ══════════════════════════════════════════════════════════════
#   ESCALAÇÃO DE AÇÃO
# ══════════════════════════════════════════════════════════════

ARMAMENTOS = {
    "pistolas":  "🔫 Pistolas",
    "sub":       "🔫 Sub",
    "fuzil":     "🔫 Fuzil",
    "fuzil_sub": "🔫 Fuzil e SMG",
    "pesado":    "💣 Armamento Pesado",
}

# Nome da ação -> (contingente mínimo, contingente máximo, rótulo mostrado)
# Todas com máximo de 12 membros (exceto a opção "Ação Customizada", que já
# é tratada à parte e permite definir min/max manualmente).
ACOES = {
    "stab":         {"nome": "Stab",        "min": 1, "max": 12, "label": "Até 12 membros"},
    "marine":       {"nome": "Marine",      "min": 1, "max": 12, "label": "Até 12 membros"},
    "gruta":        {"nome": "Gruta",       "min": 1, "max": 12, "label": "Até 12 membros"},
    "human_labs":   {"nome": "Human-Labs",  "min": 1, "max": 12, "label": "Até 12 membros"},
    "cacadores":    {"nome": "Caçadores",   "min": 1, "max": 12, "label": "Até 12 membros"},
    "avioes":       {"nome": "Aviões",      "min": 1, "max": 12, "label": "Até 12 membros"},
    "casa_o_neil":  {"nome": "Casa o Neil", "min": 1, "max": 12, "label": "Até 12 membros"},
    "paleto":       {"nome": "Paleto",      "min": 1, "max": 12, "label": "Até 12 membros"},
}

escalacoes_ativas: dict[int, dict] = {}


def _salvar_escalacoes_ativas():
    """Persiste o dicionário de escalações ativas no banco, para que elas
    sobrevivam a um reinício do bot (deploy, crash, hospedagem reiniciando)."""
    db = load_db()
    db["escalacoes_ativas"] = {str(msg_id): dados for msg_id, dados in escalacoes_ativas.items()}
    save_db(db)


def _campo(embed: discord.Embed, nome: str):
    for i, f in enumerate(embed.fields):
        if f.name == nome:
            return i
    return None


def _lista_participantes(participantes: list, maximo: int, guild: discord.Guild) -> str:
    """Sempre mostra o número máximo de vagas (1..maximo), preenchendo com
    quem já entrou e deixando um traço nas vagas ainda livres."""
    linhas = []
    for i in range(maximo):
        numero = i + 1
        if i < len(participantes):
            uid = participantes[i]
            m = guild.get_member(int(uid)) if guild else None
            mention = m.mention if m else f"<@{uid}>"
            linhas.append(f"{numero}. {mention}")
        else:
            linhas.append(f"{numero}. —")
    return "\n".join(linhas)


class ResultadoSelect(discord.ui.Select):
    def __init__(self, painel_msg_id: int):
        self.painel_msg_id = painel_msg_id
        options = [
            discord.SelectOption(label="🏆 Vitória", value="vitoria", emoji="🏆"),
            discord.SelectOption(label="💀 Derrota", value="derrota", emoji="💀"),
            discord.SelectOption(label="🚫 N/A (não foi possível)", value="na", emoji="🚫"),
        ]
        super().__init__(placeholder="Seleciona o resultado...", options=options, custom_id="select_resultado_groove")

    async def callback(self, interaction: discord.Interaction):
        resultado = self.values[0]
        dados = escalacoes_ativas.get(self.painel_msg_id, {})

        # Registra estatísticas de Win/Lose (N/A não conta para as estatísticas,
        # pois a ação não chegou a ser concluída) — total + semanal
        if resultado in ("vitoria", "derrota"):
            db_stats   = load_db()
            is_vitoria = resultado == "vitoria"
            for uid in dados.get("participantes", []):
                for chave_membros in ("membros", "membros_semanal"):
                    m_stats = db_stats["acoes_stats"][chave_membros].setdefault(uid, {"win": 0, "lose": 0})
                    m_stats["win" if is_vitoria else "lose"] += 1
            acao_key = dados.get("acao_key")
            if acao_key:
                for chave_acoes in ("acoes", "acoes_semanal"):
                    a_stats = db_stats["acoes_stats"][chave_acoes].setdefault(
                        acao_key, {"nome": dados.get("acao_nome", acao_key), "win": 0, "lose": 0}
                    )
                    a_stats["win" if is_vitoria else "lose"] += 1
            save_db(db_stats)

        # Atualiza o REGISTRO (canal de relatório) — usa o post_msg_id salvo, não o id do painel
        canal_post = bot.get_channel(dados.get("canal_id", 0))
        if canal_post and dados.get("post_msg_id"):
            try:
                msg   = await canal_post.fetch_message(dados["post_msg_id"])
                embed = msg.embeds[0]
                embed.title = f"📋 Registo de Ação — {dados.get('acao_nome', '')}"
                if resultado == "vitoria":
                    embed.color   = COR_APROVADO
                    resultado_txt = "🏆 VITÓRIA"
                elif resultado == "derrota":
                    embed.color   = COR_RECUSADO
                    resultado_txt = "💀 DERROTA"
                else:
                    embed.color   = COR_AMARELO
                    resultado_txt = "🚫 N/A — Não foi possível realizar"

                i = _campo(embed, "Status:")
                if i is not None:
                    embed.set_field_at(i, name="Status:", value="✅ Finalizada", inline=False)

                embed.add_field(name="Resultado:", value=resultado_txt, inline=False)
                await msg.edit(embed=embed, view=None)
            except Exception as e:
                print(f"[ESCALACAO] Erro ao atualizar registo: {e}")

        # Apaga a mensagem do painel (participar/sair) — só o Registo (com o
        # resultado) deve permanecer visível depois de finalizada.
        canal_painel = bot.get_channel(dados.get("canal_id_painel", CANAL_ESCALACAO_PAINEL_ID))
        if canal_painel:
            try:
                painel_msg = await canal_painel.fetch_message(self.painel_msg_id)
                await painel_msg.delete()
            except Exception as e:
                print(f"[ESCALACAO] Erro ao apagar painel: {e}")

        if self.painel_msg_id in escalacoes_ativas:
            del escalacoes_ativas[self.painel_msg_id]
            _salvar_escalacoes_ativas()

        textos = {"vitoria": "VITÓRIA 🏆", "derrota": "DERROTA 💀", "na": "N/A 🚫"}
        await interaction.response.send_message(
            f"✅ Escalação finalizada com **{textos.get(resultado, resultado)}**!",
            ephemeral=True
        )


class FinalizarEscalacaoView(discord.ui.View):
    def __init__(self, painel_msg_id: int):
        super().__init__(timeout=60)
        self.add_item(ResultadoSelect(painel_msg_id=painel_msg_id))


class EscalacaoPainelView(discord.ui.View):
    def __init__(self, msg_id: int = 0):
        super().__init__(timeout=None)
        self.msg_id = msg_id

    @discord.ui.button(label="⚔️ Participar", style=discord.ButtonStyle.success,   custom_id="btn_esc_part_groove")
    async def participar(self, interaction: discord.Interaction, button: discord.ui.Button):
        dados = escalacoes_ativas.get(self.msg_id)
        if not dados:
            await interaction.response.send_message("❌ Escalação não encontrada ou finalizada.", ephemeral=True)
            return
        uid = str(interaction.user.id)
        if uid in dados["participantes"]:
            await interaction.response.send_message("⚠️ Já estás na lista.", ephemeral=True)
            return
        if len(dados["participantes"]) >= dados["max"]:
            await interaction.response.send_message("🚫 **Escalação cheia. Tente em uma próxima ação.**", ephemeral=True)
            return
        dados["participantes"].append(uid)
        await self._atualizar_embeds(interaction, dados)
        await interaction.response.send_message("✅ Entraste na escalação!", ephemeral=True)

    @discord.ui.button(label="🚪 Sair",       style=discord.ButtonStyle.danger,     custom_id="btn_esc_sair_groove")
    async def sair(self, interaction: discord.Interaction, button: discord.ui.Button):
        dados = escalacoes_ativas.get(self.msg_id)
        if not dados:
            await interaction.response.send_message("❌ Escalação não encontrada.", ephemeral=True)
            return
        uid = str(interaction.user.id)
        if uid not in dados["participantes"]:
            await interaction.response.send_message("⚠️ Não estás na lista.", ephemeral=True)
            return
        dados["participantes"].remove(uid)
        await self._atualizar_embeds(interaction, dados)
        await interaction.response.send_message("✅ Saíste da escalação.", ephemeral=True)

    @discord.ui.button(label="🏁 Finalizar",  style=discord.ButtonStyle.secondary,  custom_id="btn_esc_fin_groove")
    async def finalizar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not tem_gerente(interaction.user):
            await interaction.response.send_message("❌ Apenas gerentes podem finalizar.", ephemeral=True)
            return
        view = FinalizarEscalacaoView(painel_msg_id=self.msg_id)
        await interaction.response.send_message("Seleciona o resultado:", view=view, ephemeral=True)

    async def _atualizar_embeds(self, interaction: discord.Interaction, dados: dict):
        guild = interaction.guild
        valor_participantes = _lista_participantes(dados["participantes"], dados["max"], guild)
        _salvar_escalacoes_ativas()

        # Painel (participar/sair)
        canal_painel = bot.get_channel(dados["canal_id_painel"])
        if canal_painel:
            try:
                msg = await canal_painel.fetch_message(self.msg_id)
                embed = msg.embeds[0]
                i = _campo(embed, "Participantes:")
                if i is not None:
                    embed.set_field_at(i, name="Participantes:", value=valor_participantes, inline=False)
                await msg.edit(embed=embed)
            except Exception:
                pass

        # Registo/relatório
        canal_post = bot.get_channel(dados["canal_id"])
        if canal_post:
            try:
                msg2 = await canal_post.fetch_message(dados["post_msg_id"])
                embed2 = msg2.embeds[0]
                i2 = _campo(embed2, "Participantes:")
                if i2 is not None:
                    embed2.set_field_at(i2, name="Participantes:", value=valor_participantes, inline=False)
                await msg2.edit(embed=embed2)
            except Exception:
                pass


def _slugify_acao(nome: str) -> str:
    """Gera uma chave estável a partir do nome digitado, para que ações
    customizadas com o mesmo nome acumulem estatísticas juntas."""
    slug = nome.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "_", slug).strip("_")
    return f"custom_{slug}" if slug else "custom_acao"


async def _criar_escalacao(interaction: discord.Interaction, armamento_key: str, acao_key: str, acao_custom: dict | None = None):
    arm_label = ARMAMENTOS.get(armamento_key, armamento_key)
    acao      = acao_custom if acao_custom is not None else ACOES[acao_key]
    guild     = interaction.guild

    canal_post   = bot.get_channel(CANAL_ESCALACAO_POST_ID)
    canal_painel = bot.get_channel(CANAL_ESCALACAO_PAINEL_ID)
    if not canal_post or not canal_painel:
        await interaction.response.send_message("❌ Canais de escalação não encontrados.", ephemeral=True)
        return

    valor_inicial = _lista_participantes([], acao["max"], guild)

    # Embed de registo (vira "Registo de Ação" ao finalizar)
    embed_post = discord.Embed(
        title=f"⚔️ {acao['nome'].upper()}",
        color=COR_GROVE, timestamp=datetime.now(timezone.utc)
    )
    embed_post.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
    embed_post.add_field(name="Ação:",           value=acao["nome"],   inline=False)
    embed_post.add_field(name="Armamento:",      value=arm_label,      inline=True)
    embed_post.add_field(name="Nº de membros:",  value=acao["label"],  inline=True)
    embed_post.add_field(name="Status:",         value="Em andamento", inline=False)
    embed_post.add_field(name="Participantes:",  value=valor_inicial,  inline=False)
    embed_post.set_footer(text=f"Silver Dollar • Criado por {interaction.user.display_name}")

    msg_post = await canal_post.send(embed=embed_post)

    # Painel de participação (Participar/Sair/Finalizar)
    embed_painel = discord.Embed(
        title=f"⚔️ Escalação Ativa: {acao['nome']}",
        description=(
            f"**Contingente:** {acao['label']}\n\n"
            "Use os botões abaixo para participar ou sair."
        ),
        color=COR_GROVE
    )
    embed_painel.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
    embed_painel.add_field(name="Participantes:", value=valor_inicial, inline=False)
    embed_painel.set_footer(text="Silver Dollar")

    msg_painel = await canal_painel.send(content="@everyone", embed=embed_painel,
                                          allowed_mentions=discord.AllowedMentions(everyone=True))
    await msg_painel.edit(view=EscalacaoPainelView(msg_id=msg_painel.id))

    escalacoes_ativas[msg_painel.id] = {
        "acao_nome":      acao["nome"],
        "acao_key":       acao_key,
        "armamento":      arm_label,
        "max":            acao["max"],
        "participantes":  [],
        "canal_id":        canal_post.id,
        "canal_id_painel": canal_painel.id,
        "post_msg_id":    msg_post.id,
    }
    _salvar_escalacoes_ativas()
    bot.add_view(EscalacaoPainelView(msg_id=msg_painel.id), message_id=msg_painel.id)

    await interaction.response.send_message(
        f"✅ Escalação de **{acao['nome']}** criada em {canal_painel.mention}!",
        ephemeral=True
    )


class EscalacaoCustomModal(discord.ui.Modal, title="✏️ Ação Customizada"):
    nome_acao = discord.ui.TextInput(label="Nome da ação", placeholder="Ex: Roubo ao Cofre X", required=True, max_length=80)
    qtd_min   = discord.ui.TextInput(label="Nº mínimo de membros", placeholder="Ex: 4", required=True, max_length=3)
    qtd_max   = discord.ui.TextInput(label="Nº máximo de membros", placeholder="Ex: 6 (pode ser igual ao mínimo)", required=True, max_length=3)

    def __init__(self, armamento_key: str):
        super().__init__()
        self.armamento_key = armamento_key

    async def on_submit(self, interaction: discord.Interaction):
        try:
            minimo = int(self.qtd_min.value.strip())
            maximo = int(self.qtd_max.value.strip())
        except ValueError:
            await interaction.response.send_message("❌ Quantidades inválidas. Use apenas números.", ephemeral=True)
            return
        if minimo < 1 or maximo < 1 or maximo < minimo:
            await interaction.response.send_message(
                "❌ Verifique os números — o máximo deve ser maior ou igual ao mínimo, e ambos maiores que 0.",
                ephemeral=True
            )
            return

        nome = self.nome_acao.value.strip()
        if not nome:
            await interaction.response.send_message("❌ Informe um nome para a ação.", ephemeral=True)
            return

        label = f"{minimo} membros" if minimo == maximo else f"{minimo} a {maximo} membros"
        acao_custom = {"nome": nome, "min": minimo, "max": maximo, "label": label}
        acao_key    = _slugify_acao(nome)

        await _criar_escalacao(interaction, self.armamento_key, acao_key, acao_custom=acao_custom)


class EscalacaoAcaoSelect(discord.ui.Select):
    def __init__(self, armamento_key: str):
        self.armamento_key = armamento_key
        options = [
            discord.SelectOption(label=v["nome"], value=k, description=v["label"])
            for k, v in ACOES.items()
        ]
        options.append(
            discord.SelectOption(
                label="✏️ Ação Customizada", value="custom",
                description="Digite o nome e o contingente manualmente", emoji="✏️"
            )
        )
        super().__init__(placeholder="Seleciona a ação a ser puxada...", options=options, custom_id="select_acao_groove")

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "custom":
            await interaction.response.send_modal(EscalacaoCustomModal(armamento_key=self.armamento_key))
            return
        await _criar_escalacao(interaction, self.armamento_key, self.values[0])


class EscalacaoAcaoView(discord.ui.View):
    def __init__(self, armamento_key: str):
        super().__init__(timeout=60)
        self.add_item(EscalacaoAcaoSelect(armamento_key=armamento_key))


class EscalacaoArmSelect(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=v, value=k) for k, v in ARMAMENTOS.items()]
        super().__init__(placeholder="Seleciona o armamento...", options=options, custom_id="select_arm_groove")

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="⚔️ Criar Escalação", description="Agora seleciona a **ação** a ser puxada:", color=COR_GROVE)
        await interaction.response.send_message(embed=embed, view=EscalacaoAcaoView(armamento_key=self.values[0]), ephemeral=True)


class EscalacaoIniciarView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(EscalacaoArmSelect())


@bot.tree.command(name="escalacao", description="Cria uma escalação de ação.")
@app_commands.checks.has_permissions(manage_messages=True)
async def escalacao(interaction: discord.Interaction):
    embed = discord.Embed(title="⚔️ Criar Escalação", description="Seleciona o armamento:", color=COR_GROVE)
    await interaction.response.send_message(embed=embed, view=EscalacaoIniciarView(), ephemeral=True)


@bot.tree.command(name="setup_escalacao", description="Envia o painel de escalação no canal.")
@app_commands.checks.has_permissions(administrator=True)
async def setup_escalacao(interaction: discord.Interaction):
    embed = discord.Embed(
        title="⚔️ Escalações – Silver Dollar",
        description="Quando uma escalação for criada, os botões de **Participar / Sair / Finalizar** aparecerão aqui.\n\nFique de olho! 🩷",
        color=COR_GROVE
    )
    embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
    embed.set_footer(text="Silver Dollar")
    await interaction.channel.send(embed=embed)
    await interaction.response.send_message("✅ Painel de escalação enviado!", ephemeral=True)


# ══════════════════════════════════════════════════════════════
#   REGISTRO MANUAL DE AÇÃO (WIN/LOSE)
# ══════════════════════════════════════════════════════════════
# Painel fixo com um botão "Criar Nova Ação". Ao clicar, abre um formulário
# pedindo o nome do fight e contra qual organização foi, e em seguida a
# pessoa escolhe o resultado (Vitória/Derrota) em botões — tudo registado
# manualmente pelo próprio membro, sem depender do sistema de escalação.

class WinLoseResultView(discord.ui.View):
    def __init__(self, nome_fight: str, org: str):
        super().__init__(timeout=180)
        self.nome_fight = nome_fight
        self.org        = org

    async def _registar(self, interaction: discord.Interaction, resultado: str):
        agora = datetime.now(timezone.utc)
        embed = discord.Embed(
            title="⚔️ Ação Registada",
            color=COR_APROVADO if resultado == "vitoria" else COR_RECUSADO,
            timestamp=agora
        )
        embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
        embed.add_field(name="🗡️ Fight",        value=self.nome_fight, inline=True)
        embed.add_field(name="🏴 Org Adversária", value=self.org,        inline=True)
        embed.add_field(name="📊 Resultado",     value="🏆 VITÓRIA" if resultado == "vitoria" else "💀 DERROTA", inline=True)
        embed.add_field(name="👤 Registado por", value=interaction.user.mention, inline=False)
        embed.set_footer(text=f"ID: {interaction.user.id}")

        canal_log = bot.get_channel(CANAL_LOG_WINLOSE_ID)
        if canal_log:
            await canal_log.send(embed=embed)

        for item in self.children:
            item.disabled = True

        texto = "🏆 Vitória" if resultado == "vitoria" else "💀 Derrota"
        await interaction.response.edit_message(
            content=f"✅ Ação **{self.nome_fight}** registada como **{texto}**!",
            view=self
        )

    @discord.ui.button(label="🏆 Vitória", style=discord.ButtonStyle.success, custom_id="btn_wl_vitoria")
    async def vitoria(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._registar(interaction, "vitoria")

    @discord.ui.button(label="💀 Derrota", style=discord.ButtonStyle.danger, custom_id="btn_wl_derrota")
    async def derrota(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._registar(interaction, "derrota")


class WinLoseModal(discord.ui.Modal, title="🗡️ Registar Nova Ação"):
    nome_fight = discord.ui.TextInput(label="Nome do Fight", placeholder="Ex: Invasão na Gruta", required=True, max_length=100)
    org        = discord.ui.TextInput(label="Contra qual Org?", placeholder="Ex: MS13", required=True, max_length=80)

    async def on_submit(self, interaction: discord.Interaction):
        view = WinLoseResultView(nome_fight=self.nome_fight.value, org=self.org.value)
        await interaction.response.send_message(
            f"🗡️ **Fight:** {self.nome_fight.value}\n🏴 **Org:** {self.org.value}\n\n"
            "Seleciona o resultado da ação:",
            view=view, ephemeral=True
        )


class WinLosePainelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🗡️ Criar Nova Ação", style=discord.ButtonStyle.primary, custom_id="btn_criar_acao_winlose")
    async def criar_acao(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(WinLoseModal())


@bot.tree.command(name="setup_winlose", description="Envia o painel de registo manual de ações (Win/Lose).")
@app_commands.checks.has_permissions(administrator=True)
async def setup_winlose(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🗡️ Central de Planejamento",
        description="Clica abaixo para planejar uma nova ação, informar contra qual organização foi e registar o resultado.",
        color=COR_GROVE
    )
    embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
    embed.set_thumbnail(url=LOGO_URL)
    embed.set_footer(text="Silver Dollar")
    await interaction.channel.send(embed=embed, view=WinLosePainelView())
    await interaction.response.send_message("✅ Painel de Win/Lose enviado!", ephemeral=True)


# ══════════════════════════════════════════════════════════════
#   CONTAGEM DE KILLS
# ══════════════════════════════════════════════════════════════
# Painel fixo com um botão "Registar Kills". Ao clicar, abre um formulário
# onde a pessoa escreve a quantidade (1 a 12) e, opcionalmente, o link do clip.

class ContagemModal(discord.ui.Modal, title="☠️ Registar Kills"):
    kills     = discord.ui.TextInput(label="Quantidade de Kills (1 a 12)", placeholder="Ex: 5", required=True, max_length=2)
    link_clip = discord.ui.TextInput(label="Link do Clip (opcional)", placeholder="https://...", required=False, max_length=300)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            qtd = int(self.kills.value.strip())
        except ValueError:
            await interaction.response.send_message("❌ Quantidade inválida. Use apenas números.", ephemeral=True)
            return
        if qtd < 1 or qtd > 12:
            await interaction.response.send_message("❌ A quantidade deve estar entre 1 e 12.", ephemeral=True)
            return

        embed = discord.Embed(title="☠️ Kills Registadas", color=COR_GROVE, timestamp=datetime.now(timezone.utc))
        embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
        embed.add_field(name="👤 Membro", value=interaction.user.mention, inline=True)
        embed.add_field(name="☠️ Kills",  value=f"**{qtd}**",             inline=True)
        if self.link_clip.value:
            embed.add_field(name="🎬 Clip", value=self.link_clip.value, inline=False)
        embed.set_footer(text=f"ID: {interaction.user.id}")

        canal_log = bot.get_channel(CANAL_LOG_CONTAGEM_ID)
        if canal_log:
            await canal_log.send(embed=embed)
            await interaction.response.send_message(f"✅ **{qtd}** kill(s) registada(s)!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Canal de log de contagem não configurado.", ephemeral=True)


class ContagemPainelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="☠️ Registar Kills", style=discord.ButtonStyle.danger, custom_id="btn_registar_kills")
    async def registar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ContagemModal())


@bot.tree.command(name="setup_contagem", description="Envia o painel de contagem de kills.")
@app_commands.checks.has_permissions(administrator=True)
async def setup_contagem(interaction: discord.Interaction):
    embed = discord.Embed(
        title="☠️ Contagem de Kills",
        description="Clica abaixo para registar suas kills e, se quiser, o link do clip.",
        color=COR_GROVE
    )
    embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
    embed.set_thumbnail(url=LOGO_URL)
    embed.set_footer(text="Silver Dollar")
    await interaction.channel.send(embed=embed, view=ContagemPainelView())
    await interaction.response.send_message("✅ Painel de contagem enviado!", ephemeral=True)


# ══════════════════════════════════════════════════════════════
#   AUSÊNCIA
# ══════════════════════════════════════════════════════════════

class AusenciaModal(discord.ui.Modal, title="Registar Ausência"):
    motivo = discord.ui.TextInput(label="Motivo",            placeholder="Motivo da ausência", required=True, style=discord.TextStyle.paragraph)
    saida  = discord.ui.TextInput(label="Data de Saída",     placeholder="Ex: 13/05/2026",     required=True, max_length=20)
    volta  = discord.ui.TextInput(label="Previsão de Volta", placeholder="Ex: 20/05/2026",     required=True, max_length=20)

    async def on_submit(self, interaction: discord.Interaction):
        canal = bot.get_channel(CANAL_APROV_AUSENCIA_ID)
        if not canal:
            await interaction.response.send_message("❌ Canal não encontrado.", ephemeral=True)
            return
        agora = datetime.now(timezone.utc)
        embed = discord.Embed(title="😴 Solicitação de Ausência", color=COR_AUSENCIA, timestamp=agora)
        embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.add_field(name="Utilizador", value=interaction.user.mention, inline=True)
        embed.add_field(name="Motivo",  value=self.motivo.value,        inline=False)
        embed.add_field(name="Saída",   value=self.saida.value,         inline=True)
        embed.add_field(name="Volta",   value=self.volta.value,         inline=True)
        embed.set_footer(text=f"ID: {interaction.user.id}")
        view = AprovarRecusarAusenciaView(
            user_id=interaction.user.id,
            motivo=self.motivo.value,
            saida=self.saida.value,
            volta=self.volta.value,
            canal_origem_id=interaction.channel_id
        )
        await canal.send(embed=embed, view=view)
        await interaction.response.send_message("✅ Solicitação de ausência enviada! Aguarda.", ephemeral=True)


class RetirarAusenciaView(discord.ui.View):
    def __init__(self, user_id: int = 0):
        super().__init__(timeout=None)
        self.user_id = user_id

    @discord.ui.button(label="✅ Retirar Ausência", style=discord.ButtonStyle.success, custom_id="btn_ret_aus_groove")
    async def retirar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id and not tem_staff(interaction.user):
            await interaction.response.send_message("❌ Sem permissão.", ephemeral=True)
            return

        db  = load_db()
        uid = str(self.user_id)
        aus = db["ausencias"].get(uid, {})
        if uid in db["ausencias"]:
            db["ausencias"][uid]["ativa"]   = False
            db["ausencias"][uid]["retorno"] = datetime.now(timezone.utc).isoformat()
        save_db(db)

        membro    = interaction.guild.get_member(self.user_id)
        cargo_aus = interaction.guild.get_role(CARGO_AUSENCIA_ID)
        if membro and cargo_aus and cargo_aus in membro.roles:
            await membro.remove_roles(cargo_aus, reason="Retornou da ausência")

        button.disabled = True
        button.label    = "Ausência Encerrada"
        await interaction.response.edit_message(content="✅ Ausência encerrada! Bem-vindo de volta. 🩷", view=self)

        canal_log = bot.get_channel(CANAL_LOG_AUSENCIA_ID)
        if canal_log:
            log = discord.Embed(title="✅ Ausência Retirada", color=COR_APROVADO, timestamp=datetime.now(timezone.utc))
            log.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
            log.set_thumbnail(url=interaction.user.display_avatar.url)
            log.add_field(name="Membro", value=interaction.user.mention, inline=True)
            log.add_field(name="Motivo", value=aus.get("motivo", "—"),   inline=True)
            log.add_field(name="Saída",  value=aus.get("saida",  "—"),   inline=True)
            log.add_field(name="Volta",  value=aus.get("volta",  "—"),   inline=True)
            await canal_log.send(embed=log)

        await asyncio.sleep(5)
        thread = interaction.channel
        if isinstance(thread, (discord.Thread, discord.TextChannel)):
            try:
                await thread.delete()
            except Exception:
                pass


class AprovarRecusarAusenciaView(discord.ui.View):
    def __init__(self, user_id: int = 0, motivo: str = "", saida: str = "", volta: str = "", canal_origem_id: int = 0):
        super().__init__(timeout=None)
        self.user_id         = user_id
        self.motivo          = motivo
        self.saida           = saida
        self.volta           = volta
        self.canal_origem_id = canal_origem_id

    @discord.ui.button(label="Aprovar", style=discord.ButtonStyle.success, custom_id="btn_apr_aus_groove", emoji="✅")
    async def aprovar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not tem_staff(interaction.user):
            await interaction.response.send_message("❌ Sem permissão.", ephemeral=True)
            return
        guild  = interaction.guild
        membro = guild.get_member(self.user_id)
        if not membro:
            await interaction.response.send_message("❌ Utilizador não encontrado.", ephemeral=True)
            return

        cargo_aus = guild.get_role(CARGO_AUSENCIA_ID)
        if cargo_aus:
            await membro.add_roles(cargo_aus, reason=f"Ausência aprovada por {interaction.user}")

        db  = load_db()
        uid = str(self.user_id)
        db["ausencias"][uid] = {
            "ativa": True, "motivo": self.motivo,
            "saida": self.saida, "volta": self.volta,
            "aprovado_em": datetime.now(timezone.utc).isoformat(),
            "canal_origem_id": self.canal_origem_id
        }
        save_db(db)

        embed = interaction.message.embeds[0]
        embed.color = COR_APROVADO
        embed.add_field(name="✅ APROVADO POR", value=interaction.user.mention, inline=False)
        await interaction.response.edit_message(embed=embed, view=None)

        # Thread no canal onde foi solicitado
        canal_aus = bot.get_channel(self.canal_origem_id) or bot.get_channel(CANAL_APROV_AUSENCIA_ID)
        if canal_aus:
            try:
                thread = await canal_aus.create_thread(
                    name=f"ausencia-{membro.display_name}",
                    type=discord.ChannelType.private_thread
                )
                await thread.add_user(membro)
                view_ret = RetirarAusenciaView(user_id=self.user_id)
                await thread.send(
                    f"{membro.mention}\n\n**😴 Ausência aprovada!**\n\n"
                    f"**Motivo:** {self.motivo}\n**Saída:** {self.saida}\n**Volta:** {self.volta}\n\n"
                    "Quando retornar, clica no botão abaixo:",
                    view=view_ret
                )
            except Exception as e:
                print(f"[AUSENCIA] Erro ao criar thread: {e}")

        canal_log = bot.get_channel(CANAL_LOG_AUSENCIA_ID)
        if canal_log:
            log = discord.Embed(title="😴 Ausência Aprovada", color=COR_AUSENCIA, timestamp=datetime.now(timezone.utc))
            log.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
            log.set_thumbnail(url=membro.display_avatar.url)
            log.add_field(name="Membro",       value=membro.mention,           inline=True)
            log.add_field(name="Aprovado por", value=interaction.user.mention, inline=True)
            log.add_field(name="Motivo",       value=self.motivo,              inline=False)
            log.add_field(name="Saída",        value=self.saida,               inline=True)
            log.add_field(name="Volta",        value=self.volta,               inline=True)
            await canal_log.send(embed=log)

        await interaction.followup.send(f"✅ Ausência de {membro.mention} aprovada!", ephemeral=True)

    @discord.ui.button(label="Recusar", style=discord.ButtonStyle.danger, custom_id="btn_rec_aus_groove", emoji="❌")
    async def recusar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not tem_staff(interaction.user):
            await interaction.response.send_message("❌ Sem permissão.", ephemeral=True)
            return
        embed = interaction.message.embeds[0]
        embed.color = COR_RECUSADO
        embed.add_field(name="❌ RECUSADO POR", value=interaction.user.mention, inline=False)
        await interaction.response.edit_message(embed=embed, view=None)
        await interaction.followup.send("❌ Ausência recusada.", ephemeral=True)


class AusenciaSetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="😴 Registar Ausência", style=discord.ButtonStyle.primary, custom_id="btn_reg_aus_groove")
    async def registar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AusenciaModal())


@bot.tree.command(name="setup_ausencia", description="Envia o painel de ausência no canal.")
@app_commands.checks.has_permissions(administrator=True)
async def setup_ausencia(interaction: discord.Interaction):
    embed = discord.Embed(
        title="😴 Ausência – Silver Dollar",
        description=(
            "Precisa se ausentar?\n\n"
            "Clica no botão abaixo, preencha o formulário e aguarda a aprovação.\n"
            "Ao seres aprovado(a), receberás automaticamente o cargo de **Ausência**."
        ),
        color=COR_AUSENCIA
    )
    embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
    embed.set_thumbnail(url=LOGO_URL)
    embed.set_footer(text="Silver Dollar")
    await interaction.channel.send(embed=embed, view=AusenciaSetupView())
    await interaction.response.send_message("✅ Painel de ausência enviado!", ephemeral=True)


# ══════════════════════════════════════════════════════════════
#   META DE FARM SEMANAL
# ══════════════════════════════════════════════════════════════
# A meta é semanal, permanente (fixa em um canal) e é atualizada sempre que
# alguém usa "Trocar Meta" dentro do ticket de farm. Itens com valor 0 (ou
# não informados) não aparecem no embed/anúncio — apenas o que tiver 1+.

META_LABELS = {
    "oleo":         ("🛢️ Óleo",              "Barris"),
    "plastico":     ("🧴 Plástico",           "Unidades"),
    "garrafas":     ("🍾 Garrafas Vazias",    "Unidades"),
    "tinta":        ("🎨 Tinta",              "Unidades"),
    "crop_maconha": ("🌿 Crop de Maconha",    "Unidades"),
}

# sinônimos aceitos no texto livre do modal -> chave interna
META_CHAVES = {
    "oleo":         ["oleo", "óleo"],
    "plastico":     ["plastico", "plástico"],
    "garrafas":     ["garrafa"],
    "tinta":        ["tinta"],
    "crop_maconha": ["crop"],
    "dinheiro_sujo":["dinheiro"],
}


def _valor_int(valor) -> int:
    try:
        return int(str(valor).replace(".", "").replace(",", ""))
    except (ValueError, TypeError):
        return 0


def build_meta_embed(db: dict) -> discord.Embed:
    m = db.get("meta", META_PADRAO)
    embed = discord.Embed(
        title="📊 META DE FARM SEMANAL",
        description="Com a mudança de necessidades, o novo farm será dos seguintes itens:",
        color=COR_GROVE, timestamp=datetime.now(timezone.utc)
    )
    embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)

    for chave, (label, unidade) in META_LABELS.items():
        v = _valor_int(m.get(chave))
        if v >= 1:
            embed.add_field(name=label, value=f"{fmt_valor(m.get(chave))} {unidade}", inline=True)

    dv = _valor_int(m.get("dinheiro_sujo"))
    if dv >= 1:
        embed.add_field(name="💵 Dinheiro Sujo", value=f"R$ {fmt_valor(m.get('dinheiro_sujo'))}", inline=False)

    embed.add_field(
        name="📌 Observação",
        value="O cumprimento da meta é fundamental para que o estoque não zere e todos tenham material para trabalhar.",
        inline=False
    )
    embed.set_footer(text="Silver Dollar • Meta Semanal")
    return embed


async def atualizar_meta_semanal(guild: discord.Guild | None = None) -> discord.Message | None:
    """Edita (ou cria) a mensagem fixa da Meta Semanal no canal de meta."""
    canal_meta = bot.get_channel(CANAL_META_ID)
    if not canal_meta:
        return None

    db    = load_db()
    embed = build_meta_embed(db)
    msg_id = db["meta"].get("message_id")

    msg = None
    if msg_id:
        try:
            msg = await canal_meta.fetch_message(msg_id)
            await msg.edit(embed=embed)
        except Exception:
            msg = None

    if msg is None:
        msg = await canal_meta.send(embed=embed)
        db["meta"]["message_id"] = msg.id
        save_db(db)

    return msg


@bot.tree.command(name="meta", description="Exibe/atualiza a Meta de Farm Semanal.")
async def meta(interaction: discord.Interaction):
    msg = await atualizar_meta_semanal(interaction.guild)
    if msg:
        await interaction.response.send_message(f"✅ Meta Semanal atualizada em {msg.channel.mention}!", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Canal de meta não configurado.", ephemeral=True)


# ══════════════════════════════════════════════════════════════
#   TICKETS  (apenas Sala de Farm)
# ══════════════════════════════════════════════════════════════

def _parse_meta_itens(texto: str) -> dict:
    """Converte um texto multilinha 'Item: Quantidade' em {chave_interna: quantidade},
    reconhecendo Óleo, Plástico, Garrafas, Tinta, Crop de Maconha e Dinheiro Sujo."""
    valores: dict[str, int] = {}
    for linha in texto.splitlines():
        linha = linha.strip()
        if not linha or ":" not in linha:
            continue
        nome, qtd_txt = linha.split(":", 1)
        nome    = nome.strip().lower()
        qtd_txt = qtd_txt.strip().replace(".", "")
        try:
            qtd = int(qtd_txt)
        except ValueError:
            continue
        for chave, sinonimos in META_CHAVES.items():
            if any(s in nome for s in sinonimos):
                valores[chave] = qtd
                break
    return valores


class TrocarMetaModal(discord.ui.Modal, title="🔄 Mudança de Farm"):
    """Cada item tem seu próprio campo — o utilizador digita SÓ a quantidade,
    não precisa escrever o nome do item."""
    oleo         = discord.ui.TextInput(label="🛢️ Óleo (Barris)",           placeholder="Ex: 40", required=False, max_length=10)
    plastico     = discord.ui.TextInput(label="🧴 Plástico (Unidades)",      placeholder="Ex: 70", required=False, max_length=10)
    garrafas     = discord.ui.TextInput(label="🍾 Garrafas Vazias (Unid.)",  placeholder="Ex: 30", required=False, max_length=10)
    tinta        = discord.ui.TextInput(label="🎨 Tinta (Unidades)",         placeholder="Ex: 20", required=False, max_length=10)
    crop_maconha = discord.ui.TextInput(label="🌿 Crop de Maconha (Unid.)",  placeholder="Ex: 15", required=False, max_length=10)

    def __init__(self, modo: str):
        super().__init__()
        self.modo = modo  # "individual" ou "geral"

    async def on_submit(self, interaction: discord.Interaction):
        # Defer imediatamente: o restante do processamento (editar mensagem fixa,
        # anunciar em outro canal, etc.) pode levar mais de 3s e era isso que
        # causava o "não respondeu a tempo" no botão Geral.
        await interaction.response.defer(ephemeral=True, thinking=False)

        campos = {
            "oleo":         self.oleo.value,
            "plastico":     self.plastico.value,
            "garrafas":     self.garrafas.value,
            "tinta":        self.tinta.value,
            "crop_maconha": self.crop_maconha.value,
        }
        valores: dict[str, int] = {}
        for chave, texto in campos.items():
            texto = (texto or "").strip().replace(".", "")
            if not texto:
                continue
            try:
                valores[chave] = int(texto)
            except ValueError:
                continue

        if not valores:
            await interaction.followup.send("❌ Nenhum item válido informado.", ephemeral=True)
            return

        linhas = []
        for chave, qtd in valores.items():
            if qtd < 1:
                continue  # itens com 0 não aparecem
            label, unidade = META_LABELS[chave]
            linhas.append(f"{label}: {fmt_valor(qtd)} {unidade}")
        texto_itens = "\n".join(linhas) if linhas else "Nenhum item com quantidade informada."

        if self.modo == "individual":
            embed = discord.Embed(
                title="🔄 Meta Alterada (Individual)",
                description=texto_itens,
                color=COR_GROVE, timestamp=datetime.now(timezone.utc)
            )
            embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
            embed.set_footer(text=f"Alterado por {interaction.user.display_name} • Válido apenas nesta sala")
            await interaction.channel.send(embed=embed)
            await interaction.followup.send("✅ Meta individual registada nesta sala!", ephemeral=True)
        else:
            db = load_db()
            for chave, qtd in valores.items():
                db["meta"][chave] = qtd
            save_db(db)
            await atualizar_meta_semanal(interaction.guild)

            canal_anuncio = bot.get_channel(CANAL_INFO_META_ID) if CANAL_INFO_META_ID else None
            canal_anuncio = canal_anuncio or bot.get_channel(CANAL_META_ID)
            if canal_anuncio:
                embed_anuncio = discord.Embed(
                    title="📢 Meta de Farm Atualizada",
                    description=texto_itens,
                    color=COR_GROVE, timestamp=datetime.now(timezone.utc)
                )
                embed_anuncio.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
                embed_anuncio.set_footer(text=f"Alterado por {interaction.user.display_name}")
                try:
                    await canal_anuncio.send(
                        content="@here",
                        embed=embed_anuncio,
                        allowed_mentions=discord.AllowedMentions(everyone=True)
                    )
                except Exception as e:
                    print(f"[META] Erro ao anunciar: {e}")

            await interaction.followup.send("✅ Meta geral atualizada e anunciada!", ephemeral=True)

        canal_log = bot.get_channel(CANAL_LOG_CALC_ID)
        if canal_log:
            log = discord.Embed(title="🔄 Log – Trocar Meta", color=COR_LOG, timestamp=datetime.now(timezone.utc))
            log.add_field(name="Alterado por", value=interaction.user.mention,        inline=True)
            log.add_field(name="Modo",         value=self.modo.capitalize(),          inline=True)
            log.add_field(name="Itens",        value=texto_itens,                     inline=False)
            await canal_log.send(embed=log)


class TrocarMetaTipoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(label="📍 Individual", style=discord.ButtonStyle.secondary, custom_id="btn_meta_individual_groove")
    async def individual(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TrocarMetaModal(modo="individual"))

    @discord.ui.button(label="📢 Geral", style=discord.ButtonStyle.success, custom_id="btn_meta_geral_groove")
    async def geral(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TrocarMetaModal(modo="geral"))


class CandidaturaModal(discord.ui.Modal, title="📋 Candidatura à Organização"):
    nome            = discord.ui.TextInput(label="Nome", placeholder="O teu nome", required=True, max_length=80)
    idade           = discord.ui.TextInput(label="Idade", placeholder="Ex: 21", required=True, max_length=3)
    clips           = discord.ui.TextInput(label="Clips / HLs", placeholder="Link para os teus clips ou highlights", required=True, max_length=300)
    disponibilidade = discord.ui.TextInput(
        label="Disponibilidade", placeholder="Ex: Todos os dias, das 20h às 00h",
        style=discord.TextStyle.paragraph, required=True, max_length=300
    )

    async def on_submit(self, interaction: discord.Interaction):
        guild     = interaction.guild
        membro    = interaction.user
        categoria = guild.get_channel(CATEGORIA_FARM_ID)
        if not categoria or not isinstance(categoria, discord.CategoryChannel):
            await interaction.response.send_message("❌ Categoria não encontrada.", ephemeral=True)
            return

        canal_nome       = f"📋・{membro.display_name.lower().replace(' ', '-')}"
        cargo_staff_objs = [guild.get_role(cid) for cid in CARGOS_STAFF_IDS if guild.get_role(cid)]
        cargo_gerente    = guild.get_role(CARGO_GERENTE_ID)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            membro:             discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            guild.me:           discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True),
        }
        for cr in cargo_staff_objs:
            overwrites[cr] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, manage_channels=True)
        if cargo_gerente:
            overwrites[cargo_gerente] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, manage_channels=True)

        canal_ticket = await guild.create_text_channel(
            name=canal_nome, category=categoria, overwrites=overwrites,
            reason=f"Candidatura de {membro}"
        )

        embed = discord.Embed(title="📋 Candidatura à Organização", color=COR_GROVE, timestamp=datetime.now(timezone.utc))
        embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
        embed.set_thumbnail(url=membro.display_avatar.url)
        embed.add_field(name="👤 Candidato",         value=membro.mention,               inline=True)
        embed.add_field(name="📛 Nome",               value=self.nome.value,              inline=True)
        embed.add_field(name="🎂 Idade",              value=self.idade.value,             inline=True)
        embed.add_field(name="🎬 Clips / HLs",        value=self.clips.value,             inline=False)
        embed.add_field(name="🕒 Disponibilidade",    value=self.disponibilidade.value,   inline=False)
        embed.add_field(name="Estado",               value="A aguardar análise...",       inline=False)
        embed.set_footer(text=f"ID: {membro.id}")

        view = CandidaturaView(user_id=membro.id)
        msg  = await canal_ticket.send(content=membro.mention, embed=embed, view=view)
        await msg.pin()

        if cargo_gerente:
            await canal_ticket.send(
                f"{cargo_gerente.mention} — nova candidatura de {membro.mention}!",
                allowed_mentions=discord.AllowedMentions(roles=True)
            )

        await interaction.response.send_message(f"✅ Candidatura submetida: {canal_ticket.mention}", ephemeral=True)


class CandidaturaView(discord.ui.View):
    def __init__(self, user_id: int = 0):
        super().__init__(timeout=None)
        self.user_id = user_id

    @discord.ui.button(label="📣 Notificar Candidato", style=discord.ButtonStyle.secondary, custom_id="btn_farm_ping_groove")
    async def notificar(self, interaction: discord.Interaction, button: discord.ui.Button):
        membro = interaction.guild.get_member(self.user_id)
        if membro:
            await interaction.response.send_message(
                f"{membro.mention} — o responsável vai analisar a tua candidatura em breve! 💜",
                allowed_mentions=discord.AllowedMentions(users=True)
            )
        else:
            await interaction.response.send_message("❌ Candidato não encontrado.", ephemeral=True)


class PainelTicketsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📋 Candidatar-me", style=discord.ButtonStyle.success, custom_id="btn_abrir_farm_groove")
    async def abrir_candidatura(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CandidaturaModal())


@bot.tree.command(name="setup_tickets", description="Envia o painel de candidaturas no canal.")
@app_commands.checks.has_permissions(administrator=True)
async def setup_tickets(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📋 Candidatura – Silver Dollar",
        description=(
            "Queres juntar-te à organização?\n\n"
            "Clica no botão abaixo para preencheres a tua candidatura.\n"
            "Um responsável irá analisar o teu pedido em breve. 💜"
        ),
        color=COR_GROVE
    )
    embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
    embed.set_thumbnail(url=LOGO_URL)
    embed.set_footer(text="Silver Dollar")
    await interaction.channel.send(embed=embed, view=PainelTicketsView())
    await interaction.response.send_message("✅ Painel enviado!", ephemeral=True)


@bot.tree.command(name="trocar_meta", description="[Staff] Altera a meta de farm (individual ou geral).")
@app_commands.checks.has_permissions(manage_messages=True)
async def trocar_meta_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔄 Trocar Meta",
        description=(
            "**📍 Individual** — altera apenas neste canal.\n"
            "**📢 Geral** — atualiza a Meta Semanal e anuncia com @here em #info-meta."
        ),
        color=COR_GROVE
    )
    await interaction.response.send_message(embed=embed, view=TrocarMetaTipoView(), ephemeral=True)


# ══════════════════════════════════════════════════════════════
#   STATUS  (Ações por Membro / Ações da Facção)
#   Cada categoria pode ser vista em modo "total" (desde o início do bot)
#   ou "semanal" (reinicia toda segunda-feira 00:00 UTC).
# ══════════════════════════════════════════════════════════════

def _barra_progresso(pct: float, tamanho: int = 10) -> str:
    pct = max(0, min(100, pct))
    cheio = round(pct / 100 * tamanho)
    return "🟩" * cheio + "⬜" * (tamanho - cheio)


def build_acoes_membro_embed(guild: discord.Guild, uid: str, periodo: str = "total") -> discord.Embed:
    db      = load_db()
    chave   = "membros" if periodo == "total" else "membros_semanal"
    stats   = db.get("acoes_stats", {}).get(chave, {}).get(uid)
    membro  = guild.get_member(int(uid)) if guild else None
    nome    = membro.display_name if membro else f"ID {uid}"
    rotulo  = "Total (desde o início)" if periodo == "total" else "Semanal"

    embed = discord.Embed(title=f"⚔️ Status de Ações — {nome} ({rotulo})", color=COR_GROVE, timestamp=datetime.now(timezone.utc))
    embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
    if membro:
        embed.set_thumbnail(url=membro.display_avatar.url)

    if not stats:
        embed.description = "Nenhuma ação registada ainda para este membro neste período."
        return embed

    win     = stats.get("win", 0)
    lose    = stats.get("lose", 0)
    total   = win + lose
    winrate = (win / total * 100) if total else 0

    embed.add_field(name="⚔️ Ações Totais", value=f"**{total}**", inline=True)
    embed.add_field(name="🏆 Vitórias",      value=f"**{win}** ({(win/total*100):.0f}%)" if total else "0", inline=True)
    embed.add_field(name="💀 Derrotas",      value=f"**{lose}** ({(lose/total*100):.0f}%)" if total else "0", inline=True)
    embed.add_field(name="📊 Winrate",       value=f"{_barra_progresso(winrate)}  **{winrate:.0f}%**", inline=False)
    embed.set_footer(text="Silver Dollar • Estatísticas de Ações (N/A não é contabilizado)")
    return embed


def build_acoes_faccao_embed(periodo: str = "total") -> discord.Embed:
    db     = load_db()
    chave  = "acoes" if periodo == "total" else "acoes_semanal"
    acoes  = db.get("acoes_stats", {}).get(chave, {})
    rotulo = "Total (desde o início)" if periodo == "total" else "Semanal"
    embed  = discord.Embed(title=f"🏴 Status de Ações — Facção ({rotulo})", color=COR_GROVE, timestamp=datetime.now(timezone.utc))
    embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
    embed.set_thumbnail(url=LOGO_URL)

    if not acoes:
        embed.description = "Nenhuma ação registada ainda neste período."
        return embed

    linhas_dados = []
    for chave_acao, a in acoes.items():
        win = a.get("win", 0); lose = a.get("lose", 0); total = win + lose
        winrate = (win / total * 100) if total else 0
        linhas_dados.append((a.get("nome", chave_acao), total, win, lose, winrate))
    linhas_dados.sort(key=lambda x: x[1], reverse=True)

    largura = max(6, max(len(n) for n, *_ in linhas_dados))
    header  = f"{'Ação':<{largura}}  {'Feitas':>6}  {'Win':>5}  {'Lose':>5}  {'WR':>5}"
    linhas  = [header, "─" * len(header)]
    for nome, total, win, lose, winrate in linhas_dados:
        linhas.append(f"{nome:<{largura}}  {total:>6}  {win:>5}  {lose:>5}  {winrate:>4.0f}%")

    embed.description = "```\n" + "\n".join(linhas) + "\n```"
    embed.set_footer(text="Silver Dollar • Estatísticas por tipo de ação (N/A não é contabilizado)")
    return embed


class StatusMembroSelect(discord.ui.Select):
    def __init__(self, guild: discord.Guild, periodo: str):
        self.guild   = guild
        self.periodo = periodo
        db     = load_db()
        chave  = "membros" if periodo == "total" else "membros_semanal"
        membros_ids = list(db.get("acoes_stats", {}).get(chave, {}).keys())
        options = []
        for uid in membros_ids[:25]:
            m    = guild.get_member(int(uid)) if guild else None
            nome = m.display_name if m else f"ID {uid}"
            options.append(discord.SelectOption(label=nome[:100], value=uid))
        if not options:
            options = [discord.SelectOption(label="Nenhum dado disponível", value="none")]
        super().__init__(placeholder="Seleciona o membro...", options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "none":
            await interaction.response.send_message("❌ Nenhum dado de ações registado ainda neste período.", ephemeral=True)
            return
        embed = build_acoes_membro_embed(interaction.guild, self.values[0], self.periodo)
        await interaction.response.send_message(embed=embed, ephemeral=True)


class StatusAcoesMembroView(discord.ui.View):
    def __init__(self, guild: discord.Guild, periodo: str):
        super().__init__(timeout=60)
        self.add_item(StatusMembroSelect(guild, periodo))


class StatusCategoriaView(discord.ui.View):
    """Botões de categoria (Ações por Membro / Ações da Facção) já filtrados
    pelo período (Total ou Semanal) escolhido no ecrã anterior."""
    def __init__(self, periodo: str):
        super().__init__(timeout=180)
        self.periodo = periodo

    @discord.ui.button(label="⚔️ Ações (Membro)", style=discord.ButtonStyle.primary)
    async def acoes_membro(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Seleciona o membro para veres o estado:",
            view=StatusAcoesMembroView(interaction.guild, self.periodo),
            ephemeral=True
        )

    @discord.ui.button(label="🏴 Ações (Facção)", style=discord.ButtonStyle.secondary)
    async def acoes_faccao(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = build_acoes_faccao_embed(self.periodo)
        await interaction.response.send_message(embed=embed, ephemeral=True)


class StatusPeriodoView(discord.ui.View):
    """Primeiro ecrã do /status: escolher entre Total e Semanal."""
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📌 Total (desde o início)", style=discord.ButtonStyle.primary, custom_id="btn_status_total_groove")
    async def total(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="📊 Central de Estado — Total",
            description=(
                "Dados **desde o início do bot**. Escolhe abaixo:\n\n"
                "**⚔️ Ações (Membro)** — desempenho individual nas ações\n"
                "**🏴 Ações (Facção)** — desempenho geral por tipo de ação"
            ),
            color=COR_GROVE
        )
        embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
        await interaction.response.send_message(embed=embed, view=StatusCategoriaView("total"), ephemeral=True)

    @discord.ui.button(label="📅 Semanal", style=discord.ButtonStyle.secondary, custom_id="btn_status_semanal_groove")
    async def semanal(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="📊 Central de Estado — Semanal",
            description=(
                "Dados da **semana atual** (reinicia toda segunda-feira). Escolhe abaixo:\n\n"
                "**⚔️ Ações (Membro)** — desempenho individual nas ações\n"
                "**🏴 Ações (Facção)** — desempenho geral por tipo de ação"
            ),
            color=COR_GROVE
        )
        embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
        await interaction.response.send_message(embed=embed, view=StatusCategoriaView("semanal"), ephemeral=True)


@bot.tree.command(name="status", description="Abre o painel de estado (ações).")
async def status(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📊 Central de Status – Silver Dollar",
        description=(
            "Escolha o período que deseja visualizar:\n\n"
            "**📌 Total** — estatísticas acumuladas desde o início do bot\n"
            "**📅 Semanal** — estatísticas da semana atual (reinicia toda segunda-feira)"
        ),
        color=COR_GROVE
    )
    embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
    embed.set_thumbnail(url=LOGO_URL)
    embed.set_footer(text="Silver Dollar")
    await interaction.response.send_message(embed=embed, view=StatusPeriodoView(), ephemeral=True)


async def verificar_reset_semanal():
    """Zera os placares semanais de ações toda segunda-feira às 00:00 UTC,
    mantendo os totais (desde o início do bot) intactos."""
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            db     = load_db()
            agora  = datetime.now(timezone.utc)
            proximo_reset = datetime.fromisoformat(db["semana"]["proximo_reset"])
            if agora >= proximo_reset:
                db["acoes_stats"]["membros_semanal"] = {}
                db["acoes_stats"]["acoes_semanal"]    = {}
                db["semana"]["inicio"]        = agora.isoformat()
                db["semana"]["proximo_reset"] = _proxima_segunda(agora).isoformat()
                save_db(db)

                canal_log = bot.get_channel(CANAL_LOG_CALC_ID)
                if canal_log:
                    embed = discord.Embed(
                        title="🔄 Ranking Semanal Reiniciado",
                        description="Os placares semanais de **Ações** foram zerados para a nova semana. Os totais desde o início do bot mantêm-se intactos.",
                        color=COR_GROVE, timestamp=agora
                    )
                    embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
                    await canal_log.send(embed=embed)
        except Exception as e:
            print(f"[STATUS] Erro no reset semanal: {e}")
        await asyncio.sleep(1800)  # verifica a cada 30 minutos


@bot.tree.command(name="resetar_ranking_semanal", description="[Staff] Zera manualmente o ranking semanal de ações.")
@app_commands.checks.has_permissions(manage_messages=True)
async def resetar_ranking_semanal(interaction: discord.Interaction):
    db    = load_db()
    agora = datetime.now(timezone.utc)
    db["acoes_stats"]["membros_semanal"] = {}
    db["acoes_stats"]["acoes_semanal"]    = {}
    db["semana"]["inicio"]        = agora.isoformat()
    db["semana"]["proximo_reset"] = _proxima_segunda(agora).isoformat()
    save_db(db)
    await interaction.response.send_message("✅ Ranking semanal reiniciado manualmente! Os totais não foram afetados.", ephemeral=True)


# ══════════════════════════════════════════════════════════════
#   /comandos  e  /config_comandos
# ══════════════════════════════════════════════════════════════

class ConfigComandosModal(discord.ui.Modal, title="⚙️ Configurar /comandos"):
    texto = discord.ui.TextInput(
        label="Texto exibido no /comandos",
        style=discord.TextStyle.paragraph,
        required=True, max_length=4000
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = load_db()
        db.setdefault("config", {})["comandos_texto"] = self.texto.value
        save_db(db)
        await interaction.response.send_message("✅ Texto do `/comandos` atualizado com sucesso!", ephemeral=True)


@bot.tree.command(name="comandos", description="Mostra a lista de comandos do servidor.")
async def comandos(interaction: discord.Interaction):
    db    = load_db()
    texto = db.get("config", {}).get("comandos_texto", TEXTO_COMANDOS_PADRAO)
    embed = discord.Embed(title="📋 Comandos – Silver Dollar", description=texto, color=COR_GROVE)
    embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
    embed.set_thumbnail(url=LOGO_URL)
    embed.set_footer(text="Silver Dollar")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="config_comandos", description="[Staff] Edita o texto exibido pelo comando /comandos.")
@app_commands.checks.has_permissions(manage_messages=True)
async def config_comandos(interaction: discord.Interaction):
    db          = load_db()
    texto_atual = db.get("config", {}).get("comandos_texto", TEXTO_COMANDOS_PADRAO)
    modal = ConfigComandosModal()
    modal.texto.default = texto_atual
    await interaction.response.send_modal(modal)


# ══════════════════════════════════════════════════════════════
#   ADVERTÊNCIAS
# ══════════════════════════════════════════════════════════════

ADV_CONFIG = {
    "verbal":    {"cargo_id": CARGO_ADV_VERBAL_ID, "label": "Nível 1 – ADV VERBAL", "expiracao_dias": 7,    "expiracao_label": "7 dias"},
    "warn1":     {"cargo_id": CARGO_ADV_WARN1_ID,  "label": "Nível 2 – ADV ¹",      "expiracao_dias": 10,   "expiracao_label": "10 dias"},
    "warn2":     {"cargo_id": CARGO_ADV_WARN2_ID,  "label": "Nível 3 – ADV ²",      "expiracao_dias": 15,   "expiracao_label": "15 dias"},
    "warn3":     {"cargo_id": CARGO_ADV_WARN3_ID,  "label": "Nível 4 – ADV ³",      "expiracao_dias": 20,   "expiracao_label": "20 dias"},
    "exonerado": {"cargo_id": CARGO_EXONERADO_ID,  "label": "Exonerado",             "expiracao_dias": None, "expiracao_label": "Nunca expira"},
}


class AdvNivelSelect(discord.ui.Select):
    def __init__(self, membro_alvo: discord.Member):
        self.membro_alvo = membro_alvo
        options = [
            discord.SelectOption(label="Nível 1 – ADV VERBAL", value="verbal",    emoji="⚠️", description="Expira: 7 dias"),
            discord.SelectOption(label="Nível 2 – ADV ¹",      value="warn1",     emoji="⚠️", description="Expira: 10 dias"),
            discord.SelectOption(label="Nível 3 – ADV ²",      value="warn2",     emoji="⚠️", description="Expira: 15 dias"),
            discord.SelectOption(label="Nível 4 – ADV ³",      value="warn3",     emoji="⚠️", description="Expira: 20 dias"),
            discord.SelectOption(label="Exonerado",             value="exonerado", emoji="🚫", description="Nunca expira"),
        ]
        super().__init__(placeholder="Seleciona o nível...", options=options, custom_id="select_adv_groove")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AdvertenciaModal(membro_alvo=self.membro_alvo, nivel=self.values[0]))


class AdvertenciaModal(discord.ui.Modal, title="Aplicar Advertência"):
    motivo = discord.ui.TextInput(label="Motivo", placeholder="Descreva o motivo", required=True, style=discord.TextStyle.paragraph)

    def __init__(self, membro_alvo: discord.Member, nivel: str):
        super().__init__()
        self.membro_alvo = membro_alvo
        self.nivel       = nivel

    async def on_submit(self, interaction: discord.Interaction):
        cfg   = ADV_CONFIG[self.nivel]
        db    = load_db()
        uid   = str(self.membro_alvo.id)
        agora = datetime.now(timezone.utc)

        if uid not in db["advertencias"]:
            db["advertencias"][uid] = []

        expira_em = None
        if cfg["expiracao_dias"]:
            expira_em = (agora + timedelta(days=cfg["expiracao_dias"])).isoformat()

        adv = {
            "nivel":        self.nivel,
            "label":        cfg["label"],
            "motivo":       self.motivo.value,
            "aplicado_por": interaction.user.id,
            "data":         agora.isoformat(),
            "expira_em":    expira_em,
            "numero":       len(db["advertencias"][uid]) + 1,
            "cargo_id":     cfg["cargo_id"],
            "ativa":        True,
        }
        db["advertencias"][uid].append(adv)
        save_db(db)

        cargo_adv = interaction.guild.get_role(cfg["cargo_id"])
        if cargo_adv:
            await self.membro_alvo.add_roles(cargo_adv, reason=f"ADV por {interaction.user}")

        canal_adv = bot.get_channel(CANAL_LOG_ADVERTENCIAS_ID)
        if canal_adv:
            embed = discord.Embed(title=f"⚠️ {cfg['label']}", color=COR_ADV, timestamp=agora)
            embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
            embed.set_thumbnail(url=self.membro_alvo.display_avatar.url)
            embed.add_field(name="Membro",       value=self.membro_alvo.mention, inline=True)
            embed.add_field(name="Aplicado por", value=interaction.user.mention, inline=True)
            embed.add_field(name="Nível",        value=cfg["label"],             inline=True)
            embed.add_field(name="Expiração",    value=cfg["expiracao_label"],   inline=True)
            embed.add_field(name="Motivo",       value=self.motivo.value,        inline=False)
            if expira_em:
                embed.add_field(name="Expira em", value=f"<t:{int(datetime.fromisoformat(expira_em).timestamp())}:f>", inline=True)
            embed.set_footer(text=f"ID: {self.membro_alvo.id}")
            await canal_adv.send(embed=embed)

        canal_anuncio_adv = bot.get_channel(CANAL_ANUNCIO_ADV_ID)
        if canal_anuncio_adv:
            try:
                embed_anuncio = discord.Embed(title=f"⚠️ {cfg['label']}", color=COR_ADV, timestamp=agora)
                embed_anuncio.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
                embed_anuncio.set_thumbnail(url=self.membro_alvo.display_avatar.url)
                embed_anuncio.add_field(name="Membro",       value=self.membro_alvo.mention, inline=True)
                embed_anuncio.add_field(name="Aplicado por", value=interaction.user.mention, inline=True)
                embed_anuncio.add_field(name="Nível",        value=cfg["label"],             inline=True)
                embed_anuncio.add_field(name="Expiração",    value=cfg["expiracao_label"],   inline=True)
                embed_anuncio.add_field(name="Motivo",       value=self.motivo.value,        inline=False)
                embed_anuncio.set_footer(text="Silver Dollar")
                await canal_anuncio_adv.send(embed=embed_anuncio)
            except Exception as e:
                print(f"[ADV] Erro ao anunciar: {e}")

        try:
            dm = discord.Embed(
                title=f"⚠️ Recebeste uma advertência — {cfg['label']}",
                description=f"**Servidor:** {interaction.guild.name}\n**Motivo:** {self.motivo.value}\n**Expiração:** {cfg['expiracao_label']}",
                color=COR_ADV, timestamp=agora
            )
            await self.membro_alvo.send(embed=dm)
        except Exception:
            pass

        await interaction.response.send_message(
            f"⚠️ **{cfg['label']}** aplicada a {self.membro_alvo.mention}. Expira em: **{cfg['expiracao_label']}**.",
            ephemeral=True
        )


async def verificar_adv_expiradas():
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            db    = load_db()
            agora = datetime.now(timezone.utc)
            alt   = False
            for uid, advs in db.get("advertencias", {}).items():
                for adv in advs:
                    if not adv.get("ativa") or not adv.get("expira_em"):
                        continue
                    if agora >= datetime.fromisoformat(adv["expira_em"]):
                        adv["ativa"] = False
                        alt          = True
                        for guild in bot.guilds:
                            m = guild.get_member(int(uid))
                            if m:
                                cargo = guild.get_role(adv.get("cargo_id", 0))
                                if cargo and cargo in m.roles:
                                    try:
                                        await m.remove_roles(cargo, reason="ADV expirada")
                                    except Exception:
                                        pass
                                c = bot.get_channel(CANAL_LOG_ADVERTENCIAS_ID)
                                if c:
                                    log = discord.Embed(
                                        title="✅ ADV Expirada",
                                        description=f"A ADV **{adv.get('label','')}** de {m.mention} expirou e foi removida.",
                                        color=COR_APROVADO, timestamp=agora
                                    )
                                    log.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
                                    await c.send(embed=log)
            if alt:
                save_db(db)
        except Exception as e:
            print(f"[ADV] Erro: {e}")
        await asyncio.sleep(300)


@bot.tree.command(name="advertir", description="Aplica uma advertência a um membro.")
@app_commands.describe(membro="Membro a ser advertido")
@app_commands.checks.has_permissions(manage_roles=True)
async def advertir(interaction: discord.Interaction, membro: discord.Member):
    view = discord.ui.View(timeout=60)
    view.add_item(AdvNivelSelect(membro_alvo=membro))
    await interaction.response.send_message(f"Seleciona o nível para {membro.mention}:", view=view, ephemeral=True)


@bot.tree.command(name="ver_advertencias", description="Veja as advertências ativas de um membro.")
@app_commands.describe(membro="Membro para consultar")
@app_commands.checks.has_permissions(manage_roles=True)
async def ver_advertencias(interaction: discord.Interaction, membro: discord.Member):
    db   = load_db()
    uid  = str(membro.id)
    advs = [a for a in db.get("advertencias", {}).get(uid, []) if a.get("ativa")]
    if not advs:
        await interaction.response.send_message(f"✅ {membro.mention} não tem advertências ativas.", ephemeral=True)
        return
    embed = discord.Embed(title=f"⚠️ Advertências – {membro.display_name}", color=COR_ADV)
    embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
    embed.set_thumbnail(url=membro.display_avatar.url)
    embed.description = f"Total ativas: **{len(advs)}**"
    for adv in advs:
        staff = interaction.guild.get_member(adv.get("aplicado_por", 0))
        expira_em = adv.get("expira_em")
        if expira_em:
            expira_txt = f"<t:{int(datetime.fromisoformat(expira_em).timestamp())}:f>"
        else:
            expira_txt = "Nunca expira"
        embed.add_field(
            name=f"#{adv['numero']} — {adv['label']}",
            value=f"**Motivo:** {adv['motivo']}\n**Por:** {staff.mention if staff else '?'}\n**Expira:** {expira_txt}",
            inline=False
        )
    await interaction.response.send_message(embed=embed, ephemeral=True)


# ══════════════════════════════════════════════════════════════
#   CONTROLE DE BAÚ  (registos agrupados/colunares — layout vertical)
# ══════════════════════════════════════════════════════════════
# Como modais do Discord não aceitam upload de imagem, o fluxo é:
# 1) Modal pede os itens em formato agrupado, um por linha:
#       "Glock: 2"
#       "Munição: 60"
#    (o bot junta tudo em uma única operação: cada item numa linha própria)
# 2) O bot pede para a pessoa ENVIAR a foto como próxima mensagem no canal
#    (ela pode colar a imagem da área de transferência com Ctrl+V direto
#    na caixa de mensagem do Discord — é o equivalente mais próximo)
# 3) O bot captura essa mensagem, pega o anexo e posta o log com a imagem
#    no canal de LOGS BAU, e tenta fechar/apagar a interface original
#    automaticamente. Se o envio do log falhar (ex: erro ao anexar a
#    imagem), o registo NÃO é descartado: o bot avisa a pessoa e volta a
#    aguardar uma nova foto, de forma segura.

aguardando_foto_bau: dict[int, dict] = {}  # user_id -> {"tipo":..., "itens": [...], "motivo":..., "interaction": ...}


def _parse_itens_bau(texto: str) -> list[tuple[str, int]]:
    """Converte um texto multilinha 'Item: Quantidade' em uma lista [(item, qtd), ...],
    agrupando quantidades quando o mesmo item aparece mais de uma vez."""
    itens: dict[str, int] = {}
    for linha in texto.splitlines():
        linha = linha.strip()
        if not linha:
            continue
        if ":" in linha:
            nome, qtd_txt = linha.split(":", 1)
        else:
            partes = linha.rsplit(" ", 1)
            if len(partes) == 2 and partes[1].isdigit():
                nome, qtd_txt = partes
            else:
                nome, qtd_txt = linha, "1"
        nome = nome.strip()
        qtd_txt = qtd_txt.strip()
        try:
            qtd = int(qtd_txt)
        except ValueError:
            qtd = 1
        if not nome:
            continue
        chave = nome.lower()
        itens[chave] = itens.get(chave, 0) + qtd

    # recupera a grafia original mapeando novamente (usa a primeira linha correspondente)
    resultado = []
    vistos = set()
    for linha in texto.splitlines():
        linha = linha.strip()
        if not linha:
            continue
        if ":" in linha:
            nome = linha.split(":", 1)[0].strip()
        else:
            partes = linha.rsplit(" ", 1)
            nome = partes[0].strip() if len(partes) == 2 and partes[1].isdigit() else linha.strip()
        chave = nome.lower()
        if chave in itens and chave not in vistos:
            resultado.append((nome, itens[chave]))
            vistos.add(chave)
    return resultado


def _formatar_itens_bau(itens: list[tuple[str, int]], sinal: str) -> str:
    """Layout vertical: um item por linha (sem pipes '|' cortando/quebrando a mensagem)."""
    return "\n".join(f"{sinal}{qtd} {nome}" for nome, qtd in itens)


class BauEntradaModal(discord.ui.Modal, title="📦 Entrada no Baú"):
    itens = discord.ui.TextInput(
        label="Itens (um por linha: Item: Quantidade)",
        placeholder="Glock: 2\nMunição: 60",
        style=discord.TextStyle.paragraph,
        required=True, max_length=500
    )

    async def on_submit(self, interaction: discord.Interaction):
        itens_parseados = _parse_itens_bau(self.itens.value)
        if not itens_parseados:
            await interaction.response.send_message("❌ Nenhum item válido informado.", ephemeral=True)
            return

        resumo = _formatar_itens_bau(itens_parseados, "+")
        aguardando_foto_bau[interaction.user.id] = {
            "tipo": "entrada", "itens": itens_parseados, "motivo": None, "interaction": interaction
        }
        await interaction.response.send_message(
            f"📦 Entrada registada:\n{resumo}\n\n"
            "📸 Agora **envie a foto** aqui no canal (pode colar com Ctrl+V) para concluir o registo.",
            ephemeral=True
        )


class BauSaidaModal(discord.ui.Modal, title="📦 Saída do Baú"):
    itens = discord.ui.TextInput(
        label="Itens (um por linha: Item: Quantidade)",
        placeholder="Glock: 2\nMunição: 60",
        style=discord.TextStyle.paragraph,
        required=True, max_length=500
    )
    motivo = discord.ui.TextInput(label="Motivo da retirada", placeholder="Ex: Uso em ação", required=True, style=discord.TextStyle.paragraph, max_length=300)

    async def on_submit(self, interaction: discord.Interaction):
        itens_parseados = _parse_itens_bau(self.itens.value)
        if not itens_parseados:
            await interaction.response.send_message("❌ Nenhum item válido informado.", ephemeral=True)
            return

        resumo = _formatar_itens_bau(itens_parseados, "-")
        aguardando_foto_bau[interaction.user.id] = {
            "tipo": "saida", "itens": itens_parseados, "motivo": self.motivo.value, "interaction": interaction
        }
        await interaction.response.send_message(
            f"📦 Saída registada:\n{resumo}\n\n"
            "📸 Agora **envie a foto** aqui no canal (pode colar com Ctrl+V) para concluir o registo.",
            ephemeral=True
        )


@bot.event
async def on_message(message: discord.Message):
    # Necessário para o restante do sistema de comandos com prefixo continuar funcionando
    await bot.process_commands(message)

    if message.author.bot:
        return

    pendente = aguardando_foto_bau.get(message.author.id)
    if not pendente:
        return
    if not message.attachments:
        return  # espera até a pessoa mandar uma mensagem com imagem

    anexo = message.attachments[0]
    if not (anexo.content_type and anexo.content_type.startswith("image/")):
        return  # ignora se o anexo não for imagem

    tipo   = pendente["tipo"]
    itens  = pendente["itens"]
    motivo = pendente["motivo"]
    interacao_original = pendente.get("interaction")

    sinal    = "+" if tipo == "entrada" else "-"
    resumo   = _formatar_itens_bau(itens, sinal)

    canal_log = bot.get_channel(CANAL_LOG_BAU_ID)
    if tipo == "entrada":
        embed = discord.Embed(title="📥 Entrada no Baú", color=COR_APROVADO, timestamp=datetime.now(timezone.utc))
        embed.add_field(name="Itens",   value=resumo,                  inline=False)
        embed.add_field(name="Membro",  value=message.author.mention,  inline=True)
    else:
        embed = discord.Embed(title="📤 Saída do Baú", color=COR_RECUSADO, timestamp=datetime.now(timezone.utc))
        embed.add_field(name="Itens",   value=resumo,                  inline=False)
        embed.add_field(name="Membro",  value=message.author.mention,  inline=True)
        embed.add_field(name="Motivo",  value=motivo,                  inline=False)
    embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
    embed.set_image(url=anexo.url)
    embed.set_footer(text=f"ID: {message.author.id}")

    # Envio seguro: se falhar ao salvar a foto no log (ex: erro de rede,
    # anexo expirado, permissão), NÃO descarta o registo — pede a foto de
    # novo em vez de perder a movimentação.
    log_enviado = False
    if canal_log:
        try:
            await canal_log.send(embed=embed)
            log_enviado = True
        except Exception as e:
            print(f"[BAU] Erro ao enviar log: {e}")
    else:
        print("[BAU] Canal de log-bau não encontrado.")

    if not log_enviado:
        # mantém o pedido pendente e pede a foto novamente
        aguardando_foto_bau[message.author.id] = pendente
        try:
            await message.channel.send(
                f"{message.author.mention} ⚠️ Não consegui salvar a foto no log. "
                "Por favor, **envie a foto novamente** para concluir o registo.",
                delete_after=20
            )
        except Exception:
            pass
        return  # não remove a mensagem nem encerra a interação — continua aguardando

    del aguardando_foto_bau[message.author.id]

    try:
        await message.add_reaction("✅")
    except Exception:
        pass
    try:
        await message.delete()
    except Exception:
        pass

    # Tenta encerrar/remover automaticamente a interface (mensagem ephemeral)
    # aberta pelo modal, para que o utilizador não precise clicar em "Ignorar mensagem".
    # Se não for possível (token expirado, permissão etc.), o registo já foi
    # gravado normalmente no canal de Logs BAU acima.
    if interacao_original is not None:
        try:
            await interacao_original.delete_original_response()
        except Exception:
            pass


class ControleBauView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📥 Entrada", style=discord.ButtonStyle.success, custom_id="btn_bau_entrada_groove")
    async def entrada(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BauEntradaModal())

    @discord.ui.button(label="📤 Saída", style=discord.ButtonStyle.danger, custom_id="btn_bau_saida_groove")
    async def saida(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BauSaidaModal())


@bot.tree.command(name="setup_bau", description="Envia o painel de controle de baú no canal.")
@app_commands.checks.has_permissions(administrator=True)
async def setup_bau(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📦 Controle de Baú – Silver Dollar",
        description=(
            "Use os botões abaixo para registar movimentações do baú.\n\n"
            "Podes registar **vários itens de uma vez**, um por linha, no formato:\n"
            "`Item: Quantidade`\n\n"
            "Exemplo:\n```\nGlock: 2\nMunição: 60\n```\n"
            "Depois de preencher, envie a **foto do comprovante** no canal "
            "(pode colar com Ctrl+V) para concluir o registo."
        ),
        color=COR_GROVE
    )
    embed.set_author(name=NOME_SERVIDOR, icon_url=LOGO_URL)
    embed.set_thumbnail(url=LOGO_URL)
    embed.set_footer(text="Silver Dollar")
    await interaction.channel.send(embed=embed, view=ControleBauView())
    await interaction.response.send_message("✅ Painel de controle de baú enviado!", ephemeral=True)


# ══════════════════════════════════════════════════════════════
#   ON READY
# ══════════════════════════════════════════════════════════════

@bot.event
async def on_ready():
    print(f"✅ Silver Dollar Bot online como {bot.user}")
    bot.add_view(SETView())
    bot.add_view(AprovarRecusarSETView())
    bot.add_view(PainelTicketsView())
    bot.add_view(CandidaturaView(user_id=0))
    bot.add_view(EscalacaoPainelView(msg_id=0))
    bot.add_view(AusenciaSetupView())
    bot.add_view(AprovarRecusarAusenciaView(user_id=0))
    bot.add_view(RetirarAusenciaView(user_id=0))
    bot.add_view(ControleBauView())
    bot.add_view(StatusPeriodoView())
    bot.add_view(WinLosePainelView())
    bot.add_view(ContagemPainelView())

    # Recarrega escalações que ainda estavam ativas antes do bot reiniciar,
    # e revincula a view de cada uma à mensagem correta (Participar/Sair/
    # Finalizar volta a funcionar mesmo depois de um restart/deploy).
    global escalacoes_ativas
    db_boot = load_db()
    escalacoes_salvas = db_boot.get("escalacoes_ativas", {})
    escalacoes_ativas.clear()
    for msg_id_str, dados in escalacoes_salvas.items():
        try:
            msg_id = int(msg_id_str)
        except (TypeError, ValueError):
            continue
        escalacoes_ativas[msg_id] = dados
        bot.add_view(EscalacaoPainelView(msg_id=msg_id), message_id=msg_id)
    if escalacoes_ativas:
        print(f"✅ {len(escalacoes_ativas)} escalação(ões) ativa(s) recarregada(s).")

    bot.loop.create_task(verificar_adv_expiradas())
    bot.loop.create_task(verificar_reset_semanal())

    try:
        # IMPORTANTE: copiamos os comandos para cada guild ANTES de limpar a
        # árvore global, porque copy_global_to() só consegue copiar os
        # comandos que ainda estão registados globalmente em memória. Fazer
        # isto na ordem inversa (como estava antes) esvaziava a árvore antes
        # da cópia, e por isso NENHUM comando chegava a ser sincronizado —
        # era esse o motivo dos comandos não aparecerem no Discord.
        for guild in bot.guilds:
            try:
                bot.tree.copy_global_to(guild=guild)
                synced_guild = await bot.tree.sync(guild=guild)
                print(f"✅ {len(synced_guild)} comando(s) sincronizado(s) instantaneamente em '{guild.name}'.")
            except Exception as e:
                print(f"❌ Erro ao sincronizar em '{guild.name}': {e}")

        # Só agora limpamos e sincronizamos os comandos GLOBAIS, para evitar
        # que fiquem duplicados/atrasados na lista global (cada guild já tem
        # a sua própria cópia instantânea acima).
        bot.tree.clear_commands(guild=None)
        await bot.tree.sync()
        print("✅ Comandos globais antigos removidos (evita duplicação).")
    except Exception as e:
        print(f"❌ Erro: {e}")


bot.run(TOKEN)
