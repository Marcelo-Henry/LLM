# diff_viewer.py
import difflib

def show_diff(old_content: str, new_content: str, filepath: str, action: str):
    """Mostra diff visual sem confirmação."""
    
    # Determina se é criação ou modificação
    is_new = not old_content
    tool_name = "write" if action == "write_file" else "write"
    
    # Header
    if is_new:
        print(f"\nI'll create the following file: \033[95m{filepath}\033[0m (using tool: {tool_name})")
    else:
        print(f"\nI'll modify the following file: \033[95m{filepath}\033[0m (using tool: {tool_name})")
    
    # Split em linhas
    old_lines = old_content.splitlines(keepends=True) if old_content else []
    new_lines = new_content.splitlines(keepends=True)
    
    # Gera diff unificado
    diff = list(difflib.unified_diff(old_lines, new_lines, lineterm=''))
    
    # Pula headers do unified_diff (primeiras 2 linhas)
    if len(diff) > 2:
        diff = diff[2:]
    
    # Mostra diff colorido com numeração
    print()
    new_line_num = 0
    for line in diff:
        if line.startswith('@@'):
            continue
        elif line.startswith('+'):
            new_line_num += 1
            print(f"\033[32m+   {new_line_num:>3}: {line[1:]}\033[0m", end='')
        elif line.startswith('-'):
            print(f"\033[31m-      : {line[1:]}\033[0m", end='')
        else:
            new_line_num += 1
            print(f"    {new_line_num:>3}: {line[1:]}", end='')
    
    # Se não houver diff (arquivo idêntico), mostra conteúdo
    if not diff:
        for i, line in enumerate(new_lines, 1):
            print(f"\033[32m+   {i:>3}: {line}\033[0m", end='')
    
    print()  # Nova linha final
