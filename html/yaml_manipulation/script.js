// Seleção de elementos do DOM
const inputArquivo = document.getElementById("inputArquivo");
const textareaYaml = document.getElementById("textareaYamlBruto");
const botaoParsear = document.getElementById("botaoParsear");
const inputNovaChave = document.getElementById("inputNovaChave");
const inputNovoValor = document.getElementById("inputNovoValor");
const botaoAdicionar = document.getElementById("botaoAdicionar");
const corpoTabela = document.getElementById("corpoTabela");
const botaoDownload = document.getElementById("botaoDownload");
const spanMensagemErro = document.getElementById("spanMensagemErro");

// Objeto em memória que representa o YAML carregado
let objetoYaml = {};

// Opções para gerar YAML com fluxos inline e strings sempre entre aspas
const opcoesDumpYaml = {
  flowLevel: 1,
  styles: { "!!seq": "flow" },
  quotingType: '"',
  forceQuotes: true,
};

// 1. Importar arquivo YAML
inputArquivo.addEventListener("change", (evento) => {
  const arquivo = evento.target.files[0];
  if (!arquivo) return;

  spanMensagemErro.textContent = "";
  const leitor = new FileReader();

  leitor.onload = () => {
    textareaYaml.value = leitor.result;
  };
  leitor.onerror = () => {
    spanMensagemErro.textContent = "Erro ao ler o arquivo YAML.";
  };

  leitor.readAsText(arquivo);
});

// 2. Parsear YAML bruto e popular tabela
botaoParsear.addEventListener("click", () => {
  spanMensagemErro.textContent = "";
  try {
    const dados = jsyaml.load(textareaYaml.value);
    if (typeof dados !== "object" || Array.isArray(dados)) {
      throw new Error("O YAML deve ser um mapa de chave:valor.");
    }
    objetoYaml = dados;
    atualizarTabelaCRUD();
  } catch (erro) {
    spanMensagemErro.textContent = "Erro ao parsear YAML: " + erro.message;
  }
});

// 3. Atualiza a tabela HTML para exibir e editar cada par
function atualizarTabelaCRUD() {
  corpoTabela.innerHTML = "";

  Object.entries(objetoYaml).forEach(([chave, valor]) => {
    const linha = document.createElement("tr");

    // Coluna da chave
    const celulaChave = document.createElement("td");
    celulaChave.textContent = chave;
    linha.appendChild(celulaChave);

    // Coluna do valor (input)
    const celulaValor = document.createElement("td");
    const inputValor = document.createElement("input");
    inputValor.type = "text";
    inputValor.value =
      typeof valor === "object" ? JSON.stringify(valor) : String(valor);
    celulaValor.appendChild(inputValor);
    linha.appendChild(celulaValor);

    // Coluna de ações
    const celulaAcoes = document.createElement("td");

    // Botão Atualizar
    const botaoAtualizar = document.createElement("button");
    botaoAtualizar.textContent = "✏️ Atualizar";
    botaoAtualizar.onclick = () => {
      try {
        objetoYaml[chave] = jsyaml.load(inputValor.value);
      } catch {
        objetoYaml[chave] = inputValor.value;
      }
      atualizarTabelaCRUD();
      sincronizarTextarea();
    };
    celulaAcoes.appendChild(botaoAtualizar);

    // Botão Remover
    const botaoRemover = document.createElement("button");
    botaoRemover.textContent = "🗑️ Remover";
    botaoRemover.onclick = () => {
      delete objetoYaml[chave];
      atualizarTabelaCRUD();
      sincronizarTextarea();
    };
    celulaAcoes.appendChild(botaoRemover);

    linha.appendChild(celulaAcoes);
    corpoTabela.appendChild(linha);
  });

  // Após desenhar, atualiza o YAML bruto
  sincronizarTextarea();
}

// 4. Criar novo par chave:valor
botaoAdicionar.addEventListener("click", () => {
  const chave = inputNovaChave.value.trim();
  const raw = inputNovoValor.value.trim();

  if (!chave) {
    alert("Informe uma chave.");
    return;
  }
  if (chave in objetoYaml) {
    alert("Essa chave já existe.");
    return;
  }

  try {
    objetoYaml[chave] = jsyaml.load(raw);
  } catch {
    objetoYaml[chave] = raw;
  }

  inputNovaChave.value = "";
  inputNovoValor.value = "";
  atualizarTabelaCRUD();
});

// Sincroniza o textarea com o objeto em memória
function sincronizarTextarea() {
  textareaYaml.value = jsyaml.dump(objetoYaml, opcoesDumpYaml);
}

// 5. Baixar (download) o YAML atualizado
botaoDownload.addEventListener("click", () => {
  sincronizarTextarea();
  const blob = new Blob([textareaYaml.value], { type: "text/yaml" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "data.yaml";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(link.href);
});

// Inicialização: desenhar tabela vazia
atualizarTabelaCRUD();
