import streamlit as st
from datetime import datetime, time, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ================= CONFIGURAÇÕES GERAIS =================
CALENDAR_ID = "SEU_CALENDAR_ID_AQUI@group.calendar.google.com"  # Substitua pelo ID da sua agenda
CREDENTIALS_FILE = "service_account.json"
TIMEZONE = "America/Sao_Paulo"

# Horário de funcionamento (ex: 09:00 às 19:00 com slots de 30 min)
HORA_ABERTURA = time(9, 0)
HORA_FECHAMENTO = time(19, 0)

SERVICOS = {
    "Corte": {"valor": 40.00, "duracao": 45},
    "Barba": {"valor": 30.00, "duracao": 30},
    "Corte + Barba": {"valor": 65.00, "duracao": 75}
}

# ================= CONEXÃO COM GOOGLE AGENDA =================
@st.cache_resource
def get_calendar_service():
    scopes = ['https://www.googleapis.com/auth/calendar']
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=scopes
    )
    return build('calendar', 'v3', credentials=creds)

def buscar_eventos_ocupados(data_selecionada):
    """Busca os horários já ocupados no Google Calendar para a data selecionada."""
    service = get_calendar_service()
    
    inicio_dia = datetime.combine(data_selecionada, time(0, 0)).isoformat() + "-03:00"
    fim_dia = datetime.combine(data_selecionada, time(23, 59, 59)).isoformat() + "-03:00"

    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=inicio_dia,
        timeMax=fim_dia,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    eventos = events_result.get('items', [])
    ocupados = []
    
    for evento in eventos:
        start = evento['start'].get('dateTime', evento['start'].get('date'))
        end = evento['end'].get('dateTime', evento['end'].get('date'))
        if start and end:
            dt_inicio = datetime.fromisoformat(start)
            dt_fim = datetime.fromisoformat(end)
            ocupados.append((dt_inicio.time(), dt_fim.time()))
            
    return ocupados

def gerar_horarios_disponiveis(data_selecionada, duracao_minutos):
    """Gera lista de horários livres baseado na duração do serviço escolhido."""
    ocupados = buscar_eventos_ocupados(data_selecionada)
    
    horarios_livres = []
    atual = datetime.combine(data_selecionada, HORA_ABERTURA)
    fechamento = datetime.combine(data_selecionada, HORA_FECHAMENTO)
    
    agora = datetime.now()

    while atual + timedelta(minutes=duracao_minutos) <= fechamento:
        fim_servico = atual + timedelta(minutes=duracao_minutos)
        h_inicio = atual.time()
        h_fim = fim_servico.time()
        
        # Ignora horários passados se o agendamento for para o dia de hoje
        if data_selecionada == agora.date() and atual <= agora:
            atual += timedelta(minutes=30)
            continue
            
        # Verifica conflito com eventos já agendados
        conflito = False
        for oc_ini, oc_fim in ocupados:
            if max(h_inicio, oc_ini) < min(h_fim, oc_fim):
                conflito = True
                break
                
        if not conflito:
            horarios_livres.append(h_inicio.strftime("%H:%M"))
            
        atual += timedelta(minutes=30)  # Intervalo de início dos slots
        
    return horarios_livres

def criar_evento(nome, telefone, servico_nome, data, horario_str):
    service = get_calendar_service()
    
    duracao = SERVICOS[servico_nome]["duracao"]
    valor = SERVICOS[servico_nome]["valor"]
    
    horario_inicio = datetime.strptime(horario_str, "%H:%M").time()
    dt_inicio = datetime.combine(data, horario_inicio)
    dt_fim = dt_inicio + timedelta(minutes=duracao)

    corpo_evento = {
        'summary': f"💈 {servico_nome} - {nome}",
        'description': f"Cliente: {nome}\nWhatsApp: {telefone}\nServiço: {servico_nome} (R$ {valor:.2f})\nDuração: {duracao} min",
        'start': {
            'dateTime': dt_inicio.isoformat(),
            'timeZone': TIMEZONE,
        },
        'end': {
            'dateTime': dt_fim.isoformat(),
            'timeZone': TIMEZONE,
        },
    }

    service.events().insert(calendarId=CALENDAR_ID, body=corpo_evento).execute()

# ================= INTERFACE DO USUÁRIO =================
st.set_page_config(page_title="Agendamento Barbearia", page_icon="💈", layout="centered")

st.markdown("<h1 style='text-align: center;'>✂️ Barbearia Estilo</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Agende seu horário em poucos cliques</p>", unsafe_allow_html=True)
st.divider()

# Formulário
st.subheader("1. Seus Dados")
col_nome, col_tel = st.columns(2)
with col_nome:
    nome = st.text_input("Nome completo *")
with col_tel:
    telefone = st.text_input("WhatsApp / Telefone *", placeholder="(11) 99999-9999")

st.subheader("2. Escolha o Serviço")
opcoes_servico = [f"{k} — R$ {v['valor']:.2f} ({v['duracao']} min)" for k, v in SERVICOS.items()]
servico_escolhido = st.radio("Serviços disponíveis:", opcoes_servico, index=0)

# Extrai o nome limpo do serviço
nome_servico = servico_escolhido.split(" — ")[0]
duracao_selecionada = SERVICOS[nome_servico]["duracao"]

st.subheader("3. Data e Horário")
hoje = datetime.now().date()
data_selecionada = st.date_input("Selecione o dia desejado:", min_value=hoje, max_value=hoje + timedelta(days=30))

horarios_disponiveis = gerar_horarios_disponiveis(data_selecionada, duracao_selecionada)

if horarios_disponiveis:
    horario_selecionado = st.selectbox("Horários livres encontrados:", horarios_disponiveis)
else:
    st.warning("⚠️ Nenhum horário disponível para esta data ou duração. Por favor, escolha outro dia.")
    horario_selecionado = None

st.divider()

if st.button("Confirmar Agendamento 📅", use_container_width=True, type="primary"):
    if not nome.strip() or not telefone.strip():
        st.error("Por favor, preencha seu nome e telefone antes de confirmar.")
    elif not horario_selecionado:
        st.error("Por favor, selecione um horário válido.")
    else:
        try:
            with st.spinner("Agendando na barbearia..."):
                criar_evento(nome, telefone, nome_servico, data_selecionada, horario_selecionado)
            st.balloons()
            st.success(f"""
            ✅ **Agendamento confirmado com sucesso!**
            - **Cliente:** {nome}
            - **Serviço:** {nome_servico} (R$ {SERVICOS[nome_servico]['valor']:.2f})
            - **Data:** {data_selecionada.strftime('%d/%m/%Y')} às {horario_selecionado}
            """)
        except Exception as e:
            st.error(f"Erro ao processar o agendamento: {e}")