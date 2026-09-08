let alunos = [];
let turmas = [];
let nextId = 1;

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function carregarTokenCsrf() {
    const resposta = await fetch('/get-token', {
        credentials: 'same-origin',
        cache: 'no-store'
    });
    if (!resposta.ok) throw new Error('Não foi possível obter o token CSRF');
    return resposta.headers.get('X-CSRF-Token');
}

async function carregarTurmas() {
    try {
        const resposta = await fetch('/API/GetTurmas', {
            credentials: 'same-origin'
        });
        if (!resposta.ok) {
            throw new Error('Resposta inválida da API');
        }

        const dados = await resposta.json();
        turmas = Array.isArray(dados) ? dados : [];
    } catch (erro) {
        console.error('Falha ao carregar turmas!', erro);
        turmas = [];
    }

    const selectTurma = document.getElementById('Select-turma');
    if (selectTurma) {
        selectTurma.innerHTML = '<option value="">Selecione uma turma</option>';
        turmas.forEach(turma => {
            const option = document.createElement('option');
            option.value = turma.nome;
            option.textContent = turma.nome;
            selectTurma.appendChild(option);
        });
    }
}

async function carregarAlunos() {
    try {
        const resposta = await fetch('/API/GetAlunos', {
            credentials: 'same-origin'
        });

        if (!resposta.ok) {
            throw new Error('Resposta inválida da API');
        }

        const dados = await resposta.json();
        alunos = Array.isArray(dados) ? dados : [];
        renderizarAlunos(alunos);
        return alunos;
    } catch (erro) {
        console.error('Falha ao carregar alunos!', erro);
        alunos = [];
        renderizarAlunos(alunos);
        return [];
    }
}

function renderizarAlunos(lista) {
    var tbody = document.getElementById('tableBody');
    var dados = Array.isArray(lista) ? lista : alunos;

    if (!Array.isArray(dados) || dados.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="empty-state">
                    <i class="fas fa-user-slash"></i>
                    <p>Nenhum aluno encontrado</p>
                    <button class="btn-primary" onclick="abrirModal()">
                        <i class="fas fa-plus"></i> Adicionar
                    </button>
                </td>
            </tr>
        `;
        var totalEl = document.getElementById('totalRegistros');
        if (totalEl) totalEl.textContent = '0 alunos';
        return;
    }

    var html = '';
    for (var i = 0; i < dados.length; i++) {
        var a = dados[i];
        var statusClass = a.status === 'Ativo' || a.status === 'ativo/a' ? 'ativo' : a.status === 'Pendente' || a.status === 'indefinido/a' ? 'pendente' : 'inativo';
        html += `
            <tr>
                <td id='idAluno'>${a.id}</td>
                <td><strong>${a.nome}</strong></td>
                <td>${a.matricula}</td>
                <td>${a.cpf}</td>
                <td>${a.turma || '-'}</td>
                <td><span class="status-badge ${statusClass}">${a.status}</span></td>
                <td>
                    <button class="action-btn view" onclick="visualizarAluno('${a.id}')" title="Visualizar"><i class="fas fa-eye"></i></button>
                    <button class="action-btn edit" onclick="editarAluno('${a.id}')" title="Editar"><i class="fas fa-edit"></i></button>
                    <button class="action-btn delete" onclick="excluirAluno('${a.id}')" title="Excluir"><i class="fas fa-trash"></i></button>
                </td>
            </tr>
        `;
    }
    tbody.innerHTML = html;

    var totalEl = document.getElementById('totalRegistros');
    if (totalEl) totalEl.textContent = dados.length + ' alunos';
}

function visualizarAluno(id) {
    var aluno = alunos.find(a => String(a.id) === String(id));
    if (!aluno) {
        alert('Aluno não encontrado!');
        return;
    }
    window.location.href = '/Aluno/' + String(aluno.id);
}

function filtrar() {
    var search = document.getElementById('searchInput').value.toLowerCase();
    var status = document.getElementById('filterStatus').value;

    var filtrados = [];
    for (var i = 0; i < alunos.length; i++) {
        var a = alunos[i];
        var matchSearch = (a.nome || '').toLowerCase().includes(search) || (a.matricula || '').includes(search) || (a.cpf || '').includes(search);
        var matchStatus = status === '' || a.status === status;
        if (matchSearch && matchStatus) {
            filtrados.push(a);
        }
    }

    renderizarAlunos(filtrados);
}

function limparFiltros() {
    document.getElementById('searchInput').value = '';
    document.getElementById('filterStatus').value = '';
    renderizarAlunos(alunos);
}

function editarAluno(id) {
    var aluno = null;
    for (var i = 0; i < alunos.length; i++) {
        if (String(alunos[i].id) === String(id)) {
            aluno = alunos[i];
            break;
        }
    }
    if (!aluno) return;

    document.getElementById('modalTitle').innerHTML = '<i class="fas fa-user-edit"></i> Editar Aluno';
    document.getElementById('btnSalvar').textContent = 'Atualizar';
    document.getElementById('itemId').value = aluno.id;
    document.getElementById('nome').value = aluno.nome;
    document.getElementById('matricula').value = aluno.matricula;
    document.getElementById('cpf').value = aluno.cpf;
    document.getElementById('Select-turma').value = aluno.turma || '';
    document.getElementById('status').value = aluno.status;
    document.getElementById('email').value = aluno.email || '';

    document.getElementById('modal').classList.add('ativo');
    document.body.style.overflow = 'hidden';
}

function abrirModal() {
    document.getElementById('modalTitle').innerHTML = '<i class="fas fa-user-plus"></i> Novo Aluno';
    document.getElementById('btnSalvar').textContent = 'Salvar';
    document.getElementById('form').reset();
    document.getElementById('itemId').value = '';
    document.getElementById('status').value = 'Ativo';

    document.getElementById('modal').classList.add('ativo');
    document.body.style.overflow = 'hidden';
}

function fecharModal() {
    document.getElementById('modal').classList.remove('ativo');
    document.body.style.overflow = '';
}

async function salvar(event) {
    event.preventDefault();

    var dados = {
        id: document.getElementById('itemId').value || null,
        nome: document.getElementById('nome').value.trim(),
        matricula: document.getElementById('matricula').value.trim(),
        cpf: document.getElementById('cpf').value.trim(),
        turma: document.getElementById('Select-turma').value,
        status: document.getElementById('status').value,
        email: document.getElementById('email').value.trim(),
    };
    const csrfToken = await carregarTokenCsrf();
    var endpoint = dados.id ? '/API/PostEditarAluno' : '/API/PostAluno';

    fetch(endpoint, {
        method: 'POST',
        headers: {
            "X-CSRF-Token": csrfToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dados)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao salvar aluno');
        }
        return response.json();
    })
    .then(async data => {
        showToast('Aluno "' + data.nome + '" salvo com sucesso!', 'success');
        await carregarAlunos();
        fecharModal();
    })
    .catch(error => {
        console.error('Erro ao salvar aluno:', error);
    });
}

async function excluirAluno(id) {
    var aluno = null;
    for (var i = 0; i < alunos.length; i++) {
        if (alunos[i].id === id) {
            aluno = alunos[i];
            break;
        }
    }
    if (!aluno) return;
    if (confirm('Tem certeza que deseja excluir "' + aluno.nome + '"?')) {
        const csrfToken = await carregarTokenCsrf();
        fetch('/API/DeleteAluno/' + id, {
            method: 'DELETE',
            headers: {
                "X-CSRF-Token": csrfToken,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao excluir aluno');
            }
            return response.json();
        })
        .then(async data => {
            await carregarAlunos();
            showToast('Aluno "' + aluno.nome + '" excluído', 'error');
        })
        .catch(error => {
            console.error('Erro ao excluir aluno:', error);
        });
    }
}

function showToast(message, type) {
    var container = document.getElementById('toast-container');
    if (!container) return;
    var toast = document.createElement('div');
    toast.className = 'toast toast-' + (type || 'info');
    toast.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" style="background:none;border:none;font-size:18px;cursor:pointer;color:#999;">×</button>
    `;
    container.appendChild(toast);
    setTimeout(function () { toast.remove(); }, 4000);
}

document.addEventListener('DOMContentLoaded', function () {
    carregarTurmas();
    carregarAlunos();
});