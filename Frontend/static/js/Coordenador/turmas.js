let turmas = [];
let cursos = [];
let nextId = 1;

async function carregarCursos() {
    try {
        const resposta = await fetch('/API/GetCursos', {
            credentials: 'same-origin'
        });

        if (!resposta.ok) {
            throw new Error('Resposta inválida da API');
        }

        const dados = await resposta.json();
        cursos = Array.isArray(dados) ? dados : [];
        return cursos;
    } catch (erro) {
        console.error('Falha ao carregar cursos!', erro);
        cursos = [];
        return [];
    }
}

async function renderizarCursos() {
    const selectCurso = document.getElementById('filterCurso');
    if (!selectCurso) {
        console.error('Elemento selectCurso não encontrado!');
        return;
    }

    const selectCursoModal = document.getElementById('curso');
    if (!selectCursoModal) {
        console.error('Elemento selectCursoModal não encontrado!');
        return;
    }


    for (const curso of cursos) {
        const option = document.createElement('option');
        option.value = curso.nome;
        option.textContent = curso.nome;
        selectCurso.appendChild(option);
        selectCursoModal.appendChild(option.cloneNode(true));
    }
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
        renderizarTurmas(turmas);
        return turmas;
    } catch (erro) {
        console.error('Falha ao carregar turmas!', erro);
        turmas = [];
        renderizarTurmas(turmas);
        return [];
    }
}

async function carregarTokenCsrf() {
    const resposta = await fetch('/get-token', {
        credentials: 'same-origin',
        cache: 'no-store'
    });
    if (!resposta.ok) throw new Error('Não foi possível obter o token CSRF');
    return resposta.headers.get('X-CSRF-Token');
}

function renderizarTurmas(lista) {
    const tbody = document.getElementById('tableBody');
    const dadosFiltrados = Array.isArray(lista) ? lista : turmas;

    if (!tbody) {
        console.error('tableBody não encontrado!');
        return;
    }

    if (!Array.isArray(dadosFiltrados) || dadosFiltrados.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="empty-state"><i class="fas fa-door-open"></i><p>Nenhuma turma encontrada</p><button class="btn-primary" onclick="abrirModal()"><i class="fas fa-plus"></i> Adicionar</button></td></tr>`;
        const totalEl = document.getElementById('totalRegistros');
        if (totalEl) totalEl.textContent = '0 turmas';
        return;
    }

    tbody.innerHTML = dadosFiltrados.map(item => {
        return `<tr>
            <td>${item.id}</td>
            <td><strong>${item.nome}</strong></td>
            <td>${item.curso}</td>
            <td>${item.periodo}</td>
            <td>${item.alunos}</td>
            <td>${item.ano}</td>
            <td>
                <button class="action-btn view" onclick="visualizar('${item.id}')"><i class="fas fa-eye"></i></button>
                <button class="action-btn edit" onclick="editar('${item.id}')"><i class="fas fa-edit"></i></button>
                <button class="action-btn delete" onclick="excluir('${item.id}')"><i class="fas fa-trash"></i></button>
            </td>
        </tr>`;
    }).join('');

    const totalEl = document.getElementById('totalRegistros');
    if (totalEl) totalEl.textContent = dadosFiltrados.length + ' turmas';
}

function filtrar() {
    const search = document.getElementById('searchInput').value.toLowerCase();
    const curso = document.getElementById('filterCurso').value;
    const periodo = document.getElementById('filterPeriodo').value;

    const filtrados = turmas.filter(item => {
        const nome = (item.nome || '').toLowerCase();
        const cursoItem = (item.curso || '').toLowerCase();
        const matchSearch = nome.includes(search) || cursoItem.includes(search);
        const matchCurso = curso === '' || item.curso === curso;
        const matchPeriodo = periodo === '' || item.periodo === periodo;
        return matchSearch && matchCurso && matchPeriodo;
    });

    renderizarTurmas(filtrados);
}

function limparFiltros() {
    document.getElementById('searchInput').value = '';
    document.getElementById('filterCurso').value = '';
    document.getElementById('filterPeriodo').value = '';
    renderizarTurmas(turmas);
}

function visualizar(id) {
    var turma = turmas.find(t => String(t.id) === String(id));
    if (!turma) {
        alert('Turma não encontrada!');
        return;
    }
    window.location.href = '/Turma/' + String(turma.id);
}

function abrirModal(item) {
    const modal = document.getElementById('modal');
    const title = document.getElementById('modalTitle');
    const btn = document.getElementById('btnSalvar');

    if (item) {
        title.innerHTML = '<i class="fas fa-edit"></i> Editar Turma';
        btn.textContent = 'Atualizar';
        document.getElementById('itemId').value = item.id;
        document.getElementById('nome').value = item.nome;
        document.getElementById('curso').value = item.curso;
        document.getElementById('periodo').value = item.periodo;
        document.getElementById('ano').value = item.ano;
    } else {
        title.innerHTML = '<i class="fas fa-door-open"></i> Nova Turma';
        btn.textContent = 'Salvar';
        document.getElementById('form').reset();
        document.getElementById('itemId').value = '';
        document.getElementById('ano').value = 2026;
    }

    modal.classList.add('ativo');
    document.body.style.overflow = 'hidden';
}

function fecharModal() {
    const modal = document.getElementById('modal');
    if (modal) modal.classList.remove('ativo');
    document.body.style.overflow = '';
}

function editar(id) {
    const item = turmas.find(item => String(item.id) === String(id));
    if (item) abrirModal(item);
}

async function salvar(event) {
    event.preventDefault();
    const dados = {
        id: document.getElementById('itemId').value || null,
        nome: document.getElementById('nome').value.trim(),
        curso: document.getElementById('curso').value,
        periodo: document.getElementById('periodo').value,
        ano: parseInt(document.getElementById('ano').value),
    };

    const csrfToken = await carregarTokenCsrf();
    var endpoint = dados.id ? '/API/PostEditarTurma' : '/API/PostTurma';

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
            throw new Error('Erro ao salvar turma');
        }
        return response.json();
    })
    .then(async data => {
        showToast('Turma "' + data.nome + '" salva com sucesso!', 'success');
        await carregarTurmas();
        fecharModal();
    })
    .catch(error => {
        console.error('Erro ao salvar turma:', error);
    });
}

async function excluir(id) {
    var turma = null;
    for (var i = 0; i < turmas.length; i++) {
        if (turmas[i].id === id) {
            turma = turmas[i];
            break;
        }
    }
    if (confirm('Tem certeza que deseja excluir "' + turma.nome + '"?')) {
        const csrfToken = await carregarTokenCsrf();
        fetch('/API/DeleteTurma/' + id, {
            method: 'DELETE',
            headers: {
                "X-CSRF-Token": csrfToken,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                showToast('Erro ao excluir turma. Verifique se a turma possui alunos cadastrados nela.', 'error');
                throw new Error('Erro ao excluir turma');
            }
            return response.json();
        })
        .then(async data => {
            await carregarTurmas();
            showToast('Turma "' + turma.nome + '" excluída', 'error');
        })
        .catch(error => {
            console.error('Erro ao excluir turma:', error);
        });
    }
}

function showToast(message, type) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast toast-' + (type || 'info');
    toast.innerHTML = `<span>${message}</span><button onclick="this.parentElement.remove()" style="background:none;border:none;font-size:18px;cursor:pointer;color:#999;">×</button>`;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

document.addEventListener('DOMContentLoaded', function () {
    carregarTurmas();
    carregarCursos().then(renderizarCursos);
});