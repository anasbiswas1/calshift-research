"""Environment bootstrap. Single source of truth. Edit here, never in notebooks."""
import os, sys, shutil, subprocess
from pathlib import Path

DRIVE_ROOT   = Path("/content/drive/MyDrive")
PARENT_DIR   = DRIVE_ROOT / "CALSHIFT_Research"
PROJECT_ROOT = PARENT_DIR / "calshift-research"

def start(pull=True):
    from google.colab import drive
    drive.mount("/content/drive")
    subprocess.run(["git","config","--global","user.name","Md Anas Biswas"], check=False)
    subprocess.run(["git","config","--global","user.email","anasbiswas@gmail.com"], check=False)
    subprocess.run(["git","config","--global","credential.helper","store"], check=False)
    for fn, dest in [(".git-credentials","/root/.git-credentials"),
                     (".gitconfig","/root/.gitconfig")]:
        src = PARENT_DIR / fn
        if src.exists():
            shutil.copy(src, dest); os.chmod(dest, 0o600)
    os.chdir(PROJECT_ROOT)
    sys.path.insert(0, str(PROJECT_ROOT / "src"))
    if pull:
        subprocess.run(["git","pull","--ff-only","--quiet"], check=False)
    import config
    return config

def git(*args, show=True):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if show:
        if r.stdout.strip(): print(r.stdout.strip())
        if r.stderr.strip(): print(r.stderr.strip())
    return r

def save(message):
    for s, d in [("/root/.git-credentials", PARENT_DIR / ".git-credentials"),
                 ("/root/.gitconfig",       PARENT_DIR / ".gitconfig")]:
        if os.path.exists(s): shutil.copy(s, d)
    os.chdir(PROJECT_ROOT)
    git("add","-A", show=False)
    if git("status","--porcelain", show=False).stdout.strip():
        git("commit","-m",message)
        r = git("push","-u","origin","main")
        if r.returncode: print("PUSH FAILED. Commit is safe locally.")
    else:
        print("nothing to commit")
    print(git("log","--oneline","-3", show=False).stdout)
