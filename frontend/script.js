const API = 'http://localhost:5000/api';

const qs = id => document.getElementById(id);

window.onload = () => {
  setupThemeToggle();
  checkSession();
  setupAuth();
  setupTaskHandlers();
  setupAI();
  setupTelegram();
};

function setupThemeToggle() {
  const btn = document.createElement('button');
  btn.id = 'dark-toggle';
  btn.textContent = 'Toggle Dark Mode';
  document.body.appendChild(btn);
  btn.onclick = () => document.body.classList.toggle('dark-mode');
}

function checkSession() {
  fetch(`${API}/auth/me`).then(res => res.json()).then(data => {
    if (data.username) {
      showDashboard();
    } else {
      hideDashboard();
    }
  });
}

function showDashboard() {
  qs('auth').style.display = 'none';
  qs('dashboard').style.display = 'block';
  qs('ai-section').style.display = 'block';
  qs('telegram-section').style.display = 'block';
  qs('logout-btn').style.display = 'block';
  loadTasks();
}

function hideDashboard() {
  qs('auth').style.display = 'block';
  qs('dashboard').style.display = 'none';
  qs('ai-section').style.display = 'none';
  qs('telegram-section').style.display = 'none';
  qs('logout-btn').style.display = 'none';
}

function setupAuth() {
  qs('login-btn').onclick = () => {
    fetch(`${API}/auth/login`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        username: qs('auth-username').value,
        password: qs('auth-password').value
      })
    }).then(r => r.json()).then(checkSession);
  };

  qs('register-btn').onclick = () => {
    fetch(`${API}/auth/register`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        username: qs('auth-username').value,
        password: qs('auth-password').value
      })
    }).then(r => r.json()).then(checkSession);
  };

  qs('logout-btn').onclick = () => {
    fetch(`${API}/auth/logout`, { method: 'POST' }).then(checkSession);
  };
}

function setupTaskHandlers() {
  qs('add-task-btn').onclick = () => {
    fetch(`${API}/tasks`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        title: qs('new-title').value,
        description: qs('new-desc').value,
        due_date: qs('new-due').value,
        category: qs('new-category').value
      })
    }).then(() => loadTasks());
  };
}

function loadTasks() {
  fetch(`${API}/tasks`).then(r => r.json()).then(tasks => {
    const list = qs('task-list');
    list.innerHTML = '';
    tasks.forEach(t => {
      const div = document.createElement('div');
      div.innerHTML = `
        <strong>${t.title}</strong> - ${t.status} - due ${t.due_date}<br>
        ${t.description}<br>
        <button onclick="markDone('${t._id}')">Mark Done</button>
        <button onclick="deleteTask('${t._id}')">Delete</button>
        <hr>
      `;
      list.appendChild(div);
    });
  });
}

function markDone(id) {
  fetch(`${API}/tasks/${id}`, {
    method: 'PUT',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ status: 'done' })
  }).then(() => loadTasks());
}

function deleteTask(id) {
  fetch(`${API}/tasks/${id}`, { method: 'DELETE' }).then(() => loadTasks());
}

function setupAI() {
  qs('ai-recommend-btn').onclick = () => {
    fetch(`${API}/ai/recommend`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ description: qs('ai-input').value })
    })
    .then(r => r.json())
    .then(d => qs('ai-result').textContent = d.recommendation || d.error || 'Error');
  };
}

function setupTelegram() {
  qs('update-telegram-btn').onclick = () => {
    fetch(`${API}/tasks/update-chat-id`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ telegram_chat_id: qs('telegram-id').value })
    });
  };
}
