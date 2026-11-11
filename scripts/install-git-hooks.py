#!/usr/bin/env python3
import os
import subprocess
import sys

def install_hooks():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hooks_dir = os.path.join(repo_dir, 'scripts', 'git-hooks')
    
    try:
        subprocess.run(['git', 'config', 'core.hooksPath', 'scripts/git-hooks'], check=True, cwd=repo_dir)
        print("[SUCCESS] Configured git core.hooksPath -> scripts/git-hooks")
    except Exception as e:
        print(f"[ERROR] Failed to set core.hooksPath: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    install_hooks()
