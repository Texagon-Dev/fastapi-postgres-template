#!/usr/bin/env python3
import os
import shutil
import sys
from pathlib import Path

def setup_env():
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

def setup_git_hooks():
    hooks_dir = Path(".git/hooks")
    pre_commit_src = Path("misc/pre-commit")
    
    if not pre_commit_src.exists():
        print(f"❌ Pre-commit hook not found at {pre_commit_src}")
        return False
    
    if not hooks_dir.exists():
        print("ℹ️ Initializing git repository...")
        os.system("git init")
    
    print("🔧 Setting up git hooks...")
    pre_commit_dest = hooks_dir / "pre-commit"
    
    # Copy the pre-commit hook
    shutil.copy(pre_commit_src, pre_commit_dest)
    
    # Make it executable
    pre_commit_dest.chmod(0o755)
    print("✅ Git hooks set up successfully")
    return True

def main():
    print("🚀 Starting project setup...")
    
    if not setup_env():
        sys.exit(1)
    
    if not setup_git_hooks():
        print("⚠️  Git hooks setup failed, but continuing...")
    
    print("\n🎉 Setup completed successfully!")
    print("Please review the .env file and update any necessary values.")

if __name__ == "__main__":
    main()