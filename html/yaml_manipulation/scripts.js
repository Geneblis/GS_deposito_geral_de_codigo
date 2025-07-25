// 1) Seleção de elementos
const txtYaml = document.getElementById("rawYaml");
const btnLoad = document.getElementById("btnLoad");
const lblMessage = document.getElementById("message");
const tbody = document.getElementById("yamlTable");
const inpKey = document.getElementById("newKey");
const inpValue = document.getElementById("newValue");
const btnAdd = document.getElementById("btnAdd");
const btnExport = document.getElementById("btnExport");

// 2) Objeto em memória
let dataObj = {};

// 3) Carrega YAML da textarea
btnLoad.addEventListener("click", () => {
  lblMessage.textContent = "";
  try {
    const texto = txtYaml.value;
    const parsed = jsyaml.load(texto);
    if (typeof parsed !== "object" || Array.isArray(parsed)) {
      throw new Error("YAML deve ser um mapa (chave: valor).");
    }
    dataObj = parsed;
    renderTable();
  } catch (e) {
    lblMessage.textContent = `Erro ao carregar YAML: ${e.message}`;
  }
});

// 4) Renderiza a tabela
function renderTable() {
  tbody.innerHTML = "";
  Object.entries(dataObj).forEach(([key, val]) => {
    const tr = document.createElement("tr");

    // coluna chave
    const tdK = document.createElement("td");
    tdK.textContent = key;
    tr.appendChild(tdK);

    // coluna valor
    const tdV = document.createElement("td");
    const inpV = document.createElement("input");
    inpV.type = "text";
    inpV.value = typeof val === "object" ? JSON.stringify(val) : String(val);
    tdV.appendChild(inpV);
    tr.appendChild(tdV);

    // coluna ações
    const tdA = document.createElement("td");

    // botão atualizar
    const btnU = document.createElement("button");
    btnU.textContent = "✏️";
    btnU.onclick = () => {
      let raw = inpV.value.trim();
      try {
        dataObj[key] = jsyaml.load(raw);
      } catch {
        dataObj[key] = raw;
      }
      renderTable();

      // atualiza o YAML cru
      const novoYaml = jsyaml.dump(dataObj, {
        flowLevel: 1,
        styles: { "!!seq": "flow" },
      });
      txtYaml.value = novoYaml;
    };
    tdA.appendChild(btnU);

    // botão remover
    const btnD = document.createElement("button");
    btnD.textContent = "🗑️";
    btnD.onclick = () => {
      delete dataObj[key];
      renderTable();
      // também atualizar textarea:
      txtYaml.value = jsyaml.dump(dataObj, {
        flowLevel: 1,
        styles: { "!!seq": "flow" },
      });
    };
    tdA.appendChild(btnD);

    tr.appendChild(tdA);
    tbody.appendChild(tr);
  });
}

// 5) Adicionar novo par
btnAdd.addEventListener("click", () => {
  const key = inpKey.value.trim();
  const raw = inpValue.value.trim();
  if (!key) {
    alert("Informe uma chave.");
    return;
  }
  if (key in dataObj) {
    alert("Chave já existe.");
    return;
  }

  try {
    dataObj[key] = jsyaml.load(raw);
  } catch {
    dataObj[key] = raw;
  }
  inpKey.value = "";
  inpValue.value = "";
  renderTable();
});

// 6) Exportar para YAML + download
btnExport.addEventListener("click", () => {
  // 6.1 Atualiza textarea
  const yamlStr = jsyaml.dump(dataObj, {
    flowLevel: 1,
    styles: { "!!seq": "flow" },
  });
  console.log(yamlStr);
  txtYaml.value = yamlStr;

  // 6.2 Gera download
  const blob = new Blob([yamlStr], { type: "text/yaml" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "data.yaml";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(a.href);

  alert("YAML exportado com sucesso!");
});

// 7) Inicialização
renderTable(); // tabela vazia ao carregar
