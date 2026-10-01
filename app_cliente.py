import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Barbearia Style - Agendamento",
    page_icon="💈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)

# URL da automação do Google Apps Script
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzQoJrcSlveATovQ-syyGJs49JmdgkhcfkKu3jw2ve2lyN36f5fMrbsJokWzgqxNh95/exec"

html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Barbearia Style - Agendamento</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        body {{
            font-family: 'Poppins', sans-serif;
            background-color: #121212;
            color: #E0E0E0;
            margin: 0;
            padding: 0;
        }}
        .gold-bg {{ background-color: #D4AF37; }}
        .gold-text {{ color: #D4AF37; }}
        .gold-border {{ border-color: #D4AF37; }}
        .card-dark {{ background-color: #1E1E1E; }}
        .input-dark {{ background-color: #2A2A2A; color: #FFFFFF; border: 1px solid #333; }}
        .input-dark:focus {{ border-color: #D4AF37; outline: none; }}
    </style>
</head>
<body class="min-h-screen pb-16">

    <!-- Topbar -->
    <header class="card-dark border-b border-zinc-800 sticky top-0 z-50 shadow-md">
        <div class="max-w-3xl mx-auto px-4 py-4 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <i class="fa-solid font-bold text-2xl gold-text fa-scissors"></i>
                <h1 class="text-xl font-bold tracking-wide">BARBEARIA <span class="gold-text">STYLE</span></h1>
            </div>
            <div id="user-pill" class="hidden items-center gap-3">
                <span id="user-greeting" class="text-xs text-zinc-300 font-semibold"></span>
                <button onclick="logout()" class="text-xs text-red-400 hover:text-red-300 border border-red-900/50 px-3 py-1 rounded-full bg-red-950/20 transition">
                    <i class="fa-solid fa-right-from-bracket mr-1"></i> Sair
                </button>
            </div>
        </div>
    </header>

    <main class="max-w-2xl mx-auto px-4 mt-8">

        <!-- ================= 1. TELA DE AUTENTICAÇÃO (LOGIN / CADASTRO) ================= -->
        <div id="auth-section" class="space-y-6">
            
            <!-- FORMULÁRIO DE LOGIN -->
            <div id="login-box" class="card-dark p-6 sm:p-8 rounded-2xl border border-zinc-800 shadow-2xl">
                <div class="text-center mb-6">
                    <div class="w-14 h-14 gold-bg text-black rounded-full flex items-center justify-center mx-auto text-xl font-bold mb-3">
                        <i class="fa-solid fa-lock"></i>
                    </div>
                    <h2 class="text-2xl font-bold">Acesse sua Conta</h2>
                    <p class="text-zinc-400 text-xs mt-1">Utilize seu e-mail e senha para agendar</p>
                </div>

                <form onsubmit="handleLogin(event)" class="space-y-4">
                    <div>
                        <label class="block text-xs text-zinc-400 mb-1">E-mail *</label>
                        <input type="email" id="login-email" required placeholder="seuemail@exemplo.com" class="w-full p-3 rounded-lg input-dark text-sm">
                    </div>
                    <div>
                        <label class="block text-xs text-zinc-400 mb-1">Senha *</label>
                        <input type="password" id="login-password" required placeholder="••••••••" class="w-full p-3 rounded-lg input-dark text-sm">
                    </div>

                    <button type="submit" id="btn-login" class="w-full gold-bg text-black font-bold py-3 rounded-lg hover:bg-yellow-400 transition mt-2 flex items-center justify-center gap-2">
                        Entrar
                    </button>
                </form>

                <div class="mt-6 text-center border-t border-zinc-800 pt-4 text-xs text-zinc-400">
                    Ainda não possui conta? 
                    <button onclick="showRegisterForm()" class="gold-text font-bold hover:underline ml-1">Cadastre-se</button>
                </div>
            </div>

            <!-- FORMULÁRIO DE CADASTRO -->
            <div id="register-box" class="card-dark p-6 sm:p-8 rounded-2xl border border-zinc-800 shadow-2xl hidden">
                <div class="text-center mb-6">
                    <div class="w-14 h-14 bg-zinc-800 text-yellow-500 rounded-full flex items-center justify-center mx-auto text-xl font-bold mb-3 border border-zinc-700">
                        <i class="fa-solid fa-user-plus"></i>
                    </div>
                    <h2 class="text-2xl font-bold">Criar Conta</h2>
                    <p class="text-zinc-400 text-xs mt-1">Preencha todos os campos obrigatórios abaixo</p>
                </div>

                <form onsubmit="handleRegister(event)" class="space-y-4">
                    <div>
                        <label class="block text-xs text-zinc-400 mb-1">Nome Completo *</label>
                        <input type="text" id="reg-name" required placeholder="Ex: Carlos Oliveira" class="w-full p-3 rounded-lg input-dark text-sm">
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-xs text-zinc-400 mb-1">WhatsApp / Telefone *</label>
                            <input type="tel" id="reg-phone" required placeholder="(16) 99999-9999" class="w-full p-3 rounded-lg input-dark text-sm">
                        </div>
                        <div>
                            <label class="block text-xs text-zinc-400 mb-1">Data de Nascimento *</label>
                            <input type="date" id="reg-birthdate" required class="w-full p-3 rounded-lg input-dark text-sm">
                        </div>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 border-t border-zinc-800 pt-4">
                        <div>
                            <label class="block text-xs text-zinc-400 mb-1">E-mail (Seu Usuário) *</label>
                            <input type="email" id="reg-email" required placeholder="seuemail@exemplo.com" class="w-full p-3 rounded-lg input-dark text-sm">
                        </div>
                        <div>
                            <label class="block text-xs text-zinc-400 mb-1">Senha *</label>
                            <input type="password" id="reg-password" required placeholder="Crie uma senha" class="w-full p-3 rounded-lg input-dark text-sm">
                        </div>
                    </div>

                    <button type="submit" id="btn-register" class="w-full gold-bg text-black font-bold py-3 rounded-lg hover:bg-yellow-400 transition mt-3 flex items-center justify-center gap-2">
                        Finalizar Cadastro
                    </button>
                </form>

                <div class="mt-6 text-center border-t border-zinc-800 pt-4 text-xs text-zinc-400">
                    Já tem uma conta? 
                    <button onclick="showLoginForm()" class="gold-text font-bold hover:underline ml-1">Voltar ao Login</button>
                </div>
            </div>

        </div>

        <!-- ================= 2. TELA DE AGENDAMENTO (USUÁRIO LOGADO) ================= -->
        <div id="booking-section" class="hidden space-y-6">

            <!-- Card com dados pré-definidos do cliente logado -->
            <div class="card-dark p-4 rounded-xl border border-zinc-800 flex justify-between items-center text-xs">
                <div>
                    <span class="text-zinc-500 block">Cliente Conectado:</span>
                    <strong id="display-client-name" class="text-sm gold-text"></strong>
                    <span id="display-client-phone" class="text-zinc-400 ml-2"></span>
                    <p id="display-client-info" class="text-zinc-500 text-[11px] mt-0.5"></p>
                </div>
                <span class="bg-green-900/40 text-green-400 px-2.5 py-1 rounded-full text-[11px] font-medium">Conta Ativa</span>
            </div>

            <form onsubmit="handleBooking(event)" class="space-y-6">
                <!-- 1. Escolha de Serviços -->
                <div class="card-dark p-6 rounded-xl border border-zinc-800 shadow-lg">
                    <h3 class="text-lg font-semibold mb-4 flex items-center gold-text">
                        <i class="fa-solid fa-cut mr-2"></i> 1. Escolha o Serviço
                    </h3>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4" id="services-container"></div>
                </div>

                <!-- 2. Seleção de Data e Horário -->
                <div class="card-dark p-6 rounded-xl border border-zinc-800 shadow-lg">
                    <h3 class="text-lg font-semibold mb-4 flex items-center gold-text">
                        <i class="fa-solid fa-calendar-days mr-2"></i> 2. Data e Horário
                    </h3>
                    
                    <div class="mb-6">
                        <div class="flex justify-between items-center mb-2">
                            <label class="block text-xs text-zinc-400">Selecione o Dia *</label>
                            <span id="status-sync-slots" class="text-[11px] text-zinc-500"></span>
                        </div>
                        <input type="date" id="booking-date" required onchange="renderTimeSlots()" class="w-full p-3 rounded-lg input-dark text-sm">
                    </div>

                    <div>
                        <label class="block text-xs text-zinc-400 mb-2">Horários Disponíveis (09:00 às 18:00) *</label>
                        <div id="timeslots-container" class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-2"></div>
                    </div>
                </div>

                <!-- 3. Confirmação -->
                <div class="card-dark p-6 rounded-xl border border-zinc-800 shadow-lg flex flex-col sm:flex-row justify-between items-center gap-4">
                    <div>
                        <span class="text-xs text-zinc-400 block">Total no Local</span>
                        <span id="total-price" class="text-2xl font-bold gold-text">R$ 0,00</span>
                    </div>
                    <button type="submit" id="submit-btn" class="w-full sm:w-auto gold-bg text-black font-bold px-8 py-3 rounded-lg hover:bg-yellow-400 transition shadow-lg text-center flex items-center justify-center gap-2">
                        <i class="fa-solid fa-check-circle"></i> Confirmar Agendamento
                    </button>
                </div>
            </form>

        </div>

    </main>

    <!-- Modal de Sucesso -->
    <div id="success-modal" class="fixed inset-0 bg-black/80 hidden items-center justify-center p-4 z-50">
        <div class="card-dark p-6 rounded-2xl max-w-md w-full border border-zinc-700 text-center relative space-y-4">
            <div class="w-16 h-16 gold-bg text-black rounded-full flex items-center justify-center mx-auto text-2xl font-bold">
                <i class="fa-solid fa-check"></i>
            </div>
            <h3 class="text-xl font-bold">Agendamento Realizado!</h3>
            <p class="text-zinc-400 text-sm" id="modal-details"></p>
            <div id="sync-status" class="text-xs text-yellow-500 py-1"></div>

            <div class="pt-4 space-y-2">
                <a id="google-calendar-link" target="_blank" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg block flex items-center justify-center gap-2 transition">
                    <i class="fa-brands fa-google"></i> Adicionar ao meu Google Agenda
                </a>
                <button onclick="closeModal()" class="w-full bg-zinc-800 hover:bg-zinc-700 text-zinc-300 font-semibold py-3 px-4 rounded-lg transition">
                    Fechar
                </button>
            </div>
        </div>
    </div>

    <script>
        const WEB_APP_URL = "{WEB_APP_URL}";

        // Função universal para formatar qualquer data para o padrão PT-BR (DD/MM/AAAA)
        function formatDateBR(dateStr) {{
            if (!dateStr) return '';
            const clean = dateStr.toString().split('T')[0].trim();
            if (clean.includes('-')) {{
                const parts = clean.split('-');
                if (parts.length === 3) {{
                    return `${{parts[2].padStart(2, '0')}}/${{parts[1].padStart(2, '0')}}/${{parts[0]}}`;
                }}
            }}
            return clean;
        }}

        const services = [
            {{ id: 'corte', name: 'Corte de Cabelo', price: 45.00, durationMin: 30, duration: '30 min', icon: 'fa-scissors' }},
            {{ id: 'barba', name: 'Barba Modelada', price: 35.00, durationMin: 30, duration: '30 min', icon: 'fa-user' }},
            {{ id: 'combo', name: 'Corte + Barba', price: 70.00, durationMin: 60, duration: '60 min', icon: 'fa-crown' }}
        ];

        // Grade fixa: 30 em 30 minutos das 09:00 até as 18:00
        const defaultTimeSlots = [
            "09:00", "09:30", 
            "10:00", "10:30", 
            "11:00", "11:30", 
            "12:00", "12:30", 
            "13:00", "13:30", 
            "14:00", "14:30", 
            "15:00", "15:30", 
            "16:00", "16:30", 
            "17:00", "17:30", 
            "18:00"
        ];

        let currentUser = null;
        let selectedService = services[0];
        let selectedTime = null;
        let occupiedSlots = [];

        window.onload = () => {{
            checkExistingSession();
            renderServices();
            setMinDate();
            renderFixedGrid();
            renderTimeSlots();
        }};

        /* ---------- RENDERIZAÇÃO DA TABELA FIXADA ---------- */
        function renderFixedGrid() {{
            const container = document.getElementById('timeslots-container');
            container.innerHTML = defaultTimeSlots.map(time => {{
                const isOccupied = occupiedSlots.includes(time);
                if (isOccupied) {{
                    return `
                        <button type="button" disabled class="p-2 rounded-lg bg-zinc-800/40 text-zinc-600 border border-zinc-800 text-xs cursor-not-allowed line-through">
                            ${{time}}
                        </button>`;
                }}
                const isSelected = selectedTime === time;
                return `
                    <button type="button" onclick="selectTime('${{time}}')" id="time-btn-${{time.replace(':', '')}}" 
                            class="p-2 rounded-lg border text-xs font-medium transition ${{isSelected ? 'gold-bg text-black border-yellow-500 font-bold' : 'input-dark border-zinc-700 hover:border-yellow-500'}}">
                        ${{time}}
                    </button>`;
            }}).join('');
        }}

        /* ---------- GESTÃO DE AUTENTICAÇÃO COM PLANILHA ---------- */
        function checkExistingSession() {{
            const session = localStorage.getItem('barber_current_client');
            if (session) {{
                currentUser = JSON.parse(session);
                showBookingView();
            }} else {{
                showLoginForm();
            }}
        }}

        function showLoginForm() {{
            document.getElementById('auth-section').classList.remove('hidden');
            document.getElementById('login-box').classList.remove('hidden');
            document.getElementById('register-box').classList.add('hidden');
            document.getElementById('booking-section').classList.add('hidden');
            document.getElementById('user-pill').classList.add('hidden');
        }}

        function showRegisterForm() {{
            document.getElementById('login-box').classList.add('hidden');
            document.getElementById('register-box').classList.remove('hidden');
        }}

        async function handleRegister(e) {{
            e.preventDefault();

            const name = document.getElementById('reg-name').value.trim();
            const phone = document.getElementById('reg-phone').value.trim();
            const birthdate = document.getElementById('reg-birthdate').value.trim();
            const email = document.getElementById('reg-email').value.trim().toLowerCase();
            const password = document.getElementById('reg-password').value.trim();

            // Validação estrita: todos os campos são 100% obrigatórios
            if (!name || !phone || !birthdate || !email || !password) {{
                alert("Por favor, preencha todos os campos obrigatórios do cadastro.");
                return;
            }}

            const btn = document.getElementById('btn-register');
            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Gravando no sistema...';

            // Data de nascimento formatada estritamente em PT-BR (DD/MM/AAAA)
            const birthdateBR = formatDateBR(birthdate);

            try {{
                const params = new URLSearchParams({{
                    action: "register",
                    nome: name,
                    telefone: phone,
                    nascimento: birthdateBR,
                    email: email,
                    senha: password
                }});

                const response = await fetch(`${{WEB_APP_URL}}?${{params.toString()}}`);
                const res = await response.json();

                if (res.status === 'success') {{
                    currentUser = {{ name, phone, birthdate: birthdateBR, email }};
                    localStorage.setItem('barber_current_client', JSON.stringify(currentUser));
                    showBookingView();
                }} else {{
                    alert(res.message || "Erro ao realizar cadastro.");
                }}
            }} catch (error) {{
                console.error("Erro no cadastro:", error);
                alert("Erro ao conectar ao sistema. Verifique sua conexão.");
            }} finally {{
                btn.disabled = false;
                btn.innerHTML = 'Finalizar Cadastro';
            }}
        }}

        async function handleLogin(e) {{
            e.preventDefault();

            const email = document.getElementById('login-email').value.trim().toLowerCase();
            const password = document.getElementById('login-password').value;

            if (!email || !password) {{
                alert("Por favor, informe seu e-mail e sua senha.");
                return;
            }}

            const btn = document.getElementById('btn-login');
            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Validando acesso...';

            try {{
                const response = await fetch(`${{WEB_APP_URL}}?action=login&email=${{encodeURIComponent(email)}}&password=${{encodeURIComponent(password)}}`);
                const res = await response.json();

                if (res.status === 'ok') {{
                    currentUser = {{
                        name: res.user.nome,
                        phone: res.user.telefone,
                        birthdate: formatDateBR(res.user.nascimento),
                        email: res.user.email
                    }};
                    localStorage.setItem('barber_current_client', JSON.stringify(currentUser));
                    showBookingView();
                }} else {{
                    alert(res.message || "E-mail ou senha inválidos.");
                }}
            }} catch (error) {{
                alert("Erro ao consultar o sistema de clientes. Verifique sua conexão.");
            }} finally {{
                btn.disabled = false;
                btn.innerHTML = 'Entrar';
            }}
        }}

        function logout() {{
            localStorage.removeItem('barber_current_client');
            currentUser = null;
            showLoginForm();
        }}

        function showBookingView() {{
            document.getElementById('auth-section').classList.add('hidden');
            document.getElementById('booking-section').classList.remove('hidden');
            document.getElementById('user-pill').classList.remove('hidden');
            document.getElementById('user-pill').classList.add('flex');

            const firstName = currentUser.name ? currentUser.name.split(' ')[0] : 'Cliente';
            document.getElementById('user-greeting').innerText = `Olá, ${{firstName}}`;
            document.getElementById('display-client-name').innerText = currentUser.name;
            document.getElementById('display-client-phone').innerText = currentUser.phone;
            
            const nascBR = formatDateBR(currentUser.birthdate);
            document.getElementById('display-client-info').innerText = `📧 ${{currentUser.email}} | 🎂 ${{nascBR}}`;
            renderTimeSlots();
        }}

        /* ---------- FLUXO DE AGENDAMENTO ---------- */
        function setMinDate() {{
            const dateInput = document.getElementById('booking-date');
            const today = new Date().toISOString().split('T')[0];
            dateInput.min = today;
            dateInput.value = today;
        }}

        function renderServices() {{
            const container = document.getElementById('services-container');
            container.innerHTML = services.map(s => `
                <div onclick="selectService('${{s.id}}')" id="service-card-${{s.id}}" 
                     class="cursor-pointer p-4 rounded-lg border border-zinc-700 transition card-dark hover:border-yellow-500 ${{s.id === selectedService.id ? 'gold-border border-2 bg-zinc-800' : ''}}">
                    <div class="flex justify-between items-start mb-2">
                        <i class="fa-solid ${{s.icon}} text-lg gold-text"></i>
                        <span class="text-xs bg-zinc-800 px-2 py-0.5 rounded text-zinc-400">${{s.duration}}</span>
                    </div>
                    <h4 class="font-bold text-sm mb-1">${{s.name}}</h4>
                    <span class="gold-text font-semibold text-sm">R$ ${{s.price.toFixed(2).replace('.', ',')}}</span>
                </div>
            `).join('');
            updateTotalPrice();
        }}

        function selectService(id) {{
            selectedService = services.find(s => s.id === id);
            renderServices();
        }}

        function updateTotalPrice() {{
            document.getElementById('total-price').innerText = `R$ ${{selectedService.price.toFixed(2).replace('.', ',')}}`;
        }}

        async function renderTimeSlots() {{
            const dateVal = document.getElementById('booking-date').value;
            const statusEl = document.getElementById('status-sync-slots');
            selectedTime = null;

            if (!dateVal) return;

            if (statusEl) statusEl.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-1"></i> Verificando disponibilidade...';

            try {{
                const res = await fetch(`${{WEB_APP_URL}}?action=get_busy&date=${{dateVal}}`);
                const data = await res.json();
                if (data.status === 'ok') {{
                    occupiedSlots = data.busy.map(b => b.start);
                }} else {{
                    occupiedSlots = [];
                }}
            }} catch(e) {{
                occupiedSlots = [];
            }} finally {{
                if (statusEl) statusEl.innerHTML = '<span class="text-green-400"><i class="fa-solid fa-circle-check mr-1"></i> Agenda atualizada</span>';
                renderFixedGrid();
            }}
        }}

        function selectTime(time) {{
            selectedTime = time;
            defaultTimeSlots.forEach(t => {{
                const btn = document.getElementById(`time-btn-${{t.replace(':', '')}}`);
                if (btn) {{
                    if (t === time) {{
                        btn.className = "p-2 rounded-lg border text-xs font-bold gold-bg text-black border-yellow-500";
                    }} else {{
                        btn.className = "p-2 rounded-lg border text-xs font-medium input-dark border-zinc-700 hover:border-yellow-500";
                    }}
                }}
            }});
        }}

        async function handleBooking(e) {{
            e.preventDefault();

            if (!selectedTime) {{
                alert("Por favor, selecione um horário disponível.");
                return;
            }}

            const submitBtn = document.getElementById('submit-btn');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Agendando no Google...';

            const date = document.getElementById('booking-date').value;
            const dateBR = formatDateBR(date);

            const newBooking = {{
                nome: currentUser.name,
                telefone: currentUser.phone,
                nascimento: formatDateBR(currentUser.birthdate),
                email: currentUser.email,
                servico: selectedService.name,
                valor: selectedService.price,
                duracao: selectedService.durationMin,
                data: date,       // Formato ISO para a data do evento
                data_br: dateBR,  // Data em formato PT-BR para lançamentos e descrições
                horario: selectedTime
            }};

            const syncStatusEl = document.getElementById('sync-status');
            syncStatusEl.innerText = "⏳ Gravando na Google Agenda do barbeiro...";

            try {{
                await fetch(WEB_APP_URL, {{
                    method: 'POST',
                    mode: 'no-cors',
                    headers: {{ 'Content-Type': 'text/plain;charset=utf-8' }},
                    body: JSON.stringify(newBooking)
                }});

                syncStatusEl.innerText = "✅ Salvo com sucesso na Google Agenda do barbeiro!";
                syncStatusEl.className = "text-xs text-green-400 py-1";
            }} catch (error) {{
                console.error(error);
                syncStatusEl.innerText = "⚠️ Agendado localmente (verifique a sincronização com a Google Agenda).";
            }} finally {{
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fa-solid fa-check-circle"></i> Confirmar Agendamento';
            }}

            const googleUrl = generateGoogleCalendarUrl(newBooking);

            document.getElementById('modal-details').innerHTML = `
                <strong>${{newBooking.nome}}</strong>, seu agendamento foi realizado!<br><br>
                ✂️ <strong>Serviço:</strong> ${{newBooking.servico}}<br>
                📅 <strong>Data:</strong> ${{dateBR}}<br>
                ⏰ <strong>Horário:</strong> ${{newBooking.horario}}<br>
                💰 <strong>Valor:</strong> R$ ${{newBooking.valor.toFixed(2).replace('.', ',')}}
            `;
            document.getElementById('google-calendar-link').href = googleUrl;
            document.getElementById('success-modal').classList.remove('hidden');
            document.getElementById('success-modal').classList.add('flex');

            renderTimeSlots();
        }}

        function generateGoogleCalendarUrl(booking) {{
            const title = encodeURIComponent(`Barbearia Style: ${{booking.servico}}`);
            const details = encodeURIComponent(`Agendamento de ${{booking.servico}} para ${{booking.nome}}.\\nTelefone: ${{booking.telefone}}\\nNascimento: ${{booking.nascimento}}\\nE-mail: ${{booking.email}}\\nData: ${{booking.data_br}}\\nValor: R$ ${{booking.valor.toFixed(2)}}`);
            const location = encodeURIComponent("Barbearia Style");

            const [year, month, day] = booking.data.split('-');
            const [hour, minute] = booking.horario.split(':');
            
            const startDate = new Date(Date.UTC(year, month - 1, day, hour, minute));
            const endDate = new Date(startDate.getTime() + (booking.duracao || 30) * 60000);

            const isoStart = startDate.toISOString().replace(/-|:|\.\d\d\d/g, "");
            const isoEnd = endDate.toISOString().replace(/-|:|\.\d\d\d/g, "");

            return `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${{title}}&dates=${{isoStart}}/${{isoEnd}}&details=${{details}}&location=${{location}}`;
        }}

        function closeModal() {{
            document.getElementById('success-modal').classList.add('hidden');
            document.getElementById('success-modal').classList.remove('flex');
        }}
    </script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=True)