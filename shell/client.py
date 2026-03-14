import socketio
import threading
import sys
import os

sio = socketio.Client()

current_tab = None
waiting = threading.Event()

@sio.event
def connect():
    print("\033[92m[Connected to terminal server]\033[0m")
    sio.emit("new_tab")

@sio.on("tab_created")
def on_tab_created(data):
    global current_tab
    current_tab = data["tabId"]
    print(f"\033[94m[Tab created: {current_tab}]\033[0m")
    waiting.set()

@sio.on("command_result")
def on_result(data):
    if data.get("output"):
        print(data["output"], end="")
    if data.get("error"):
        print(f"\033[91m{data['error']}\033[0m", end="")
    waiting.set()

@sio.on("tab_closed")
def on_tab_closed(data):
    print(f"\033[93m[Tab {data['tabId']} closed]\033[0m")

def show_help():
    print("""
\033[96mCommands:\033[0m
  newtab          → naya tab banao
  tabs            → sab tabs dekho
  switch <tabId>  → tab switch karo
  closetab        → current tab band karo
  exit            → quit
  (koi bhi OS command)
""")

def main():
    global current_tab  # ← fix yahan hai
    print("\033[1m\033[95m")
    print("  ╔══════════════════════════════╗")
    print("  ║   Advanced Terminal v2.0     ║")
    print("  ║   Node + Django + Python     ║")
    print("  ╚══════════════════════════════╝")
    print("\033[0m")

    try:
        sio.connect("http://localhost:3000")
    except Exception:
        print("\033[91mError: Node.js server nahi mila. Pehle 'node server.js' chalao\033[0m")
        sys.exit(1)

    waiting.wait()

    while True:
        try:
            cwd_short = "~"
            cmd = input(f"\n\033[92m[{current_tab[:8]}]\033[0m \033[94m{cwd_short}\033[0m > ")

            if not cmd.strip():
                continue

            if cmd == "exit":
                sio.disconnect()
                print("Bye!")
                break

            elif cmd == "help":
                show_help()

            elif cmd == "newtab":
                waiting.clear()
                sio.emit("new_tab")
                waiting.wait()

            elif cmd == "tabs":
                sio.emit("get_tabs")

            elif cmd.startswith("switch "):
                current_tab = cmd.split(" ", 1)[1].strip()
                print(f"Switched to tab: {current_tab}")

            elif cmd == "closetab":
                sio.emit("close_tab", {"tabId": current_tab})

            else:
                waiting.clear()
                sio.emit("run_command", {
                    "command": cmd,
                    "tabId":   current_tab
                })
                waiting.wait(timeout=35)

        except KeyboardInterrupt:
            print("\n(exit likhke band karo)")

if __name__ == "__main__":
    main()