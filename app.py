import datetime
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

# --- CONFIGURAÇÃO DE SERVIÇOS E VALORES ---
SERVICOS = {
    "Corte de Cabelo": 45.00,
    "Barba": 35.00,
    "Corte + Barba": 70.00
}

# --- AUTENTICAÇÃO COM CONTA DE SERVIÇO ---
@st.cache_resource
def autenticar_google():
    """Autentica na API do Google Calendar usando Conta de Serviço via Streamlit Secrets."""
    try:
        # Lê credenciais diretamente dos Secrets do Streamlit Cloud
        if "gcp_service_account" in st.secrets:
            creds_info = dict(st.secrets["gcp_service_account"])
            # Corrige quebras de linha na private_key caso venham escapadas
            if "\\n" in creds_info.get("private_key", ""):
                creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
            creds = service_account.Credentials.from_service_account_info(
                creds_info, scopes=SCOPES
            )
        else:
            # Fallback para desenvolvimento local via arquivo JSON
            creds = service_account.Credentials.from_service_account_file(
                "service_account.json", scopes=SCOPES
            )
        return build('calendar', 'v3', credentials=creds)
    except Exception as e:
        st.error(f"Erro na autenticação do Google Calendar: {e}")
        return None

def obter_calendar_id():
    """Obtém o ID da agenda dos Secrets ou usa a agenda principal."""
    return st.secrets.get("CALENDAR_ID", "primary")

# --- BUSCA DE HORÁRIOS OCUPADOS ---
def obter_horarios_ocupados(service, data):
    """Busca no Google Agenda os horários já ocupados para a data informada."""
    calendar_id = obter_calendar_id()
    
    # Define o intervalo do dia em UTC-3 (Horário de Brasília)
    inicio_dia = datetime.datetime.combine(data, datetime.time(0, 0, 0)).isoformat() + '-03:00'
    fim_dia = datetime.datetime.combine(data, datetime.time(23, 59, 59)).isoformat() + '-03:00'

    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=inicio_dia,
        timeMax=fim_dia,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    horarios_ocupados = []

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        if start and 'T' in start:
            # Converte para objeto datetime para extrair a hora correta
            dt = datetime.datetime.fromisoformat(start)
            horarios_ocupados.append(dt.strftime("%H:%M"))
            
    return horarios_ocupados

# --- AGENDAMENTO NO GOOGLE CALENDAR ---
def criar_agendamento_google(service, nome, telefone, servico, valor, data, horario):
    """Cria um novo evento no Google Agenda."""
    calendar_id = obter_calendar_id()
    hora, minuto = map(int, horario.split(':'))
    data_inicio = datetime.datetime.combine(data, datetime.time(hora, minuto))
    data_fim = data_inicio + datetime.timedelta(minutes=45)

    evento = {
        'summary': f'💈 {servico} - {nome}',
        'description': f'Cliente: {nome}\nWhatsApp: {telefone}\nServiço: {servico}\nValor: R$ {valor:.2f}',
        'start': {
            'dateTime': data_inicio.isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': data_fim.isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
    }

    service.events().insert(calendarId=calendar_id, body=evento).execute()

# --- INTERFACE DE USUÁRIO (STREAMLIT) ---
def main():
    st.set_page_config(page_title="Agendamento Barbearia", page_icon="💈", layout="centered")
    
    st.title("💈 Barbearia Style - Agendamento")
    st.write("Escolha o serviço, a data e o horário para agendar seu atendimento.")

    calendar_service = autenticar_google()
    if not calendar_service:
        st.stop()

    # 1. Dados do Cliente
    st.subheader("1. Seus Dados")
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome Completo")
    with col2:
        telefone = st.text_input("WhatsApp / Telefone", placeholder="(11) 99999-9999")

    # 2. Escolha do Serviço
    st.subheader("2. Escolha o Serviço")
    opcao_servico = st.radio(
        "Selecione uma opção:",
        options=list(SERVICOS.keys()),
        format_func=lambda x: f"{x} — R$ {SERVICOS[x]:.2f}"
    )
    valor_servico = SERVICOS[opcao_servico]

    # 3. Escolha da Data
    st.subheader("3. Selecione a Data")
    data_selecionada = st.date_input(
        "Data do agendamento", 
        min_value=datetime.date.today(),
        max_value=datetime.date.today() + datetime.timedelta(days=30)
    )

    # 4. Seleção de Horários Disponíveis
    st.subheader("4. Horários Disponíveis")
    
    horarios_totais = [
        "09:00", "10:00", "11:00", "13:00", 
        "14:00", "15:00", "16:00", "17:00", "18:00"
    ]

    with st.spinner("Buscando horários disponíveis..."):
        horarios_ocupados = obter_horarios_ocupados(calendar_service, data_selecionada)
        
    agora = datetime.datetime.now()
    horarios_livres = []
    
    for h in horarios_totais:
        if h in horarios_ocupados:
            continue
        # Se for no mesmo dia, remove horários do passado
        if data_selecionada == datetime.date.today():
            h_obj = datetime.datetime.strptime(h, "%H:%M").time()
            if datetime.datetime.combine(data_selecionada, h_obj) <= agora:
                continue
        horarios_livres.append(h)

    if not horarios_livres:
        st.warning("Não há horários disponíveis para esta data. Por favor, escolha outro dia.")
        horario_selecionado = None
    else:
        horario_selecionado = st.selectbox("Horários livres:", horarios_livres)

    st.write("---")
    if st.button("Confirmar Agendamento", type="primary", use_container_width=True):
        if not nome.strip() or not telefone.strip():
            st.error("Por favor, preencha seu nome e telefone antes de confirmar.")
        elif not horario_selecionado:
            st.error("Selecione um horário disponível.")
        else:
            try:
                with st.spinner("Registrando agendamento..."):
                    criar_agendamento_google(
                        service=calendar_service,
                        nome=nome,
                        telefone=telefone,
                        servico=opcao_servico,
                        valor=valor_servico,
                        data=data_selecionada,
                        horario=horario_selecionado
                    )
                st.success(f"✅ Agendamento realizado com sucesso para {data_selecionada.strftime('%d/%m/%Y')} às {horario_selecionado}!")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao salvar na agenda: {e}")

if __name__ == '__main__':
    main()