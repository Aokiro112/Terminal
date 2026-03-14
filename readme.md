# Advanced Terminal 🖥️

A powerful multi-process terminal built from scratch using **Python**, **Django**, and **Node.js** — all working together in real-time.

> ⚠️ This project is actively maintained. More features coming soon!

---

## 🏗️ Architecture

```
Python Client (CLI)
      ↓
Node.js Server (WebSocket + Tab Manager)
      ↓
Django Backend (Command Execution Engine)
      ↓
Operating System
```

---

## ⚡ Tech Stack

| Layer | Technology | Role |
|-------|-----------|------|
| CLI Client | Python + Socket.IO | User interface & input |
| Realtime Server | Node.js + Socket.IO | Tab management & WebSocket |
| Backend API | Django (Python) | Command execution engine |

---

## 📋 Requirements

Pehle yeh sab install karo apne PC mein:

| Software | Download Link |
|----------|--------------|
| Python 3.x | https://python.org |
| Node.js | https://nodejs.org |
| Git | https://git-scm.com |

---

## 🛠️ First Time Setup

### 1. Repository clone karo
```bash
git clone https://github.com/yourusername/advanced-terminal.git
cd advanced-terminal
```

### 2. Django dependencies install karo
```bash
cd backend
pip install django djangorestframework
python manage.py migrate
cd ..
```

### 3. Node.js dependencies install karo
```bash
cd node-server
npm install socket.io express axios
cd ..
```

### 4. Python client dependency install karo
```bash
pip install python-socketio[client]
```

---

## 🚀 Terminal Start Karna

### Option 1 — One Click (Recommended)
```
C:\Terminal\ folder mein jao
start.bat pe double click karo
```
Bas! Teeno servers automatically start ho jaayenge.

### Option 2 — Manual (3 alag terminals mein)
```bash
# Terminal 1 — Django Backend
cd backend
python manage.py runserver 8000

# Terminal 2 — Node.js Server
cd node-server
node server.js

# Terminal 3 — Python Client
cd shell
python client.py
```

> ⚠️ Hamesha is order mein start karo — pehle Django, phir Node.js, phir Client

---

## 🖥️ Terminal Use Karna

Terminal start hone ke baad aisa dikhega:
```
  ╔══════════════════════════════╗
  ║   Advanced Terminal v2.0     ║
  ║   Node + Django + Python     ║
  ╚══════════════════════════════╝

[Connected to terminal server]
[Tab created: tab_xxxxxxx]

[tab_xxxx] ~ >
```

### Built-in Commands

| Command | Kya karta hai |
|---------|--------------|
| `help` | Saare commands dikhata hai |
| `newtab` | Naya tab banata hai |
| `tabs` | Saare open tabs dikhata hai |
| `switch <tabId>` | Kisi aur tab mein switch karta hai |
| `closetab` | Current tab band karta hai |
| `exit` | Terminal band karta hai |

### OS Commands (sab kaam karte hain)

```bash
dir              # files aur folders dikhao
ipconfig         # network info
ping google.com  # internet check karo
cd folder_name   # folder change karo
echo Hello       # text print karo
mkdir newfolder  # naya folder banao
```

### Multiple Tabs Use Karna

```bash
# Naya tab banao
newtab

# Saare tabs dekho
tabs

# Kisi tab mein switch karo (tabId copy karke likho)
switch tab_1773446453043

# Current tab band karo
closetab
```

---

## 📁 Project Structure

```
Terminal/
├── backend/               → Django REST API
│   ├── config/
│   │   ├── settings.py
│   │   └── urls.py
│   └── terminal/
│       ├── views.py
│       ├── urls.py
│       └── executor.py
├── node-server/           → Node.js WebSocket Server
│   ├── server.js
│   ├── tabManager.js
│   └── package.json
├── shell/                 → Python CLI Client
│   └── client.py
├── start.bat              → One-click startup
├── .gitignore
└── README.md
```

---

## ❌ Common Errors aur Fix

### Error: Node server error
```
Django server band ho gaya hoga
Fix: Terminal 1 mein python manage.py runserver 8000 dobara chalao
```

### Error: Cannot connect to server
```
Node.js server nahi chal raha
Fix: Terminal 2 mein node server.js dobara chalao
```

### Error: Module not found
```
Dependencies install nahi hain
Fix: Setup ke steps dobara follow karo
```

---

## 🗺️ Roadmap

- [ ] SSH support
- [ ] File explorer sidebar
- [ ] Themes (dark / light / custom)
- [ ] Tab autocomplete
- [ ] Plugin system
- [ ] Linux & macOS support
- [ ] Web UI (browser based terminal)
- [ ] Command aliases
- [ ] Terminal split view
- [ ] Command suggestions (AI powered)

---

## 📌 Note

This project is in **active development**. Star ⭐ the repo to stay updated on new features!

---

## 📄 License

MIT License — free to use and modify.