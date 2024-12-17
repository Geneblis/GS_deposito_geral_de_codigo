function adicionarBotoesFechar() {
    document.querySelectorAll("li").forEach((item) => {
        if (!item.querySelector(".fechar")) {
            const span = document.createElement("span");
            span.className = "fechar";
            span.textContent = "\u00D7";
            span.onclick = function () {
                this.parentElement.style.display = "none";
            };
            item.appendChild(span);
        }
    });
}

// Ao clicar em um item da lista trocar a classe para checked
document.querySelector('ul').addEventListener('click', (ev) => {
    if (ev.target.tagName === 'LI') {
        ev.target.classList.toggle('checked');
    }
});
function adicionarNovoElemento() {
    const inputValor = document.getElementById("afazeres").value.trim();
    if (inputValor === '') {
        alert("Você precisa escrever algo!");
        return;
    }

    const li = document.createElement("li");
    li.textContent = inputValor;
    document.getElementById("meusAfazeres").appendChild(li);

    document.getElementById("afazeres").value = ""; // Limpa o input

    adicionarBotoesFechar();
}
adicionarBotoesFechar();
