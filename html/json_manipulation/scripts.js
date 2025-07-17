// 1. Seleção de elementos do DOM
const txtJsonBruto = document.getElementById("rawJson");
const btnCarregar = document.getElementById("btnLoad");
const lblMensagem = document.getElementById("message");
const corpoTabela = document.getElementById("jsonTable");
const txtChaveNova = document.getElementById("newKey");
const txtValorNovo = document.getElementById("newValue");
const btnAdicionar = document.getElementById("btnAdd");
const btnExportar = document.getElementById("btnExport");

// 2. Objeto que armazena o JSON em memória
let objetoJson = {};

// 3. Função para carregar arquivo JSON via fetch
async function carregarArquivoJson() {
  lblMensagem.textContent = "";
  try {
    const resposta = await fetch("arquivo.json");
    if (!resposta.ok) throw new Error("HTTP " + resposta.status);
    objetoJson = await resposta.json();
    atualizarTabela();
  } catch (erro) {
    lblMensagem.textContent = "Erro ao carregar JSON: " + erro.message;
  }
}

// 4. Função para desenhar a tabela a partir de objetoJson
function atualizarTabela() {
  corpoTabela.innerHTML = ""; // limpa conteúdo

  Object.entries(objetoJson).forEach(([chave, valor]) => {
    const linha = document.createElement("tr");

    // Coluna da chave
    const celChave = document.createElement("td");
    celChave.textContent = chave;
    linha.appendChild(celChave);

    // Coluna do valor (input editável)
    const celValor = document.createElement("td");
    const inpValor = document.createElement("input");
    inpValor.type = "text";
    inpValor.value = JSON.stringify(valor);
    celValor.appendChild(inpValor);
    linha.appendChild(celValor);

    // Coluna de ações
    const celAcoes = document.createElement("td");

    // Botão Atualizar (Update)
    const btnAtualizar = document.createElement("button");
    btnAtualizar.textContent = "Atualizar";
    btnAtualizar.onclick = () => {
      const txt = inpValor.value.trim();
      try {
        objetoJson[chave] = JSON.parse(txt);
      } catch {
        objetoJson[chave] = txt;
      }
      atualizarTabela();
    };
    celAcoes.appendChild(btnAtualizar);

    // Botão Remover (Delete)
    const btnRemover = document.createElement("button");
    btnRemover.textContent = "Remover";
    btnRemover.onclick = () => {
      delete objetoJson[chave];
      atualizarTabela();
    };
    celAcoes.appendChild(btnRemover);

    linha.appendChild(celAcoes);
    corpoTabela.appendChild(linha);
  });
}

// 5. Evento: carregar JSON bruto manualmente (textarea → objetoJson)
btnCarregar.addEventListener("click", () => {
  lblMensagem.textContent = "";
  try {
    const texto = txtJsonBruto.value;
    const parsed = JSON.parse(texto);
    if (typeof parsed !== "object" || Array.isArray(parsed)) {
      throw new Error("JSON precisa ser um objeto {chave:valor}");
    }
    objetoJson = parsed;
    atualizarTabela();
  } catch (erro) {
    lblMensagem.textContent = "Erro ao ler JSON: " + erro.message;
  }
});

// 6. Evento: adicionar nova chave/valor (Create)
btnAdicionar.addEventListener("click", () => {
  const chave = txtChaveNova.value.trim();
  const entrada = txtValorNovo.value.trim();

  if (!chave) {
    alert("Informe uma chave.");
    return;
  }
  if (chave in objetoJson) {
    alert("Chave já existe.");
    return;
  }

  let valorFinal;
  try {
    valorFinal = JSON.parse(entrada);
  } catch {
    valorFinal = entrada;
  }

  objetoJson[chave] = valorFinal;
  txtChaveNova.value = "";
  txtValorNovo.value = "";
  atualizarTabela();
});

// 7. Evento: exportar para textarea + download do arquivo JSON
btnExportar.addEventListener("click", () => {
  const jsonFormatado = JSON.stringify(objetoJson, null, 2);

  // 7.1 → Atualiza textarea
  txtJsonBruto.value = jsonFormatado;

  // 7.2 → Gera download
  const blob = new Blob([jsonFormatado], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const baixable = document.createElement("baixable");
  baixable.href = url;
  baixable.download = "arquivo.json";
  document.body.appendChild(baixable);
  baixable.click();
  document.body.removeChild(baixable);
  URL.revokeObjectURL(url);

  alert("JSON exportado reniciando a pagina...");
});

// 8. Inicialização: carrega JSON do arquivo e desenha tabela
carregarArquivoJson();
