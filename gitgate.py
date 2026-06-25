import os
import sys
import subprocess
from groq import Groq
from rich.console import Console
from rich.prompt import Confirm
from rich.status import Status

console = Console()
CLAUDE_ORANGE = "bold #D97706"

def is_git_repository():
    """Checks if the current working directory is inside a Git repo."""
    try:
        # Run a low-overhead git command to check repo validity
        subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"], stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    # 1. Automatic Git Environment Check
    if not is_git_repository():
        console.print(f"[{CLAUDE_ORANGE}]gitGate[/{CLAUDE_ORANGE}] [bold yellow]⚠ Outside Git Repo[/bold yellow] — No active repository detected here.")
        sys.exit(0)

    # 2. Capture the staged code changes
    diff_output = ""
    for flag in [["git", "diff", "--staged"], ["git", "diff", "--cached"]]:
        try:
            diff_output = subprocess.check_output(flag, stderr=subprocess.DEVNULL).decode("utf-8")
            if diff_output.strip():
                break
        except Exception:
            continue
            
    if not diff_output.strip():
        console.print(f"[{CLAUDE_ORANGE}]gitGate •[/{CLAUDE_ORANGE}] No staged changes found to analyze.")
        sys.exit(0)

    # 3. Read the Markdown Instruction file
    # We will point this to a reliable global home path (~/.gitgate/review_rules.md)
    home_dir = os.path.expanduser("~")
    global_rules_path = os.path.join(home_dir, ".gitgate", "review_rules.md")
    
    try:
        with open(global_rules_path, "r") as f:
            system_instructions = f.read()
    except FileNotFoundError:
        console.print(f"[bold red]❌ Error:[/bold red] review_rules.md missing at {global_rules_path}")
        sys.exit(1)

    # 4. Streamlined Loading Spinner
    console.print()
    with Status(f"[{CLAUDE_ORANGE}] gitGate •[/{CLAUDE_ORANGE}] Analyzing changes...", spinner="dots", spinner_style=CLAUDE_ORANGE):
        try:
            client = Groq(api_key="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")
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_instructions},
                    {"role": "user", "content": f"Review this diff:\n\n{diff_output}"}
                ],
                temperature=0.2,
            )
            result = response.choices[0].message.content.strip()
        except Exception as e:
            console.print(f"[bold red]❌ Connection Error:[/bold red] Details: {e}")
            sys.exit(1)

    # 5. Clean Text Output
    if "STATUS: GOOD" in result:
        clean_text = result.replace("STATUS: GOOD |", "").strip()
        console.print(f"[{CLAUDE_ORANGE}]gitGate[/{CLAUDE_ORANGE}] [bold green]✔ PASS[/bold green] — {clean_text}")
        console.print()
    else:
        clean_text = result.replace("STATUS: NEEDS_FIX |", "").strip()
        console.print(f"[{CLAUDE_ORANGE}]gitGate[/{CLAUDE_ORANGE}] [bold red]✕ BLOCKED[/bold red] — {clean_text}")
        console.print()

    # 6. Inline bypass option
    should_push = Confirm.ask(f"[bold white]Force bypass block and proceed with commit?[/bold white]")
    console.print()
    
    if should_push:
        console.print(f"[{CLAUDE_ORANGE}]🚀 Changes bypassed. Proceeding to commit.[/{CLAUDE_ORANGE}]\n")
        sys.exit(0)
    else:
        console.print("[bold red]🛑 Aborted. Commit dropped successfully.[/bold red]\n")
        sys.exit(1)

if __name__ == "__main__":
    main()