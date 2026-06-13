from pathlib import Path
import requests
import zipfile
import io
import shutil
import os
import stat
import time

# =============================
# UI
# =============================
print("\n=================================")
print("        🚀 Kaido Installer")
print("=================================\n")

# =============================
# CONFIG
# =============================
BASE_URL = "https://raw.githubusercontent.com/Create-Lua/kaido/main/release"
KAIDO_DIR = Path.home() / ".kaido"
TEMP_DIR = KAIDO_DIR / "_temp"
CLI_PATH = Path("/opt/homebrew/bin/kaido")

# =============================
# EXISTING INSTALL CHECK (NEW)
# =============================
def handle_existing_install():
    print("\n⚠️ Kaido is already installed.")
    print("[1] Update (keep packages)")
    print("[2] Reinstall (wipe everything)")
    print("[3] Cancel")

    choice = input("Choose: ").strip()

    if choice == "1":
        print("\n🔄 Updating Kaido (keeping packages)...")

        kaido_py = KAIDO_DIR / "kaido.py"
        tools_dir = KAIDO_DIR / "tools"

        if kaido_py.exists():
            os.remove(kaido_py)

        if tools_dir.exists():
            shutil.rmtree(tools_dir)

        print("✔ Core removed, packages preserved")
        return True

    elif choice == "2":
        print("\n💣 Reinstalling Kaido (full wipe)...")

        if KAIDO_DIR.exists():
            shutil.rmtree(KAIDO_DIR)

        KAIDO_DIR.mkdir(parents=True, exist_ok=True)

        print("✔ Fresh install directory created")
        return True

    else:
        print("❌ Cancelled.")
        return False


if KAIDO_DIR.exists():
    proceed = handle_existing_install()
    if not proceed:
        exit()

# =============================
# VERSION SELECT
# =============================
version = input("📦 Version (latest / 1.0 / 1.1) [latest]: ").strip() or "latest"

url = f"{BASE_URL}/{version}.zip"

print(f"\n🔎 Selected version : {version}")
print(f"🌐 Source           : {url}\n")

confirm = input("⚡ Install Kaido? (y/n): ").strip().lower()
if confirm != "y":
    print("❌ Cancelled.")
    exit()

# =============================
# DOWNLOAD
# =============================
print("\n⬇ Downloading Kaido...")

try:
    r = requests.get(url, timeout=30)
except Exception as e:
    print(f"❌ Network error: {e}")
    exit()

if r.status_code != 200:
    print("❌ Download failed (bad version or URL).")
    exit()

# =============================
# TEMP SETUP
# =============================
print("📦 Preparing installer...")

if TEMP_DIR.exists():
    shutil.rmtree(TEMP_DIR)

TEMP_DIR.mkdir(parents=True, exist_ok=True)

# =============================
# EXTRACT
# =============================
print("📂 Extracting package...")

zipfile.ZipFile(io.BytesIO(r.content)).extractall(TEMP_DIR)

# =============================
# FIND REAL ROOT (FIXED LOGIC)
# =============================
root = TEMP_DIR

while True:
    contents = list(root.iterdir())

    if len(contents) == 1 and contents[0].is_dir():
        root = contents[0]
    else:
        break

# =============================
# INSTALL
# =============================
print("⚙ Installing files...")

KAIDO_DIR.mkdir(parents=True, exist_ok=True)

for item in root.iterdir():
    dest = KAIDO_DIR / item.name

    if dest.exists():
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            os.remove(dest)

    if item.is_dir():
        shutil.copytree(item, dest, dirs_exist_ok=True)
    else:
        shutil.copy2(item, dest)

# cleanup
shutil.rmtree(TEMP_DIR)

# =============================
# CLI SETUP
# =============================
print("\n🔧 Setting up CLI...")

kaido_main = KAIDO_DIR / "kaido.py"

if not kaido_main.exists():
    print("❌ kaido.py missing — install aborted.")
    exit()

wrapper = f"""#!/bin/bash
exec python3 "{kaido_main}" "$@"
"""

CLI_PATH.write_text(wrapper)
os.chmod(CLI_PATH, os.stat(CLI_PATH).st_mode | stat.S_IEXEC)

# =============================
# DONE
# =============================
print("\n=================================")
print("✔ Kaido installed successfully!")
print(f"📍 Location: {KAIDO_DIR}")
print("💻 CLI: kaido")
print("=================================\n")