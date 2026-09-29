import streamlit as st
import requests
import datetime

# ================= CONFIGURAÇÃO =================
st.set_page_config(
    page_title="Painel do Barbeiro - Barbearia Style",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização moderna escura com detalhes dourados
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            max-width: 900px !important;
        }
        .stApp {
            background-color: #121212;
            color: #E0E0E0;
        }
        .card-agendamento {
            background-color: #1E1E1E;
            border: 1px solid #2F2F2F;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# URL da sua automação no Google Apps Script
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzQoJrcSlveATovQ-syyGJs49JmdgkhcfkKu3jw2ve2lyN36f5fMrbsJokWzgqxNh95/exec"

# ================= FUNÇÕES DE INTEGRAÇÃO =================
def carregar_agendamentos(data_str):
    """Busca os agendamentos reais gravados no Google Calendar via Apps Script."""
    try:
        url = f"{WEB_APP_URL}?action=get_bookings&date={data_str}"
        response = requests.get(url, timeout=15)
        res = response.json()
        if res.get("status") == "ok":
            return res.get("bookings", [])
    except Exception as e:
        st.error(f"Erro ao consultar a Google Agenda: {e}")
    return []

def cancelar_evento(event_id):
    """Exclui o agendamento diretamente do Google Calendar."""
    try:
        response = requests.post(
            WEB_APP_URL,
            json={"action": "cancel", "eventId": event_id},
            timeout=15
        )
        res = response.json()
        return res.get("status") == "success"
    except Exception:
        return False

# ================= INTERFACE =================
# Cabeçalho
col_logo, col_link = st.columns([3, 1])
with col_logo:
    st.markdown("## ✂️ Painel do **Barbeiro**")
    st.caption("Consulte os horários agendados em tempo real na sua Google Agenda")
with col_link:
    st.markdown(
        """
        <div style="text-align: right; margin-top: 10px;">
            <a href="https://calendar.google.com" target="_blank" style="text-decoration:none; background-color:#2A2A2A; color:#D4AF37; padding:8px 14px; border-radius:20px; font-size:12px; border:1px solid #D4AF37;">
                📅 Abrir Google Agenda
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("---")

# Filtro de Data
col_data, col_refresh = st.columns([3, 1])
with col_data:
    data_selecionada = st.date_input("Filtrar por data:", value=datetime.date.today())
with col_refresh:
    st.write("")
    st.write("")
    if st.button("🔄 Atualizar", use_container_width=True):
        st.rerun()

data_str = data_selecionada.strftime("%Y-%m-%d")

# Consulta dos eventos
with st.spinner("Buscando agendamentos no Google Agenda..."):
    agendamentos = carregar_agendamentos(data_str)

# Métricas Rápidas
col_m1, col_m2 = st.columns(2)
with col_m1:
    st.metric("Total de Clientes no Dia", len(agendamentos))
with col_m2:
    faturamento = 0.0
    for ag in agendamentos:
        desc = ag.get("description", "")
        if "R$" in desc:
            try:
                val_str = desc.split("R$")[1].strip().split("\n")[0].replace(",", ".")
                faturamento += float(val_str)
            except Exception:
                pass
    st.metric("Faturamento Estimado", f"R$ {faturamento:.2f}".replace(".", ","))

st.write("---")

# Lista de Horários
if not agendamentos:
    st.info("Nenhum agendamento encontrado para esta data no Google Agenda.")
else:
    # Ordena por horário crescente
    agendamentos.sort(key=lambda x: x.get("time", ""))
    
    for ag in agendamentos:
        hora = ag.get("time", "--:--")
        titulo = ag.get("title", "Agendamento")
        descricao = ag.get("description", "Sem detalhes adicionais")
        ev_id = ag.get("id")

        with st.container():
            col_info, col_btn = st.columns([4, 1])
            with col_info:
                st.markdown(f"### ⏰ {hora} - {titulo}")
                linhas = descricao.split("\n")
                for linha in linhas:
                    st.write(f"- {linha}")
            
            with col_btn:
                st.write("")
                st.write("")
                if st.button("❌ Cancelar", key=f"btn_{ev_id}", use_container_width=True):
                    with st.spinner("Excluindo do Google Agenda..."):
                        if cancelar_evento(ev_id):
                            st.success("Cancelado com sucesso!")
                            st.rerun()
                        else:
                            st.error("Erro ao cancelar o evento.")
            st.write("---")