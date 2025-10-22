#!/usr/bin/env python3
import os
import shutil
import sys
import subprocess
from pathlib import Path

def run_command(cmd: str, cwd: str = None) -> bool:
    """Run a shell command and return True if successful."""
    print(f"\n$ {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True, cwd=cwd)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with exit code {e.returncode}")
        return False

def setup_env() -> bool:
    """Set up the environment file."""
    example_env = Path(".example.env")
    env_file = Path(".env")
    
    if not example_env.exists():
        print("❌ .example.env not found. Please create it first.")
        return False
    
    if not env_file.exists():
        print("🔄 Creating .env from .example.env...")
        shutil.copy(example_env, env_file)
        print("✅ Created .env file")
    else:
        print("ℹ️ .env file already exists, skipping creation")
    return True

def setup_git_hooks() -> bool:
    """Set up git hooks."""
    hooks_dir = Path(".git/hooks")
    pre_commit_src = Path("misc/pre-commit")
    pre_commit_dest = hooks_dir / "pre-commit"
    
    if not pre_commit_src.exists():
        print(f"❌ Pre-commit hook not found at {pre_commit_src}")
        return False
    
    # Ensure .git directory exists
    if not Path(".git").exists():
        print("ℹ️ Initializing git repository...")
        if not run_command("git init"):
            return False
    
    # Create hooks directory if it doesn't exist
    hooks_dir.mkdir(exist_ok=True, parents=True)
    
    print("🔧 Setting up git hooks...")
    
    # Read the custom hook content first to fail fast if there's an issue
    try:
        with open(pre_commit_src, 'r') as f:
            hook_content = f.read()
    except Exception as e:
        print(f"❌ Failed to read custom pre-commit hook: {e}")
        return False
    
    # Write directly to the destination
    try:
        with open(pre_commit_dest, 'w') as f:
            f.write(hook_content)
        
        # Make the hook executable
        pre_commit_dest.chmod(0o755)
        print(f"✅ Installed custom pre-commit hook to {pre_commit_dest}")
        
        # Verify the hook was written correctly
        with open(pre_commit_dest, 'r') as f:
            installed_content = f.read()
            if installed_content != hook_content:
                print("❌ Warning: The installed hook content doesn't match the source!")
                return False
            
    except Exception as e:
        print(f"❌ Failed to install custom pre-commit hook: {e}")
        return False
    
    print("✅ Git hooks set up successfully")
    return True

def main():
    print("\n🚀 Starting project setup...")
    
    # Create scripts directory if it doesn't exist
    scripts_dir = Path("scripts")
    scripts_dir.mkdir(exist_ok=True)
    
    if not setup_env():
        sys.exit(1)
    
    if not setup_git_hooks():
        print("⚠️  Git hooks setup had issues, but continuing...")
    
    print("\n🎉 Setup completed successfully!")
    print("Next steps:")
    print("1. Review and update the .env file with your configuration")
    print("2. Run 'uv sync' to install dependencies")
    print("3. Run 'uv run alembic upgrade head' to set up the database")
    print("4. Run 'uv run uvicorn app.main:app --reload' to start the development server")

if __name__ == "__main__":
    main()
