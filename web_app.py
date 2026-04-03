from flask import Flask, render_template_string, request, jsonify
import sqlite3
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import os

app = Flask(__name__)

try:
    FUSO_BRASIL = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO_BRASIL = timezone(timedelta(hours=-3))

def agora_brasil():
    return datetime.now(FUSO_BRASIL)

def data_brasil():
    return agora_brasil().date()

def timestamp_brasil():
    return agora_brasil()

DATABASE = os.path.join(os.path.dirname(__file__), 'atualizacoes.db')

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS atualizacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            feito INTEGER DEFAULT 0,
            data_criacao TEXT NOT NULL,
            data_conclusao TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tracker de Atualizações</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e;
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            color: #00d4aa;
        }
        .form-card {
            background: #16213e;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #888;
        }
        input, textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid #333;
            border-radius: 8px;
            background: #0f0f23;
            color: #fff;
            font-size: 14px;
        }
        input:focus, textarea:focus {
            outline: none;
            border-color: #00d4aa;
        }
        button {
            background: #00d4aa;
            color: #1a1a2e;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            font-size: 14px;
            width: 100%;
        }
        button:hover {
            background: #00b894;
        }
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        .tab {
            flex: 1;
            padding: 12px;
            background: #16213e;
            border: none;
            border-radius: 8px;
            color: #888;
            cursor: pointer;
            font-weight: bold;
        }
        .tab.active {
            background: #00d4aa;
            color: #1a1a2e;
        }
        .tab:hover:not(.active) {
            background: #1f2b4a;
        }
        .item {
            background: #16213e;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 15px;
            display: flex;
            gap: 15px;
            align-items: flex-start;
        }
        .checkbox {
            width: 24px;
            height: 24px;
            border: 2px solid #00d4aa;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            margin-top: 2px;
        }
        .checkbox.feito {
            background: #00d4aa;
        }
        .checkbox.feito::after {
            content: '✓';
            color: #1a1a2e;
            font-weight: bold;
        }
        .item-content {
            flex: 1;
        }
        .item-title {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .item-title.feito {
            text-decoration: line-through;
            color: #666;
        }
        .item-desc {
            color: #888;
            font-size: 14px;
        }
        .item-date {
            color: #555;
            font-size: 12px;
            margin-top: 5px;
        }
        .item-actions {
            display: flex;
            gap: 10px;
        }
        .btn-delete {
            background: #e74c3c;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
        }
        .btn-delete:hover {
            background: #c0392b;
        }
        .empty {
            text-align: center;
            color: #555;
            padding: 40px;
        }
        .stats {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat {
            flex: 1;
            background: #16213e;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #00d4aa;
        }
        .stat-label {
            color: #666;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 Tracker de Atualizações</h1>
        
        <div class="form-card">
            <h3 style="margin-bottom: 15px; color: #00d4aa;">Nova Atualização</h3>
            <div class="form-group">
                <label>Título</label>
                <input type="text" id="titulo" placeholder="Digite o título...">
            </div>
            <div class="form-group">
                <label>Descrição (opcional)</label>
                <textarea id="descricao" rows="3" placeholder="Detalhes da atualização..."></textarea>
            </div>
            <button onclick="adicionarAtualizacao()">Adicionar</button>
        </div>

        <div class="stats">
            <div class="stat">
                <div class="stat-value" id="total">0</div>
                <div class="stat-label">Total</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="pendentes">0</div>
                <div class="stat-label">Pendentes</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="feitos">0</div>
                <div class="stat-label">Feitos</div>
            </div>
        </div>

        <div class="tabs">
            <button class="tab active" onclick="filtrar('todas')">Todas</button>
            <button class="tab" onclick="filtrar('pendentes')">Pendentes</button>
            <button class="tab" onclick="filtrar('feitas')">Feitas</button>
        </div>

        <div id="lista"></div>
    </div>

    <script>
        let filtroAtual = 'todas';

        function carregar() {
            fetch('/api/atualizacoes')
                .then(r => r.json())
                .then(data => {
                    atualizarStats(data);
                    renderizar(data);
                });
        }

        function atualizarStats(data) {
            const total = data.length;
            const feitos = data.filter(a => a.feito).length;
            document.getElementById('total').textContent = total;
            document.getElementById('pendentes').textContent = total - feitos;
            document.getElementById('feitos').textContent = feitos;
        }

        function renderizar(data) {
            const lista = document.getElementById('lista');
            let filtradas = data;
            
            if (filtroAtual === 'pendentes') {
                filtradas = data.filter(a => !a.feito);
            } else if (filtroAtual === 'feitas') {
                filtradas = data.filter(a => a.feito);
            }

            if (filtradas.length === 0) {
                lista.innerHTML = '<div class="empty">Nenhuma atualização encontrada</div>';
                return;
            }

            lista.innerHTML = filtradas.map(a => `
                <div class="item">
                    <div class="checkbox ${a.feito ? 'feito' : ''}" onclick="toggleFeito(${a.id}, ${!a.feito})"></div>
                    <div class="item-content">
                        <div class="item-title ${a.feito ? 'feito' : ''}">${escapeHtml(a.titulo)}</div>
                        ${a.descricao ? `<div class="item-desc">${escapeHtml(a.descricao)}</div>` : ''}
                        <div class="item-date">Criado: ${a.data_criacao}</div>
                        ${a.data_conclusao ? `<div class="item-date" style="color: #00d4aa;">Feito: ${a.data_conclusao}</div>` : ''}
                    </div>
                    <div class="item-actions">
                        <button class="btn-delete" onclick="deletar(${a.id})">Excluir</button>
                    </div>
                </div>
            `).join('');
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function filtrar(tipo) {
            filtroAtual = tipo;
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            event.target.classList.add('active');
            fetch('/api/atualizacoes')
                .then(r => r.json())
                .then(data => {
                    atualizarStats(data);
                    renderizar(data);
                });
        }

        function adicionarAtualizacao() {
            const titulo = document.getElementById('titulo').value.trim();
            const descricao = document.getElementById('descricao').value.trim();

            if (!titulo) {
                alert('Digite um título');
                return;
            }

            fetch('/api/adicionar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ titulo, descricao })
            })
            .then(r => r.json())
            .then(() => {
                document.getElementById('titulo').value = '';
                document.getElementById('descricao').value = '';
                carregar();
            });
        }

        function toggleFeito(id, feito) {
            fetch(`/api/toggle/${id}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ feito })
            })
            .then(r => r.json())
            .then(() => carregar());
        }

        function deletar(id) {
            if (!confirm('Deseja excluir esta atualização?')) return;
            fetch(`/api/deletar/${id}`, { method: 'DELETE' })
                .then(r => r.json())
                .then(() => carregar());
        }

        setInterval(carregar, 10000);
        carregar();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/atualizacoes')
def get_atualizacoes():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM atualizacoes ORDER BY feito ASC, data_criacao DESC')
    rows = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/adicionar', methods=['POST'])
def adicionar():
    data = request.json
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(
        'INSERT INTO atualizacoes (titulo, descricao, data_criacao) VALUES (?, ?, ?)',
        (data['titulo'], data.get('descricao', ''), timestamp_brasil().strftime('%Y-%m-%d %H:%M'))
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/toggle/<int:id>', methods=['POST'])
def toggle(id):
    data = request.json
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    if data['feito']:
        c.execute(
            'UPDATE atualizacoes SET feito = 1, data_conclusao = ? WHERE id = ?',
            (timestamp_brasil().strftime('%Y-%m-%d %H:%M'), id)
        )
    else:
        c.execute(
            'UPDATE atualizacoes SET feito = 0, data_conclusao = NULL WHERE id = ?',
            (id,)
        )
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/deletar/<int:id>', methods=['DELETE'])
def deletar(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('DELETE FROM atualizacoes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
