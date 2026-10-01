import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Painel do Barbeiro - Barbearia Style",
    page_icon="✂️",
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

html_code = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel do Barbeiro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        body {
            font-family: 'Poppins', sans-serif;
            background-color: #121212;
            color: #E0E0E0;
            margin: 0;
            padding: 0;
        }
        .gold-bg { background-color: #D4AF37; }
        .gold-text { color: #D4AF37; }
        .gold-border { border-color: #D4AF37; }
        .card-dark { background-color: #1E1E1E; }
        .input-dark { background-color: #2A2A2A; color: #FFFFFF; border: 1px solid #333; }
        .input-dark:focus { border-color: #D4AF37; outline: none; }
    </style>
</head>
<body class="min-h-screen pb-16">

    <!-- Topbar -->
    <header class="card-dark border-b border-zinc-800 sticky top-0 z-50 shadow-md">
        <div class="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <i class="fa-solid font-bold text-2xl gold-text fa-scissors"></i>
                <h1 class="text-xl font-bold tracking-wide">PAINEL DO <span class="gold-text">BARBEIRO</span></h1>
            </div>
            <div class="flex items-center gap-2">
                <a href="https://calendar.google.com" target="_blank" class="text-xs gold-text border border-yellow-600/50 px-3 py-1.5 rounded-full hover:bg-yellow-500 hover:text-black transition flex items-center gap-1.5">
                    <i class="fa-brands fa-google"></i> Google Agenda
                </a>
            </div>
        </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 mt-8">
        
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
            <div>
                <h2 class="text-2xl font-bold">Fila de Atendimentos</h2>
                <p class="text-zinc-400 text-xs">Visualize, conclua e lance atendimentos na planilha com facilidade.</p>
            </div>
            
            <div class="flex items-center gap-2 w-full sm:w-auto">
                <!-- Botão de Novo Agendamento pelo Barbeiro -->
                <button onclick="openBookingModal()" class="gold-bg text-black font-bold text-xs px-3.5 py-2 rounded-lg hover:bg-yellow-400 transition flex items-center gap-1.5 shadow">
                    <i class="fa-solid fa-calendar-plus"></i> Novo Agendamento
                </button>

                <!-- Filtro de Data -->
                <div class="card-dark p-1.5 px-3 rounded-lg border border-zinc-800 flex items-center gap-2">
                    <label class="text-xs text-zinc-400">Data:</label>
                    <input type="date" id="filter-date" onchange="renderBookings()" class="p-1 rounded input-dark text-xs">
                    <button onclick="renderBookings()" class="text-xs gold-text hover:text-yellow-400 p-1" title="Atualizar">
                        <i class="fa-solid fa-arrows-rotate"></i>
                    </button>
                </div>
            </div>
        </div>

        <!-- Métricas Rápidas: Agenda + Financeiro da Planilha -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
            <div class="card-dark p-3.5 rounded-xl border border-zinc-800">
                <span class="text-zinc-400 text-[11px] block">Agenda do Dia</span>
                <span id="metric-total" class="text-xl font-bold text-white">0</span>
            </div>
            <div class="card-dark p-3.5 rounded-xl border border-zinc-800">
                <span class="text-zinc-400 text-[11px] block">Previsto (Agenda)</span>
                <span id="metric-revenue" class="text-xl font-bold gold-text">R$ 0,00</span>
            </div>
            <div class="card-dark p-3.5 rounded-xl border border-zinc-800">
                <span class="text-zinc-400 text-[11px] block">Recebido no Dia (Confirmado)</span>
                <span id="metric-received-day" class="text-xl font-bold text-green-400">R$ 0,00</span>
                <span id="metric-qty-day" class="text-[10px] text-zinc-500 block">0 atendimentos</span>
            </div>
            <div class="card-dark p-3.5 rounded-xl border border-zinc-800">
                <span class="text-zinc-400 text-[11px] block">Recebido no Mês</span>
                <span id="metric-received-month" class="text-xl font-bold text-yellow-400">R$ 0,00</span>
                <span id="metric-qty-month" class="text-[10px] text-zinc-500 block">0 atendimentos</span>
            </div>
        </div>

        <!-- Lista de Agendamentos -->
        <div id="bookings-list" class="space-y-4">
            <!-- Itens inseridos dinamicamente -->
        </div>

    </main>

    <!-- ================= MODAL DE NOVO AGENDAMENTO (BARBEIRO) ================= -->
    <div id="modal-new-booking" class="fixed inset-0 bg-black/80 hidden items-center justify-center p-4 z-50">
        <div class="card-dark p-6 rounded-2xl max-w-lg w-full border border-zinc-700 relative space-y-4 max-h-[90vh] overflow-y-auto">
            <div class="flex justify-between items-center border-b border-zinc-800 pb-3">
                <h3 class="text-lg font-bold flex items-center gold-text">
                    <i class="fa-solid fa-calendar-plus mr-2"></i> Agendar Cliente
                </h3>
                <button onclick="closeBookingModal()" class="text-zinc-400 hover:text-white text-lg">&times;</button>
            </div>

            <!-- Busca rápida de clientes cadastrados -->
            <div>
                <label class="block text-xs text-zinc-400 mb-1">Buscar Cliente Cadastrado (Opcional):</label>
                <div class="flex gap-2">
                    <select id="select-registered-client" onchange="autoFillClientData()" class="w-full p-2.5 rounded-lg input-dark text-xs">
                        <option value="">-- Selecione ou digite manualmente abaixo --</option>
                    </select>
                    <button onclick="loadClientsList()" title="Recarregar clientes" class="p-2 border border-zinc-700 rounded-lg input-dark text-xs hover:border-yellow-500">
                        <i class="fa-solid fa-arrows-rotate"></i>
                    </button>
                </div>
            </div>

            <form onsubmit="handleManualBooking(event)" class="space-y-3">
                <div>
                    <label class="block text-xs text-zinc-400 mb-1">Nome Completo *</label>
                    <input type="text" id="manual-name" required placeholder="Nome do cliente" class="w-full p-2.5 rounded-lg input-dark text-xs">
                </div>

                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block text-xs text-zinc-400 mb-1">WhatsApp / Telefone *</label>
                        <input type="tel" id="manual-phone" required placeholder="(16) 99999-9999" class="w-full p-2.5 rounded-lg input-dark text-xs">
                    </div>
                    <div>
                        <label class="block text-xs text-zinc-400 mb-1">Data de Nascimento</label>
                        <input type="date" id="manual-birthdate" class="w-full p-2.5 rounded-lg input-dark text-xs">
                    </div>
                </div>

                <div>
                    <label class="block text-xs text-zinc-400 mb-1">Serviço *</label>
                    <select id="manual-service" required class="w-full p-2.5 rounded-lg input-dark text-xs">
                        <option value="Corte de Cabelo" data-price="45.00" data-duration="30">Corte de Cabelo — R$ 45,00 (30 min)</option>
                        <option value="Barba Modelada" data-price="35.00" data-duration="30">Barba Modelada — R$ 35,00 (30 min)</option>
                        <option value="Corte + Barba" data-price="70.00" data-duration="60">Corte + Barba — R$ 70,00 (60 min)</option>
                    </select>
                </div>

                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block text-xs text-zinc-400 mb-1">Data *</label>
                        <input type="date" id="manual-date" required class="w-full p-2.5 rounded-lg input-dark text-xs">
                    </div>
                    <div>
                        <label class="block text-xs text-zinc-400 mb-1">Horário *</label>
                        <select id="manual-time" required class="w-full p-2.5 rounded-lg input-dark text-xs">
                            <option value="09:00">09:00</option><option value="09:30">09:30</option>
                            <option value="10:00">10:00</option><option value="10:30">10:30</option>
                            <option value="11:00">11:00</option><option value="11:30">11:30</option>
                            <option value="12:00">12:00</option><option value="12:30">12:30</option>
                            <option value="13:00">13:00</option><option value="13:30">13:30</option>
                            <option value="14:00">14:00</option><option value="14:30">14:30</option>
                            <option value="15:00">15:00</option><option value="15:30">15:30</option>
                            <option value="16:00">16:00</option><option value="16:30">16:30</option>
                            <option value="17:00">17:00</option><option value="17:30">17:30</option>
                            <option value="18:00">18:00</option>
                        </select>
                    </div>
                </div>

                <div class="pt-3 flex justify-end gap-2 border-t border-zinc-800">
                    <button type="button" onclick="closeBookingModal()" class="px-4 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-xs text-zinc-300">
                        Cancelar
                    </button>
                    <button type="submit" id="btn-save-manual" class="px-5 py-2 rounded-lg gold-bg text-black font-bold text-xs hover:bg-yellow-400 transition">
                        Confirmar e Agendar
                    </button>
                </div>
            </form>
        </div>
    </div>

    <!-- ================= MODAL DE AVISO DE CANCELAMENTO VIA WHATSAPP ================= -->
    <div id="modal-cancel-msg" class="fixed inset-0 bg-black/80 hidden items-center justify-center p-4 z-50">
        <div class="card-dark p-6 rounded-2xl max-w-md w-full border border-zinc-700 relative space-y-4">
            <div class="w-12 h-12 bg-red-950/40 text-red-400 border border-red-900 rounded-full flex items-center justify-center mx-auto text-xl font-bold">
                <i class="fa-solid fa-ban"></i>
            </div>
            <h3 class="text-lg font-bold text-center">Horário Cancelado</h3>
            <p class="text-zinc-400 text-xs text-center">O evento foi removido do Google Agenda. Deseja enviar mensagem de aviso ao cliente no WhatsApp?</p>

            <div class="bg-zinc-900 p-3 rounded-lg border border-zinc-800 text-xs text-zinc-300 space-y-1">
                <strong class="text-white block" id="cancel-preview-name"></strong>
                <p id="cancel-preview-details" class="text-zinc-400"></p>
            </div>

            <div class="space-y-2 pt-2">
                <a id="btn-whatsapp-cancel" target="_blank" class="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-2.5 px-4 rounded-lg block flex items-center justify-center gap-2 transition text-xs">
                    <i class="fa-brands fa-whatsapp text-sm"></i> Enviar Mensagem de Cancelamento
                </a>
                <button onclick="closeCancelModal()" class="w-full bg-zinc-800 hover:bg-zinc-700 text-zinc-300 py-2 px-4 rounded-lg transition text-xs">
                    Fechar
                </button>
            </div>
        </div>
    </div>

    <script>
        const WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzQoJrcSlveATovQ-syyGJs49JmdgkhcfkKu3jw2ve2lyN36f5fMrbsJokWzgqxNh95/exec";
        let bookings = [];
        let clientsList = [];

        window.onload = () => {
            const today = new Date().toISOString().split('T')[0];
            const dateInput = document.getElementById('filter-date');
            dateInput.value = today;
            document.getElementById('manual-date').value = today;
            renderBookings();
            loadClientsList();
        };

        async function loadClientsList() {
            try {
                const res = await fetch(`${WEB_APP_URL}?action=list_clients`);
                const data = await res.json();
                if (data.status === 'ok') {
                    clientsList = data.clients || [];
                    const select = document.getElementById('select-registered-client');
                    select.innerHTML = '<option value="">-- Selecione ou digite manualmente abaixo --</option>' +
                        clientsList.map((c, idx) => `
                            <option value="${idx}">${c.nome} (${c.telefone || 'Sem fone'})</option>
                        `).join('');
                }
            } catch (e) {
                console.warn("Aviso ao buscar clientes:", e);
            }
        }

        function autoFillClientData() {
            const selIdx = document.getElementById('select-registered-client').value;
            if (selIdx !== "") {
                const client = clientsList[parseInt(selIdx)];
                if (client) {
                    document.getElementById('manual-name').value = client.nome;
                    document.getElementById('manual-phone').value = client.telefone;
                    if (client.nascimento) {
                        const nParts = client.nascimento.toString().split('T')[0];
                        document.getElementById('manual-birthdate').value = nParts;
                    }
                }
            }
        }

        async function renderBookings() {
            const filterDate = document.getElementById('filter-date').value;
            const container = document.getElementById('bookings-list');

            if (!filterDate) return;

            container.innerHTML = `
                <div class="text-center text-zinc-400 py-12 card-dark rounded-xl border border-zinc-800">
                    <i class="fa-solid fa-circle-notch fa-spin text-2xl gold-text mb-3 block"></i>
                    Carregando dados da Agenda e da Planilha...
                </div>`;

            // 1. Busca agendamentos da agenda
            try {
                const response = await fetch(`${WEB_APP_URL}?action=get_bookings&date=${filterDate}`);
                const data = await response.json();

                if (data.status === 'ok') {
                    bookings = data.bookings.map(item => {
                        const desc = item.description || '';
                        let phone = '';
                        let service = '';
                        let birthdate = '';
                        let email = '';
                        let price = 0;

                        desc.split('\\n').forEach(line => {
                            if (line.includes('WhatsApp:') || line.includes('Telefone:')) {
                                phone = line.split(':')[1]?.trim() || '';
                            }
                            if (line.includes('Nascimento:')) {
                                birthdate = line.split(':')[1]?.trim() || '';
                            }
                            if (line.includes('E-mail:')) {
                                email = line.split(':')[1]?.trim() || '';
                            }
                            if (line.includes('Serviço:')) {
                                service = line.split(':')[1]?.split('(')[0]?.trim() || '';
                            }
                            if (line.includes('R$')) {
                                const valStr = line.split('R$')[1]?.trim()?.replace(',', '.') || '0';
                                price = parseFloat(valStr) || 0;
                            }
                        });

                        const isCompleted = item.title.includes('[CONCLUÍDO]') || desc.includes('ATENDIMENTO CONCLUÍDO');
                        let cleanTitle = item.title.replace(/^✅\s*\[CONCLUÍDO\]\s*/i, '').replace(/^💈\s*/, '');
                        let extractedName = cleanTitle;
                        let extractedService = service;

                        if (cleanTitle.includes(' - ')) {
                            const titleParts = cleanTitle.split(' - ');
                            extractedService = extractedService || titleParts[0].trim();
                            extractedName = titleParts[1].trim();
                        }

                        return {
                            id: item.id,
                            title: item.title,
                            time: item.time,
                            name: extractedName || 'Cliente',
                            service: extractedService || 'Serviço',
                            phone: phone || '',
                            birthdate: birthdate || '',
                            email: email || '',
                            price: price,
                            date: filterDate,
                            isCompleted: isCompleted
                        };
                    });
                } else {
                    bookings = [];
                }
            } catch (err) {
                console.error("Erro ao buscar agendamentos:", err);
                bookings = [];
            }

            // 2. Busca resumo financeiro na aba Historico_Atendimentos
            try {
                const fRes = await fetch(`${WEB_APP_URL}?action=get_financial_summary&date=${filterDate}`);
                const fData = await fRes.json();
                if (fData.status === 'ok') {
                    document.getElementById('metric-received-day').innerText = `R$ ${Number(fData.totalDia).toFixed(2).replace('.', ',')}`;
                    document.getElementById('metric-qty-day').innerText = `${fData.qtdDia} atendimentos`;
                    document.getElementById('metric-received-month').innerText = `R$ ${Number(fData.totalMes).toFixed(2).replace('.', ',')}`;
                    document.getElementById('metric-qty-month').innerText = `${fData.qtdMes} atendimentos`;
                }
            } catch (errF) {
                console.warn("Erro ao buscar resumo financeiro:", errF);
            }

            // Métricas da agenda
            const totalRevenue = bookings.reduce((acc, curr) => acc + (curr.price || 0), 0);
            document.getElementById('metric-total').innerText = bookings.length;
            document.getElementById('metric-revenue').innerText = `R$ ${totalRevenue.toFixed(2).replace('.', ',')}`;

            if (bookings.length === 0) {
                container.innerHTML = `
                    <div class="text-center text-zinc-500 py-12 card-dark rounded-xl border border-zinc-800">
                        <i class="fa-regular fa-calendar-xmark text-4xl mb-3 text-zinc-600 block"></i>
                        Nenhum agendamento encontrado para este dia.
                    </div>`;
                return;
            }

            bookings.sort((a, b) => a.time.localeCompare(b.time));

            container.innerHTML = bookings.map((b, idx) => `
                <div class="card-dark p-4 sm:p-5 rounded-xl border border-zinc-800 shadow-md flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                    <div class="space-y-1">
                        <div class="flex items-center gap-3">
                            <span class="gold-text font-bold text-xl">${b.time}</span>
                            <span class="font-bold text-base text-white">${b.name}</span>
                            ${b.isCompleted ? `
                                <span class="text-xs px-2.5 py-0.5 rounded-full bg-green-950/60 text-green-400 border border-green-800/60 font-semibold flex items-center gap-1">
                                    <i class="fa-solid fa-check"></i> Concluído
                                </span>
                            ` : `
                                <span class="text-xs px-2.5 py-0.5 rounded-full bg-blue-900/40 text-blue-400">
                                    Agendado
                                </span>
                            `}
                        </div>
                        <p class="text-xs text-zinc-300">
                            <strong>Serviço:</strong> ${b.service} 
                            <span class="gold-text ml-2 font-semibold">R$ ${b.price.toFixed(2).replace('.', ',')}</span>
                        </p>
                        <p class="text-xs text-zinc-400">
                            <i class="fa-brands fa-whatsapp text-green-500 mr-1"></i> ${b.phone || 'Sem fone'}
                            ${b.birthdate ? `<span class="ml-3"><i class="fa-solid fa-cake-candles mr-1"></i> Nasc: ${b.birthdate}</span>` : ''}
                        </p>
                    </div>

                    <div class="flex items-center gap-2 w-full sm:w-auto justify-end border-t sm:border-t-0 pt-3 sm:pt-0 border-zinc-800">
                        ${b.isCompleted ? `
                            <button disabled class="text-xs bg-zinc-800/80 text-zinc-500 px-3 py-2 rounded-lg cursor-not-allowed flex items-center gap-1.5 border border-zinc-700/50">
                                <i class="fa-solid fa-check-double text-green-500"></i> Lançado na Planilha
                            </button>
                        ` : `
                            <button onclick="completeAttendance(${idx})" class="text-xs bg-green-700 hover:bg-green-600 text-white font-semibold px-3 py-2 rounded-lg transition flex items-center gap-1.5 shadow">
                                <i class="fa-solid fa-circle-check"></i> Concluir Atendimento
                            </button>
                        `}

                        <button onclick="handleCancel(${idx})" class="text-xs text-red-400 hover:text-red-300 border border-red-900/50 bg-red-950/20 px-3 py-2 rounded-lg transition flex items-center gap-1">
                            <i class="fa-solid fa-ban"></i> Cancelar
                        </button>
                    </div>
                </div>
            `).join('');
        }

        async function completeAttendance(idx) {
            const b = bookings[idx];
            if (!confirm(`Confirmar conclusão do atendimento de ${b.name}? O valor de R$ ${b.price.toFixed(2).replace('.', ',')} será lançado no Histórico da planilha e mantido na agenda como confirmado.`)) {
                return;
            }

            try {
                const payload = {
                    action: "complete_attendance",
                    eventId: b.id,
                    nome: b.name,
                    nascimento: b.birthdate,
                    telefone: b.phone,
                    data: b.date,
                    servico: b.service,
                    valor: b.price,
                    horario: b.time
                };

                await fetch(WEB_APP_URL, {
                    method: 'POST',
                    mode: 'no-cors',
                    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
                    body: JSON.stringify(payload)
                });

                alert("✅ Atendimento concluído! Lançado na planilha e mantido na agenda com observação.");
                renderBookings();
            } catch (err) {
                console.error("Erro ao concluir:", err);
                alert("Erro ao lançar atendimento na planilha.");
            }
        }

        async function handleCancel(idx) {
            const b = bookings[idx];
            if (!confirm(`Deseja realmente cancelar o agendamento de ${b.name} às ${b.time}?`)) {
                return;
            }

            try {
                await fetch(WEB_APP_URL, {
                    method: 'POST',
                    mode: 'no-cors',
                    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
                    body: JSON.stringify({ action: 'cancel', eventId: b.id })
                });
            } catch (e) {
                console.error("Erro ao cancelar:", e);
            }

            const cleanPhone = (b.phone || '').replace(/\\D/g, '');
            const dataFmt = b.date.split('-').reverse().join('/');
            
            const textoMensagem = encodeURIComponent(
                `Olá, ${b.name}! 💈\\n` +
                `Informamos que o seu agendamento na Barbearia Style para o serviço *${b.service}*, marcado para o dia *${dataFmt}* às *${b.time}*, precisou ser *cancelado*.\\n\\n` +
                `Caso queira remarcar, basta acessar o nosso link de agendamento ou nos responder por aqui. Pedimos desculpas pelo transtorno!`
            );

            const whatsappUrl = cleanPhone ? `https://wa.me/55${cleanPhone}?text=${textoMensagem}` : `https://wa.me/?text=${textoMensagem}`;

            document.getElementById('cancel-preview-name').innerText = b.name;
            document.getElementById('cancel-preview-details').innerText = `${b.service} | ${dataFmt} às ${b.time} (${b.phone || 'Sem fone'})`;
            document.getElementById('btn-whatsapp-cancel').href = whatsappUrl;

            document.getElementById('modal-cancel-msg').classList.remove('hidden');
            document.getElementById('modal-cancel-msg').classList.add('flex');

            renderBookings();
        }

        function closeCancelModal() {
            document.getElementById('modal-cancel-msg').classList.add('hidden');
            document.getElementById('modal-cancel-msg').classList.remove('flex');
        }

        function openBookingModal() {
            document.getElementById('modal-new-booking').classList.remove('hidden');
            document.getElementById('modal-new-booking').classList.add('flex');
        }

        function closeBookingModal() {
            document.getElementById('modal-new-booking').classList.add('hidden');
            document.getElementById('modal-new-booking').classList.remove('flex');
        }

        async function handleManualBooking(e) {
            e.preventDefault();
            const btn = document.getElementById('btn-save-manual');
            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-1"></i> Agendando...';

            const name = document.getElementById('manual-name').value.trim();
            const phone = document.getElementById('manual-phone').value.trim();
            const birthdate = document.getElementById('manual-birthdate').value;
            const serviceSelect = document.getElementById('manual-service');
            const service = serviceSelect.value;
            const price = parseFloat(serviceSelect.selectedOptions[0].getAttribute('data-price')) || 45.00;
            const duration = parseInt(serviceSelect.selectedOptions[0].getAttribute('data-duration')) || 30;
            const date = document.getElementById('manual-date').value;
            const time = document.getElementById('manual-time').value;

            try {
                const payload = {
                    nome: name,
                    telefone: phone,
                    nascimento: birthdate,
                    servico: service,
                    valor: price,
                    duracao: duration,
                    data: date,
                    horario: time
                };

                await fetch(WEB_APP_URL, {
                    method: 'POST',
                    mode: 'no-cors',
                    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
                    body: JSON.stringify(payload)
                });

                alert("✅ Agendamento realizado com sucesso na Google Agenda!");
                closeBookingModal();
                
                document.getElementById('filter-date').value = date;
                renderBookings();
            } catch (err) {
                console.error("Erro ao agendar:", err);
                alert("Erro ao realizar agendamento manual.");
            } finally {
                btn.disabled = false;
                btn.innerHTML = 'Confirmar e Agendar';
            }
        }
    </script>
</body>
</html>
"""

components.html(html_code, height=920, scrolling=True)