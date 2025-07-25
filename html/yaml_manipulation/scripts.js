// 1) Seleção de elementos do DOM
const textareaYamlBruto = document.getElementById("rawYaml");
const botaoCarregarYaml = document.getElementById("btnLoad");
const labelMensagemErro = document.getElementById("message");
const corpoTabelaYaml = document.getElementById("yamlTable");
const inputNovaChave = document.getElementById("newKey");
const inputNovoValor = document.getElementById("newValue");
const botaoAdicionarPar = document.getElementById("btnAdd");
const botaoExportarYaml = document.getElementById("btnExport");

// 2) Objeto em memória que guarda o YAML parseado
let objetoYamlEmMemoria = {};

// 3) Opções comuns para gerar o YAML com arrays inline e strings sempre entre aspas
const yamlDumpOptions = {
  flowLevel: 1, // Sequências a partir do nível 1 em estilo [a, b, c]
  styles: { "!!seq": "flow" },
  quotingType: '"', // Usa aspas duplas
  forceQuotes: true, // Força aspas em todos os valores de string
};

// 4) Evento: carrega e parseia o YAML da textarea
botaoCarregarYaml.addEventListener("click", () => {
  labelMensagemErro.textContent = "";
  try {
    const textoYaml = textareaYamlBruto.value;
    const parsedYaml = jsyaml.load(textoYaml);
    if (typeof parsedYaml !== "object" || Array.isArray(parsedYaml)) {
      throw new Error("YAML deve ser um mapa (chave: valor).");
    }
    objetoYamlEmMemoria = parsedYaml;
    atualizarTabelaYaml();
    sincronizarTextareaComObjeto();
  } catch (erro) {
    labelMensagemErro.textContent = `Erro ao carregar YAML: ${erro.message}`;
  }
});

// 5) Função que renderiza a tabela HTML a partir de objetoYamlEmMemoria
function atualizarTabelaYaml() {
  corpoTabelaYaml.innerHTML = "";

  Object.entries(objetoYamlEmMemoria).forEach(([chave, valor]) => {
    const linhaTabela = document.createElement("tr");

    // Coluna: chave
    const celulaChave = document.createElement("td");
    celulaChave.textContent = chave;
    linhaTabela.appendChild(celulaChave);

    // Coluna: valor
    const celulaValor = document.createElement("td");
    const inputValor = document.createElement("input");
    inputValor.type = "text";
    inputValor.value =
      typeof valor === "object" ? JSON.stringify(valor) : String(valor);
    celulaValor.appendChild(inputValor);
    linhaTabela.appendChild(celulaValor);

    // Coluna: ações (atualizar / remover)
    const celulaAcoes = document.createElement("td");

    // Botão: atualizar valor
    const botaoAtualizar = document.createElement("button");
    botaoAtualizar.textContent = "✏️ Atualizar";
    botaoAtualizar.onclick = () => {
      const textoEntrada = inputValor.value.trim();
      try {
        objetoYamlEmMemoria[chave] = jsyaml.load(textoEntrada);
      } catch {
        objetoYamlEmMemoria[chave] = textoEntrada;
      }
      atualizarTabelaYaml();
      sincronizarTextareaComObjeto();
    };
    celulaAcoes.appendChild(botaoAtualizar);

    // Botão: remover par
    const botaoRemover = document.createElement("button");
    botaoRemover.textContent = "🗑️ Remover";
    botaoRemover.onclick = () => {
      delete objetoYamlEmMemoria[chave];
      atualizarTabelaYaml();
      sincronizarTextareaComObjeto();
    };
    celulaAcoes.appendChild(botaoRemover);

    linhaTabela.appendChild(celulaAcoes);
    corpoTabelaYaml.appendChild(linhaTabela);
  });
}

// 6) Evento: adicionar um novo par chave/valor
botaoAdicionarPar.addEventListener("click", () => {
  const novaChave = inputNovaChave.value.trim();
  const valorBruto = inputNovoValor.value.trim();

  if (!novaChave) {
    alert("Informe uma chave.");
    return;
  }
  if (novaChave in objetoYamlEmMemoria) {
    alert("Chave já existe.");
    return;
  }

  try {
    objetoYamlEmMemoria[novaChave] = jsyaml.load(valorBruto);
  } catch {
    objetoYamlEmMemoria[novaChave] = valorBruto;
  }
  inputNovaChave.value = "";
  inputNovoValor.value = "";
  atualizarTabelaYaml();
  sincronizarTextareaComObjeto();
});

// 7) Evento: exportar o objeto para YAML e iniciar download
botaoExportarYaml.addEventListener("click", () => {
  sincronizarTextareaComObjeto();

  const yamlString = jsyaml.dump(objetoYamlEmMemoria, yamlDumpOptions);
  const arquivoBlob = new Blob([yamlString], { type: "text/yaml" });
  const linkDownload = document.createElement("a");
  linkDownload.href = URL.createObjectURL(arquivoBlob);
  linkDownload.download = "data.yaml";
  document.body.appendChild(linkDownload);
  linkDownload.click();
  document.body.removeChild(linkDownload);
  URL.revokeObjectURL(linkDownload.href);

  alert("YAML exportado com sucesso!");
});

// 8) Função auxiliar: atualiza a textarea com o objeto em memória
function sincronizarTextareaComObjeto() {
  const yamlParaTextarea = jsyaml.dump(objetoYamlEmMemoria, yamlDumpOptions);
  textareaYamlBruto.value = yamlParaTextarea;
}

// 9) Inicialização: renderiza tabela vazia e sincroniza textarea
atualizarTabelaYaml();
sincronizarTextareaComObjeto();
