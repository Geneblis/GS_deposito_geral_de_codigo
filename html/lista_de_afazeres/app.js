const STORAGE_KEY = "planner_todo_data_v1";

const state = {
  todos: [],
  notes: [],
  settings: { autosave: true },
};

const tabs = document.querySelectorAll(".tab-btn");
const tabPanels = document.querySelectorAll(".tab-panel");

const todoListElement = document.getElementById("todoList");
const noteListElement = document.getElementById("noteList");

const modalTodo = document.getElementById("modalTodo");
const modalNote = document.getElementById("modalNote");

const openAddTodoBtn = document.getElementById("openAddTodo");
const saveTodoBtn = document.getElementById("saveTodo");
const cancelTodoBtn = document.getElementById("cancelTodo");

const openAddNoteBtn = document.getElementById("openAddNote");
const saveNoteBtn = document.getElementById("saveNote");
const cancelNoteBtn = document.getElementById("cancelNote");

const autosaveToggle = document.getElementById("autosaveToggle");
const clearRemovedBtn = document.getElementById("clearRemoved");

const todoTitleInput = document.getElementById("todoTitle");
const todoDescriptionInput = document.getElementById("todoDescription");
const checklistItemsList = document.getElementById("checklistItems");
const newChecklistTextInput = document.getElementById("newChecklistText");
const addChecklistItemBtn = document.getElementById("addChecklistItem");
const modalTodoTitle = document.getElementById("modalTodoTitle");

const noteFormDate = document.getElementById("noteFormDate");
const noteTitleInput = document.getElementById("noteTitle");
const noteContentInput = document.getElementById("noteContent");
const modalNoteTitleEl = document.getElementById("modalNoteTitle");
const noteDateInput = document.getElementById("noteDate");

let currentEditingTodoId = null;
let modalChecklist = [];
let currentEditingNoteId = null;

function generateId(prefix) {
  prefix = prefix || "";
  return (
    prefix +
    Date.now().toString(36) +
    Math.floor(Math.random() * 1000).toString(36)
  );
}

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    const parsed = JSON.parse(raw);
    if (parsed.todos) state.todos = parsed.todos;
    if (parsed.notes) state.notes = parsed.notes;
    if (parsed.settings) state.settings = parsed.settings;
  } catch (e) {
    console.error("loadState", e);
  }
}

function saveState() {
  try {
    if (!state.settings.autosave) return;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (e) {
    console.error("saveState", e);
  }
}

function switchTab(tabName) {
  tabs.forEach(function (btn) {
    if (btn.dataset.tab === tabName) btn.classList.add("active");
    else btn.classList.remove("active");
  });
  tabPanels.forEach(function (panel) {
    if (panel.id === "tab-" + tabName) panel.classList.add("active");
    else panel.classList.remove("active");
  });
}

function clearElement(el) {
  while (el.firstChild) el.removeChild(el.firstChild);
}

function openTodoModal(todoId) {
  currentEditingTodoId = todoId || null;
  modalChecklist = [];
  todoTitleInput.value = "";
  todoDescriptionInput.value = "";
  checklistItemsList.innerHTML = "";
  modalTodoTitle.textContent = todoId ? "Editar tarefa" : "Adicionar tarefa";
  if (todoId) {
    var t = state.todos.find(function (x) {
      return x.id === todoId;
    });
    if (t) {
      todoTitleInput.value = t.title || "";
      todoDescriptionInput.value = t.description || "";
      modalChecklist = (t.checklist || []).map(function (it) {
        return { id: it.id, text: it.text, checked: !!it.checked };
      });
    }
  }
  renderChecklistModal();
  modalTodo.classList.remove("hidden");
  todoTitleInput.focus();
}

function closeTodoModal() {
  modalTodo.classList.add("hidden");
  currentEditingTodoId = null;
  modalChecklist = [];
}

function renderChecklistModal() {
  clearElement(checklistItemsList);
  if (!modalChecklist.length) {
    var info = document.createElement("li");
    info.textContent = "Nenhum item na checklist.";
    checklistItemsList.appendChild(info);
    return;
  }
  modalChecklist.forEach(function (item) {
    var li = document.createElement("li");
    li.className = "check-item";
    var cb = document.createElement("input");
    cb.type = "checkbox";
    cb.checked = !!item.checked;
    cb.addEventListener("change", function () {
      item.checked = cb.checked;
      saveState();
    });
    var span = document.createElement("span");
    span.className = "check-text";
    span.textContent = item.text;
    var controls = document.createElement("div");
    controls.style.marginLeft = "auto";
    var editBtn = document.createElement("button");
    editBtn.textContent = "Editar";
    var removeBtn = document.createElement("button");
    removeBtn.textContent = "Remover";
    editBtn.addEventListener("click", function () {
      var val = prompt("Editar item:", item.text);
      if (val !== null) {
        item.text = val.trim();
        renderChecklistModal();
      }
    });
    removeBtn.addEventListener("click", function () {
      modalChecklist = modalChecklist.filter(function (c) {
        return c.id !== item.id;
      });
      renderChecklistModal();
    });
    controls.appendChild(editBtn);
    controls.appendChild(removeBtn);
    li.appendChild(cb);
    li.appendChild(span);
    li.appendChild(controls);
    checklistItemsList.appendChild(li);
  });
}

addChecklistItemBtn.addEventListener("click", function () {
  var txt = newChecklistTextInput.value.trim();
  if (!txt) return;
  modalChecklist.push({ id: generateId("c_"), text: txt, checked: false });
  newChecklistTextInput.value = "";
  renderChecklistModal();
});

saveTodoBtn.addEventListener("click", function () {
  var title = todoTitleInput.value.trim();
  if (!title) {
    alert("Título obrigatório");
    todoTitleInput.focus();
    return;
  }
  var description = todoDescriptionInput.value.trim();
  var checklist = modalChecklist.map(function (it) {
    return { id: it.id, text: it.text, checked: !!it.checked };
  });
  if (currentEditingTodoId) {
    var existing = state.todos.find(function (t) {
      return t.id === currentEditingTodoId;
    });
    if (existing) {
      existing.title = title;
      existing.description = description;
      existing.checklist = checklist;
      existing.updatedAt = Date.now();
    }
  } else {
    var newTodo = {
      id: generateId("td_"),
      title: title,
      description: description,
      checklist: checklist,
      done: false,
      removed: false,
      createdAt: Date.now(),
    };
    state.todos.unshift(newTodo);
  }
  saveState();
  renderTodos();
  closeTodoModal();
});

cancelTodoBtn.addEventListener("click", function () {
  closeTodoModal();
});

function createChecklistSummary(list) {
  var container = document.createElement("div");
  container.style.marginTop = "8px";
  list.forEach(function (it) {
    var line = document.createElement("div");
    line.style.fontSize = "13px";
    line.style.color = it.checked ? "#8bc34a" : "var(--muted)";
    line.textContent = "· " + it.text;
    container.appendChild(line);
  });
  return container;
}

function renderTodos() {
  clearElement(todoListElement);
  if (!state.todos.length) {
    var empty = document.createElement("div");
    empty.className = "muted";
    empty.textContent = 'Nenhuma tarefa ainda. Clique em "Adicionar tarefa".';
    todoListElement.appendChild(empty);
    return;
  }
  state.todos.forEach(function (todo) {
    var card = document.createElement("div");
    card.className = "todo-card";
    if (todo.removed) card.style.opacity = 0.45;
    var left = document.createElement("div");
    left.className = "todo-left";
    var meta = document.createElement("div");
    meta.className = "todo-meta";
    var titleEl = document.createElement("div");
    titleEl.className = "todo-title";
    titleEl.textContent = todo.title;
    var descEl = document.createElement("div");
    descEl.style.marginTop = "6px";
    descEl.textContent = todo.description || "";
    meta.appendChild(titleEl);
    meta.appendChild(descEl);
    if (todo.checklist && todo.checklist.length) {
      meta.appendChild(createChecklistSummary(todo.checklist));
    }
    var created = document.createElement("div");
    created.className = "todo-meta";
    created.style.marginTop = "8px";
    created.textContent =
      "Criado: " + new Date(todo.createdAt).toLocaleString();
    meta.appendChild(created);
    left.appendChild(meta);
    var actions = document.createElement("div");
    actions.className = "todo-actions";
    var doneBtn = document.createElement("button");
    doneBtn.textContent = todo.done ? "Desmarcar" : "Completar";
    var editBtn = document.createElement("button");
    editBtn.textContent = "Editar";
    var removeBtn = document.createElement("button");
    removeBtn.textContent = todo.removed ? "Restaurar" : "Remover";
    var delPermBtn = document.createElement("button");
    delPermBtn.textContent = "Excluir";
    doneBtn.addEventListener("click", function () {
      todo.done = !todo.done;
      saveState();
      renderTodos();
    });
    editBtn.addEventListener("click", function () {
      openTodoModal(todo.id);
    });
    removeBtn.addEventListener("click", function () {
      todo.removed = !todo.removed;
      saveState();
      renderTodos();
    });
    delPermBtn.addEventListener("click", function () {
      if (!confirm("Excluir permanentemente esta tarefa?")) return;
      state.todos = state.todos.filter(function (t) {
        return t.id !== todo.id;
      });
      saveState();
      renderTodos();
    });
    actions.appendChild(doneBtn);
    actions.appendChild(editBtn);
    actions.appendChild(removeBtn);
    actions.appendChild(delPermBtn);
    card.appendChild(left);
    card.appendChild(actions);
    todoListElement.appendChild(card);
  });
}

function openNoteModal(noteId) {
  currentEditingNoteId = noteId || null;
  noteFormDate.value =
    noteDateInput.value || new Date().toISOString().slice(0, 10);
  noteTitleInput.value = "";
  noteContentInput.value = "";
  modalNoteTitleEl.textContent = noteId ? "Editar nota" : "Nova nota";
  if (noteId) {
    var n = state.notes.find(function (x) {
      return x.id === noteId;
    });
    if (n) {
      noteFormDate.value = n.date;
      noteTitleInput.value = n.title;
      noteContentInput.value = n.content;
    }
  }
  modalNote.classList.remove("hidden");
  noteTitleInput.focus();
}

function closeNoteModal() {
  modalNote.classList.add("hidden");
  currentEditingNoteId = null;
}

saveNoteBtn.addEventListener("click", function () {
  var date = noteFormDate.value || new Date().toISOString().slice(0, 10);
  var title = noteTitleInput.value.trim();
  var content = noteContentInput.value.trim();
  if (!title) {
    alert("Título da nota obrigatório");
    noteTitleInput.focus();
    return;
  }
  if (currentEditingNoteId) {
    var existing = state.notes.find(function (n) {
      return n.id === currentEditingNoteId;
    });
    if (existing) {
      existing.date = date;
      existing.title = title;
      existing.content = content;
      existing.updatedAt = Date.now();
    }
  } else {
    state.notes.unshift({
      id: generateId("nt_"),
      date: date,
      title: title,
      content: content,
      createdAt: Date.now(),
    });
  }
  saveState();
  renderNotes();
  closeNoteModal();
});

cancelNoteBtn.addEventListener("click", function () {
  closeNoteModal();
});

function renderNotes() {
  clearElement(noteListElement);
  if (!state.notes.length) {
    var empty = document.createElement("div");
    empty.className = "muted";
    empty.textContent =
      'Nenhuma nota. Escolha uma data e clique em "Adicionar nota".';
    noteListElement.appendChild(empty);
    return;
  }
  var notesSorted = state.notes.slice().sort(function (a, b) {
    if (b.date === a.date) return b.createdAt - a.createdAt;
    return b.date.localeCompare(a.date);
  });
  notesSorted.forEach(function (note) {
    var card = document.createElement("div");
    card.className = "note-card";
    var meta = document.createElement("div");
    meta.className = "note-meta";
    meta.textContent = note.date + " • " + note.title;
    var body = document.createElement("div");
    body.textContent = note.content;
    var actions = document.createElement("div");
    actions.style.marginTop = "8px";
    var editBtn = document.createElement("button");
    editBtn.textContent = "Editar";
    var delBtn = document.createElement("button");
    delBtn.textContent = "Excluir";
    editBtn.addEventListener("click", function () {
      openNoteModal(note.id);
    });
    delBtn.addEventListener("click", function () {
      if (!confirm("Excluir esta nota?")) return;
      state.notes = state.notes.filter(function (n) {
        return n.id !== note.id;
      });
      saveState();
      renderNotes();
    });
    actions.appendChild(editBtn);
    actions.appendChild(delBtn);
    card.appendChild(meta);
    card.appendChild(body);
    card.appendChild(actions);
    noteListElement.appendChild(card);
  });
}

tabs.forEach(function (btn) {
  btn.addEventListener("click", function () {
    switchTab(btn.dataset.tab);
  });
});

autosaveToggle.addEventListener("change", function () {
  state.settings.autosave = autosaveToggle.checked;
  saveState();
});

openAddTodoBtn.addEventListener("click", function () {
  openTodoModal();
});

openAddNoteBtn.addEventListener("click", function () {
  openNoteModal();
});

clearRemovedBtn.addEventListener("click", function () {
  state.todos = state.todos.filter(function (t) {
    return !t.removed;
  });
  renderTodos();
  saveState();
});

noteDateInput.addEventListener("change", function () {
  noteFormDate.value = noteDateInput.value;
});

loadState();
autosaveToggle.checked = !!state.settings.autosave;
switchTab("todos");
renderTodos();
renderNotes();
