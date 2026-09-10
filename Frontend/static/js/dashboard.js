const contAlunos = document.getElementById("contagemAlunos");
const contProfessores = document.getElementById("contagemProfessores");
const contDisciplinas = document.getElementById("contagemDisciplinas");
const contTurmas = document.getElementById("contagemTurmas");
const ultimasMatriculas = document.getElementById("ultimasMatriculas");

function atualizarContagens() {
    fetch("/API/GetAlunosCount")
        .then(response => response.json())
        .then(data => {
            contAlunos.textContent = data;
        });
    fetch("/API/GetProfessoresCount")
        .then(response => response.json())
        .then(data => {
            contProfessores.textContent = data;
        });
    fetch("/API/GetDisciplinasCount")
        .then(response => response.json())
        .then(data => {
            contDisciplinas.textContent = data;
        });
    fetch("/API/GetTurmasCount")
        .then(response => response.json())
        .then(data => {
            contTurmas.textContent = data;
        });
}

function listarUltimasMatriculas() {
    fetch("/API/GetUltimosAlunos")
        .then(response => response.json())
        .then(data => {
            ultimasMatriculas.innerHTML = "";
            data.forEach(matricula => {
                const tr = document.createElement("tr");
                Object.values(matricula).forEach(valor => {
                    const td = document.createElement("td");
                    td.textContent = valor ?? "";
                    tr.appendChild(td);
                });
                ultimasMatriculas.appendChild(tr);
            });
        })
}

window.addEventListener("load", () => {
    atualizarContagens();
    listarUltimasMatriculas();
});