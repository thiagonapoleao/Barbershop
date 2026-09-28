import datetime
import os.path
import streamlit as st

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Escopo necessário para ler e criar eventos na Google Agenda
SCOPES = ['https://www.googleapis.com/auth/calendar']

# --- CONFIGURAÇÃO DE SERVIÇOS E VALORES ---
SERVICOS = {
    "Corte de Cabelo": 45.00,
    "Barba": 35.00,
    "Corte + Barba": 70.00
}

# --- AUTENTICAÇÃO GOOGLE CALENDAR ---
def autenticar_google():
    """Autentica o usuário na API do Google Calendar usando OAuth 2.0."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                st.error("Arquivo 'credentials.json' não encontrado. Configure suas credenciais do Google Cloud.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

# --- BUSCA DE HORÁRIOS OCUPADOS ---
def obter_horarios_ocupados(service, data):
    """Busca no Google Agenda os horários já agendados para a data informada."""
    inicio_dia = datetime.datetime.combine(data, datetime.time(0, 0, 0)).isoformat() + 'Z'
    fim_dia = datetime.datetime.combine(data, datetime.time(23, 59, 59)).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary',
        timeMin=inicio_dia,
        timeMax=fim_dia,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    horarios_ocupados = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        if 'T' in start:
            # Extrai o horário (HH:MM) do ISO string
            hora_inicio = start.split('T')[1][:5]
            horarios_ocupados.append(hora_inicio)
            
    return horarios_ocupados

# --- AGENDAMENTO NO GOOGLE CALENDAR ---
def criar_agendamento_google(service, nome, telefone, servico, valor, data, horario):
    """Cria um novo evento no Google Agenda."""
    hora, minuto = map(int, horario.split(':'))
    data_inicio = datetime.datetime.combine(data, datetime.time(hora, minuto))
    data_fim = data_inicio + datetime.timedelta(minutes=45) # Duração padrão de 45min

    evento = {
        'summary': f'💈 Barbeiro: {servico} - {nome}',
        'description': f'Cliente: {nome}\nTelefone: {telefone}\nServiço: {servico}\nValor: R$ {valor:.2f}',
        'start': {
            'dateTime': data_inicio.isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': data_fim.isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
    }

    service.events().insert(calendarId='primary', body=evento).execute()

# --- INTERFACE DE USUÁRIO (STREAMLIT) ---
def main():
    st.set_page_config(page_title="Agendamento Barbearia", page_icon="💈", layout="centered")
    
    st.title("💈 Barbearia Style - Agendamento")
    st.write("Escolha o serviço, a data e o horário para agendar seu atendimento.")

    # Conectar à API do Google
    calendar_service = autenticar_google()
    if not calendar_service:
        st.stop()

    # 1. Dados do Cliente
    st.subheader("1. Seus Dados")
    nome = st.text_input("Nome Completo")
    telefone = st.text_input("Telefone (com DDD)")

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
    data_selecionada = st.date_input("Data do agendamento", min_value=datetime.date.today())

    # 4. Seleção de Horários Disponíveis
    st.subheader("4. Horários Disponíveis")
    
    # Horários padrão de funcionamento da barbearia (ex: 09:00 às 18:00)
    horarios_totais = [
        "09:00", "10:00", "11:00", "13:00", 
        "14:00", "15:00", "16:00", "17:00", "18:00"
    ]

    # Busca horários ocupados direto do Google Calendar
    horarios_ocupados = obter_horarios_ocupados(calendar_service, data_selecionada)
    horarios_livres = [h for h in horarios_totais if h not in horarios_ocupados]

    if not horarios_livres:
        st.warning("Não há horários disponíveis para esta data. Escolha outro dia.")
        horario_selecionado = None
    else:
        horario_selecionado = st.selectbox("Horários livres:", horarios_livres)

    # Botão de Confirmação
    st.write("---")
    if st.button("Confirmar Agendamento", type="primary"):
        if not nome or not telefone:
            st.error("Por favor, preencha seu nome e telefone antes de confirmar.")
        elif not horario_selecionado:
            st.error("Selecione um horário disponível.")
        else:
            with st.spinner("Agendando no Google Agenda..."):
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

if __name__ == '__main__':
    main()