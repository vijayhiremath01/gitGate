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
    home_dir = os.path.expanduser("~")
    global_rules_path = os.path.join(home_dir, ".gitgate", "review_rules.md")
    
    try:
        with open(global_rules_path, "r") as f:
            base_rules = f.read()
    except FileNotFoundError:
        console.print(f"[bold red]❌ Error:[/bold red] review_rules.md missing at {global_rules_path}")
        sys.exit(1)

    # Appending strict multi-file formatting rules dynamically to system instructions
    formatting_directive = (
        "\n\nCRITICAL FORMATTING RULES FOR MULTI-FILE OUTPUT:\n"
        "If there are no issues, output exactly: STATUS: GOOD | All files look clean.\n"
        "If there are issues, list each violation on a NEW line starting exactly like this:\n"
        "STATUS: NEEDS_FIX | [filename] : Line [X] | [Brief description of issue]\n"
        "Do not include conversational filler, markdown code blocks, or extra notes."
    )
    system_instructions = base_rules + formatting_directive

    # 4. Streamlined Loading Spinner
    console.print()
    with Status(f"[{CLAUDE_ORANGE}] gitGate •[/{CLAUDE_ORANGE}] Analyzing multiple files...", spinner="dots", spinner_style=CLAUDE_ORANGE):
        try:
            client = Groq(api_key="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")
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_instructions},
                    {"role": "user", "content": f"Review this diff across files:\n\n{diff_output}"}
                ],
                temperature=0.1, # Dropped temperature slightly for strict layout compliance
            )
            raw_result = response.choices[0].message.content.strip()
        except Exception as e:
            console.print(f"[bold red]❌ Connection Error:[/bold red] Details: {e}")
            sys.exit(1)

    # 5. Clean Multi-Line & Multi-File Text Output Parsing
    lines = raw_result.split("\n")
    is_blocked = False
    
    console.print(f"[{CLAUDE_ORANGE}]gitGate Results:[/{CLAUDE_ORANGE}]")
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if "STATUS: GOOD" in line:
            clean_text = line.replace("STATUS: GOOD |", "").strip()
            console.print(f"  [bold green]✔ PASS[/bold green] — {clean_text}")
        elif "STATUS: NEEDS_FIX" in line:
            is_blocked = True
            clean_text = line.replace("STATUS: NEEDS_FIX |", "").strip()
            
            # Splitting components cleanly down by file metadata
            if "|" in clean_text:
                file_info, message = clean_text.split("|", 1)
                console.print(f"  [bold red]✕ BLOCKED[/bold red] [cyan]{file_info.strip()}[/cyan] — {message.strip()}")
            else:
                console.print(f"  [bold red]✕ BLOCKED[/bold red] — {clean_text}")

    console.print()

    # 6. Inline bypass option
    if is_blocked:
        should_push = Confirm.ask(f"[bold white]Force bypass blocks and proceed with commit?[/bold white]")
        console.print()
        
        if should_push:
            console.print(f"[{CLAUDE_ORANGE}]🚀 Changes bypassed. Proceeding to commit.[/{CLAUDE_ORANGE}]\n")
            sys.exit(0)
        else:
            console.print("[bold red]🛑 Aborted. Commit dropped successfully.[/bold red]\n")
            sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()