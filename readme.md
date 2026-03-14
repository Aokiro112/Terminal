# 🖥️ Advanced Terminal

> A powerful natural-language terminal built from scratch using **Python**, **Django**, and **Node.js**.  
> Type commands in plain English — no memorizing syntax needed.

> ⚠️ **Actively maintained** — new features and improvements coming regularly. Star ⭐ the repo to stay updated!

---

## 📸 Preview

```
  ╔══════════════════════════════╗
  ║   Advanced Terminal v2.0     ║
  ║   Node + Django + Python     ║
  ╚══════════════════════════════╝

[Connected to terminal server]
[Tab created: tab_1773446453043]

C:\Users\mayan> create folder Projects
✓ Folder ban gaya!
   Naam  : Projects
   Kahan : C:\Users\mayan\Projects

C:\Users\mayan> show
📍 Location: C:\Users\mayan
──────────────────────────────────────────────────
🗂️  Folders (3):
  📁  Desktop
  📁  Documents
  📁  Projects

📝 Files (2):
  📄  notes.txt  (1 KB)
  📄  config.json  (3 KB)
──────────────────────────────────────────────────
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              Python CLI Client                  │
│         (shell/client.py — user types here)     │
└────────────────────┬────────────────────────────┘
                     │ WebSocket (Socket.IO)
┌────────────────────▼────────────────────────────┐
│            Node.js Server — Port 3000           │
│     (Tab Manager + Real-time Communication)     │
└────────────────────┬────────────────────────────┘
                     │ HTTP (REST API)
┌────────────────────▼────────────────────────────┐
│           Django Backend — Port 8000            │
│       (Command Execution + Natural Language)    │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│              Windows OS                         │
│     (Files, Folders, Apps, Network, etc.)       │
└─────────────────────────────────────────────────┘
```

---

## ⚡ Tech Stack

| Layer | Technology | Port | Role |
|-------|-----------|------|------|
| CLI Client | Python 3 + Socket.IO | — | User interface |
| Realtime Server | Node.js + Socket.IO + Express | 3000 | Tab manager & WebSocket |
| Backend API | Django 6 + Django REST Framework | 8000 | Command execution engine |

---

## 📋 Requirements

Pehle yeh sab apne PC mein install karo:

| Software | Version | Download |
|----------|---------|----------|
| Python | 3.10+ | https://python.org/downloads |
| Node.js | 18+ | https://nodejs.org |
| Git | Latest | https://git-scm.com |

---

## 🛠️ Installation — First Time Setup

### Step 1 — Repository clone karo
```bash
git clone https://github.com/yourusername/advanced-terminal.git
cd advanced-terminal
```

### Step 2 — Django backend setup karo
```bash
cd backend
pip install django djangorestframework
python manage.py migrate
cd ..
```

### Step 3 — Node.js server setup karo
```bash
cd node-server
npm install socket.io express axios
cd ..
```

### Step 4 — Python client setup karo
```bash
pip install python-socketio[client]
```

---

## 🚀 Terminal Start Karna

### ✅ Option 1 — One Click (Recommended)
```
C:\Terminal\ folder mein jao
start.bat pe double click karo
```
Teeno servers automatically start ho jaate hain — Django, Node.js, aur Client.

### 🔧 Option 2 — Manual Start (3 alag terminals mein)

> ⚠️ **Zaroori:** Hamesha is order mein start karo — pehle Django, phir Node.js, phir Client.

```bash
# Terminal 1 — Django Backend (Port 8000)
cd backend
python manage.py runserver 8000

# Terminal 2 — Node.js Server (Port 3000)
cd node-server
node server.js

# Terminal 3 — Python CLI Client
cd shell
python client.py
```

---

## 📁 Project Structure

```
Terminal/
│
├── backend/                      → Django REST API
│   ├── config/
│   │   ├── settings.py           → Django settings
│   │   └── urls.py               → Main URL routing
│   └── terminal/
│       ├── executor.py           → Natural language command engine ⭐
│       ├── views.py              → API views (run, history, cwd)
│       └── urls.py               → Terminal URL routing
│
├── node-server/                  → Node.js WebSocket Server
│   ├── server.js                 → Main server + Socket.IO
│   ├── tabManager.js             → Multiple tab management
│   └── package.json
│
├── shell/                        → Python CLI Client
│   └── client.py                 → User types commands here
│
├── start.bat                     → One-click startup script
├── .gitignore
└── README.md
```

---

## 🖥️ Commands — Full List

### 📁 Folder Commands
| Command | Kya hoga |
|---------|---------|
| `open folder <naam>` | Folder khulega (File Explorer bhi) |
| `open downloads` | Downloads folder |
| `open documents` | Documents folder |
| `open desktop` | Desktop folder |
| `create folder <naam>` | Naya folder banega (location bhi batayega) |
| `make folder <naam>` | Same as above |
| `delete folder <naam>` | Folder delete hoga |
| `rename folder <old> <new>` | Folder ka naam badlega |

### 📄 File Commands
| Command | Kya hoga |
|---------|---------|
| `create file <naam>` | Naya file banega (location bhi batayega) |
| `make file <naam>` | Same as above |
| `delete file <naam>` | File delete hogi |
| `open file <naam>` | File khulegi (default app mein) |
| `read file <naam>` | File ka content dikhega |
| `write file <naam> <content>` | File mein content likhega |
| `copy file <source> <destination>` | File copy hogi |
| `move file <source> <destination>` | File move hogi |
| `find file <naam>` | File dhundhega current folder mein |
| `rename file <old> <new>` | File ka naam badlega |

### 👁️ Show Commands
| Command | Kya hoga |
|---------|---------|
| `show` | Files + folders list (size ke saath) |
| `show folders` | Sirf folders |
| `show file <naam>` | File ka content |
| `show info` | CPU, RAM, Disk, OS — sab ek saath |
| `show ip` | IP address |
| `show wifi` | Available WiFi networks |
| `show processes` | Chal rahe apps/processes |
| `show disk` | Disk space |
| `show packages` | Installed pip packages |
| `show date` | Aaj ki date |
| `show time` | Current time |

### 🗺️ Navigation Commands
| Command | Kya hoga |
|---------|---------|
| `where am i` | Current folder ka path |
| `go back` | Pichle folder mein jaao |
| `go home` | Home folder mein jaao |
| `go to <path>` | Kisi bhi path pe jaao |
| `cd <path>` | Standard folder change |

### 🌐 Network Commands
| Command | Kya hoga |
|---------|---------|
| `check internet` | Google ko ping karega |
| `ping <site>` | Kisi bhi site ko ping karo |
| `show ip` | IP address details |
| `show wifi` | Available WiFi networks |
| `my wifi` | Connected WiFi ki info |
| `show ports` | Open network ports |

### 💻 System Commands
| Command | Kya hoga |
|---------|---------|
| `show info` | CPU, RAM, Disk, OS info |
| `show processes` | Running processes/apps |
| `kill <app.exe>` | App force close karo |
| `show disk` | Disk space |
| `show cpu` | CPU usage |
| `show ram` | RAM usage |
| `shutdown` | PC band karo |
| `restart` | PC restart karo |
| `shutdown in <minutes>` | Timer se band karo |
| `cancel shutdown` | Shutdown cancel karo |
| `clear screen` | Screen saaf karo |

### 🚀 App Commands
| Command | Kya hoga |
|---------|---------|
| `open notepad` | Notepad khulega |
| `open calculator` | Calculator khulega |
| `open paint` | MS Paint khulega |
| `open chrome` | Chrome browser khulega |
| `open edge` | Edge browser khulega |
| `open firefox` | Firefox khulega |
| `open <app name>` | Koi bhi app kholo |
| `search <query>` | Google mein search karega |

### 🐍 Python Commands
| Command | Kya hoga |
|---------|---------|
| `run <file.py>` | Python file chalao |
| `install <package>` | pip install |
| `uninstall <package>` | pip uninstall |
| `show packages` | Installed packages list |

### 🔧 Git Commands
| Command | Kya hoga |
|---------|---------|
| `git status` | Repo status |
| `git init` | Naya repo banao |
| `commit <message>` | Add + commit ek saath |
| `push` | GitHub pe push karo |
| `pull` | Latest changes lo |
| `clone <url>` | Repo clone karo |

### 🗂️ Tab Commands (CLI mein)
| Command | Kya hoga |
|---------|---------|
| `newtab` | Naya tab banao |
| `tabs` | Saare open tabs dekho |
| `switch <tabId>` | Kisi aur tab mein jao |
| `closetab` | Current tab band karo |
| `help` | Saare commands dekho |
| `exit` | Terminal band karo |

---

## ❌ Common Errors aur Fix

### ❌ "Node server error"
```
Kya hua  : Django server band ho gaya
Fix      : Terminal 1 mein dobara chalao:
           python manage.py runserver 8000
```

### ❌ "Cannot connect to server"
```
Kya hua  : Node.js server nahi chal raha
Fix      : Terminal 2 mein dobara chalao:
           node server.js
```

### ❌ "Module not found"
```
Kya hua  : Koi dependency install nahi hai
Fix      : Installation steps dobara follow karo
```

### ❌ "Folder/File nahi mila"
```
Kya hua  : Galat naam ya wrong folder mein ho
Fix      : Pehle "where am i" likho, phir "show" se
           dekho kya available hai
```

---

## 🗺️ Roadmap — Coming Soon

- [ ] AI-powered command suggestions
- [ ] SSH support
- [ ] File explorer sidebar
- [ ] Themes (dark / light / custom colors)
- [ ] Tab autocomplete
- [ ] Plugin system
- [ ] Linux & macOS support
- [ ] Web UI (browser-based terminal)
- [ ] Command aliases (apne shortcuts banao)
- [ ] Terminal split view (2 terminals ek saath)
- [ ] Command scheduler (time pe command chalao)
- [ ] File preview in terminal

---

## 🤝 Contributing

Pull requests welcome hain! Koi bhi feature suggest karna ho toh Issues mein batao.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 👨‍💻 Author

Made with ❤️ from scratch — Python + Django + Node.js