let Professores = [];
let nextId = 1;

async function carregarProfessores() {
    try {
        const resposta = await fetch('/API/GetProfessores', {
            credentials: 'same-origin'
        });

        if (!resposta.ok) {
            throw new Error('Resposta inválida da API');
        }

        const dados = await resposta.json();
        Professores = Array.isArray(dados) ? dados : [];
        renderizar(Professores);
        return Professores;
    } catch (erro) {
        console.error('Falha ao carregar Professores!', erro);
        Professores = [];
        renderizar(Professores);
        return [];
    }
}

function renderizar(Professores) {
    const tbody = document.getElementById('tableBody');
    const dadosFiltrados = Professores;

    if (dadosFiltrados.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="empty-state"><i class="fas fa-user-slash"></i><p>Nenhum professor encontrado</p><button class="btn-primary" onclick="abrirModal()"><i class="fas fa-plus"></i> Adicionar</button></td></tr>`;
        document.getElementById('totalRegistros').textContent = '0 professores';
        return;
    }

    tbody.innerHTML = dadosFiltrados.map(item => {
        const statusClass = item.status === 'Ativo' ? 'ativo' : item.status === 'Afastado' ? 'afastado' : 'inativo';
        return `<tr>
            <td>${item.id}</td>
            <td><strong>${item.nome}</strong></td>
            <td>${item.matricula}</td>
            <td>${item.cpf}</td>
            <td>${item.disciplina}</td>
            <td><span class="status-badge ${statusClass}">${item.status}</span></td>
            <td>
                <button class="action-btn view" onclick="visualizar(${item.id})"><i class="fas fa-eye"></i></button>
                <button class="action-btn edit" onclick="editar(${item.id})"><i class="fas fa-edit"></i></button>
                <button class="action-btn delete" onclick="excluir(${item.id})"><i class="fas fa-trash"></i></button>
            </td>
        </tr>`;
    }).join('');

    document.getElementById('totalRegistros').textContent = dadosFiltrados.length + ' professores';
}

function filtrar() {
    const search = document.getElementById('searchInput').value.toLowerCase();
    const status = document.getElementById('filterStatus').value;
    const filtrados = dados.filter(item => {
        const matchSearch = item.nome.toLowerCase().includes(search) || item.matricula.includes(search) || item.cpf.includes(search);
        const matchStatus = status === '' || item.status === status;
        return matchSearch && matchStatus;
    });
    renderizar(filtrados);
}

function limparFiltros() {
    document.getElementById('searchInput').value = '';
    document.getElementById('filterStatus').value = '';
    renderizar(dados);
}

function visualizar(id) {
    window.location.href = '/Coordenador/Professor/' + id;
}

function abrirModal(item) {
    const modal = document.getElementById('modal');
    const title = document.getElementById('modalTitle');
    const btn = document.getElementById('btnSalvar');

    if (item) {
        title.innerHTML = '<i class="fas fa-user-edit"></i> Editar Professor';
        btn.textContent = 'Atualizar';
        document.getElementById('itemId').value = item.id;
        document.getElementById('nome').value = item.nome;
        document.getElementById('matricula').value = item.matricula;
        document.getElementById('cpf').value = item.cpf;
        document.getElementById('disciplina').value = item.disciplina;
        document.getElementById('status').value = item.status;
        document.getElementById('email').value = item.email || '';
        document.getElementById('telefone').value = item.telefone || '';
    } else {
        title.innerHTML = '<i class="fas fa-user-plus"></i> Novo Professor';
        btn.textContent = 'Salvar';
        document.getElementById('form').reset();
        document.getElementById('itemId').value = '';
        document.getElementById('status').value = 'Ativo';
    }

    modal.classList.add('ativo');
    document.body.style.overflow = 'hidden';
}

function fecharModal() {
    document.getElementById('modal').classList.remove('ativo');
    document.body.style.overflow = '';
}

function editar(id) {
    const item = dados.find(item => item.id === id);
    if (item) abrirModal(item);
}

function salvar(event) {
    event.preventDefault();
    const id = document.getElementById('itemId').value;
    const dadosItem = {
        nome: document.getElementById('nome').value.trim(),
        matricula: document.getElementById('matricula').value.trim(),
        cpf: document.getElementById('cpf').value.trim(),
        disciplina: document.getElementById('disciplina').value.trim(),
        status: document.getElementById('status').value,
        email: document.getElementById('email').value.trim(),
        telefone: document.getElementById('telefone').value.trim()
    };

    if (id) {
        const index = dados.findIndex(item => item.id === parseInt(id));
        if (index !== -1) {
            dados[index] = { ...dados[index], ...dadosItem };
            showToast('Professor atualizado com sucesso!', 'success');
        }
    } else {
        dadosItem.id = nextId++;
        dados.push(dadosItem);
        showToast('Professor cadastrado com sucesso!', 'success');
    }

    fecharModal();
    renderizar(dados);
}

function excluir(id) {
    const item = dados.find(item => item.id === id);
    if (!item) return;
    if (confirm('Tem certeza que deseja excluir "' + item.nome + '"?')) {
        dados = dados.filter(item => item.id !== id);
        renderizar(dados);
        showToast('Professor "' + item.nome + '" excluído', 'error');
    }
}

function showToast(message, type) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast toast-' + (type || 'info');
    toast.innerHTML = `<span>${message}</span><button onclick="this.parentElement.remove()" style="background:none;border:none;font-size:18px;cursor:pointer;color:#999;">×</button>`;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

document.addEventListener('DOMContentLoaded', function () {
    carregarProfessores();
});