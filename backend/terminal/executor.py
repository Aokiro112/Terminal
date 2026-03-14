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

        if low.startswith("open folder") or low.startswith("open downloads") or low.startswith("open documents") or low.startswith("open desktop"):
            if low == "open downloads":
                folder = os.path.join(os.path.expanduser("~"), "Downloads")
                subprocess.Popen(f'explorer "{folder}"')
                return self._open_folder(folder)
            if low == "open documents":
                folder = os.path.join(os.path.expanduser("~"), "Documents")
                subprocess.Popen(f'explorer "{folder}"')
                return self._open_folder(folder)
            if low == "open desktop":
                folder = os.path.join(os.path.expanduser("~"), "Desktop")
                subprocess.Popen(f'explorer "{folder}"')
                return self._open_folder(folder)
            folder = cmd[11:].strip()
            full_path = folder if os.path.isabs(folder) else os.path.join(self.cwd, folder)
            subprocess.Popen(f'explorer "{os.path.normpath(full_path)}"')
            return self._open_folder(folder)

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

        # ── SHOW commands ──────────────────────────────

        if low in ["show", "show files", "list files", "files", "ls", "dir"]:
            return self._show_files()

        if low in ["show folders", "list folders", "folders"]:
            return self._show_folders_only()

        if low.startswith("show file "):
            return self._read_file(cmd[10:].strip())

        if low in ["show info", "system info", "pc info", "show system"]:
            return self._show_system_info()

        if low in ["show ip", "my ip", "ip address", "ipconfig"]:
            return self._run("ipconfig")

        if low in ["show wifi", "wifi list", "available wifi"]:
            return self._run("netsh wlan show networks")

        if low in ["show processes", "running apps", "processes", "tasklist"]:
            return self._run("tasklist")

        if low in ["show ports", "open ports", "ports"]:
            return self._run("netstat -an")

        if low in ["show env", "environment", "env variables"]:
            return self._run("set")

        if low in ["show packages", "installed packages", "pip list"]:
            return self._run("pip list")

        if low in ["show disk", "disk space", "storage", "check disk", "disk info"]:
            return self._run("wmic logicaldisk get size,freespace,caption")

        if low in ["show cpu", "cpu usage", "show ram", "ram usage", "memory usage"]:
            return self._run("wmic cpu get loadpercentage && wmic OS get FreePhysicalMemory")

        if low in ["show date", "date", "today", "what date"]:
            return self._run("date /t")

        if low in ["show time", "time", "what time", "current time"]:
            return self._run("time /t")

        # ── NAVIGATION commands ────────────────────────

        if low in ["where am i", "current folder", "pwd", "location"]:
            return self._ok(f"Tum yahan ho: {self.cwd}\n")

        if low in ["go back", "back", "go up"]:
            parent = os.path.dirname(self.cwd)
            subprocess.Popen(f'explorer "{parent}"')
            return self._open_folder(parent)

        if low in ["go home", "home"]:
            home = os.path.expanduser("~")
            subprocess.Popen(f'explorer "{home}"')
            return self._open_folder(home)

        if low.startswith("go to"):
            path = cmd.split(" ", 2)[2].strip()
            subprocess.Popen(f'explorer "{os.path.normpath(path)}"')
            return self._open_folder(path)

        if low.startswith("cd "):
            return self._open_folder(cmd[3:].strip())

        # ── NETWORK commands ───────────────────────────

        if low in ["check internet", "ping google", "internet check"]:
            return self._run("ping google.com -n 4")

        if low.startswith("ping "):
            return self._run(f"ping {cmd[5:].strip()} -n 4")

        if low in ["my wifi", "connected wifi", "wifi name"]:
            return self._run("netsh wlan show interfaces")

        # ── SYSTEM commands ────────────────────────────

        if low.startswith("kill ") or low.startswith("stop "):
            app = cmd.split(" ", 1)[1].strip()
            return self._run(f"taskkill /IM {app} /F")

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
            full = os.path.join(self.cwd, app)
            if os.path.isdir(full) or os.path.isdir(app):
                path = full if os.path.isdir(full) else app
                subprocess.Popen(f'explorer "{os.path.normpath(path)}"')
                return self._open_folder(path)
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

        # ── NODE commands ──────────────────────────────

        if low.startswith("npm install "):
            return self._run(cmd)

        if low in ["npm list", "node packages"]:
            return self._run("npm list")

        if low.startswith("node "):
            return self._run(cmd)

        # ── ENVIRONMENT commands ───────────────────────

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
            filepath = os.path.join(self.cwd, filename)
            open(filepath, 'w').close()
            return self._ok(f"✓ File ban gayi!\n   Naam  : {filename}\n   Kahan : {filepath}\n")
        except Exception as e:
            return self._err(str(e))

    def _create_folder(self, folder):
        if not folder:
            return self._err("Folder ka naam batao")
        try:
            folderpath = os.path.join(self.cwd, folder)
            os.makedirs(folderpath, exist_ok=True)
            return self._ok(f"✓ Folder ban gaya!\n   Naam  : {folder}\n   Kahan : {folderpath}\n")
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
            folders = []
            files = []
            for i in items:
                full = os.path.join(self.cwd, i)
                if os.path.isdir(full):
                    folders.append(f"  📁  {i}")
                else:
                    size = os.path.getsize(full)
                    if size < 1024:
                        size_str = f"{size} B"
                    elif size < 1024 * 1024:
                        size_str = f"{size//1024} KB"
                    else:
                        size_str = f"{size//1024//1024} MB"
                    files.append(f"  📄  {i}  ({size_str})")

            output = f"\n📍 Location: {self.cwd}\n"
            output += f"{'─'*50}\n"
            if folders:
                output += f"\n🗂️  Folders ({len(folders)}):\n" + "\n".join(folders) + "\n"
            if files:
                output += f"\n📝 Files ({len(files)}):\n" + "\n".join(files) + "\n"
            if not folders and not files:
                output += "\n  (Yahan kuch nahi hai)\n"
            output += f"{'─'*50}\n"
            return self._ok(output)
        except Exception as e:
            return self._err(str(e))

    def _show_folders_only(self):
        try:
            items = os.listdir(self.cwd)
            folders = [f"  📁  {i}" for i in items if os.path.isdir(os.path.join(self.cwd, i))]
            output = f"\n📍 Location: {self.cwd}\n{'─'*50}\n"
            if folders:
                output += f"\n🗂️  Folders ({len(folders)}):\n" + "\n".join(folders) + "\n"
            else:
                output += "\n  (Koi folder nahi)\n"
            output += f"{'─'*50}\n"
            return self._ok(output)
        except Exception as e:
            return self._err(str(e))

    def _show_system_info(self):
        output = f"\n💻 System Info\n{'─'*50}\n"
        try:
            r = subprocess.run("wmic cpu get name", shell=True, capture_output=True, text=True)
            lines = [l.strip() for l in r.stdout.strip().split("\n") if l.strip() and "Name" not in l]
            cpu = lines[0] if lines else "N/A"
            output += f"  🔲 CPU     : {cpu}\n"

            r = subprocess.run("wmic OS get TotalVisibleMemorySize,FreePhysicalMemory", shell=True, capture_output=True, text=True)
            lines = [l.strip() for l in r.stdout.strip().split("\n") if l.strip() and "Total" not in l and "Free" not in l]
            if lines:
                nums = lines[0].split()
                if len(nums) == 2:
                    free_mb = int(nums[0]) // 1024
                    total_mb = int(nums[1]) // 1024
                    output += f"  🧠 RAM     : {free_mb} MB free / {total_mb} MB total\n"

            r = subprocess.run("wmic logicaldisk get caption,freespace,size", shell=True, capture_output=True, text=True)
            output += f"  💾 Disk    :\n"
            for line in r.stdout.strip().split("\n")[1:]:
                parts = line.split()
                if len(parts) == 3:
                    try:
                        drive = parts[0]
                        free_gb = int(parts[1]) // (1024**3)
                        total_gb = int(parts[2]) // (1024**3)
                        output += f"             {drive} — {free_gb} GB free / {total_gb} GB total\n"
                    except Exception:
                        pass

            r = subprocess.run("wmic os get caption", shell=True, capture_output=True, text=True)
            os_lines = [l.strip() for l in r.stdout.strip().split("\n") if l.strip() and "Caption" not in l]
            os_name = os_lines[0] if os_lines else "N/A"
            output += f"  🪟 OS      : {os_name}\n"
            output += f"  👤 User    : {os.environ.get('USERNAME', 'N/A')}\n"
            output += f"  📍 Folder  : {self.cwd}\n"
            output += f"{'─'*50}\n"
        except Exception as e:
            output += f"  Error: {e}\n"
        return self._ok(output)

    def _help(self):
        return self._ok("""
╔══════════════════════════════════════════════════╗
║           ADVANCED TERMINAL - HELP               ║
╚══════════════════════════════════════════════════╝

📁 FOLDER:
   open folder <naam>          → folder kholo + Explorer bhi
   create folder <naam>        → naya folder banao
   delete folder <naam>        → folder hatao
   rename folder <old> <new>   → naam badlo
   open downloads / documents / desktop

📄 FILE:
   create file <naam>          → naya file banao
   delete file <naam>          → file hatao
   open file <naam>            → file kholo
   read file <naam>            → file padho
   write file <naam> <text>    → file mein likho
   copy file <src> <dst>       → copy karo
   move file <src> <dst>       → move karo
   find file <naam>            → dhundho

👁️  SHOW:
   show                        → files + folders list
   show folders                → sirf folders
   show file <naam>            → file ka content
   show info                   → CPU, RAM, Disk, OS info
   show ip                     → IP address
   show wifi                   → WiFi networks
   show processes              → chal rahe apps
   show disk                   → disk space
   show packages               → pip packages

🗺️  NAVIGATION:
   where am i                  → current location
   go back                     → pichha jao
   go home                     → home folder
   go to <path>                → kisi bhi path pe jao

🌐 NETWORK:
   check internet              → internet check karo
   ping <site>                 → ping karo
   my wifi                     → connected wifi info

💻 SYSTEM:
   show info                   → system details
   kill <app.exe>              → app band karo
   shutdown / restart          → PC band/restart karo
   shutdown in <mins>          → timer se band karo
   cancel shutdown             → shutdown cancel karo

🚀 APPS:
   open notepad / calculator / paint / chrome / edge
   search <query>              → Google search

🐍 PYTHON:
   run <file.py>               → Python file chalao
   install <package>           → pip install
   uninstall <package>         → pip uninstall

🔧 GIT:
   git status / git init
   commit <message>            → add + commit
   push / pull / clone <url>

══════════════════════════════════════════════════
""")

    def get_history(self, tab_id=None):
        if tab_id:
            return [h for h in self.history if h["tab"] == tab_id]
        return self.history


executor = CommandExecutor()