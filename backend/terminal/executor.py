import subprocess
import os

class CommandExecutor:
    def __init__(self):
        self.cwd = os.path.expanduser("~")
        self.history = []
        self.env = os.environ.copy()

    def execute(self, command, tab_id="default"):
        self.history.append({"tab": tab_id, "cmd": command})
        cmd = command.strip().lower()

        # ── Natural language commands ──────────────────

        # "open folder <name>"
        if cmd.startswith("open folder"):
            folder = command.strip()[11:].strip()
            return self._open_folder(folder)

        # "create file <name>"
        if cmd.startswith("create file"):
            filename = command.strip()[11:].strip()
            return self._create_file(filename)

        # "create folder <name>"
        if cmd.startswith("create folder"):
            folder = command.strip()[13:].strip()
            return self._create_folder(folder)

        # "delete file <name>"
        if cmd.startswith("delete file"):
            filename = command.strip()[11:].strip()
            return self._delete_file(filename)

        # "delete folder <name>"
        if cmd.startswith("delete folder"):
            folder = command.strip()[13:].strip()
            return self._delete_folder(folder)

        # "show files"
        if cmd in ["show files", "list files", "files"]:
            return self._show_files()

        # "where am i"
        if cmd in ["where am i", "current folder", "pwd"]:
            return {"output": f"Tum yahan ho: {self.cwd}\n", "error": "", "cwd": self.cwd}

        # "go back"
        if cmd in ["go back", "back"]:
            parent = os.path.dirname(self.cwd)
            return self._open_folder(parent)

        # cd command
        if cmd.startswith("cd "):
            path = command.strip()[3:].strip()
            try:
                new_path = os.path.join(self.cwd, path)
                os.chdir(new_path)
                self.cwd = os.getcwd()
                return {"output": f"Folder change ho gaya: {self.cwd}\n", "error": "", "cwd": self.cwd}
            except Exception as e:
                return {"output": "", "error": f"Folder nahi mila: {e}\n", "cwd": self.cwd}

        # ── Normal OS commands ─────────────────────────
        try:
            result = subprocess.run(
                command,
                shell=True,
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
            return {"output": "", "error": "Timeout: command 30s se zyada chala\n", "cwd": self.cwd}
        except Exception as e:
            return {"output": "", "error": str(e) + "\n", "cwd": self.cwd}

    # ── Helper functions ───────────────────────────────

    def _open_folder(self, folder):
        try:
            # Full path hai ya relative
            if os.path.isabs(folder):
                new_path = folder
            else:
                new_path = os.path.join(self.cwd, folder)

            new_path = os.path.normpath(new_path)
            os.chdir(new_path)
            self.cwd = os.getcwd()
            return {"output": f"✓ Folder khul gaya: {self.cwd}\n", "error": "", "cwd": self.cwd}
        except FileNotFoundError:
            return {"output": "", "error": f"✗ '{folder}' naam ka folder nahi mila\n", "cwd": self.cwd}
        except Exception as e:
            return {"output": "", "error": str(e) + "\n", "cwd": self.cwd}

    def _create_file(self, filename):
        if not filename:
            return {"output": "", "error": "✗ File ka naam batao\n", "cwd": self.cwd}
        try:
            filepath = os.path.join(self.cwd, filename)
            with open(filepath, 'w') as f:
                f.write("")
            return {"output": f"✓ File ban gayi: {filename}\n", "error": "", "cwd": self.cwd}
        except Exception as e:
            return {"output": "", "error": str(e) + "\n", "cwd": self.cwd}

    def _create_folder(self, folder):
        if not folder:
            return {"output": "", "error": "✗ Folder ka naam batao\n", "cwd": self.cwd}
        try:
            folderpath = os.path.join(self.cwd, folder)
            os.makedirs(folderpath, exist_ok=True)
            return {"output": f"✓ Folder ban gaya: {folder}\n", "error": "", "cwd": self.cwd}
        except Exception as e:
            return {"output": "", "error": str(e) + "\n", "cwd": self.cwd}

    def _delete_file(self, filename):
        if not filename:
            return {"output": "", "error": "✗ File ka naam batao\n", "cwd": self.cwd}
        try:
            filepath = os.path.join(self.cwd, filename)
            os.remove(filepath)
            return {"output": f"✓ File delete ho gayi: {filename}\n", "error": "", "cwd": self.cwd}
        except FileNotFoundError:
            return {"output": "", "error": f"✗ '{filename}' nahi mili\n", "cwd": self.cwd}
        except Exception as e:
            return {"output": "", "error": str(e) + "\n", "cwd": self.cwd}

    def _delete_folder(self, folder):
        if not folder:
            return {"output": "", "error": "✗ Folder ka naam batao\n", "cwd": self.cwd}
        try:
            import shutil
            folderpath = os.path.join(self.cwd, folder)
            shutil.rmtree(folderpath)
            return {"output": f"✓ Folder delete ho gaya: {folder}\n", "error": "", "cwd": self.cwd}
        except FileNotFoundError:
            return {"output": "", "error": f"✗ '{folder}' nahi mila\n", "cwd": self.cwd}
        except Exception as e:
            return {"output": "", "error": str(e) + "\n", "cwd": self.cwd}

    def _show_files(self):
        try:
            items = os.listdir(self.cwd)
            folders = [f"📁 {i}" for i in items if os.path.isdir(os.path.join(self.cwd, i))]
            files   = [f"📄 {i}" for i in items if os.path.isfile(os.path.join(self.cwd, i))]
            output  = "\n".join(folders + files) + "\n"
            return {"output": output or "Kuch nahi hai yahan\n", "error": "", "cwd": self.cwd}
        except Exception as e:
            return {"output": "", "error": str(e) + "\n", "cwd": self.cwd}

    def get_history(self, tab_id=None):
        if tab_id:
            return [h for h in self.history if h["tab"] == tab_id]
        return self.history

executor = CommandExecutor()