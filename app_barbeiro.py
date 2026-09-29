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
        .card-dark { background-color: #1E1E1E; }
        .input-dark { background-color: #2A2A2A; color: #FFFFFF; border: 1px solid #333; }
        .input-dark:focus { border-color: #D4AF37; outline: none; }
    </style>
</head>
<body class="min-h-screen pb-16">

    <header class="card-dark border-b border-zinc-800 sticky top-0 z-50 shadow-md">
        <div class="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <i class="fa-solid font-bold text-2xl gold-text fa-scissors"></i>
                <h1 class="text-xl font-bold tracking-wide">PAINEL DO <span class="gold-text">BARBEIRO</span></h1>
            </div>
            <a href="https://calendar.google.com" target="_blank" class="text-xs gold-text border border-yellow-600/50 px-3 py-1.5 rounded-full hover:bg-yellow-500 hover:text-black transition flex items-center gap-1.5">
                <i class="fa-brands fa-google"></i> Abrir Google Agenda
            </a>
        </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 mt-8">
        
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
            <div>
                <h2 class="text-2xl font-bold">Fila de Atendimentos</h2>
                <p class="text-zinc-400 text-xs">Visualize e gerencie os horários agendados pelos clientes.</p>
            </div>
            
            <!-- Filtro de Data -->
            <div class="card-dark p-2 px-3 rounded-xl border border-zinc-800 flex items-center gap-3">
                <label class="text-xs text-zinc-400">Data:</label>
                <input type="date" id="filter-date" onchange="renderBookings()" class="p-2 rounded-lg input-dark text-xs">
                <button onclick="renderBookings()" class="text-xs gold-text hover:text-yellow-400 p-1.5" title="Atualizar">
                    <i class="fa-solid fa-arrows-rotate"></i>
                </button>
            </div>
        </div>

        <!-- Métricas Rápidas do Dia -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
            <div class="card-dark p-4 rounded-xl border border-zinc-800">
                <span class="text-zinc-400 text-xs block">Total de Agendamentos</span>
                <span id="metric-total" class="text-2xl font-bold text-white">0</span>
            </div>
            <div class="card-dark p-4 rounded-xl border border-zinc-800">
                <span class="text-zinc-400 text-xs block">Faturamento Previsto</span>
                <span id="metric-revenue" class="text-2xl font-bold gold-text">R$ 0,00</span>
            </div>
            <div class="card-dark p-4 rounded-xl border border-zinc-800">
                <span class="text-zinc-400 text-xs block">Atendimentos Ativos</span>
                <span id="metric-active" class="text-2xl font-bold text-green-400">0</span>
            </div>
        </div>

        <!-- Lista de Agendamentos -->
        <div id="bookings-list" class="space-y-4">
            <!-- Itens inseridos dinamicamente -->
        </div>

    </main>

    <script>
        const WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzQoJrcSlveATovQ-syyGJs49JmdgkhcfkKu3jw2ve2lyN36f5fMrbsJokWzgqxNh95/exec";
        let bookings = [];

        window.onload = () => {
            const today = new Date().toISOString().split('T')[0];
            const dateInput = document.getElementById('filter-date');
            dateInput.value = today;
            renderBookings();
        };

        async function renderBookings() {
            const filterDate = document.getElementById('filter-date').value;
            const container = document.getElementById('bookings-list');

            if (!filterDate) return;

            container.innerHTML = `
                <div class="text-center text-zinc-400 py-12 card-dark rounded-xl border border-zinc-800">
                    <i class="fa-solid fa-circle-notch fa-spin text-2xl gold-text mb-3 block"></i>
                    Carregando agendamentos do Google Agenda...
                </div>`;

            try {
                const response = await fetch(`${WEB_APP_URL}?action=get_bookings&date=${filterDate}`);
                const data = await response.json();

                if (data.status === 'ok') {
                    bookings = data.bookings.map(item => {
                        const desc = item.description || '';
                        let phone = '';
                        let service = '';
                        let price = 0;

                        desc.split('\\n').forEach(line => {
                            if (line.includes('WhatsApp:') || line.includes('Telefone:')) {
                                phone = line.split(':')[1]?.trim() || '';
                            }
                            if (line.includes('Serviço:')) {
                                service = line.split(':')[1]?.split('(')[0]?.trim() || '';
                            }
                            if (line.includes('R$')) {
                                const valStr = line.split('R$')[1]?.trim()?.replace(',', '.') || '0';
                                price = parseFloat(valStr) || 0;
                            }
                        });

                        return {
                            id: item.id,
                            title: item.title,
                            time: item.time,
                            name: item.title.replace(/^💈\\s*/, '').split(' - ')[1] || item.title,
                            service: service || item.title.replace(/^💈\\s*/, '').split(' - ')[0] || 'Serviço',
                            phone: phone || 'Não informado',
                            price: price,
                            status: 'confirmado'
                        };
                    });
                } else {
                    bookings = [];
                }
            } catch (err) {
                console.error("Erro ao buscar no Google Agenda:", err);
                bookings = JSON.parse(localStorage.getItem('barber_bookings')) || [];
                bookings = bookings.filter(b => b.date === filterDate);
            }

            // Atualiza métricas
            const activeBookings = bookings.filter(b => b.status !== 'cancelado');
            const totalRevenue = activeBookings.reduce((acc, curr) => acc + (curr.price || 0), 0);

            document.getElementById('metric-total').innerText = bookings.length;
            document.getElementById('metric-active').innerText = activeBookings.length;
            document.getElementById('metric-revenue').innerText = `R$ ${totalRevenue.toFixed(2).replace('.', ',')}`;

            if (bookings.length === 0) {
                container.innerHTML = `
                    <div class="text-center text-zinc-500 py-12 card-dark rounded-xl border border-zinc-800">
                        <i class="fa-regular fa-calendar-xmark text-4xl mb-3 text-zinc-600 block"></i>
                        Nenhum agendamento encontrado para este dia.
                    </div>`;
                return;
            }

            // Ordena por horário crescente
            bookings.sort((a, b) => a.time.localeCompare(b.time));

            container.innerHTML = bookings.map(b => `
                <div class="card-dark p-5 rounded-xl border border-zinc-800 shadow-md flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                    <div class="space-y-1">
                        <div class="flex items-center gap-3">
                            <span class="gold-text font-bold text-xl">${b.time}</span>
                            <span class="font-bold text-base text-white">${b.name}</span>
                            <span class="text-xs px-2.5 py-0.5 rounded-full ${b.status === 'cancelado' ? 'bg-red-900/40 text-red-400' : 'bg-green-900/40 text-green-400'}">
                                ${b.status}
                            </span>
                        </div>
                        <p class="text-xs text-zinc-300">
                            <strong>Serviço:</strong> ${b.service} 
                            <span class="gold-text ml-2 font-semibold">R$ ${b.price.toFixed(2).replace('.', ',')}</span>
                        </p>
                        <p class="text-xs text-zinc-400">
                            <i class="fa-brands fa-whatsapp text-green-500 mr-1"></i> ${b.phone}
                        </p>
                    </div>

                    <div class="flex items-center gap-2 w-full sm:w-auto justify-end border-t sm:border-t-0 pt-3 sm:pt-0 border-zinc-800">
                        ${b.status !== 'cancelado' ? `
                            <button onclick="cancelBooking('${b.id}')" class="text-xs text-red-400 hover:text-red-300 border border-red-900/50 bg-red-950/20 px-3 py-2 rounded-lg transition">
                                <i class="fa-solid fa-ban mr-1"></i> Cancelar
                            </button>
                        ` : ''}
                    </div>
                </div>
            `).join('');
        }

        async function cancelBooking(id) {
            if (confirm("Deseja realmente cancelar este horário?")) {
                try {
                    await fetch(WEB_APP_URL, {
                        method: 'POST',
                        mode: 'no-cors',
                        headers: { 'Content-Type': 'text/plain;charset=utf-8' },
                        body: JSON.stringify({ action: 'cancel', eventId: id })
                    });
                } catch (e) {
                    console.error("Erro ao cancelar no Apps Script:", e);
                }

                // Remove do backup local se existir
                let localBookings = JSON.parse(localStorage.getItem('barber_bookings')) || [];
                localBookings = localBookings.map(b => String(b.id) === String(id) ? { ...b, status: 'cancelado' } : b);
                localStorage.setItem('barber_bookings', JSON.stringify(localBookings));

                renderBookings();
            }
        }
    </script>
</body>
</html>
"""

components.html(html_code, height=850, scrolling=True)