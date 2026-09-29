import streamlit as st
import streamlit.components.v1 as components

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Barbearia Style - Agendamento",
    page_icon="💈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilo para ocultar os elementos padrão do Streamlit e expandir a tela
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)

# URL da sua automação no Google Apps Script
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzQoJrcSlveATovQ-syyGJs49JmdgkhcfkKu3jw2ve2lyN36f5fMrbsJokWzgqxNh95/exec"

# Aplicação completa em HTML/CSS/JS injetada no Streamlit
html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Barbearia Style - Agendamento Online</title>
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
<body class="min-h-screen pb-12">

    <!-- Header / Navbar -->
    <header class="card-dark border-b border-zinc-800 sticky top-0 z-50 shadow-md">
        <div class="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <i class="fa-solid font-bold text-2xl gold-text fa-scissors"></i>
                <h1 class="text-xl font-bold tracking-wide">BARBEARIA <span class="gold-text">STYLE</span></h1>
            </div>
            <button id="toggle-view-btn" onclick="toggleView()" class="text-xs gold-text border gold-border px-3 py-1.5 rounded-full hover:bg-yellow-500 hover:text-black transition">
                <i class="fa-solid fa-user-shield mr-1"></i> Painel do Barbeiro
            </button>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 mt-8">

        <!-- VISÃO DO CLIENTE -->
        <div id="client-view">
            <div class="text-center mb-8">
                <h2 class="text-3xl font-bold mb-2">Agende seu Horário</h2>
                <p class="text-zinc-400 text-sm">Escolha o serviço, data e horário ideais para você.</p>
            </div>

            <form id="booking-form" onsubmit="handleBooking(event)" class="space-y-6">
                
                <!-- 1. Dados Pessoais -->
                <div class="card-dark p-6 rounded-xl border border-zinc-800 shadow-lg">
                    <h3 class="text-lg font-semibold mb-4 flex items-center gold-text">
                        <i class="fa-solid fa-user mr-2"></i> 1. Seus Dados
                    </h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-xs text-zinc-400 mb-1">Nome Completo *</label>
                            <input type="text" id="client-name" required placeholder="Digite seu nome" class="w-full p-3 rounded-lg input-dark text-sm">
                        </div>
                        <div>
                            <label class="block text-xs text-zinc-400 mb-1">Telefone (WhatsApp) *</label>
                            <input type="tel" id="client-phone" required placeholder="(16) 99999-9999" class="w-full p-3 rounded-lg input-dark text-sm">
                        </div>
                    </div>
                </div>

                <!-- 2. Escolha de Serviços -->
                <div class="card-dark p-6 rounded-xl border border-zinc-800 shadow-lg">
                    <h3 class="text-lg font-semibold mb-4 flex items-center gold-text">
                        <i class="fa-solid fa-cut mr-2"></i> 2. Escolha o Serviço
                    </h3>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="services-container">
                        <!-- Serviços inseridos dinamicamente -->
                    </div>
                </div>

                <!-- 3. Seleção de Data e Horário -->
                <div class="card-dark p-6 rounded-xl border border-zinc-800 shadow-lg">
                    <h3 class="text-lg font-semibold mb-4 flex items-center gold-text">
                        <i class="fa-solid fa-calendar-days mr-2"></i> 3. Data e Horário
                    </h3>
                    
                    <div class="mb-6">
                        <label class="block text-xs text-zinc-400 mb-2">Selecione o Dia *</label>
                        <input type="date" id="booking-date" required onchange="renderTimeSlots()" class="w-full p-3 rounded-lg input-dark text-sm">
                    </div>

                    <div>
                        <label class="block text-xs text-zinc-400 mb-2">Horários Disponíveis *</label>
                        <div id="timeslots-container" class="grid grid-cols-3 sm:grid-cols-4 gap-2">
                            <!-- Horários carregados dinamicamente -->
                        </div>
                    </div>
                </div>

                <!-- Resumo e Confirmação -->
                <div class="card-dark p-6 rounded-xl border border-zinc-800 shadow-lg flex flex-col md:flex-row justify-between items-center gap-4">
                    <div>
                        <span class="text-xs text-zinc-400 block">Total a Pagar no Local</span>
                        <span id="total-price" class="text-2xl font-bold gold-text">R$ 0,00</span>
                    </div>
                    <button type="submit" id="submit-btn" class="w-full md:w-auto gold-bg text-black font-bold px-8 py-3 rounded-lg hover:bg-yellow-400 transition shadow-lg text-center flex items-center justify-center gap-2">
                        <i class="fa-solid fa-check-circle"></i> Confirmar Agendamento
                    </button>
                </div>
            </form>
        </div>

        <!-- VISÃO DO PAINEL DO BARBEIRO (ADMIN) -->
        <div id="admin-view" class="hidden">
            <div class="flex justify-between items-center mb-6">
                <div>
                    <h2 class="text-2xl font-bold">Painel de Agendamentos</h2>
                    <p class="text-zinc-400 text-sm">Gerencie os horários marcados pelos clientes.</p>
                </div>
            </div>

            <!-- Filtro de Data -->
            <div class="card-dark p-4 rounded-xl border border-zinc-800 mb-6 flex items-center gap-4">
                <label class="text-sm text-zinc-400">Filtrar por data:</label>
                <input type="date" id="admin-filter-date" onchange="renderAdminBookings()" class="p-2 rounded-lg input-dark text-sm">
            </div>

            <!-- Lista de Agendamentos -->
            <div id="admin-bookings-list" class="space-y-4">
                <!-- Inserido dinamicamente -->
            </div>
        </div>

    </main>

    <!-- Modal de Sucesso + Botão Google Agenda -->
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
                    <i class="fa-brands fa-google"></i> Adicionar ao Google Agenda
                </a>
                <button onclick="closeModal()" class="w-full bg-zinc-800 hover:bg-zinc-700 text-zinc-300 font-semibold py-3 px-4 rounded-lg transition">
                    Fechar
                </button>
            </div>
        </div>
    </div>

    <script>
        const WEB_APP_URL = "{WEB_APP_URL}";

        const services = [
            {{ id: 'corte', name: 'Corte de Cabelo', price: 45.00, durationMin: 30, duration: '30 min', icon: 'fa-scissors' }},
            {{ id: 'barba', name: 'Barba Modelada', price: 35.00, durationMin: 30, duration: '30 min', icon: 'fa-user' }},
            {{ id: 'combo', name: 'Corte + Barba', price: 70.00, durationMin: 60, duration: '60 min', icon: 'fa-crown' }}
        ];

        const defaultTimeSlots = ["09:00", "09:45", "10:30", "11:15", "14:00", "14:45", "15:30", "16:15", "17:00", "17:45", "18:30"];

        let selectedService = services[0];
        let selectedTime = null;
        let bookings = JSON.parse(localStorage.getItem('barber_bookings')) || [];

        window.onload = () => {{
            renderServices();
            setMinDate();
            renderTimeSlots();
        }};

        function setMinDate() {{
            const dateInput = document.getElementById('booking-date');
            const today = new Date().toISOString().split('T')[0];
            dateInput.min = today;
            dateInput.value = today;
            document.getElementById('admin-filter-date').value = today;
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

        function renderTimeSlots() {{
            const dateVal = document.getElementById('booking-date').value;
            const container = document.getElementById('timeslots-container');
            selectedTime = null;

            if (!dateVal) {{
                container.innerHTML = '<p class="col-span-4 text-xs text-zinc-500">Selecione uma data primeiro.</p>';
                return;
            }}

            const occupied = bookings
                .filter(b => b.date === dateVal && b.status !== 'cancelado')
                .map(b => b.time);

            container.innerHTML = defaultTimeSlots.map(time => {{
                const isOccupied = occupied.includes(time);
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

            const name = document.getElementById('client-name').value;
            const phone = document.getElementById('client-phone').value;
            const date = document.getElementById('booking-date').value;
            const submitBtn = document.getElementById('submit-btn');

            if (!selectedTime) {{
                alert("Por favor, selecione um horário disponível.");
                return;
            }}

            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Agendando no Google...';

            const newBooking = {{
                id: Date.now(),
                name,
                phone,
                service: selectedService.name,
                price: selectedService.price,
                duration: selectedService.durationMin,
                date,
                time: selectedTime,
                status: 'confirmado'
            }};

            // Salva localmente
            bookings.push(newBooking);
            localStorage.setItem('barber_bookings', JSON.stringify(bookings));

            const syncStatusEl = document.getElementById('sync-status');
            syncStatusEl.innerText = "⏳ Gravando na Google Agenda do barbeiro...";

            // Envia para o Google Apps Script via POST
            try {{
                const payload = {{
                    nome: newBooking.name,
                    telefone: newBooking.phone,
                    servico: newBooking.service,
                    valor: newBooking.price,
                    duracao: newBooking.duration,
                    data: newBooking.date,
                    horario: newBooking.time
                }};

                await fetch(WEB_APP_URL, {{
                    method: 'POST',
                    mode: 'no-cors',
                    headers: {{
                        'Content-Type': 'text/plain;charset=utf-8'
                    }},
                    body: JSON.stringify(payload)
                }});

                syncStatusEl.innerText = "✅ Salvo com sucesso na Google Agenda do barbeiro!";
                syncStatusEl.className = "text-xs text-green-400 py-1";
            }} catch (error) {{
                console.error("Erro ao salvar no Apps Script:", error);
                syncStatusEl.innerText = "⚠️ Agendado localmente (verifique a conexão com a agenda).";
                syncStatusEl.className = "text-xs text-yellow-500 py-1";
            }} finally {{
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fa-solid fa-check-circle"></i> Confirmar Agendamento';
            }}

            const googleUrl = generateGoogleCalendarUrl(newBooking);
            const formattedDate = new Date(date + 'T00:00:00').toLocaleDateString('pt-BR');
            document.getElementById('modal-details').innerHTML = `
                <strong>${{newBooking.name}}</strong>, seu agendamento para <strong>${{newBooking.service}}</strong> foi realizado!<br><br>
                📅 <strong>Data:</strong> ${{formattedDate}}<br>
                ⏰ <strong>Horário:</strong> ${{newBooking.time}}<br>
                💰 <strong>Valor:</strong> R$ ${{newBooking.price.toFixed(2).replace('.', ',')}}
            `;
            document.getElementById('google-calendar-link').href = googleUrl;
            document.getElementById('success-modal').classList.remove('hidden');
            document.getElementById('success-modal').classList.add('flex');

            document.getElementById('booking-form').reset();
            setMinDate();
            renderTimeSlots();
        }}

        function generateGoogleCalendarUrl(booking) {{
            const title = encodeURIComponent(`Barbearia Style: ${{booking.service}}`);
            const details = encodeURIComponent(`Agendamento de ${{booking.service}} para ${{booking.name}}.\\nTelefone: ${{booking.phone}}\\nValor: R$ ${{booking.price.toFixed(2)}}`);
            const location = encodeURIComponent("Barbearia Style");

            const [year, month, day] = booking.date.split('-');
            const [hour, minute] = booking.time.split(':');
            
            const startDate = new Date(Date.UTC(year, month - 1, day, hour, minute));
            const endDate = new Date(startDate.getTime() + (booking.duration || 45) * 60000);

            const isoStart = startDate.toISOString().replace(/-|:|\.\d\d\d/g, "");
            const isoEnd = endDate.toISOString().replace(/-|:|\.\d\d\d/g, "");

            return `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${{title}}&dates=${{isoStart}}/${{isoEnd}}&details=${{details}}&location=${{location}}`;
        }}

        function closeModal() {{
            document.getElementById('success-modal').classList.add('hidden');
            document.getElementById('success-modal').classList.remove('flex');
        }}

        function toggleView() {{
            const clientView = document.getElementById('client-view');
            const adminView = document.getElementById('admin-view');
            const btn = document.getElementById('toggle-view-btn');

            if (clientView.classList.contains('hidden')) {{
                clientView.classList.remove('hidden');
                adminView.classList.add('hidden');
                btn.innerHTML = '<i class="fa-solid fa-user-shield mr-1"></i> Painel do Barbeiro';
            }} else {{
                clientView.classList.add('hidden');
                adminView.classList.remove('hidden');
                btn.innerHTML = '<i class="fa-solid fa-scissors mr-1"></i> Área do Cliente';
                renderAdminBookings();
            }}
        }}

        function renderAdminBookings() {{
            const filterDate = document.getElementById('admin-filter-date').value;
            const container = document.getElementById('admin-bookings-list');
            
            const list = bookings.filter(b => b.date === filterDate);

            if (list.length === 0) {{
                container.innerHTML = '<p class="text-center text-zinc-500 py-8 card-dark rounded-xl border border-zinc-800">Nenhum agendamento para esta data.</p>';
                return;
            }}

            container.innerHTML = list.map(b => `
                <div class="card-dark p-4 rounded-xl border border-zinc-800 flex justify-between items-center">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="gold-text font-bold text-lg">${{b.time}}</span>
                            <span class="font-bold">${{b.name}}</span>
                            <span class="text-xs px-2 py-0.5 rounded ${{b.status === 'cancelado' ? 'bg-red-900/50 text-red-400' : 'bg-green-900/50 text-green-400'}}">${{b.status}}</span>
                        </div>
                        <p class="text-xs text-zinc-400 mt-1">Serviço: ${{b.service}} | Valor: R$ ${{b.price.toFixed(2).replace('.', ',')}}</p>
                        <p class="text-xs text-zinc-500">Contato: ${{b.phone}}</p>
                    </div>
                    <div class="flex gap-2">
                        ${{b.status !== 'cancelado' ? `
                            <button onclick="cancelBooking(${{b.id}})" class="text-xs text-red-400 hover:text-red-300 p-2 rounded bg-zinc-800">
                                <i class="fa-solid fa-ban"></i> Cancelar
                            </button>
                        ` : ''}}
                    </div>
                </div>
            `).join('');
        }}

        function cancelBooking(id) {{
            if (confirm("Deseja realmente cancelar este agendamento?")) {{
                bookings = bookings.map(b => b.id === id ? {{ ...b, status: 'cancelado' }} : b);
                localStorage.setItem('barber_bookings', JSON.stringify(bookings));
                renderAdminBookings();
                renderTimeSlots();
            }}
        }}
    </script>
</body>
</html>
"""

# Renderiza o HTML responsivo no Streamlit
components.html(html_code, height=900, scrolling=True)