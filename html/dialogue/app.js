(function () {
  // Modelo de dados
  const state = { nodes: {}, nextId: 1 };

  // Elementos do DOM
  const canvas = document.getElementById("canvas");
  const svg = document.getElementById("connections");
  const addNodeBtn = document.getElementById("addNodeBtn");
  const exportBtn = document.getElementById("exportBtn");
  const importInput = document.getElementById("importInput");
  const playBtn = document.getElementById("playBtn");
  const clearBtn = document.getElementById("clearBtn");

  const nodeIdField = document.getElementById("nodeId");
  const nodeTextField = document.getElementById("nodeText");
  const choicesList = document.getElementById("choicesList");
  const newChoiceText = document.getElementById("newChoiceText");
  const addChoiceBtn = document.getElementById("addChoiceBtn");
  const saveNodeBtn = document.getElementById("saveNodeBtn");
  const deleteNodeBtn = document.getElementById("deleteNodeBtn");

  const playModal = document.getElementById("playModal");
  const playArea = document.getElementById("playArea");
  const closePlayBtn = document.getElementById("closePlayBtn");

  let selectedNodeId = null;
  let dragInfo = null;

  // Utilities
  function makeId() {
    return "n" + state.nextId++;
  }
  function persist() {
    localStorage.setItem("branch_editor", JSON.stringify(state));
  }
  function loadPersist() {
    const raw = localStorage.getItem("branch_editor");
    if (raw) {
      try {
        const parsed = JSON.parse(raw);
        if (parsed && parsed.nodes) {
          Object.assign(state, parsed);
        }
      } catch (e) {}
    }
  }

  // DOM helpers
  function createNodeElement(node) {
    const el = document.createElement("div");
    el.className = "node";
    el.dataset.id = node.id;
    el.style.left = node.x + "px";
    el.style.top = node.y + "px";

    const header = document.createElement("div");
    header.className = "nodeHeader";
    header.textContent = node.id;
    const body = document.createElement("div");
    body.className = "nodeBody";
    body.textContent = node.text || "(sem texto)";

    el.appendChild(header);
    el.appendChild(body);

    // events
    header.addEventListener("mousedown", (ev) => startDrag(ev, el));
    el.addEventListener("click", (ev) => {
      ev.stopPropagation();
      selectNode(node.id);
    });

    return el;
  }

  function renderAll() {
    canvas.innerHTML = "";
    svg.innerHTML = "";
    for (const id in state.nodes) {
      const node = state.nodes[id];
      const el = createNodeElement(node);
      canvas.appendChild(el);
    }
    drawConnections();
  }

  function drawConnections() {
    svg.setAttribute("width", canvas.style.width || 2000);
    svg.setAttribute("height", canvas.style.height || 1200);
    svg.innerHTML = "";
    for (const id in state.nodes) {
      const node = state.nodes[id];
      node.choices.forEach((choice) => {
        const target = state.nodes[choice.target];
        if (!target) return;
        const from = getNodeCenter(id);
        const to = getNodeCenter(target.id);
        const path = document.createElementNS(
          "http://www.w3.org/2000/svg",
          "path"
        );
        const dx = to.x - from.x;
        const dy = to.y - from.y;
        const hx = from.x + dx * 0.5;
        const d = `M ${from.x} ${from.y} C ${hx} ${from.y} ${hx} ${to.y} ${to.x} ${to.y}`;
        path.setAttribute("d", d);
        path.setAttribute("stroke", "#06b6d4");
        path.setAttribute("fill", "none");
        path.setAttribute("stroke-width", "2");
        svg.appendChild(path);
      });
    }
  }

  function getNodeCenter(id) {
    const el = canvas.querySelector(`.node[data-id="${id}"]`);
    if (!el) return { x: 0, y: 0 };
    const rect = el.getBoundingClientRect();
    const canvasRect = canvas.getBoundingClientRect();
    return {
      x: rect.left - canvasRect.left + rect.width / 2,
      y: rect.top - canvasRect.top + rect.height / 2,
    };
  }

  // selection and editing
  function selectNode(id) {
    selectedNodeId = id;
    const node = state.nodes[id];
    nodeIdField.value = node.id;
    nodeTextField.value = node.text || "";
    renderChoicesList(node);
    highlightSelected();
  }

  function renderChoicesList(node) {
    choicesList.innerHTML = "";
    node.choices.forEach((c, idx) => {
      const li = document.createElement("li");
      li.className = "choiceItem";
      const txt = document.createElement("div");
      txt.innerHTML = `<strong>${c.text}</strong><br/><small>-> ${c.target}</small>`;
      const btns = document.createElement("div");
      const unlink = document.createElement("button");
      unlink.textContent = "Desvincular";
      unlink.addEventListener("click", () => {
        node.choices.splice(idx, 1);
        persist();
        renderAll();
        selectNode(node.id);
      });
      btns.appendChild(unlink);
      li.appendChild(txt);
      li.appendChild(btns);
      choicesList.appendChild(li);
    });
  }

  function highlightSelected() {
    canvas
      .querySelectorAll(".node")
      .forEach((el) => el.classList.remove("selected"));
    const el = canvas.querySelector(`.node[data-id="${selectedNodeId}"]`);
    if (el) el.classList.add("selected");
  }

  // drag
  function startDrag(ev, el) {
    ev.preventDefault();
    ev.stopPropagation();
    const id = el.dataset.id;
    const node = state.nodes[id];
    const startX = ev.clientX;
    const startY = ev.clientY;
    const origX = node.x;
    const origY = node.y;
    function onMove(e) {
      const nx = origX + (e.clientX - startX);
      const ny = origY + (e.clientY - startY);
      node.x = Math.max(0, nx);
      node.y = Math.max(0, ny);
      el.style.left = node.x + "px";
      el.style.top = node.y + "px";
      drawConnections();
    }
    function onUp() {
      document.removeEventListener("mousemove", onMove);
      document.removeEventListener("mouseup", onUp);
      persist();
    }
    document.addEventListener("mousemove", onMove);
    document.addEventListener("mouseup", onUp);
  }

  // actions
  addNodeBtn.addEventListener("click", () => {
    const id = makeId();
    const node = {
      id,
      x: 40 + Math.random() * 200,
      y: 40 + Math.random() * 120,
      text: "Novo nó",
      choices: [],
    };
    state.nodes[id] = node;
    persist();
    renderAll();
    selectNode(id);
  });

  saveNodeBtn.addEventListener("click", () => {
    if (!selectedNodeId) return;
    const node = state.nodes[selectedNodeId];
    node.text = nodeTextField.value;
    persist();
    renderAll();
    selectNode(selectedNodeId);
  });

  deleteNodeBtn.addEventListener("click", () => {
    if (!selectedNodeId) return;
    delete state.nodes[selectedNodeId];
    // remove references
    for (const k in state.nodes) {
      state.nodes[k].choices = state.nodes[k].choices.filter(
        (c) => c.target !== selectedNodeId
      );
    }
    selectedNodeId = null;
    persist();
    renderAll();
    nodeIdField.value = "";
    nodeTextField.value = "";
    choicesList.innerHTML = "";
  });

  addChoiceBtn.addEventListener("click", () => {
    if (!selectedNodeId) return;
    const text = newChoiceText.value.trim();
    if (!text) return alert("Escreve o texto da escolha");
    const targetId = makeId();
    // create target node
    const targetNode = {
      id: targetId,
      x: state.nodes[selectedNodeId].x + 260,
      y: state.nodes[selectedNodeId].y,
      text: "Novo nó (alvo)",
      choices: [],
    };
    state.nodes[targetId] = targetNode;
    state.nodes[selectedNodeId].choices.push({ text, target: targetId });
    newChoiceText.value = "";
    persist();
    renderAll();
    selectNode(selectedNodeId);
  });

  exportBtn.addEventListener("click", () => {
    const data = JSON.stringify(state, null, 2);
    const blob = new Blob([data], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "dialogue.json";
    a.click();
    URL.revokeObjectURL(url);
  });

  importInput.addEventListener("change", (ev) => {
    const f = ev.target.files[0];
    if (!f) return;
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const parsed = JSON.parse(reader.result);
        if (parsed && parsed.nodes) {
          Object.assign(state, parsed);
          renderAll();
          persist();
        } else alert("JSON inválido");
      } catch (e) {
        alert("Erro ao ler JSON");
      }
    };
    reader.readAsText(f);
  });

  clearBtn.addEventListener("click", () => {
    if (confirm("Limpar tudo?")) {
      state.nodes = {};
      state.nextId = 1;
      persist();
      renderAll();
    }
  });

  // click canvas to deselect
  canvas.addEventListener("click", () => {
    selectedNodeId = null;
    highlightSelected();
    nodeIdField.value = "";
    nodeTextField.value = "";
    choicesList.innerHTML = "";
  });

  // play preview
  playBtn.addEventListener("click", () => {
    playModal.classList.remove("hidden");
    playArea.innerHTML = "";
    const start = Object.keys(state.nodes)[0];
    if (!start) {
      playArea.textContent = "Sem nós para mostrar.";
      return;
    }
    showPlayNode(start);
  });
  closePlayBtn.addEventListener("click", () =>
    playModal.classList.add("hidden")
  );

  function showPlayNode(nodeId) {
    const node = state.nodes[nodeId];
    playArea.innerHTML = "";
    const p = document.createElement("div");
    p.textContent = node.text || "(sem texto)";
    playArea.appendChild(p);
    const ul = document.createElement("div");
    ul.style.marginTop = "12px";
    node.choices.forEach((c) => {
      const b = document.createElement("button");
      b.textContent = c.text;
      b.style.display = "block";
      b.style.marginTop = "6px";
      b.addEventListener("click", () => showPlayNode(c.target));
      ul.appendChild(b);
    });
    playArea.appendChild(ul);
  }

  // initial load
  loadPersist();
  renderAll();
})();
