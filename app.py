import datetime
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

# --- CONFIGURAÇÃO DE SERVIÇOS E VALORES ---
SERVICOS = {
    "Corte de Cabelo": {"valor": 45.00, "duracao": 45},
    "Barba": {"valor": 35.00, "duracao": 30},
    "Corte + Barba": {"valor": 70.00, "duracao": 75}
}

# --- AUTENTICAÇÃO COM CONTA DE SERVIÇO ---
@st.cache_resource
def autenticar_google():
    """Autentica na API do Google Calendar usando Conta de Serviço via st.secrets ou arquivo local."""
    try:
        if "gcp_service_account" in st.secrets:
            # Converte os dados dos secrets para um dicionário normal
            creds_info = dict(st.secrets["gcp_service_account"])
            
            # Sanitização estrita da chave privada PEM
            raw_key = creds_info.get("private_key", "")
            if "\\n" in raw_key:
                raw_key = raw_key.replace("\\n", "\n")
            
            # Remove aspas extras que o TOML possa ter mantido
            raw_key = raw_key.strip().strip("'").strip('"')
            creds_info["private_key"] = raw_key

            creds = service_account.Credentials.from_service_account_info(
                creds_info, scopes=SCOPES
            )
        else:
            # Fallback para desenvolvimento local
            creds = service_account.Credentials.from_service_account_file(
                "service_account.json", scopes=SCOPES
            )
        return build('calendar', 'v3', credentials=creds)
    except Exception as e:
        st.error(f"Erro na autenticação do Google Calendar: {e}")
        return None

def obter_calendar_id():
    """Obtém o ID da agenda dos Secrets ou utiliza a agenda primária."""
    return st.secrets.get("CALENDAR_ID", "primary")

# --- BUSCA DE HORÁRIOS OCUPADOS ---
def obter_intervalos_ocupados(service, data):
    """Busca os intervalos de início e término dos eventos já marcados na data informada."""
    calendar_id = obter_calendar_id()
    
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
    intervalos = []

    for event in events:
        start_str = event['start'].get('dateTime', event['start'].get('date'))
        end_str = event['end'].get('dateTime', event['end'].get('date'))
        if start_str and end_str and 'T' in start_str:
            dt_inicio = datetime.datetime.fromisoformat(start_str)
            dt_fim = datetime.datetime.fromisoformat(end_str)
            intervalos.append((dt_inicio.time(), dt_fim.time()))
            
    return intervalos

# --- AGENDAMENTO NO GOOGLE CALENDAR ---
def criar_agendamento_google(service, nome, telefone, servico_nome, data, horario_str):
    """Cria um novo evento no Google Agenda com duração e valores corretos."""
    calendar_id = obter_calendar_id()
    dados_servico = SERVICOS[servico_nome]
    duracao = dados_servico["duracao"]
    valor = dados_servico["valor"]
    
    hora, minuto = map(int, horario_str.split(':'))
    data_inicio = datetime.datetime.combine(data, datetime.time(hora, minuto))
    data_fim = data_inicio + datetime.timedelta(minutes=duracao)

    evento = {
        'summary': f'💈 {servico_nome} - {nome}',
        'description': f'Cliente: {nome}\nWhatsApp: {telefone}\nServiço: {servico_nome}\nValor: R$ {valor:.2f}\nDuração: {duracao} min',
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
    st.set_page_config(page_title="Barbearia - Agendamento", page_icon="💈", layout="centered")
    
    st.markdown("<h1 style='text-align: center;'>💈 Barbearia Style</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Agende seu atendimento de forma rápida</p>", unsafe_allow_html=True)
    st.write("---")

    calendar_service = autenticar_google()
    if not calendar_service:
        st.stop()

    # 1. Dados do Cliente
    st.subheader("1. Seus Dados")
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome Completo *")
    with col2:
        telefone = st.text_input("WhatsApp / Telefone *", placeholder="(11) 99999-9999")

    # 2. Escolha do Serviço
    st.subheader("2. Escolha o Serviço")
    opcao_servico = st.radio(
        "Selecione uma opção:",
        options=list(SERVICOS.keys()),
        format_func=lambda x: f"{x} — R$ {SERVICOS[x]['valor']:.2f} ({SERVICOS[x]['duracao']} min)"
    )
    duracao_servico = SERVICOS[opcao_servico]["duracao"]
    valor_servico = SERVICOS[opcao_servico]["valor"]

    # 3. Escolha da Data
    st.subheader("3. Selecione a Data")
    hoje = datetime.date.today()
    data_selecionada = st.date_input(
        "Data do agendamento", 
        min_value=hoje,
        max_value=hoje + datetime.timedelta(days=30)
    )

    # 4. Cálculo Dinâmico de Horários Livres
    st.subheader("4. Horários Disponíveis")
    
    # Grade de horários possíveis de atendimento
    grade_horarios = [
        "09:00", "09:45", "10:30", "11:15", "13:00", 
        "13:45", "14:30", "15:15", "16:00", "16:45", "17:30", "18:15"
    ]

    with st.spinner("Consultando horários disponíveis..."):
        ocupados = obter_intervalos_ocupados(calendar_service, data_selecionada)
        
    agora = datetime.datetime.now()
    horarios_livres = []
    
    for h in grade_horarios:
        h_obj = datetime.datetime.strptime(h, "%H:%M").time()
        slot_inicio = datetime.datetime.combine(data_selecionada, h_obj)
        slot_fim = slot_inicio + datetime.timedelta(minutes=duracao_servico)
        
        # Ignora horários passados caso a data seja o dia de hoje
        if data_selecionada == hoje and slot_inicio <= agora:
            continue
            
        # Valida se o serviço bate com algum evento já agendado
        conflito = False
        for oc_ini, oc_fim in ocupados:
            if max(slot_inicio.time(), oc_ini) < min(slot_fim.time(), oc_fim):
                conflito = True
                break
                
        if not conflito:
            horarios_livres.append(h)

    if not horarios_livres:
        st.warning("⚠️ Não há horários disponíveis para esta data. Por favor, selecione outro dia.")
        horario_selecionado = None
    else:
        horario_selecionado = st.selectbox("Selecione o horário:", horarios_livres)

    st.write("---")
    if st.button("Confirmar Agendamento", type="primary", use_container_width=True):
        if not nome.strip() or not telefone.strip():
            st.error("Por favor, preencha seu nome e telefone.")
        elif not horario_selecionado:
            st.error("Selecione um horário disponível antes de confirmar.")
        else:
            try:
                with st.spinner("Salvando agendamento na agenda..."):
                    criar_agendamento_google(
                        service=calendar_service,
                        nome=nome,
                        telefone=telefone,
                        servico_nome=opcao_servico,
                        data=data_selecionada,
                        horario_str=horario_selecionado
                    )
                st.balloons()
                st.success(f"""
                ✅ **Agendamento Confirmado!**
                - **Cliente:** {nome}
                - **Serviço:** {opcao_servico} (R$ {valor_servico:.2f})
                - **Data:** {data_selecionada.strftime('%d/%m/%Y')} às {horario_selecionado}
                """)
            except Exception as e:
                st.error(f"Erro ao registrar agendamento: {e}")

if __name__ == '__main__':
    main()