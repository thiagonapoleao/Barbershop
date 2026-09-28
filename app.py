import streamlit as st
import requests
import datetime

# ================= CONFIGURAÇÃO =================
# Cole aqui o link gerado na etapa de implantação do Apps Script
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzQoJrcSlveATovQ-syyGJs49JmdgkhcfkKu3jw2ve2lyN36f5fMrbsJokWzgqxNh95/exec"

SERVICOS = {
    "Corte de Cabelo": {"valor": 45.00, "duracao": 45},
    "Barba": {"valor": 35.00, "duracao": 30},
    "Corte + Barba": {"valor": 70.00, "duracao": 75}
}

# Horários de atendimento da barbearia
HORARIOS_DISPONIVEIS = [
    "09:00", "09:45", "10:30", "11:15", "13:00", 
    "13:45", "14:30", "15:15", "16:00", "16:45", "17:30", "18:15"
]

# ================= FUNÇÕES DE INTEGRAÇÃO =================
def consultar_ocupados(data_str):
    """Consulta os horários ocupados no Google Agenda via Apps Script."""
    try:
        response = requests.get(WEB_APP_URL, params={"action": "get_busy", "date": data_str}, timeout=10)
        data = response.json()
        if data.get("status") == "ok":
            return data.get("busy", [])
    except Exception as e:
        st.warning(f"Aviso ao consultar agenda: {e}")
    return []

def salvar_agendamento(nome, telefone, servico, data_str, horario_str):
    """Envia o agendamento para o Google Calendar."""
    dados_servico = SERVICOS[servico]
    payload = {
        "nome": nome,
        "telefone": telefone,
        "servico": servico,
        "valor": dados_servico["valor"],
        "duracao": dados_servico["duracao"],
        "data": data_str,
        "horario": horario_str
    }
    try:
        response = requests.post(WEB_APP_URL, json=payload, timeout=15)
        res = response.json()
        return res.get("status") == "success"
    except Exception:
        return False

# ================= INTERFACE (STREAMLIT) =================
st.set_page_config(page_title="Barbearia Style", page_icon="💈", layout="centered")

st.markdown("<h1 style='text-align: center;'>💈 Barbearia Style</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Agende seu atendimento online</p>", unsafe_allow_html=True)
st.write("---")

# 1. Dados do cliente
st.subheader("1. Seus Dados")
col1, col2 = st.columns(2)
with col1:
    nome = st.text_input("Nome Completo *")
with col2:
    telefone = st.text_input("WhatsApp com DDD *", placeholder="(11) 99999-9999")

# 2. Escolha do serviço
st.subheader("2. Escolha o Serviço")
opcao_servico = st.radio(
    "Opções disponíveis:",
    options=list(SERVICOS.keys()),
    format_func=lambda x: f"{x} — R$ {SERVICOS[x]['valor']:.2f} ({SERVICOS[x]['duracao']} min)"
)
duracao_servico = SERVICOS[opcao_servico]["duracao"]
valor_servico = SERVICOS[opcao_servico]["valor"]

# 3. Data do atendimento
st.subheader("3. Selecione a Data")
hoje = datetime.date.today()
data_selecionada = st.date_input("Data desejada", min_value=hoje, max_value=hoje + datetime.timedelta(days=30))
data_str = data_selecionada.strftime("%Y-%m-%d")

# 4. Horários livres
st.subheader("4. Horários Disponíveis")

with st.spinner("Verificando agenda..."):
    ocupados = consultar_ocupados(data_str)

agora = datetime.datetime.now()
horarios_livres = []

for h in HORARIOS_DISPONIVEIS:
    h_time = datetime.datetime.strptime(h, "%H:%M").time()
    dt_inicio = datetime.datetime.combine(data_selecionada, h_time)
    dt_fim = dt_inicio + datetime.timedelta(minutes=duracao_servico)

    # Se for hoje, ignora horários que já passaram
    if data_selecionada == hoje and dt_inicio <= agora:
        continue

    # Checa colisão com eventos já agendados
    conflito = False
    for item in ocupados:
        oc_ini = datetime.datetime.strptime(item["start"], "%H:%M").time()
        oc_fim = datetime.datetime.strptime(item["end"], "%H:%M").time()
        if max(dt_inicio.time(), oc_ini) < min(dt_fim.time(), oc_fim):
            conflito = True
            break

    if not conflito:
        horarios_livres.append(h)

if not horarios_livres:
    st.warning("Nenhum horário livre para essa data. Escolha outro dia.")
    horario_escolhido = None
else:
    horario_escolhido = st.selectbox("Escolha um horário livre:", horarios_livres)

st.write("---")

# 5. Confirmação
if st.button("Confirmar Agendamento", type="primary", use_container_width=True):
    if not nome.strip() or not telefone.strip():
        st.error("Por favor, preencha o seu nome e telefone.")
    elif not horario_escolhido:
        st.error("Selecione um horário válido.")
    elif WEB_APP_URL == "SUA_URL_DO_APPS_SCRIPT_AQUI":
        st.error("Configure a URL do Apps Script no código antes de agendar.")
    else:
        with st.spinner("Confirmando seu agendamento..."):
            sucesso = salvar_agendamento(nome, telefone, opcao_servico, data_str, horario_escolhido)

        if sucesso:
            st.balloons()
            st.success(f"""
            ✅ **Agendamento Confirmado!**
            - **Cliente:** {nome}
            - **Serviço:** {opcao_servico} (R$ {valor_servico:.2f})
            - **Data:** {data_selecionada.strftime('%d/%m/%Y')} às {horario_escolhido}
            """)
        else:
            st.error("Ocorreu um erro ao gravar na agenda. Tente novamente.")