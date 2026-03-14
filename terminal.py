import subprocess
import os

history = []

def run_command(cmd):
    # Custom commands
    if cmd.strip() == "clear":
        os.system("cls")
        return
    if cmd.strip() == "exit":
        print("Bye!")
        exit()
    if cmd.strip() == "history":
        for i, c in enumerate(history): print(f"{i+1}. {c}")
        return

    # System commands
    try:
        result = subprocess.run(
            cmd, shell=True,
            capture_output=True, text=True
        )
        if result.stdout: print(result.stdout, end="")
        if result.stderr: print(result.stderr, end="")
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("=" * 40)
    print("  My Terminal v1.0")
    print("  Type 'exit' to quit, 'history' for log")
    print("=" * 40)

    while True:
        try:
            cwd = os.getcwd()
            cmd = input(f"\n{cwd}> ")
            if not cmd.strip():
                continue
            history.append(cmd)
            run_command(cmd)
        except KeyboardInterrupt:
            print("\nCtrl+C dabaya — exit karne ke liye 'exit' likho")

if __name__ == "__main__":
    main()