import subprocess
import os
import threading

class CommandExecutor:
    def __init__(self):
        self.cwd = os.path.expanduser("~")
        self.history = []
        self.env = os.environ.copy()

    def execute(self, command, tab_id="default"):
        self.history.append({"tab": tab_id, "cmd": command})

        # cd command special handle
        if command.strip().startswith("cd "):
            path = command.strip()[3:].strip()
            try:
                new_path = os.path.join(self.cwd, path)
                os.chdir(new_path)
                self.cwd = os.getcwd()
                return {"output": "", "error": "", "cwd": self.cwd}
            except Exception as e:
                return {"output": "", "error": str(e), "cwd": self.cwd}

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
            return {"output": "", "error": "Timeout: command 30s se zyada chala", "cwd": self.cwd}
        except Exception as e:
            return {"output": "", "error": str(e), "cwd": self.cwd}

    def get_history(self, tab_id=None):
        if tab_id:
            return [h for h in self.history if h["tab"] == tab_id]
        return self.history

# Global instance
executor = CommandExecutor()