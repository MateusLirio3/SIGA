let Professores = [];
let Disciplinas = [];

async function carregarTokenCsrf() {
    const resposta = await fetch('/get-token', {
        credentials: 'same-origin',
        cache: 'no-store'
    });
    if (!resposta.ok) throw new Error('Não foi possível obter o token CSRF');
    return resposta.headers.get('X-CSRF-Token');
}

async function carregarDisciplinas() {
    const resposta = await fetch('/API/GetDisciplinas', { credentials: 'same-origin' });
    if (!resposta.ok) throw new Error('Falha ao carregar disciplinas');
    Disciplinas = await resposta.json();
    document.getElementById('disciplinas-container').innerHTML = Disciplinas.map(disciplina => `
        <label class="disciplina-option">
            <input type="checkbox" name="disciplinas" value="${disciplina.id}">
            <span>${disciplina.nome}</span>
        </label>`).join('') || '<span>Nenhuma disciplina cadastrada.</span>';
}

async function carregarProfessores() {
    const resposta = await fetch('/API/GetProfessors', { credentials: 'same-origin' });
    if (!resposta.ok) throw new Error('Falha ao carregar professores');
    Professores = await resposta.json();
    renderizar(Professores);
}

function renderizar(professores) {
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = professores.length ? professores.map((item, index) => `<tr>
        <td>${index + 1}</td><td><strong>${item.nome}</strong></td>
        <td>${item.matricula}</td><td>${item.cpf}</td>
        <td>${(item.disciplinas || []).join(', ') || '-'}</td>
        <td><button class="action-btn edit" onclick="editar('${item.id}')"><i class="fas fa-edit"></i></button>
        <button class="action-btn delete" onclick="excluir('${item.id}')"><i class="fas fa-trash"></i></button></td>
    </tr>`).join('') : '<tr><td colspan="6" class="empty-state">Nenhum professor encontrado</td></tr>';
    document.getElementById('totalRegistros').textContent = `${professores.length} professores`;
}

function filtrar() {
    const busca = document.getElementById('searchInput').value.toLowerCase();
    renderizar(Professores.filter(item => [item.nome, item.matricula, item.cpf]
        .some(valor => (valor || '').toLowerCase().includes(busca))));
}

function limparFiltros() {
    document.getElementById('searchInput').value = '';
    renderizar(Professores);
}

function abrirModal(item) {
    document.getElementById('form').reset();
    document.getElementById('itemId').value = item?.id || '';
    document.getElementById('nome').value = item?.nome || '';
    document.getElementById('matricula').value = item?.matricula || '';
    document.getElementById('cpf').value = item?.cpf || '';
    document.getElementById('email').value = item?.email || '';
    document.getElementById('modalTitle').innerHTML = item
        ? '<i class="fas fa-user-edit"></i> Editar Professor'
        : '<i class="fas fa-user-plus"></i> Novo Professor';
    document.getElementById('btnSalvar').textContent = item ? 'Atualizar' : 'Salvar';
    (item?.disciplinas || []).forEach(id => {
        const opcao = document.querySelector(`input[name="disciplinas"][value="${id}"]`);
        if (opcao) opcao.checked = true;
    });
    document.getElementById('modal').classList.add('ativo');
    document.body.style.overflow = 'hidden';
}

function fecharModal() {
    document.getElementById('modal').classList.remove('ativo');
    document.body.style.overflow = '';
}

function editar(id) {
    const professor = Professores.find(item => String(item.id) === String(id));
    if (professor) abrirModal(professor);
}

async function salvar(event) {
    event.preventDefault();
    const id = document.getElementById('itemId').value;
    const dados = {
        nome: document.getElementById('nome').value.trim(),
        matricula: document.getElementById('matricula').value.trim(),
        cpf: document.getElementById('cpf').value.trim(),
        email: document.getElementById('email').value.trim(),
        disciplinas: [...document.querySelectorAll('input[name="disciplinas"]:checked')].map(input => input.value)
    };
    const csrfToken = await carregarTokenCsrf();
    const resposta = await fetch(id ? '/API/PostEditarProfessor' : '/API/PostProfessor',
        {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRF-Token": csrfToken,
        },
        credentials: 'same-origin',
        body: JSON.stringify(id ? { ...dados, id } : dados)
    });
    if (!resposta.ok) return showToast('Não foi possível salvar o professor.', 'error');
    fecharModal();
    await carregarProfessores();
    showToast(id ? 'Professor atualizado com sucesso!' : 'Professor cadastrado com sucesso!', 'success');
}

async function excluir(id) {
    const professor = Professores.find(item => String(item.id) === String(id));
    if (!professor || !confirm(`Tem certeza que deseja excluir "${professor.nome}"?`)) return;
    const resposta = await fetch(`/API/DeleteProfessor/${id}`, { method: 'DELETE', credentials: 'same-origin' });
    if (!resposta.ok) return showToast('Não foi possível excluir o professor.', 'error');
    await carregarProfessores();
    showToast('Professor excluído com sucesso!', 'success');
}

function showToast(message, type) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type || 'info'}`;
    toast.innerHTML = `<span>${message}</span><button onclick="this.parentElement.remove()">×</button>`;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

document.addEventListener('DOMContentLoaded', async () => {
    try { await Promise.all([carregarDisciplinas(), carregarProfessores()]); }
    catch (erro) { console.error(erro); showToast('Não foi possível carregar os dados.', 'error'); }
});
