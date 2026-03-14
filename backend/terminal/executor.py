import subprocess
import os
import shutil


class CommandExecutor:
    def __init__(self):
        self.cwd = os.path.expanduser("~")
        self.history = []
        self.env = os.environ.copy()

    def execute(self, command, tab_id="default"):
        self.history.append({"tab": tab_id, "cmd": command})
        cmd = command.strip()
        low = cmd.lower()

        # ── FOLDER commands ────────────────────────────

        if low.startswith("open folder"):
            return self._open_folder(cmd[11:].strip())

        if low.startswith("create folder") or low.startswith("make folder") or low.startswith("new folder"):
            name = cmd.split(" ", 2)[2].strip()
            return self._create_folder(name)

        if low.startswith("delete folder") or low.startswith("remove folder"):
            return self._delete_folder(cmd.split(" ", 2)[2].strip())

        if low.startswith("rename folder"):
            parts = cmd.split(" ", 3)
            return self._rename(parts[2], parts[3]) if len(parts) == 4 else self._err("Purana aur naya naam dono batao")

        # ── FILE commands ──────────────────────────────

        if low.startswith("create file") or low.startswith("make file") or low.startswith("new file"):
            return self._create_file(cmd.split(" ", 2)[2].strip())

        if low.startswith("delete file") or low.startswith("remove file"):
            return self._delete_file(cmd.split(" ", 2)[2].strip())

        if low.startswith("rename file"):
            parts = cmd.split(" ", 3)
            return self._rename(parts[2], parts[3]) if len(parts) == 4 else self._err("Purana aur naya naam dono batao")

        if low.startswith("open file"):
            return self._open_file(cmd[9:].strip())

        if low.startswith("copy file"):
            parts = cmd.split(" ", 3)
            return self._copy_file(parts[2], parts[3]) if len(parts) == 4 else self._err("Source aur destination dono batao")

        if low.startswith("move file"):
            parts = cmd.split(" ", 3)
            return self._move_file(parts[2], parts[3]) if len(parts) == 4 else self._err("Source aur destination dono batao")

        if low.startswith("read file"):
            return self._read_file(cmd[9:].strip())

        if low.startswith("write file"):
            parts = cmd.split(" ", 3)
            return self._write_file(parts[2], parts[3]) if len(parts) == 4 else self._err("Filename aur content dono batao")

        if low.startswith("find file"):
            return self._find_file(cmd[9:].strip())

        # ── NAVIGATION commands ────────────────────────

        if low in ["show files", "list files", "files", "ls", "dir"]:
            return self._show_files()

        if low in ["where am i", "current folder", "pwd", "location"]:
            return self._ok(f"Tum yahan ho: {self.cwd}\n")

        if low in ["go back", "back", "go up"]:
            return self._open_folder(os.path.dirname(self.cwd))

        if low in ["go home", "home"]:
            return self._open_folder(os.path.expanduser("~"))

        if low.startswith("go to"):
            path = cmd.split(" ", 2)[2].strip()
            return self._open_folder(path)

        if low.startswith("cd "):
            return self._open_folder(cmd[3:].strip())

        # ── NETWORK commands ───────────────────────────

        if low in ["show ip", "my ip", "ip address", "ipconfig"]:
            return self._run("ipconfig")

        if low in ["check internet", "ping google", "internet check"]:
            return self._run("ping google.com -n 4")

        if low.startswith("ping "):
            return self._run(f"ping {cmd[5:].strip()} -n 4")

        if low in ["show wifi", "wifi list", "available wifi"]:
            return self._run("netsh wlan show networks")

        if low in ["my wifi", "connected wifi", "wifi name"]:
            return self._run("netsh wlan show interfaces")

        if low in ["open ports", "show ports", "ports"]:
            return self._run("netstat -an")

        # ── SYSTEM commands ────────────────────────────

        if low in ["show processes", "running apps", "processes", "tasklist"]:
            return self._run("tasklist")

        if low.startswith("kill ") or low.startswith("stop "):
            app = cmd.split(" ", 1)[1].strip()
            return self._run(f"taskkill /IM {app} /F")

        if low in ["system info", "pc info", "computer info"]:
            return self._run("systeminfo")

        if low in ["disk space", "storage", "check disk", "disk info"]:
            return self._run("wmic logicaldisk get size,freespace,caption")

        if low in ["cpu usage", "ram usage", "memory usage"]:
            return self._run("wmic cpu get loadpercentage && wmic OS get FreePhysicalMemory")

        if low in ["date", "today", "what date"]:
            return self._run("date /t")

        if low in ["time", "what time", "current time"]:
            return self._run("time /t")

        if low in ["shutdown", "shut down"]:
            return self._run("shutdown /s /t 0")

        if low in ["restart", "reboot"]:
            return self._run("shutdown /r /t 0")

        if low.startswith("shutdown in "):
            mins = cmd.split(" ", 2)[2].strip()
            secs = int(mins) * 60
            return self._run(f"shutdown /s /t {secs}")

        if low in ["cancel shutdown", "abort shutdown"]:
            return self._run("shutdown /a")

        if low in ["clear screen", "cls", "clear"]:
            return self._ok("\033[2J\033[H")

        # ── APP commands ───────────────────────────────

        if low in ["open notepad", "notepad"]:
            return self._run("start notepad")

        if low in ["open calculator", "calculator", "calc"]:
            return self._run("start calc")

        if low in ["open paint", "paint"]:
            return self._run("start mspaint")

        if low in ["open browser", "browser", "open chrome"]:
            return self._run("start chrome")

        if low in ["open firefox"]:
            return self._run("start firefox")

        if low in ["open edge"]:
            return self._run("start msedge")

        if low.startswith("open "):
            app = cmd[5:].strip()
            return self._run(f"start {app}")

        if low.startswith("search "):
            query = cmd[7:].strip()
            return self._run(f'start https://www.google.com/search?q={query.replace(" ", "+")}')

        # ── GIT commands ───────────────────────────────

        if low in ["git status", "status"]:
            return self._run("git status")

        if low in ["git init", "init repo"]:
            return self._run("git init")

        if low.startswith("git add"):
            return self._run(cmd)

        if low.startswith("commit "):
            msg = cmd[7:].strip()
            return self._run(f'git add . && git commit -m "{msg}"')

        if low in ["git push", "push"]:
            return self._run("git push")

        if low in ["git pull", "pull"]:
            return self._run("git pull")

        if low.startswith("git clone ") or low.startswith("clone "):
            url = cmd.split(" ", 2)[2] if low.startswith("git clone") else cmd[6:].strip()
            return self._run(f"git clone {url}")

        # ── PYTHON commands ────────────────────────────

        if low.startswith("run python "):
            file = cmd.split(" ", 2)[2].strip()
            return self._run(f"python {file}")

        if low.startswith("run "):
            file = cmd[4:].strip()
            return self._run(f"python {file}")

        if low.startswith("install "):
            pkg = cmd[8:].strip()
            return self._run(f"pip install {pkg}")

        if low.startswith("uninstall "):
            pkg = cmd[10:].strip()
            return self._run(f"pip uninstall {pkg} -y")

        if low in ["installed packages", "pip list", "show packages"]:
            return self._run("pip list")

        # ── NODE commands ──────────────────────────────

        if low.startswith("npm install "):
            return self._run(cmd)

        if low in ["npm list", "node packages"]:
            return self._run("npm list")

        if low.startswith("node "):
            return self._run(cmd)

        # ── ENVIRONMENT commands ───────────────────────

        if low in ["show env", "environment", "env variables"]:
            return self._run("set")

        if low.startswith("set env "):
            parts = cmd.split(" ", 3)
            if len(parts) == 4:
                os.environ[parts[2]] = parts[3]
                return self._ok(f"ENV set: {parts[2]} = {parts[3]}\n")

        # ── HELP ───────────────────────────────────────

        if low in ["help", "commands", "?"]:
            return self._help()

        # ── FALLBACK — normal OS command ───────────────
        return self._run(cmd)

    # ── Helper functions ───────────────────────────────

    def _run(self, cmd):
        try:
            result = subprocess.run(
                cmd, shell=True,
                capture_output=True,
                text=True,
                cwd=self.cwd,
                env=self.env,
                timeout=30
            )
            return {
                "output": result.stdout,
                "error": result.stderr,
                "cwd": self.cwd,
                "exit_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return self._err("Timeout: command 30s se zyada chala")
        except Exception as e:
            return self._err(str(e))

    def _ok(self, msg):
        return {"output": msg, "error": "", "cwd": self.cwd}

    def _err(self, msg):
        return {"output": "", "error": f"✗ {msg}\n", "cwd": self.cwd}

    def _open_folder(self, folder):
        try:
            path = folder if os.path.isabs(folder) else os.path.join(self.cwd, folder)
            path = os.path.normpath(path)
            os.chdir(path)
            self.cwd = os.getcwd()
            return self._ok(f"✓ Folder khul gaya: {self.cwd}\n")
        except FileNotFoundError:
            return self._err(f"'{folder}' naam ka folder nahi mila")
        except Exception as e:
            return self._err(str(e))

    def _create_file(self, filename):
        if not filename:
            return self._err("File ka naam batao")
        try:
            open(os.path.join(self.cwd, filename), 'w').close()
            return self._ok(f"✓ File ban gayi: {filename}\n")
        except Exception as e:
            return self._err(str(e))

    def _create_folder(self, folder):
        if not folder:
            return self._err("Folder ka naam batao")
        try:
            os.makedirs(os.path.join(self.cwd, folder), exist_ok=True)
            return self._ok(f"✓ Folder ban gaya: {folder}\n")
        except Exception as e:
            return self._err(str(e))

    def _delete_file(self, filename):
        if not filename:
            return self._err("File ka naam batao")
        try:
            os.remove(os.path.join(self.cwd, filename))
            return self._ok(f"✓ File delete ho gayi: {filename}\n")
        except FileNotFoundError:
            return self._err(f"'{filename}' nahi mili")
        except Exception as e:
            return self._err(str(e))

    def _delete_folder(self, folder):
        if not folder:
            return self._err("Folder ka naam batao")
        try:
            shutil.rmtree(os.path.join(self.cwd, folder))
            return self._ok(f"✓ Folder delete ho gaya: {folder}\n")
        except FileNotFoundError:
            return self._err(f"'{folder}' nahi mila")
        except Exception as e:
            return self._err(str(e))

    def _rename(self, old, new):
        try:
            os.rename(os.path.join(self.cwd, old), os.path.join(self.cwd, new))
            return self._ok(f"✓ '{old}' ka naam '{new}' ho gaya\n")
        except Exception as e:
            return self._err(str(e))

    def _open_file(self, filename):
        try:
            os.startfile(os.path.join(self.cwd, filename))
            return self._ok(f"✓ File khul gayi: {filename}\n")
        except Exception as e:
            return self._err(str(e))

    def _copy_file(self, src, dst):
        try:
            shutil.copy2(os.path.join(self.cwd, src), os.path.join(self.cwd, dst))
            return self._ok(f"✓ File copy ho gayi: {src} → {dst}\n")
        except Exception as e:
            return self._err(str(e))

    def _move_file(self, src, dst):
        try:
            shutil.move(os.path.join(self.cwd, src), os.path.join(self.cwd, dst))
            return self._ok(f"✓ File move ho gayi: {src} → {dst}\n")
        except Exception as e:
            return self._err(str(e))

    def _read_file(self, filename):
        try:
            with open(os.path.join(self.cwd, filename), 'r') as f:
                return self._ok(f.read() + "\n")
        except Exception as e:
            return self._err(str(e))

    def _write_file(self, filename, content):
        try:
            with open(os.path.join(self.cwd, filename), 'w') as f:
                f.write(content)
            return self._ok(f"✓ File mein likh diya: {filename}\n")
        except Exception as e:
            return self._err(str(e))

    def _find_file(self, filename):
        try:
            results = []
            for root, dirs, files in os.walk(self.cwd):
                for f in files:
                    if filename.lower() in f.lower():
                        results.append(os.path.join(root, f))
            if results:
                return self._ok("Mili files:\n" + "\n".join(results) + "\n")
            return self._ok(f"'{filename}' nahi mili\n")
        except Exception as e:
            return self._err(str(e))

    def _show_files(self):
        try:
            items = os.listdir(self.cwd)
            folders = [f"📁 {i}" for i in items if os.path.isdir(os.path.join(self.cwd, i))]
            files = [f"📄 {i}" for i in items if os.path.isfile(os.path.join(self.cwd, i))]
            output = "\n".join(folders + files) + "\n"
            return self._ok(output or "Kuch nahi hai yahan\n")
        except Exception as e:
            return self._err(str(e))

    def _help(self):
        return self._ok("""
📁 FOLDER:   open folder <naam>  |  create folder <naam>  |  delete folder <naam>  |  rename folder <purana> <naya>
📄 FILE:     create file <naam>  |  delete file <naam>    |  read file <naam>       |  write file <naam> <content>
             copy file <src> <dst>  |  move file <src> <dst>  |  find file <naam>   |  open file <naam>
🗺️  NAV:     show files  |  where am i  |  go back  |  go home  |  go to <path>  |  cd <path>
🌐 NETWORK:  show ip  |  check internet  |  ping <site>  |  show wifi  |  my wifi  |  open ports
💻 SYSTEM:   show processes  |  kill <app>  |  system info  |  disk space  |  cpu usage  |  date  |  time
🚀 APPS:     open notepad  |  open chrome  |  open calculator  |  open paint  |  open edge  |  search <query>
🐍 PYTHON:   run <file.py>  |  install <package>  |  uninstall <package>  |  installed packages
🔧 GIT:      git status  |  git init  |  commit <message>  |  push  |  pull  |  clone <url>
⚙️  OTHER:   shutdown  |  restart  |  shutdown in <mins>  |  cancel shutdown  |  clear screen
""")

    def get_history(self, tab_id=None):
        if tab_id:
            return [h for h in self.history if h["tab"] == tab_id]
        return self.history


executor = CommandExecutor()